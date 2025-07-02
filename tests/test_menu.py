import pytest

from fableforge import menus as menu


def test_menu_handler_invokes_action(monkeypatch):
    monkeypatch.setattr(menu, "clear_console", lambda: None)
    monkeypatch.setattr(menu.console, "print", lambda *a, **k: None)
    inputs = iter(["x", "1"])  # first invalid, then valid
    monkeypatch.setattr(menu.console, "input", lambda *_: next(inputs))

    invalid_called = []
    monkeypatch.setattr(menu.Console, "invalid_choice", lambda: invalid_called.append(True))

    called = []
    def action():
        called.append(True)
        raise StopIteration

    with pytest.raises(StopIteration):
        menu.Console.menu_handler("Title", [{"label": "Opt", "action": action}])

    assert invalid_called == [True]
    assert called == [True]


def test_play_game_passes_expected_options(monkeypatch):
    captured = {}
    def fake_menu_handler(title, options):
        captured["title"] = title
        captured["labels"] = [opt["label"] for opt in options]
    monkeypatch.setattr(menu.Console, "menu_handler", fake_menu_handler)
    menu.play_game()
    assert captured["title"] == "FableForge - Play"
    assert captured["labels"] == [
        "Character Menu",
        "Quest Menu",
        "Back to main menu",
    ]