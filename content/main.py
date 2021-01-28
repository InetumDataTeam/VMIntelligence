from content.functions import *
from content.exceptions import *
from content.context import Context
import logging

pwd = ""
bdd_name = ""
login = ""
host = ""
path = ""


# traitement du fichier si azure
def azure_traitement():
    pass


# traitement du fichier si oceanet
def oceanet_traitement():
    pass


ctx = Context(source_path=path, file_types=[("azure", azure_traitement), ("oceanet", oceanet_traitement)])
postgres_serializer = postgres_serializer(pwd, login, host, bdd_name)
it = None

try:
    it = source(ctx)
except SourceError as e:
    logging.error(e)

if it:
    for item in it:
        try:
            processed_line = pipeline(item)
            processed_line.integrate(ctx, postgres_serializer)
        except TransformError as e:
            logging.error(e)
        except SerializationError as e:
            logging.error(e)
