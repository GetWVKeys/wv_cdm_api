"""
 This file is part of the wv_cdm_api project (https://github.com/GetWVKeys/wv_cdm_api)
 Copyright (C) 2022 Notaghost, Puyodead1 and GetWVKeys contributors 
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published
 by the Free Software Foundation, version 3 of the License.
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.
 You should have received a copy of the GNU Affero General Public License
 along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
import os
import platform
import time

import humanize
import psutil
from dunamai import Style, Version
from flask import Flask, Request, jsonify, request
from werkzeug.exceptions import (
    BadRequest,
    Forbidden,
    HTTPException,
    NotImplemented,
    UnsupportedMediaType,
)
from werkzeug.middleware.proxy_fix import ProxyFix

from api import config
from api.utils import (
    Methods,
    Validators,
    check_pssh,
    construct_logger,
    mutate_challenge,
)
from pywidevine.cdm import deviceconfig
from pywidevine.cdm.cdm import Cdm

logger = construct_logger()
app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
cdm = Cdm()

sha = Version.from_git().serialize(style=Style.SemVer, dirty=True, format="{base}-post.{distance}+{commit}.{dirty}.{branch}")


def on_json_loading_failed(self, e):
    raise UnsupportedMediaType()


Request.on_json_loading_failed = on_json_loading_failed


def log_date_time_string():
    """Return the current time formatted for logging."""
    monthname = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    now = time.time()
    year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
    s = "%02d/%3s/%04d %02d:%02d:%02d" % (day, monthname[month], year, hh, mm, ss)
    return s


@app.after_request
def log_request_info(response):
    l = f'{request.remote_addr} - - [{log_date_time_string()}] "{request.method} {request.path}" {response.status_code}'

    if request.data and len(request.data) > 0 and request.headers.get("Content-Type") == "application/json":
        l += f"\nRequest Data: {request.data.decode()}"

    logger.info(l)
    return response


@app.get("/info")
def info():
    if config.DISABLE_INFO_ROUTE:
        raise Forbidden("This route has been disabled by the server administrator.")
    process = psutil.Process(os.getpid())

    return jsonify(
        {
            "hostname": platform.node(),
            "os": platform.system(),
            "os_version": platform.release(),
            "version": sha,
            "process_memory": "{:.2f} MB".format(process.memory_info().rss / 1024 / 1024),
            "process_threads": process.num_threads(),
            "process_uptime": humanize.naturaldelta(int(time.time() - process.create_time())),
            "host_uptime": humanize.naturaldelta(time.time() - psutil.boot_time()),
            "host_cpu": "{:.2f}%".format(psutil.cpu_percent()),
            "host_memory": "{:.2f} MB".format(psutil.virtual_memory().used / 1024 / 1024),
        }
    )


@app.post("/api")
def index():
    data = request.get_json()

    # validate the payload
    if not Validators.payload(data):
        return jsonify({"status": 400, "errors": Validators.payload.errors}), 400

    (method, params, token) = (data["method"], data["params"], data["token"])

    # check if the token is valid
    if token not in config.API_SECRETS:
        raise Forbidden()

    if method == Methods.GET_CHALLENGE.value:
        if not Validators.challenge(params):
            return jsonify({"status": 400, "errors": Validators.challenge.errors}), 400
        (init, cert, raw, license_type, device) = (params["init"], params["cert"], params["raw"], params["licensetype"], params["device"])
        offline = license_type == "OFFLINE"
        session_id = cdm.open_session(check_pssh(init), deviceconfig.DeviceConfig(deviceconfig.device_chromecdm_2449), raw=raw, offline=offline)

        if cert:
            cdm.set_service_certificate(session_id, cert)

        challenge = cdm.get_license_request(session_id)
        new_challenge = mutate_challenge(session_id, challenge)

        return {"challenge": new_challenge, "session_id": session_id}
    elif method == Methods.GET_KEYS.value:
        if not Validators.keys(params):
            return jsonify({"status": 400, "errors": Validators.keys.errors}), 400
        (cdmkeyresponse, session_id) = (params["cdmkeyresponse"], params["session_id"])

        new_cdmkeyresponse = mutate_challenge(session_id, cdmkeyresponse)

        cdm.provide_license(session_id, new_cdmkeyresponse)
        keys = cdm.get_content_keys(session_id)
        keys = map(lambda key: {"kid": key.kid, "key": key.key}, keys)
        return jsonify({"keys": list(keys)})
    elif method == Methods.GET_KEYS_EXCHANGE.value:
        if not Validators.kex(params):
            return jsonify({"status": 400, "errors": Validators.kex.errors}), 400
        raise NotImplemented()
    else:
        raise BadRequest("Invalid method")


@app.errorhandler(HTTPException)
def handle_exception(e: HTTPException):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "status": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


def main():
    app.run(config.API_HOST, config.API_PORT, debug=config.IS_DEVELOPMENT, use_reloader=False)


if __name__ == "__main__":
    main()
