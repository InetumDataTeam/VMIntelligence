from new.functions import *
import pytest


@pytest.mark.parametrize(
    "source_path, file_types, expected", [("je/suis/un/chemin", ["type1", "type2"], {"source_path": "je/suis/un/chemin", "file_types": ["type1", "type2"]})]
)
def test_source(source_path, file_types, expected):
    assert context(source_path, file_types) == expected


@pytest.mark.parametrize(
    "ctx,combi, expected", [(context("", ""), combinator, "")]
)
def test_source(ctx, combi, expected):
    assert source(ctx, combi) == expected


@pytest.mark.parametrize(
    "item, expected", [({"colonne0": "val", "colonne1": "val"}, {"host_type": "Azure"}), {"colonne": "valeur"}]
)
def test_pipeline(item, expected):
    assert pipeline(item).get_values() == expected

