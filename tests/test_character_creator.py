from fableforge.engine import main
from fableforge.engine.main import CharacterCreator


def test_select_class(monkeypatch):
    monkeypatch.setattr(main, "clear_console", lambda: None)
    inputs = iter(["Wizard"])
    monkeypatch.setattr(main.console, "input", lambda *_: next(inputs))
    assert CharacterCreator.select_class() == "Wizard"


def test_random_stats():
    stats = CharacterCreator.random_stats()
    assert {
        "strength",
        "dexterity",
        "intelligence",
        "charisma",
        "wisdom",
        "constitution",
    } == set(stats.__dict__.keys())
    assert all(8 <= v <= 18 for v in stats.__dict__.values())
