from presenters.consts import WAITING_SECONDS
from models import PatientModel
from datetime import datetime
from models import KeyModel
import calendar
import boto3
import time


sns = boto3.client('sns', region_name="us-east-1")


class PillPresenter:
    def __init__(self):
        self.__key_model = KeyModel()
        self.__patient_model = PatientModel()
        self.__patient_id = None
        self.__patient_name = None
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

    def save_patient_name(self, patient_id):
        self.__patient_name = self.__patient_model.get_name_by_id(patient_id)[0]

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
        message_time = f"{calendar.day_name[int(prescription_by_key['Day_Id'])]} at {prescription_by_key['Hour_Id']}."
        if prescription_by_key['obtained'] is True:
            print("pill already obtained")
            self.send_alert(message=f"obtained the same pill from box number {prescription_by_key['Box_Id']}"
                            f" originally obtained on {message_time}")
            return False
        if prescription_by_key['Hour_Id'] != timestamp or prescription_by_key['Day_Id'] != str(current_time.weekday()):
            self.send_alert(message=f"obtained a pill not at the right timing. {self.__patient_name} "
                                    f"should've obtained it on {message_time}")
            return False
        return True

    def update_obtaining(self, key):
        for i in range(len(self.patient_prescription)):
            if self.patient_prescription[i]["Cell_id"] == key:
                self.patient_prescription[i]["obtained"] = True

    def __extract_timestamps(self):
        prescription = self.patient_prescription
        self.__timestamps = [f"{row['Day_Id']}:{row['Hour_Id']}" for row in prescription]

    def __is_prescription_time_passed(self, timestamp):
        last_prescription_time = self.__timestamps[len(self.__timestamps) - 1]
        return last_prescription_time == timestamp

    def __is_obtained_on_time(self, day, hour_with_min):
        current_prescription = list(filter(lambda row: row["Day_Id"] == day and row["Hour_Id"] == hour_with_min,
                                           self.patient_prescription))[0]
        if not current_prescription["obtained"]:
            print("miss")
            return False
        print("no miss")
        return True

    def assurance_listener(self):
        for i in range(len(self.patient_prescription)):
            self.patient_prescription[i]["Day_Id"] = '5'
            self.patient_prescription[i]["Hour_Id"] = f"1:0{i}"
        print(self.patient_prescription)
        self.__extract_timestamps()
        while True:
            current_time = datetime.now()
            timestamp = f"{current_time.weekday() + 1}:{current_time.hour}:{0 if current_time.minute < 10 else ''}" \
                        f"{current_time.minute}"
            if timestamp in self.__timestamps:
                time.sleep(WAITING_SECONDS)
                day, hour_with_min = timestamp.split(':', 1)
                obtained = self.__is_obtained_on_time(day, hour_with_min)
                if not obtained:
                    print("missed")
                    self.send_alert(message=f"did not obtain a pill on {calendar.day_name[int(day) - 1]},"
                                            f" {hour_with_min}.")
                if self.__is_prescription_time_passed(timestamp):
                    break
            time.sleep(5)
        self.send_alert(message=f"finished. test complete!")

    @staticmethod
    def __send_alert(message):
        #self.patient_prescription[0]['Phone_number']
        sns.publish(PhoneNumber='+972527213340', Message=message)

    def send_alert(self, message):
        sms_template = f"Hello {self.patient_prescription[0]['First_Name']}, your patient - {self.__patient_name}, "
        self.__send_alert(sms_template + message)
