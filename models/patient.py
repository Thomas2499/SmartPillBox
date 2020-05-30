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

    def get_name_by_id(self, pid):
        data = self.__pill_dao.get("patient_name", format=pid)
        return data[0][0]

    def get_combinations(self, pid):
        data, columns = self.__pill_dao.get("patient_pills_combinations", format=pid)
        return self.__map_data_to_columns__(data, columns)

    def get_prescription(self, pid):
        data, columns = self.__pill_dao.get("patient_prescription", format=pid)
        return self.__map_data_to_columns__(data, columns)

    def update_prescription_obtain(self, *args):
        print(args)
        self.__pill_dao.update("update_patient_obtain", format=args)
