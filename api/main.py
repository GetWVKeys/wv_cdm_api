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

from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest, Forbidden, HTTPException, NotImplemented

from api import config
from api.utils import Methods, Validators

app = Flask(__name__)


@app.post("/api")
def index():
    data = request.get_json()

    # validate the payload
    if not Validators.payload(data):
        return jsonify({"status": 400, "errors": Validators.payload.errors})

    (method, params, token) = (data["method"], data["params"], data["token"])

    # check if the token is valid
    if token not in config.API_SECRETS:
        raise Forbidden()

    if method == Methods.GET_CHALLENGE.value:
        if not Validators.challenge(params):
            return jsonify({"status": 400, "errors": Validators.challenge.errors})
        raise NotImplemented()
    elif method == Methods.GET_KEYS.value:
        if not Validators.keys(params):
            return jsonify({"status": 400, "errors": Validators.challenge.errors})
        raise NotImplemented()
    elif method == Methods.GET_KEYS_EXCHANGE.value:
        if not Validators.kex(params):
            return jsonify({"status": 400, "errors": Validators.challenge.errors})
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
