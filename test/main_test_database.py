import pytest
import tempfile
from pytest_postgresql import factories
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declarative_base
import main

socket_dir = tempfile.TemporaryDirectory()
postgresql_my_proc = factories.postgresql_proc(port=None, unixsocketdir=socket_dir.name)
postgresql_my = factories.postgresql('postgresql_my_proc')


@pytest.fixture(scope='function')
def setup_database(postgresql_my):
    def dbcreator():
        return postgresql_my.cursor().connection

    engine = create_engine('postgresql+psycopg2://', creator=dbcreator)

    yield engine


@pytest.fixture(scope='function')
def dataset(setup_database):
    session = setup_database

    file = open("../res/postgres.sql")
    query = text(file.read())

    session.execute(query)
    # Ajouter la data

    yield session


def test_database(dataset):
    # Gets the session from the fixture
    session = dataset

    print(session.execute("select table_name from information_schema.tables where table_name like 'dimension%'").first())

    assert session.has_table("dimension_syges")
    assert session.has_table("dimension_vm")
    assert session.has_table("fait_cout")
    assert session.has_table("dimension_projetvm")
    assert session.has_table("dimension_projet")


def test_insertion(dataset):
    session = dataset
    # main.insertion(session, "VM", "CoutLicenceMS", "SYGES", "Client", "CoutGlobal", "Projet", "CP", "CostCenter", "hebergeur", "typeVM", "date")

    # assert session.execute("select * from dimension_syges") == ""

    # # Do some basic checking
    # assert len(session.query(User).all()) == 2
    # assert len(session.query(Account).all()) == 3
    # assert len(session.query(UserAccount).all()) == 4
    #
    # # Retrieves John and Mary
    # john = session.query(User).filter(User.username == username).one()
    #
    # # Checks their accounts
    # assert len(get_accounts_by_user(john.username, session)) == 2
    # assert len(get_accounts_by_user(mary.username, session)) == 2
    #
    # # Checks the balance
    # assert compute_balance(john.username, session) == 30.0
    # assert compute_balance(mary.username, session) == 25.0

    # Attemps to debit from the joint account, i.e index 1
    # joint_account = get_accounts_by_user(john.username, session)[1]
    # debit(joint_account.id, 10.0, session)
    # assert compute_balance(john.username, session) == 20.0
    # assert compute_balance(mary.username, session) == 15.0
