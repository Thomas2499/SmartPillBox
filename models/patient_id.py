from daos import PillDAO


class PatientIdModel:
    def __init__(self):
        self.__pill_dao = PillDAO()

    def get(self):
        data = self.__pill_dao.get("allowed_patients_ids")
        return [patient_id[0] for patient_id in data]
