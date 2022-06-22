from io import BytesIO

import barcode
from barcode.writer import ImageWriter

class BarcodeGenerator():
    def __init__(self, users_settings: dict):
        self.options = {}
        self.user_setting = users_settings
        
    def create(self, uid:str, users_barcode: str) -> BytesIO:
        if len(users_barcode) > 13:
            self.options = {
                'font_size': 8
            }
        if len(str(users_barcode)) > 20:
            raise Exception("Too big")
        rv = BytesIO()
        user_barcode_type = self.user_setting[str(uid)]["settings"]["BarcodeType"]
        BARCODE = barcode.get_barcode_class(user_barcode_type)
        BARCODE(users_barcode, writer=ImageWriter()).write(rv, options=self.options)
        return rv