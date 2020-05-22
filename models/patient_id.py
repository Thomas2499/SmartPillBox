from daos import PillDAO


class PatientIdModel:
    def __init__(self):
        self.__pill_dao = PillDAO()

    def get(self):
        data = self.__pill_dao.get("allowed_patients_ids")
        return [pid[0] for pid in data]
