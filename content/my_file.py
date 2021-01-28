from content.exceptions import FileNameException, FileTypeException
import pandas as pd


class My_file:
    def __init__(self, filename, file_types):
        self.filename = filename
        self.file_types = file_types

    def init(self):
        try:
            self.validate_file_name()
            type = self.validate_file_type()
            return self.extract(type)
        except FileNameException:
            print("FileNameException: Filename not compliant")
        except FileTypeException:
            print("FileTypeException: Type is empty")

    def validate_file_name(self):
        if self.filename:  # verifier (regex,uppercase...)
            pass
        else:
            raise FileNameException

    def validate_file_type(self):
        if self.file_types:  # verifier (regex,uppercase...)
            pass
        else:
            raise FileTypeException

    def extract(self):
        return pd.read_excel(self.type),  # extraire
