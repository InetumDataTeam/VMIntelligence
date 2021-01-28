import os

from content.processed_line import Processed_line
from content.postgres_serializer import Postgres_serializer
from content.my_file import My_file
from content.exceptions import *


# TODO
def pipeline(item):
    # mettre en forme (ajouter la date,etc... formatter la ligne en gros)
    return Processed_line(item).get_values()


def source(ctx):
    data = []
    if not os.path.isdir(ctx.source_path):
        raise DirNotFoundException
    for file in ctx.source_path:
        data.append(My_file(file, ctx.file_types).init())
    return data


def postgres_serializer(pwd, login, host, bdd_name):
    return Postgres_serializer(pwd, login, host, bdd_name)
