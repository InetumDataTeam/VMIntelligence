from new.processed_line import Processed_line
from new.postgres_serializer import Postgres_serializer
from new.my_file import my_file


# TODO
def pipeline(item):
    # mettre en forme (ajouter la date,etc... formatter la ligne en gros)
    return Processed_line(item)


def source(ctx):
    for file in ctx.source_path:
        my_file(file, ctx.file_types).init()


# TODO
def get_file_type(filename, types):
    for t in types:
        if t in filename:  # faire d'autres verifs ( uppercase etc (voir les libraries...)
            return ""


def postgres_serializer(pwd, login, host, bdd_name):
    return Postgres_serializer(pwd, login, host, bdd_name)
