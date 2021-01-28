import os

from content.processed_line import Processed_line
from content.postgres_serializer import Postgres_serializer
from content.my_file import My_file
from content.exceptions import *


def pipeline(item):
    # mettre en forme (ajouter la date,etc... formatter la ligne en gros)
    # item = {"type_file":type_file,"content":content} (dict)
    return Processed_line(item).get_values()


def source(ctx):
    data = []
    if not os.path.isdir(ctx.source_path):
        raise DirNotFoundException
    for file in ctx.source_path:
        myfile = My_file(file, ctx.file_types)
        myfile.init()
        data.extend(myfile.extract())
    return data
