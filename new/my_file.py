from new.exceptions import FileNameException, FileTypeException
import pandas as pd


class my_file:
    def __init__(self, filename, file_types):
        self.filename = filename
        self.type = type

    def init(self):

        try:
            self.validate_file_name()
            self.validate_file_type()
            return self.extract()
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
        if self.type:
            pass
        else:
            raise FileTypeException

    def extract(self):
        return pd.read_excel()  # extraire
