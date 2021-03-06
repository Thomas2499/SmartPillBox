from pill_box_app import PillBoxApp


def main():
    pill_box_app = PillBoxApp()  # Creating class instance
    pill_box_app.patient_authentication()
    pill_box_app.validate_safe_pills_combinations()
    pill_box_app.store_patient_prescription()
    pill_box_app.listen_for_keyboard_keys()


if __name__ == '__main__':
    main()
