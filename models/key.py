from daos import PillDAO


class KeyModel:
    def __init__(self):
        self.__pill_dao = PillDAO()

    def get(self):
        data = self.__pill_dao.get("allowed_keyboard_keys")
        return [key[0] for key in data]
