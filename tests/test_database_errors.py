import logging
import sqlite3
import pytest

from fableforge.data.database_manager import DatabaseManager
from fableforge.utils.utilities import setup_logging


def raise_error(*args, **kwargs):
    raise sqlite3.Error("boom")


def test_connect_error_logging(monkeypatch, caplog):
    setup_logging()
    caplog.set_level(logging.ERROR)
    monkeypatch.setattr(sqlite3, "connect", raise_error)
    manager = DatabaseManager()
    with pytest.raises(sqlite3.Error):
        manager.connect()
    assert any("boom" in rec.getMessage() for rec in caplog.records)


@pytest.mark.parametrize(
    "method,args",
    [
        ("initialize_tables", tuple()),
        ("add_item", (1, "x", 1)),
        ("remove_item", (1, "x", 1)),
        ("get_inventory", (1,)),
        ("save_quest_progress", (1, "q", "step")),
        ("load_quest_progress", (1, "q")),
        ("reset_quest_progress", (1, "q")),
    ],
)
def test_operation_error_logging(monkeypatch, caplog, method, args):
    setup_logging()
    caplog.set_level(logging.ERROR)
    manager = DatabaseManager()
    monkeypatch.setattr(manager, "connect", raise_error)
    func = getattr(manager, method)
    with pytest.raises(sqlite3.Error):
        func(*args)
    assert any("boom" in rec.getMessage() for rec in caplog.records)

