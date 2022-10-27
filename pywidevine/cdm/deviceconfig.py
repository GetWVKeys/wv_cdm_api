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

import os

device_chromecdm_2391 = {
    "name": "chromecdm_2391",
    "description": "chrome cdm windows 2391",
    "security_level": 3,
    "session_id_type": "chrome",
    "private_key_available": True,
    "vmp": True,
    "send_key_control_nonce": True,
}

device_chromecdm_2449 = {
    "name": "chromecdm_2449",
    "description": "chrome cdm windows 2449",
    "security_level": 3,
    "session_id_type": "chrome",
    "private_key_available": True,
    "vmp": True,
    "send_key_control_nonce": True,
}

devices_available = [device_chromecdm_2391, device_chromecdm_2449]

FILES_FOLDER = "devices"


class DeviceConfig:
    def __init__(self, device):
        self.device_name: str = device["name"]
        self.description: str = device["description"]
        self.security_level: int = device["security_level"]
        self.session_id_type: str = device["session_id_type"]
        self.private_key_available: bool = device["private_key_available"]
        self.vmp = device["vmp"]
        self.send_key_control_nonce = device["send_key_control_nonce"]

        if "keybox_filename" in device:
            self.keybox_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device["name"], device["keybox_filename"])
        else:
            self.keybox_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device["name"], "keybox")

        if "device_cert_filename" in device:
            self.device_cert_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device["name"], device["device_cert_filename"])
        else:
            self.device_cert_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device["name"], "device_cert")

        if "device_private_key_filename" in device:
            self.device_private_key_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device["name"], device["device_private_key_filename"])
        else:
            self.device_private_key_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device["name"], "device_private_key")

        if "device_client_id_blob_filename" in device:
            self.device_client_id_blob_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device["name"], device["device_client_id_blob_filename"])
        else:
            self.device_client_id_blob_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device["name"], "device_client_id_blob")

        if "device_vmp_blob_filename" in device:
            self.device_vmp_blob_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device["name"], device["device_vmp_blob_filename"])
        else:
            self.device_vmp_blob_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device["name"], "device_vmp_blob")

    def __repr__(self):
        return "DeviceConfig(name={}, description={}, security_level={}, session_id_type={}, private_key_available={}, vmp={})".format(
            self.device_name, self.description, self.security_level, self.session_id_type, self.private_key_available, self.vmp
        )
