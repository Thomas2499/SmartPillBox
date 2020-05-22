from views.enums import ConsolePrintColor as color
from presenters import PillPresenter
import time


class PillView:
    def __init__(self):
        self.__pill_presenter = PillPresenter()
        self.__patients_ids = self.__pill_presenter.get()
        self.print_welcome_text()

    @staticmethod
    def print_welcome_text():
        print(f"{color.HEADER}*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*{color.ENDC}")
        print(f"{color.HEADER}|              Smart PillBox              |{color.ENDC}")
        print(f"{color.HEADER}*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*{color.ENDC}")

    @staticmethod
    def print_not_valid_input(input_data):
        print(f"{color.FAIL}\nThe input {input_data} is not a valid ID in the Smart PillBox database.{color.ENDC}")
        time.sleep(3)

    @staticmethod
    def get_patient_id():
        return input("\nInsert your personal Id to proceed: ")

    def validate_input_patient_id(self, input_id):
        return input_id in self.__patients_ids


