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

import logging
import os
import time
from pathlib import Path

import tomllib

IS_DEVELOPMENT = bool(os.environ.get("DEVELOPMENT", False))
parsed_toml = tomllib.load(open("config.toml", "rb"))

SECRET_KEY = parsed_toml.get("SECRET_KEY", "S$cR3t_K3y")
API_HOST = parsed_toml.get("API_HOST")
API_PORT = int(parsed_toml.get("API_PORT", 8080))
API_URL = parsed_toml.get("API_URL", "https://server1.getwvkeys.cc")
API_SECRETS = parsed_toml.get("API_SECRETS", [])

CONSOLE_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.DEBUG
LOG_FORMAT = parsed_toml.get("LOG_FORMAT", "[%(asctime)s] [%(name)s] [%(funcName)s:%(lineno)d] %(levelname)s: %(message)s")
LOG_DATE_FORMAT = parsed_toml.get("LOG_DATE_FORMAT", "%I:%M:%S")
LOG_FILE_PATH = Path(os.getcwd(), "logs", f"{time.strftime('%Y-%m-%d')}.log")

CHALLENGES_DIR_PATH = Path(os.getcwd(), "challenges")
CHALLENGES_DIR_PATH.mkdir(exist_ok=True, parents=True)

WV_CVT = Path(os.getcwd(), "pywidevine", "wv_cvt.exe")
if not WV_CVT.exists():
    raise FileNotFoundError("wv_cvt.exe is missing")

DISABLE_INFO_ROUTE = bool(parsed_toml.get("DISABLE_INFO_ROUTE", False))
