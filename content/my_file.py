from content.exceptions import FileNameException, FileTypeException
import pandas as pd
import re
from pathlib import Path

class My_file:
    def __init__(self, filename, file_types):
        self.filename = filename
        self.file_types = file_types
        self.mytype = ""

    def init(self):
        try:
            self.validate_file_name()
            self.mytype = self.validate_file_type()
            return self.extract()
        except FileNameException:
            print("FileNameException: Filename not compliant")
        except FileTypeException:
            print("FileTypeException: Type is empty")

    def validate_file_name(self):
        if Path(self.filename).suffix == '.xlsm':
            return True
        else:
            raise FileNameException

    def validate_file_type(self):
        if re.match("^.*.OCEANET.*", self.file_types) or re.match("^.*.Azure.*", self.file_types):
            return True
        else:
            raise FileTypeException

    def extract(self):
        _, feuille, _ = self.file_types
        return pd.read_excel(self.filename, sheet_name=feuille).to_dict(orient='split').get("data")  # extraire
