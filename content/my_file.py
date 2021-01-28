from content.exceptions import FileNameException, FileTypeException
import pandas as pd


class My_file:
    def __init__(self, filename, file_types):
        self.filename = filename
        self.file_types = file_types

    def init(self):
        try:
            self.validate_file_name(self.filename)
            type = self.validate_file_type(self.file_types)
            return self.extract(type)
        except FileNameException:
            print("FileNameException: Filename not compliant")
        except FileTypeException:
            print("FileTypeException: Type is empty")

    def validate_file_name(self, filename):
        if filename:  # verifier (regex,uppercase...)
            pass
        else:
            raise FileNameException

    def validate_file_type(self, file_types):
        if file_types:  # verifier (regex,uppercase...)
            pass
        else:
            raise FileTypeException

    def extract(self, type):
        return pd.read_excel(),  # extraire
