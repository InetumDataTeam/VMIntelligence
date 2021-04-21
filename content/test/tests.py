from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError

from content.context import Context
from content.functions import *
from content.exceptions import *
from content.my_file import *
import pytest

from content.traitement import Traitement


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
        VM, SYGES, Client, CoutGlobal, CoutLicenceMS, CP, Projet, CostCenter = data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],

        if not VM == "Total" and not str(VM) == "nan" and not str(CoutLicenceMS) == "nan" and not str(SYGES) == "nan" and not str(Client) == "nan" and not str(
                CoutGlobal) == "nan" and not str(Projet) == "nan" and not str(CP) == "nan" and not str(CostCenter) == "nan":
            return VM, CoutLicenceMS, SYGES, Client, CoutGlobal, Projet, CP, CostCenter, "Oceanet", "VM", date
        else:
            return None


@pytest.mark.parametrize(
    "ctx",
    [(Context("/Users/camillesaury/Documents/workspace/python/VMIntelligence/res", [("azure", "VMAzure-Env-Projet", TraitementAzure), ("oceanet", "VMEnvProjet", TraitementOT)]))]
)
def test_source(ctx):
    assert len(source(ctx)) > 0


@pytest.mark.parametrize(
    "ctx, expected", [(Context("je/suis/un/", [("type1", TraitementAzure), ("type2", TraitementOT)]), [])]
)
def test_source_dir_error(ctx, expected):
    with pytest.raises(DirNotFoundException):
        source(ctx)


@pytest.mark.parametrize(
    "item, expected", [(
            (["VM", "SYGES", "Client", 0, 0, "Projet", "CP", "CostCenter"], (('oceanet', 'VMEnvProjet', TraitementOT), "./../../res/Inventaire OCEANET 2020-12.xlsm")),
            ("VM", 0, "SYGES", "Client", 0, "CP", "Projet", "CostCenter", "Oceanet", "VM", "2020-12-01"))]
)
def test_pipeline(item, expected):
    assert pipeline(item).get_values() == expected


# -----------------------------------MY_FILE------------------------------------------
@pytest.mark.parametrize(
    "filepath, type_files", [("/Users/camillesaury/Documents/workspace/python/VMIntelligence/res/Inventaire Azure v1.1.xlsm",
                              [("azure", "VMAzure-Env-Projet", TraitementAzure), ("oceanet", "VMEnvProjet", TraitementOT)])]
)
def test_init(filepath, type_files):
    res = My_file(filepath, type_files).init()
    assert len(res) > 0 and type(res) == list


@pytest.mark.parametrize(
    "filepath, type_files, expected", [("/Users/camillesaury/Documents/workspace/python/VMIntelligence/res/Inventaire Azure v1.1.x",
                                        [("azure", "VMAzure-Env-Projet", TraitementAzure), ("oceanet", "VMEnvProjet", TraitementOT)],
                                        "")]
)
def test_init_FileNameException(filepath, type_files, expected):
    with pytest.raises(FileNameException):
        My_file(filepath, type_files).init()


@pytest.mark.parametrize(
    "filepath, type_files, expected", [("/Users/camillesaury/Documents/workspace/python/VMIntelligence/res/postgres.sql",
                                        [("azure", "VMAzure-Env-Projet", TraitementAzure), ("oceanet", "VMEnvProjet", TraitementOT)],
                                        "")]
)
def test_init_FileTypeException(filepath, type_files, expected):
    with pytest.raises(FileTypeException):
        My_file(filepath, type_files).init()


@pytest.mark.parametrize(
    "filepath, type_files, expected", [("/Users/camillesaury/Documents/workspace/python/VMIntelligence/res/Inventaire Azure v1.1.xlsm",
                                        [("azure", "VMAzure-Env-Projet", TraitementAzure), ("oceanet", "VMEnvProjet", TraitementOT)],
                                        True)]
)
def test_validate_file_name(filepath, type_files, expected):
    assert My_file(filepath, type_files).validate_file_name() == expected


@pytest.mark.parametrize(
    "filepath, type_files, expected", [("/Users/camillesaury/Documents/workspace/python/VMIntelligence/res/Inventaire Azure v1.1.xlsm",
                                        [("azure", "VMAzure-Env-Projet", TraitementAzure), ("oceanet", "VMEnvProjet", TraitementOT)],
                                        ("azure", "VMAzure-Env-Projet", TraitementAzure))]
)
def test_validate_file_type(filepath, type_files, expected):
    assert My_file(filepath, type_files).validate_file_type() == expected


@pytest.mark.parametrize(
    "filepath, type_files", [("/Users/camillesaury/Documents/workspace/python/VMIntelligence/res/Inventaire Azure v1.1.xlsm",
                              [("azure", "VMAzure-Env-Projet", TraitementAzure), ("oceanet", "VMEnvProjet", TraitementOT)])]
)
def test_extract(filepath, type_files):
    file = My_file(filepath, type_files)
    extract = file.extract(file.validate_file_type())
    assert len(extract) > 1 and type(extract) == list


# ---------------------------------------Postgres_serializer---------------------------------------------------


def test_false_connect():
    with pytest.raises(OperationalError):
        Postgres_serializer("coucou", "coucou", "localhost", "jesaispas").connect().engine.has_table("fait_cout")


def test_connect():
    assert Postgres_serializer("postgres", "postgres", "localhost", "postgres").connect().engine.has_table("fait_cout")
