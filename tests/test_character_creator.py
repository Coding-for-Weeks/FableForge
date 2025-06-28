from fableforge import main
from fableforge.main import CharacterCreator


def test_select_class(monkeypatch):
    monkeypatch.setattr(main, "clear_console", lambda: None)
    inputs = iter(["Wizard"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))
    assert CharacterCreator.select_class() == "Wizard"


def test_random_stats():
    stats = CharacterCreator.random_stats()
    assert set(stats.keys()) == {
        "strength",
        "dexterity",
        "intelligence",
        "charisma",
        "wisdom",
        "constitution",
    }
    assert all(8 <= v <= 18 for v in stats.values())
