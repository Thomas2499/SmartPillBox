from models import PatientModel
from datetime import datetime
from models import KeyModel
import boto3
import json


class PillPresenter:
    def __init__(self):
        self.__key_model = KeyModel()
        self.__patient_model = PatientModel()
        self.__patient_id = None
        self.__patient_prescription = None

    @property
    def patient_id(self):
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value):
        self.__patient_id = value

    @property
    def patient_prescription(self):
        return self.__patient_prescription

    @patient_prescription.setter
    def patient_prescription(self, value):
        self.__patient_prescription = value

    @staticmethod
    def __retrieve_components_combination(data):
        combination = set()
        for row in data:
            row_combination = row["Does_not_Combine_With"]
            combination.update(row_combination.split(','))
        return combination

    @staticmethod
    def __refactor_day_number(prescription):
        for i in range(len(prescription)):
            day_id = prescription[i]["Day_Id"]
            prescription[i]["Day_Id"] = day_id - 2 if day_id != 1 else 6
        return prescription

    def get_patients_ids(self):
        data = self.__patient_model.get_ids()
        return data

    def validate_safe_pills_combinations(self):
        data = self.__patient_model.get_combinations(self.patient_id)
        combination = self.__retrieve_components_combination(data)
        for row in data:
            if row["Active_component"] in combination:
                return False
        return True

    def store_patient_prescription(self):
        prescription = self.__patient_model.get_prescription(self.patient_id)
        self.__refactor_day_number(prescription)
        self.patient_prescription = prescription

    def retrieve_keys(self):
        return [obtain["Cell_id"] for obtain in self.patient_prescription]

    def validate_input_key(self, key):
        prescription_keys = self.retrieve_keys()
        if key.upper() not in prescription_keys:
            return False
        return True

    def validate_input_key_timing(self, key):
        prescription_by_key = list(filter(lambda row: row['Cell_id'] == key.upper(), self.patient_prescription))[0]
        current_time = datetime.now()
        timestamp = f"{current_time.hour}:{current_time.minute}"
        if prescription_by_key['Hour_Id'] != timestamp or prescription_by_key['Day_Id'] != current_time.weekday():
            return False
        return True

