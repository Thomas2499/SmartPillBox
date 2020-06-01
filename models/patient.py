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

    def get_ids(self):  # get ids from dao (data access object)
        data = self.__pill_dao.get("allowed_patients_ids", format=None)
        return [row[0] for row in data[0]]  # extract query result from the database.

    def get_name_by_id(self, pid):  # get patient name from database with his id
        data = self.__pill_dao.get("patient_name", format=pid)  # patient id inserted to the WHERE in query
        return data[0][0]  # extract patient name from data

    def get_combinations(self, pid):
        data, columns = self.__pill_dao.get("patient_pills_combinations", format=pid)
        return self.__map_data_to_columns__(data, columns)  # mapping column name to its value

    def get_prescription(self, pid):
        data, columns = self.__pill_dao.get("patient_prescription", format=pid)
        return self.__map_data_to_columns__(data, columns)  # mapping column name to its value

    def update_prescription_obtain(self, *args):
        print(args)
        self.__pill_dao.update("update_patient_obtain", format=args)
