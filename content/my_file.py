from loguru import logger

from content.exceptions import FileNameException, FileTypeException
import pandas as pd
import re
from pathlib import Path


class My_file:
    def __init__(self, filepath, file_types):
        self.filepath = filepath
        self.file_types = file_types
        self.mytype = ""

    def init(self):
        self.mytype = self.validate_file_type()
        self.validate_file_name()

        return self.extract(self.mytype)

    def validate_file_name(self):
        if Path(self.filepath).suffix == '.xlsm':
            return True
        else:
            raise FileNameException

    def validate_file_type(self):
        for fi in self.file_types:
            f, _, _ = fi
            if re.match(f"^.*.{f}.*", str(self.filepath).lower()):
                return fi
            else:
                continue
        raise FileTypeException

    def extract(self, type_m):

        _, feuille, _ = type_m

        tab = pd.read_excel(self.filepath, sheet_name=feuille).to_dict(orient='split').get("data")

        types = [(type_m, self.filepath) for _ in range(len(tab))]
        
        tab = list(zip(tab, types))
        # logger.info(tab)
        return tab
