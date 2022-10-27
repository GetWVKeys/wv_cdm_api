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

import binascii


class Key:
    def __init__(self, kid: bytes, type: str, key: bytes, permissions=[]):
        self.kid = kid.hex()
        self.type = type
        self.key = binascii.hexlify(key).decode()
        self.permissions = permissions

    def __repr__(self):
        if self.type == "OPERATOR_SESSION":
            return "key(kid={}, type={}, key={}, permissions={})".format(self.kid, self.type, self.key, self.permissions)
        else:
            return "key(kid={}, type={}, key={})".format(self.kid, self.type, self.key)
