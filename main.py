import os
import pandas as pd
from sqlalchemy import text
from sqlalchemy import create_engine

directory = 'res'
separator = os.path.sep


def connectPostgres(host, user, passw, database):
    engine = create_engine(f"postgresql+psycopg2://{user}:{passw}@{host}:5432/{database}")
    return engine.connect()


def insertion(VM, CoutLicenceMS, SYGES, Client, CoutGlobal, Projet, CP, CostCenter, hebergeur, typeVM, date):
    # print(VM, CoutLicenceMS, SYGES, Client, CoutGlobal, Projet, CP, CostCenter, hebergeur, typeVM, date)

    sql = f"insert into dimension_syges (client, costcenter, syges) values (:Client, :CostCenter, :SYGES) ON CONFLICT(client, costcenter, syges) " \
          f"DO UPDATE SET client=excluded.client RETURNING idsyges"
    idsyges = conn.execute(text(sql), [{"Client": Client, "CostCenter": CostCenter, "SYGES": SYGES}])
    idsyges = int(str(idsyges.first()).removeprefix("(").removesuffix(")").removesuffix(","))

    # -------------------------------------------------------
    sql = f"insert into dimension_projet (idsyges, chefprojet, projet) values (:idsyges, :CP, :Projet) ON CONFLICT(idsyges, chefprojet, projet)" \
          f" DO UPDATE SET idsyges=excluded.idsyges RETURNING idprojet"
    idprojet = conn.execute(text(sql), [{"idsyges": idsyges, "CP": CP, "Projet": Projet}])
    idprojet = int(str(idprojet.first()).removeprefix("(").removesuffix(")").removesuffix(","))

    # --------------------------------------------------------
    sql = f"insert into dimension_vm (idprojet, hebergeur, typevm, vm) values (:idprojet, :hebergeur, :typeVM,:VM) ON CONFLICT(idprojet, hebergeur, typevm, vm) " \
          f"DO UPDATE SET idprojet=excluded.idprojet RETURNING idvm"
    idvm = conn.execute(text(sql), [{"idprojet": idprojet, "hebergeur": hebergeur, "typeVM": typeVM, "VM": VM}])
    idvm = int(str(idvm.first()).removeprefix("(").removesuffix(")").removesuffix(","))

    # --------------------------------------------------------
    sql = f"insert into dimension_projetvm (idprojet, idvm) values (:idprojet, :idvm) ON CONFLICT(idprojet, idvm) DO UPDATE SET idprojet=excluded.idprojet RETURNING idprojetvm"
    idprojetvm = conn.execute(text(sql), [{"idprojet": idprojet, "idvm": idvm}])
    idprojetvm = int(str(idprojetvm.first()).removeprefix("(").removesuffix(")").removesuffix(","))

    # --------------------------------------------------------
    sql = f"insert into fait_cout (date_cout, montant_hors_licencems, montant_licencems, idprojetvm) values (:date, :CoutGlobal, :CoutLicenceMS, :idprojetvm) " \
          f"ON CONFLICT(date_cout, idprojetvm) DO NOTHING"

    conn.execute(text(sql), [{"date": date, "CoutGlobal": CoutGlobal or None, "CoutLicenceMS": CoutLicenceMS or None, "idprojetvm": idprojetvm}])


def add_CP_Azure(df):
    read_file_projets = pd.read_excel(directory + separator + filename, sheet_name='Projets', usecols=['NomProj', 'CP'])

    df.insert(8, "CP", "Sans CP")
    for id, c1 in enumerate(df.values):
        for c2 in read_file_projets.values:
            if (c1[2] == c2[0]) and str(c2[1]) != "nan":
                df['CP'][id] = c2[1]

    return df


def integration(filename):
    if "Azure" in filename and ".xlsm" in filename:
        read_file = pd.read_excel(directory + separator + filename, sheet_name='VMAzure-Env-Projet',
                                  usecols=['VM', 'Projet AzureDevOps', 'Projet', 'Code SYGES', 'Cost Center', 'Client', 'Mois', 'Coût'])
        read_file = add_CP_Azure(read_file)
        dict = read_file.to_dict(orient='split')

        CoutLicenceMS = ""

        for line in dict.get("data"):
            ProjetAzureDevops, VM, Projet, CodeSyges, CostCenter, Client, date, cout, CP = line
            hebergeur = "Azure"
            typeVM = "ProjetAzureDevops" if ProjetAzureDevops else "VM"
            date = date + "-01"
            insertion(VM, CoutLicenceMS, CodeSyges, Client, cout, Projet, CP, CostCenter, hebergeur, typeVM, date)

    elif "OCEANET" and ".xlsm" in filename and ".xlsm" in filename:
        read_file = pd.read_excel(directory + separator + filename, sheet_name='VMEnvProjet',
                                  usecols=['VM', 'SYGES', 'Client', 'CoutGlobal', 'CoutLicenceMS', 'CP', 'Projet', 'CostCenter'])
        dict = read_file.to_dict(orient='split')
        hebergeur = "OCEANET"
        typeVM = "VM"
        date = filename.split("OCEANET ")[1].replace(".xlsm", "") + "-01"
        for line in dict.get("data"):
            VM, CoutLicenceMS, SYGES, Client, CoutGlobal, Projet, CP, CostCenter = line
            insertion(VM, CoutLicenceMS, SYGES, Client, CoutGlobal, Projet, CP, CostCenter, hebergeur, typeVM, date)
            # TODO verif si ya pas de 'nan'
    else:
        print("File not complient")


conn = connectPostgres("localhost", "guest", "tseug", "postgres")
for filename in os.listdir(directory):
    integration(filename)
