from views import PillView


class PillBoxApp:
    def __init__(self):
        self.__pill_view = PillView()

    def patient_authentication(self):
        empty_id = True
        while empty_id:
            input_data = self.__pill_view.get_patient_id()
            if self.__pill_view.validate_input_patient_id(input_data):
                empty_id = False
            else:
                self.__pill_view.print_not_valid_input(input_data)