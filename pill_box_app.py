from views import PillView
import threading


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
                self.__pill_view.save_patient_name(input_data)
                empty_id = False
            else:
                self.__pill_view.print_not_valid_input(input_data)

    def store_patient_prescription(self):
        self.__pill_view.store_patient_prescription()

    def validate_safe_pills_combinations(self):
        if not self.__pill_view.validate_safe_pills_combinations():
            self.__pill_view.send_alert(message="does not have a safe pills combination in the prescription.")
            exit()

    def listen_for_keyboard_keys(self):
        t = threading.Thread(target=self.__pill_view.start_event_listener)
        t.start()
        self.__pill_view.print_prescription()
        while True:
            key = input().upper()
            if not t.is_alive():
                break
            if not self.__pill_view.validate_pill_obtaining(key):
                print("you took pill not in the right timing")
            else:
                print("you took pill in the right timing")
                self.__pill_view.update_obtaining(key)
