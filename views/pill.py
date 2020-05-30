from views.enums import ConsolePrintColor as Color
from views.consts import INVALID_INPUT_DELAY, WEEKDAYS
from presenters import PillPresenter
import time


class PillView:
    def __init__(self):
        self.__pill_presenter = PillPresenter()
        self.__patients_ids = self.__pill_presenter.get_patients_ids()

    @staticmethod
    def print_welcome_text():
        print(f"{Color.HEADER}*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*{Color.ENDC}")
        print(f"{Color.HEADER}|              Smart PillBox              |{Color.ENDC}")
        print(f"{Color.HEADER}*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*{Color.ENDC}")

    @staticmethod
    def print_not_valid_input(input_data):
        print(f"{Color.FAIL}\nThe input {input_data} is not a valid patient ID in the Smart PillBox database.{Color.ENDC}")
        time.sleep(INVALID_INPUT_DELAY)

    @staticmethod
    def get_patient_id():
        return input("\nInsert your personal Id to proceed: ")

    def validate_input_patient_id(self, input_id):
        return input_id in self.__patients_ids

    def save_patient_id(self, patient_id):
        self.__pill_presenter.patient_id = patient_id

    def save_patient_name(self, patient_id):
        self.__pill_presenter.save_patient_name(patient_id)

    def validate_safe_pills_combinations(self):
        return self.__pill_presenter.validate_safe_pills_combinations()

    def store_patient_prescription(self):
        self.__pill_presenter.store_patient_prescription()

    def print_prescription(self):
        for obtaining in self.__pill_presenter.patient_prescription:
            print(f"{Color.OKBLUE}Obtain a medicine from box number {obtaining['Box_Id']}"
                  f" on {WEEKDAYS[int(obtaining['Day_Id'])]} at {obtaining['Hour_Id']}"
                  f" by pressing {obtaining['Cell_id']}.{Color.ENDC}")

    def validate_pill_obtaining(self, key):
        return self.__pill_presenter.validate_input_key(key) and self.__pill_presenter.validate_input_key_timing(key)

    def update_obtaining(self, key):
        self.__pill_presenter.update_obtaining(key)

    def start_event_listener(self):
        self.__pill_presenter.assurance_listener()

    def send_alert(self, message):
        self.__pill_presenter.send_alert(message)



