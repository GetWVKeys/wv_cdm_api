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

import base64
import binascii
import logging
import logging.handlers
import subprocess
from enum import Enum
from pathlib import Path

from cerberus import Validator
from coloredlogs import ColoredFormatter
from werkzeug.exceptions import BadRequest

from api import config

WV_SYSTEM_ID = [237, 239, 139, 169, 121, 214, 74, 206, 163, 200, 39, 220, 213, 29, 33, 237]


class Methods(Enum):
    GET_CHALLENGE = "GetChallenge"
    GET_KEYS = "GetKeys"
    GET_KEYS_EXCHANGE = "GetKeysX"


class Validators:
    CHALLENGE_SCHEMA = {
        "init": {"required": True, "type": "string", "empty": False},
        "cert": {"required": True, "type": "string", "empty": False},
        "raw": {"required": False, "type": "boolean"},
        "licensetype": {"required": True, "type": "string", "allowed": ["OFFLINE", "STREAMING"]},
        "device": {"required": True, "type": "string", "empty": True},
    }
    KEYS_SCHEMA = {"cdmkeyresponse": {"required": True, "type": "string", "empty": False}, "session_id": {"required": True, "type": "string", "empty": False}}
    KEY_EXCHANGE_SCHEMA = {
        "cdmkeyresponse": {"required": True, "type": ["string", "binary"], "empty": False},
        "encryptionkeyid": {"required": True, "type": ["string", "binary"], "empty": False},
        "hmackeyid": {"required": True, "type": ["string", "binary"], "empty": False},
        "session_id": {"required": True, "type": "string", "empty": False},
    }
    PAYLOAD_SCHEMA = {
        "method": {"required": True, "type": "string", "allowed": ["GetKeysX", "GetKeys", "GetChallenge"], "empty": False},
        "params": {"required": True, "type": "dict"},
        "token": {"required": True, "type": "string", "empty": False},
    }
    payload = Validator(PAYLOAD_SCHEMA)
    kex = Validator(KEY_EXCHANGE_SCHEMA)
    keys = Validator(KEYS_SCHEMA)
    challenge = Validator(CHALLENGE_SCHEMA)


def check_pssh(pssh_b64: str):
    try:
        pssh = base64.b64decode(pssh_b64)
        if not pssh[12:28] == bytes(WV_SYSTEM_ID):
            new_pssh = bytearray([0, 0, 0])
            new_pssh.append(32 + len(pssh))
            new_pssh[4:] = bytearray(b"pssh")
            new_pssh[8:] = [0, 0, 0, 0]
            new_pssh[13:] = WV_SYSTEM_ID
            new_pssh[29:] = [0, 0, 0, 0]
            new_pssh[31] = len(pssh)
            new_pssh[32:] = pssh
            return base64.b64encode(new_pssh).decode()
        else:
            return pssh_b64
    except binascii.Error:
        raise BadRequest("Invalid PSSH")
    except Exception as e:
        raise BadRequest(f"Unknown Error: {e}")


def construct_logger():
    # ensure parent folders exist
    config.LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # create a colored formatter for the console
    console_formatter = ColoredFormatter(config.LOG_FORMAT, datefmt=config.LOG_DATE_FORMAT)

    # create a regular non-colored formatter for the log file
    file_formatter = logging.Formatter(config.LOG_FORMAT, datefmt=config.LOG_DATE_FORMAT)

    # create a handler for console logging
    stream = logging.StreamHandler()
    stream.setLevel(config.CONSOLE_LOG_LEVEL)
    stream.setFormatter(console_formatter)

    # create a handler for file logging, 5 mb max size, with 5 backup files
    file_handler = logging.handlers.RotatingFileHandler(config.LOG_FILE_PATH, maxBytes=(1024 * 1024) * 5, backupCount=5)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(config.FILE_LOG_LEVEL)

    # construct the logger
    logger = logging.getLogger()
    logger.setLevel(config.CONSOLE_LOG_LEVEL)
    logger.addHandler(stream)
    logger.addHandler(file_handler)
    return logger


def mutate_challenge(session_id, challenge):
    orig_challenge_path = Path(config.CHALLENGES_DIR_PATH, f"{session_id}.bin")
    new_challenge_path = Path(config.CHALLENGES_DIR_PATH, f"{session_id}_new.bin")

    # write the challenge to a file
    with open(orig_challenge_path, "w") as f:
        f.write(challenge)

    # convert the challenge
    subprocess.run([config.WV_CVT, orig_challenge_path, new_challenge_path])

    # read the converted challenge
    with open(new_challenge_path, "r") as f:
        new_challenge_b64 = f.read()

    # cleanup the files
    orig_challenge_path.unlink()
    new_challenge_path.unlink()

    return new_challenge_b64
