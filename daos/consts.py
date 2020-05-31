DRIVER = "ODBC Driver 17 for SQL Server"
USERNAME = "DESKTOP-CGQADNQ\Tomer"
DATABASE = "smart_pill_box2"
SERVER = "DESKTOP-CGQADNQ"
PASSWORD = "machete"


QUERIES = {
    "allowed_keyboard_keys": "SELECT Cell_Id FROM dbo.Cell",
    "allowed_patients_ids": "SELECT Pateint_Id from dbo.Caregiver_Patient",
    "patient_name": "SELECT First_Name from dbo.Person WHERE Person_Id='{0}'",
    "patient_pills_combinations": "select Person.Phone_number, Constraint_ATC.Does_not_Combine_With,"
                                  " ATC5.Active_component FROM Prescription"
                                  " inner join Constraint_ATC on Constraint_ATC.Drug_Id=Prescription.Drug_Id"
                                  " inner join ATC5 on ATC5.Drug_Id=Prescription.Drug_Id"
                                  " inner join Person on Person.Person_Id=Prescription.Caregiver_Id"
                                  " where Pateint_Id='{0}'",
    "patient_prescription": "SELECT Person.First_Name, Person.Phone_number,"
                            " Box.Date_received, Collect.Collect_Id, Collect.is_obtained, Collect.Box_Id,"
                            " Collect.Cell_id, Collect.Day_Id, Collect.Hour_Id"
                            " FROM Collect inner join Box ON Collect.Box_Id=Box.Box_ID"
                            " inner join Person ON Box.Caregiver_Id=Person.Person_Id"
                            " Where Box.pateint_id='{0}'"
                            " Order by Box.Date_received",
    "update_patient_obtain": "UPDATE dbo.Collect SET is_obtained='{0}' WHERE Collect.Collect_Id='{1}'"
}
