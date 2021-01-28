from sqlalchemy import create_engine, text


class Postgres_serializer:
    def __init__(self, pwd, login, host, bdd_name):
        self.pwd = pwd
        self.bdd_name = bdd_name
        self.login = login
        self.host = host
        self.engine = ""

    def connect(self):
        self.engine = create_engine(f"postgresql+psycopg2://{self.login}:{self.pwd}@{self.host}:5432/{self.bdd_name}")

    def insert(self, content):
        VM, CoutLicenceMS, SYGES, Client, CoutGlobal, Projet, CP, CostCenter, hebergeur, typeVM, date = content

        print(VM, CoutLicenceMS, SYGES, Client, CoutGlobal, Projet, CP, CostCenter, hebergeur, typeVM, date)

        sql = f"insert into dimension_syges (client, costcenter, syges) values (:Client, :CostCenter, :SYGES) ON CONFLICT(client, costcenter, syges) " \
              f"DO UPDATE SET client=excluded.client RETURNING idsyges"
        idsyges = self.engine.execute(text(sql), [{"Client": Client, "CostCenter": CostCenter, "SYGES": SYGES}])
        idsyges = int(str(idsyges.first()).removeprefix("(").removesuffix(")").removesuffix(","))

        # -------------------------------------------------------
        sql = f"insert into dimension_projet (idsyges, chefprojet, projet) values (:idsyges, :CP, :Projet) ON CONFLICT(idsyges, chefprojet, projet)" \
              f" DO UPDATE SET idsyges=excluded.idsyges RETURNING idprojet"
        idprojet = self.engine.execute(text(sql), [{"idsyges": idsyges, "CP": CP, "Projet": Projet}])
        idprojet = int(str(idprojet.first()).removeprefix("(").removesuffix(")").removesuffix(","))

        # --------------------------------------------------------
        sql = f"insert into dimension_vm (idprojet, hebergeur, typevm, vm) values (:idprojet, :hebergeur, :typeVM,:VM) ON CONFLICT(idprojet, hebergeur, typevm, vm) " \
              f"DO UPDATE SET idprojet=excluded.idprojet RETURNING idvm"
        idvm = self.engine.execute(text(sql), [{"idprojet": idprojet, "hebergeur": hebergeur, "typeVM": typeVM, "VM": VM}])
        idvm = int(str(idvm.first()).removeprefix("(").removesuffix(")").removesuffix(","))

        # --------------------------------------------------------
        sql = f"insert into dimension_projetvm (idprojet, idvm) values (:idprojet, :idvm) ON CONFLICT(idprojet, idvm) DO UPDATE SET idprojet=excluded.idprojet RETURNING idprojetvm"
        idprojetvm = self.engine.execute(text(sql), [{"idprojet": idprojet, "idvm": idvm}])
        idprojetvm = int(str(idprojetvm.first()).removeprefix("(").removesuffix(")").removesuffix(","))

        # --------------------------------------------------------
        sql = f"insert into fait_cout (date_cout, montant_hors_licencems, montant_licencems, idprojetvm) values (:date, :CoutGlobal, :CoutLicenceMS, :idprojetvm) " \
              f"ON CONFLICT(date_cout, idprojetvm) DO NOTHING"

        self.engine.execute(text(sql), [{"date": date, "CoutGlobal": CoutGlobal or None, "CoutLicenceMS": CoutLicenceMS or None, "idprojetvm": idprojetvm}])
