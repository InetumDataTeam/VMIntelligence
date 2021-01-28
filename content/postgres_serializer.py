class Postgres_serializer:
    def __init__(self, pwd, login, host, bdd_name):
        self.pwd = pwd
        self.bdd_name = bdd_name
        self.login = login
        self.host = host

    def connect(self):
        pass
