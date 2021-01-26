from new.context import Context
from new.functions import *
import pytest


@pytest.mark.parametrize(
    "ctx,combinator, expected", [(Context().add_source_path(path=""), combinator,"")]
)
def test_source(ctx, combinator, expected):
    assert source(ctx, combinator) == expected


@pytest.mark.parametrize(
    "item, expected", [({"colonne0": "val", "colonne1": "val"}, {"host_type": "Azure"}),{"colonne": "valeur"}]
)
def test_pipeline(item, expected):
    assert pipeline(item).get_values() == expected

