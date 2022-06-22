import os
import json
import logging

class UserHandler():
    def __init__(self):
        self.DIR = "userdata"
        if not os.path.exists(self.DIR):
            os.mkdir(self.DIR)
            logging.info("FOLDER {userdata} not found. Creating...")

        self.userdata = {}
        for uid in os.listdir(self.DIR):
            with open(f"{self.DIR}/{uid}/{uid}.json", "r", encoding="utf-8") as userfile:
                self.userdata = json.load(userfile)

    def save(self, user_id: str) -> None:
        user_path = f"{self.DIR}/{user_id}"
        if not os.path.exists(user_path):
            os.mkdir(user_path)
            logging.info(f"USER'S (id: {user_id}) folder not found. Creating...")

        with open(f'{user_path}/{user_id}.json', 'w', encoding="utf-8") as fp:
            json.dump(self.userdata, fp, indent=4, ensure_ascii=False)
            logging.info(f"USER'S (id: {user_id}) data saved")

    def get(self, user_id: str, param:str) -> dict:
        try:
            return self.userdata[str(user_id)][param]
        except:
            return {}

    def get_product(self, user_id: str, product_articul:str) -> dict:
        try:
            return self.userdata[str(user_id)]["products"][product_articul]
        except:
            return {}
    
    def get_products(self, user_id: str) -> dict:
        try:
            return self.userdata[str(user_id)]["products"]
        except:
            return {}

    def create_user(self, user_id: str) -> None:
        user_id = str(user_id)
        if user_id not in self.userdata:
            self.userdata[user_id] = {"brand":"", "seller":"", "settings":{}, "BarcodeType": "ean13"}
            self.save(user_id)
            logging.info(f"NEW USER (id: {user_id}) CREATED")
    
    def add_dict(self, user_id: str, dict_slice:dict) -> None:
        user_id = str(user_id)
        for k, v in dict_slice.items():
            self.userdata[user_id][k] = v
        self.save(user_id)
    
    def product_set(self, user_id: str, product_articul:str, product_info: dict) -> None:
        user_id = str(user_id)
        try:
            self.userdata[user_id]["products"][product_articul] = product_info
        except KeyError:
            self.userdata[user_id].setdefault("products", {product_articul: product_info})
        self.save(user_id)

    def product_add(self, user_id: str, product_articul:str, key:str, value: str) -> None:
        user_id = str(user_id)
        if product_articul in self.userdata[user_id]["products"]:
            self.userdata[user_id]["products"][product_articul][key] = value
        else:
            self.product_set(user_id, product_articul, {key: value})
    
    def product_del(self, user_id: str, key) -> None:
        user_id = str(user_id)
        del self.userdata[user_id]["products"][key]
        self.save(user_id)
    
    def settings_add(self, user_id: str, key: str, value: str) -> None:
        user_id = str(user_id)
        try:
            self.userdata[user_id]["settings"][key] = value
        except KeyError:
            self.userdata[user_id].setdefault("settings", {key: value})
        self.save(user_id)
    
    def settings_get(self, user_id: str, key: str) -> dict:
        user_id = str(user_id)
        try:
            return self.userdata[user_id]["settings"][key]
        except KeyError:
            return {}