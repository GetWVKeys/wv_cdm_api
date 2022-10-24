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

from enum import Enum

from cerberus import Validator


class Methods(Enum):
    GET_CHALLENGE = "GetChallenge"
    GET_KEYS = "GetKeys"
    GET_KEYS_EXCHANGE = "GetKeysX"


class Validators:
    CHALLENGE_SCHEMA = {
        "init": {"required": True, "type": "string"},
        "cert": {"required": True, "type": "string"},
        "raw": {"required": True, "type": "boolean"},
        "licensetype": {"required": True, "type": "string", "allowed": ["OFFLINE", "STREAMING"]},
        "device": {"required": True, "type": "string"},
    }
    KEYS_SCHEMA = {"cdmkeyresponse": {"required": True, "type": ["string", "binary"]}, "session_id": {"required": True, "type": "string"}}
    KEY_EXCHANGE_SCHEMA = {
        "cdmkeyresponse": {"required": True, "type": ["string", "binary"]},
        "encryptionkeyid": {"required": True, "type": ["string", "binary"]},
        "hmackeyid": {"required": True, "type": ["string", "binary"]},
        "session_id": {"required": True, "type": "string"},
    }
    PAYLOAD_SCHEMA = {
        "method": {"required": True, "type": "string", "allowed": ["GetKeysX", "GetKeys", "GetChallenge"]},
        "params": {"required": True, "type": "dict"},
        "token": {"required": True, "type": "string"},
    }
    payload = Validator(PAYLOAD_SCHEMA)
    kex = Validator(KEY_EXCHANGE_SCHEMA)
    keys = Validator(KEYS_SCHEMA)
    challenge = Validator(CHALLENGE_SCHEMA)
