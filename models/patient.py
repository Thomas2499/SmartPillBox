from daos import PillDAO


class PatientModel:
    def __init__(self):
        self.__pill_dao = PillDAO()

    @staticmethod
    def __map_data_to_columns__(data, columns):
        mapping = []
        for row_index in range(len(data)):
            row = {columns[cell_index]: data[row_index][cell_index] for cell_index in range(len(data[row_index]))}
            mapping.append(row)
        return mapping

    def get_ids(self):
        data = self.__pill_dao.get("allowed_patients_ids", format=None)
        return [row[0] for row in data[0]]

    def get_combinations(self, patient_id):
        data, columns = self.__pill_dao.get("patient_pills_combinations", format=patient_id)
        return self.__map_data_to_columns__(data, columns)

    def get_prescription(self, patient_id):
        data, columns = self.__pill_dao.get("patient_prescription", format=patient_id)
        return self.__map_data_to_columns__(data, columns)
