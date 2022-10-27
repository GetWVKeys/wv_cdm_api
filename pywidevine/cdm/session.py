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

from typing import Optional, Union

from pywidevine.cdm.deviceconfig import DeviceConfig
from pywidevine.cdm.formats.wv_proto2_pb2 import (
    SignedDeviceCertificate,
    SignedLicense,
    SignedLicenseRequest,
    SignedLicenseRequestRaw,
)
from pywidevine.cdm.key import Key


class Session:
    def __init__(self, session_id: str, init_data: bytes, device_config: DeviceConfig, raw: bool, offline: bool):
        self.session_id = session_id
        self.init_data = init_data
        self.raw = raw
        self.offline = offline
        self.device_config = device_config
        self.device_key = None
        self.session_key = None
        self.derived_keys = {"enc": None, "auth_1": None, "auth_2": None}
        self.license_request: Union[SignedLicenseRequest, SignedLicenseRequestRaw]
        self.signed_license: Optional[SignedLicense] = None
        self.signed_device_certificate: Optional[SignedDeviceCertificate] = None
        self.privacy_mode = False
        self.keys: list[Key] = []
