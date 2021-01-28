from content.functions import *
from content.exceptions import *
from content.context import Context
import logging

from content.traitement import Traitement

pwd = ""
bdd_name = ""
login = ""
host = ""
path = ""


class TraitementAzure(Traitement):
    def init(self, data):
        cols = 'VM', 'Projet AzureDevOps', 'Projet', 'Code SYGES', 'Cost Center', 'Client', 'Mois', 'Coût'


class TraitementOT(Traitement):
    def init(self, data):
        cols = 'VM', 'SYGES', 'Client', 'CoutGlobal', 'CoutLicenceMS', 'CP', 'Projet', 'CostCenter'


ctx = Context(source_path=path, file_types=[("azure", "VMAzure-Env-Projet", TraitementAzure), ("oceanet", "VMEnvProjet", TraitementOT)])
postgres_serializer = Postgres_serializer(pwd, login, host, bdd_name).connect()
it = None

try:
    it = source(ctx)
except SourceError as e:
    logging.error(e)

if it:
    for item in it:
        try:
            processed_line = pipeline(item)
            processed_line.integrate(postgres_serializer)
        except TransformError as e:
            logging.error(e)
        except SerializationError as e:
            logging.error(e)
