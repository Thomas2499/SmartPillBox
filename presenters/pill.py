from presenters.consts import WAITING_SECONDS, ISRAEL_CALLING_CODE
from models import PatientModel
from datetime import datetime, timedelta
from models import KeyModel
import calendar
import boto3
import time


sns = boto3.client('sns', region_name="us-east-1")


class PillPresenter:
    def __init__(self):
        self.__key_model = KeyModel()
        self.__patient_model = PatientModel()
        # temporary parameters for patient information
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
    def __retrieve_components_combination(data):  # retrieve unique combinations
        combination = set()  # empty set for saving unique data (10,10,10) => (10)
        for row in data:
            row_combination = row["Does_not_Combine_With"]
            combination.update(row_combination.split(','))  # "10,10,10" => [10,10,10] insert data to set
        return combination

    @staticmethod
    def __refactor_day_number(prescription):  # convert from database day to python format
        for i in range(len(prescription)):
            day_id = prescription[i]["Day_Id"]
            prescription[i]["Day_Id"] = day_id - 2 if day_id != 1 else 6
        return prescription

    @staticmethod
    def __add_obtained_prescription_field(prescription):
        updated_prescription = []
        for row in prescription:
            row.update({"obtained": False})  # add field to check if the pill is obtained or not
            updated_prescription.append(row)
        return updated_prescription

    def get_patients_ids(self):  # get patients ids from model
        data = self.__patient_model.get_ids()
        return data

    def validate_safe_pills_combinations(self):
        data = self.__patient_model.get_combinations(self.patient_id)
        combination = self.__retrieve_components_combination(data)  # create list of unique combinations
        for row in data:
            if row["Active_component"] in combination:
                return False
        return True

    def store_patient_prescription(self):  # get and store prescription in the temporary database
        prescription = self.__patient_model.get_prescription(self.patient_id)
        prescription = self.__refactor_day_number(prescription)  # convert from database day to python format
        prescription = self.__add_obtained_prescription_field(prescription)  # add obtaining key to check if patient took the pill
        self.patient_prescription = prescription

    def save_patient_name(self, patient_id):
        self.__patient_name = self.__patient_model.get_name_by_id(patient_id)[0]  # store patient name in the temporary db.

    def retrieve_keys(self):  # returns list of valid keys from prescription from temporary database
        return [obtain["Cell_id"] for obtain in self.patient_prescription]

    def validate_input_key(self, key):  # return true or false if the key is valid
        prescription_keys = self.retrieve_keys()  # returns list of valid keys from prescription from temporary database
        if key not in prescription_keys:
            print("You've pressed an invalid key")
            return False
        return True

    @staticmethod
    def __retrieve_time_borders(prescription):
        current_time = datetime.now()
        current_timestamp = datetime.strptime(
            f"{current_time.weekday() + 1}:{current_time.hour}:{0 if current_time.minute < 10 else ''}"
            f"{current_time.minute}", '%d:%H:%M')  # 0:8:30 (python format) => Monday, 8:30 AM
        prescription_timestamp = datetime.strptime(
            f"{prescription['Day_Id'] + 1}:{prescription['Hour_Id']}", '%d:%H:%M')  # cast from string to datetime (in python)
        border_timestamp = prescription_timestamp + timedelta(minutes=WAITING_SECONDS / 60)  # adds 30 minutes to border timestamp
        return current_timestamp, prescription_timestamp, border_timestamp

    def validate_input_key_timing(self, key):
        prescription_by_key = list(filter(lambda row: row['Cell_id'] == key, self.patient_prescription))[0]  # get obtaining by it's pressed key
        message_time = f"{calendar.day_name[int(prescription_by_key['Day_Id'])]} at {prescription_by_key['Hour_Id']}."  # create string of the time of obtaining

        if prescription_by_key['obtained'] is True:  # if patient pressed the same key
            self.send_alert(message=f"obtained the same pill from box number {prescription_by_key['Box_Id']}"
                            f" originally obtained on {message_time}")
            return False

        current_timestamp, prescription_timestamp, border_timestamp = self.__retrieve_time_borders(prescription_by_key)
        if not prescription_timestamp < current_timestamp < border_timestamp:  # if the current time is not between 8:30 to 9:00, border - time limit for obtain
            self.send_alert(message=f"obtained a pill not at the right timing. {self.__patient_name} "
                                    f"should've obtained it on {message_time}")
            return False
        return True

    def update_obtaining(self, key):
        for i in range(len(self.patient_prescription)):
            if self.patient_prescription[i]["Cell_id"] == key:  # update obtaining to true in temporary database
                self.patient_prescription[i]["obtained"] = True

    def __extract_timestamps(self):  # build from prescription time - a timestamp => 1:20:30
        prescription = self.patient_prescription
        self.__timestamps = [f"{row['Day_Id']}:{row['Hour_Id']}" for row in prescription]  # create list of timestamps

    def __is_prescription_time_passed(self, timestamp):  # checks if it's now the last obtaining time
        last_prescription_time = self.__timestamps[len(self.__timestamps) - 1]  # takes the last timestamp from temporary db
        return last_prescription_time == timestamp

    def __is_obtained_on_time(self, day, hour_with_min):  # checks if obtain pill on time
        current_prescription = list(filter(lambda row: row["Day_Id"] == day and row["Hour_Id"] == hour_with_min,
                                           self.patient_prescription))[0]  # filter the obtaining for the current time.
        if not current_prescription["obtained"]:  # checks if obtain is true or false
            return False, current_prescription
        return True, current_prescription

    def assurance_listener(self):  # checks if at the end of obtaining time (8:30 => 9:00) patient didn't take a pill
        self.__extract_timestamps()
        while True:
            current_time = datetime.now()  # gets the time right now
            timestamp = f"{current_time.weekday()}:{current_time.hour}:{0 if current_time.minute < 10 else ''}" \
                        f"{current_time.minute}"  # Monday 8:30 => 0:8:30
            if timestamp in self.__timestamps:  # checks if it is time to take pill
                time.sleep(WAITING_SECONDS)  # the thread waiting 30 minutes until pill time limit.
                day, hour_with_min = timestamp.split(':', 1)  # => day = 0, hour_with_min = 8:30
                obtained, current_prescription = self.__is_obtained_on_time(day, hour_with_min)
                if not obtained:
                    self.send_alert(message=f"did not obtain a pill on {calendar.day_name[int(day)]},"
                                            f" {hour_with_min}.")  # on Monday, 8:30
                self.__store_obtained(obtained, current_prescription['Collect_Id'])  # update Collect table with is_obtained (true/false)
                if self.__is_prescription_time_passed(timestamp):  # checks if obtaining is the last row in database.
                    break
            time.sleep(5)

    def __store_obtained(self, is_obtained, collect_id):
        self.__patient_model.update_prescription_obtain(is_obtained, collect_id)

    def __send_alert(self, message):
        phone_number = f"{ISRAEL_CALLING_CODE}{self.patient_prescription[0]['Phone_number'][1:]}"  # build valid international phone number
        sns.publish(PhoneNumber=phone_number, Message=message)

    def send_alert(self, message):
        sms_template = f"Hello {self.patient_prescription[0]['First_Name']}, your patient - {self.__patient_name}, "  # insert variables to string
        self.__send_alert(sms_template + message)
