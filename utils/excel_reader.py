import os

import openpyxl


class ExcelReader:
    base_dir = os.getcwd()  # equivalent to System.getProperty("user.dir")
    path_1 = os.path.join(base_dir, "testdata", "testdata.xlsx")

    def __init__(self, sheet_name: str = "Sheet1"): # Centralized path construction

        # Directory of excel_reader.py → project/utils
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level → project/
        project_root = os.path.dirname(current_dir)
        # Now point to project/testdata/testdata.xlsx
        self.file_path = os.path.join(project_root, "testdata", "testdata.xlsx")

        self.sheet_name = sheet_name
        self.workbook = openpyxl.load_workbook(self.file_path)
        self.sheet = self.workbook[self.sheet_name]

    def get_credentials(self, tc_id: str):
        """
        Reads username and password for the given test case ID.
        Assumes columns: TC_ID | Username | Password
        """
        for row in self.sheet.iter_rows(min_row=2, values_only=True):  # skip header
            if row[0] == tc_id:
                return {"username": row[1], "password": row[2]}
        raise ValueError(f"Test case ID '{tc_id}' not found in sheet '{self.sheet_name}'")
