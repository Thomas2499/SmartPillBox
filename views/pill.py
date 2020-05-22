from views.enums import ConsolePrintColor as Color
from views.consts import INVALID_INPUT_DELAY
from presenters import PillPresenter
import time


class PillView:
    def __init__(self):
        self.__pill_presenter = PillPresenter()
        self.__patients_ids = self.__pill_presenter.get()
        self.print_welcome_text()

    @staticmethod
    def print_welcome_text():
        print(f"{Color.HEADER}*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*{Color.ENDC}")
        print(f"{Color.HEADER}|              Smart PillBox              |{Color.ENDC}")
        print(f"{Color.HEADER}*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*{Color.ENDC}")

    @staticmethod
    def print_not_valid_input(input_data):
        print(f"{Color.FAIL}\nThe input {input_data} is not a valid ID in the Smart PillBox database.{Color.ENDC}")
        time.sleep(INVALID_INPUT_DELAY)

    @staticmethod
    def get_patient_id():
        return input("\nInsert your personal Id to proceed: ")

    def validate_input_patient_id(self, input_id):
        return input_id in self.__patients_ids


