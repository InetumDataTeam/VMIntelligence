import reader as r
import pytest as pt

def test_read_directory_exception() :
    with pt.raises(FileNotFoundError) as excinfo:
        r.read("test")
        #excinfo.match(FileNotFoundError)
        excinfo.match("[WinError 3] Le chemin d’accès spécifié est introuvable: 'test'")

