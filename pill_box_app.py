from views import PillView
import json


class PillBoxApp:
    def __init__(self):
        self.__pill_view = PillView()
        self.__pill_view.print_welcome_text()

    def patient_authentication(self):
        empty_id = True
        while empty_id:
            input_data = self.__pill_view.get_patient_id()
            if self.__pill_view.validate_input_patient_id(input_data):
                self.__pill_view.save_patient_id(input_data)
                empty_id = False
            else:
                self.__pill_view.print_not_valid_input(input_data)

    def validate_safe_pills_combinations(self):
        if not self.__pill_view.validate_safe_pills_combinations():
            self.__pill_view.send_alert()
        else:
            self.__pill_view.send_alert()

    def store_patient_prescription(self):
        self.__pill_view.store_patient_prescription()

    def listen_for_keyboard_keys(self):
        self.__pill_view.print_prescription()
        while True:
            key = input()
            if not self.__pill_view.validate_pill_obtaining(key):
                print("took pill not in the right timing")
                self.__pill_view.send_alert()
            else:
                print("took pill in the right timing")



