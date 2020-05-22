from models import PatientIdModel
from models import KeyModel


class PillPresenter:
    def __init__(self):
        self.__key_model = KeyModel()
        self.__patient_id_model = PatientIdModel()

    def get(self):
        data = self.__patient_id_model.get()
        return data
