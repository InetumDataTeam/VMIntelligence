from content.context import Context
from content.functions import *
from content.exceptions import *
import pytest

from content.traitement import Traitement


class TraitementAzure(Traitement):
    def init(self, data):
        pass


class TraitementOceanet(Traitement):
    def init(self, data):
        pass


@pytest.mark.parametrize(
    "ctx, expected", [(Context("../../res", [("type1", TraitementAzure), ("type2", TraitementOceanet)]), [])]
)
def test_source(ctx, expected):
    assert len(source(ctx)) > 0


@pytest.mark.parametrize(
    "ctx, expected", [(Context("je/suis/un/", [("type1", TraitementAzure), ("type2", TraitementOceanet)]), [])]
)
def test_source_dir_error(ctx, expected):
    with pytest.raises(DirNotFoundException):
        source(ctx)


@pytest.mark.parametrize(
    "item, expected", [()]
)
def test_pipeline(item, expected):
    assert pipeline(item).get_values() == expected


# -----------------------------------MY_FILE------------------------------------------
@pytest.mark.parametrize(
    "filename, type_files, expected", [("", "", "")]
)
def test_init(filename, type_files, expected):
    assert True


@pytest.mark.parametrize(
    "filename, expected", [()]
)
def test_validate_file_name(filename, expected):
    pass


@pytest.mark.parametrize(
    "file_types, expected", [()]
)
def test_validate_file_type(file_types, expected):
    pass


@pytest.mark.parametrize(
    "type, expected", [()]
)
def test_extract(type, expected):
    pass


# --------------------------------------Processed_line------------------------------------------------

@pytest.mark.parametrize(
    "ctx, postgres_serializer, expected", [()]
)
def test_integrate(ctx, postgres_serializer, expected):
    pass


@pytest.mark.parametrize(
    "expected", [()]
)
def test_get_values(expected):
    pass


@pytest.mark.parametrize(
    "type_file,content, expected", [()]
)
def test_construct_line(type_file, content, expected):
    pass


# ---------------------------------------Postgres_serializer---------------------------------------------------


@pytest.mark.parametrize(
    " expected", [()]
)
def test_connect(expected):
    pass
