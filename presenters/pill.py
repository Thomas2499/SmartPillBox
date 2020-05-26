from presenters.consts import WAITING_SECONDS
from models import PatientModel
from datetime import datetime
from models import KeyModel
import boto3
import time


sns = boto3.client('sns', region_name="us-east-1")


class PillPresenter:
    def __init__(self):
        self.__key_model = KeyModel()
        self.__patient_model = PatientModel()
        self.__patient_id = None
        self.__patient_prescription = None
        self.__timestamps = None

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

    @staticmethod
    def __add_obtained_prescription_field(prescription):
        updated_prescription = []
        for row in prescription:
            row.update({"obtained": False})
            updated_prescription.append(row)
        return updated_prescription

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
        prescription = self.__refactor_day_number(prescription)
        prescription = self.__add_obtained_prescription_field(prescription)
        self.patient_prescription = prescription

    def retrieve_keys(self):
        return [obtain["Cell_id"] for obtain in self.patient_prescription]

    def validate_input_key(self, key):
        prescription_keys = self.retrieve_keys()
        if key not in prescription_keys:
            print("You've pressed an invalid key")
            return False
        return True

    def validate_input_key_timing(self, key):
        prescription_by_key = list(filter(lambda row: row['Cell_id'] == key, self.patient_prescription))[0]
        current_time = datetime.now()
        timestamp = f"{current_time.hour}:{0 if current_time.minute < 10 else ''}{current_time.minute}"
        if prescription_by_key['obtained'] is True:
            print("pill already obtained")
            self.send_alert()
            return False
        if prescription_by_key['Hour_Id'] != timestamp or prescription_by_key['Day_Id'] != str(current_time.weekday()):
            return False
        return True

    def update_obtaining(self, key):
        for i in range(len(self.patient_prescription)):
            if self.patient_prescription[i]["Cell_id"] == key:
                self.patient_prescription[i]["obtained"] = True

    def __extract_timestamps(self):
        prescription = self.__patient_prescription
        self.__timestamps = [f"{row['Day_Id']}:{row['Hour_Id']}" for row in prescription]

    def __is_prescription_time_passed(self, timestamp):
        last_prescription_time = self.__timestamps[len(self.__timestamps) - 1]
        return last_prescription_time == timestamp

    def __is_obtained_on_time(self, day, hour_with_min):
        current_prescription = list(filter(lambda row: row["Day_Id"] == day and row["Hour_Id"] == hour_with_min,
                                           self.patient_prescription))[0]
        if not current_prescription["obtained"]:
            return False
        return True

    def assurance_listener(self):
        self.patient_prescription[len(self.patient_prescription) - 1]["Day_Id"] = '2'
        self.patient_prescription[len(self.patient_prescription) - 1]["Hour_Id"] = '0:24'
        self.__extract_timestamps()
        while True:
            current_time = datetime.now()
            timestamp = f"{current_time.weekday()}:{current_time.hour}:{0 if current_time.minute < 10 else ''}" \
                        f"{current_time.minute}"
            if timestamp in self.__timestamps:
                time.sleep(WAITING_SECONDS)
                day, hour_with_min = timestamp.split(':', 1)
                if not self.__is_obtained_on_time(day, hour_with_min):
                    print("missed!")
                    self.send_alert(message=f"you missed! on {day}  {hour_with_min}")
                if self.__is_prescription_time_passed(timestamp):
                    break
            time.sleep(5)

    @staticmethod
    def send_alert(message):
        sns.publish(PhoneNumber='+972527213340', Message=message)
