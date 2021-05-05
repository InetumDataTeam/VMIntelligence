from content.functions import *
from content.exceptions import *
from content.context import Context
from loguru import logger
import pandas as pd
from content.traitement import Traitement
import setuptools
import click
import time
from watchdog.observers import Observer
from watchdog.events import FileMovedEvent,FileModifiedEvent

class TraitementAzure(Traitement):

    def init(self, data, filename):
        VM, Projet_AzureDevOps, Projet, SYGES, CP, CostCenter, Client, Mois, Cout = data[3], data[2], data[5], data[6], data[7], data[8], data[9], data[10], data[11]
        typeVM = "ProjetAzureDevops" if not str(Projet_AzureDevOps) == "nan" else "VM"
        VM = VM if not str(VM) == "nan" else Projet_AzureDevOps
        date = str(Mois) + "-01"
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


@click.command()
@click.option("--pwd", help="Database Password")
@click.option("--bdd_name", help="Database Name")
@click.option("--login", help="Database Username")
@click.option("--host", help="Database Server Host")
@click.option("--port", help="Database Server Port")
@click.option("--path", help="Files Path")
def main(pwd: str, bdd_name: str, login: str, host: str, port: str, path: str):
    ctx = Context(source_path=path, file_types=[("azure", "VMAzure-Env-Projet", TraitementAzure), ("oceanet", "VMEnvProjet", TraitementOT)])
    postgres_serializer = Postgres_serializer(pwd, login, host, port, bdd_name).connect()
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

