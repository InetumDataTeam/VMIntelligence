from content.functions import *
from content.exceptions import *
from content.context import Context
from loguru import logger
import pandas as pd
from content.traitement import Traitement

pwd = "postgres"
bdd_name = "postgres"
login = "postgres"
host = "localhost"
path = "./../res"


class TraitementAzure(Traitement):

    def init(self, data, filename):
        read_file_projets = pd.read_excel(filename, sheet_name='Projets', usecols=['NomProj', 'CP'])
        VM, Projet_AzureDevOps, Projet, SYGES, CostCenter, Client, Mois, Cout = data[3], data[2], data[5], data[6], data[7], data[8], data[9], data[10]
        typeVM = "ProjetAzureDevops" if not str(Projet_AzureDevOps) == "nan" else "VM"
        VM = VM if not str(VM) == "nan" else Projet_AzureDevOps
        CP = ""
        date = Mois + "-01"
        for c2 in read_file_projets.values:
            if (data[5] == c2[0]) and str(c2[1]) != "nan":
                CP = c2[1]
        return VM, 0, SYGES, Client, Cout, Projet, CP, CostCenter, "Azure", typeVM, date


class TraitementOT(Traitement):
    def init(self, data, filename):
        date = filename.split("OCEANET ")[1].replace(".xlsm", "") + "-01"
        VM, SYGES, Client, CoutGlobal, CoutLicenceMS, CP, Projet, CostCenter = data[0], data[16], data[17], data[19], data[15], data[24], data[23], data[25],

        if not VM == "Total" and not str(VM) == "nan" and not str(CoutLicenceMS) == "nan" and not str(SYGES) == "nan" and not str(Client) == "nan" and not str(
                CoutGlobal) == "nan" and not str(Projet) == "nan" and not str(CP) == "nan" and not str(CostCenter) == "nan":
            return VM, CoutLicenceMS, SYGES, Client, CoutGlobal, Projet, CP, CostCenter, "Oceanet", "VM", date
        else:
            return None


ctx = Context(source_path=path, file_types=[("azure", "VMAzure-Env-Projet", TraitementAzure), ("oceanet", "VMEnvProjet", TraitementOT)])
postgres_serializer = Postgres_serializer(pwd, login, host, bdd_name).connect()
it = None

try:
    it = source(ctx)
except SourceError as e:
    logger.error(e)

if it:
    for item in it:
        try:
            processed_line = pipeline(item)
            processed_line.integrate(postgres_serializer)
        except TransformError as e:
            logger.error(e)
        except SerializationError as e:
            logger.error(e)
