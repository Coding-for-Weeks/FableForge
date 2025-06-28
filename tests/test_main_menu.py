import builtins
from fableforge import main


def test_main_menu_exit(monkeypatch):
    monkeypatch.setattr(main, "clear_console", lambda: None)
    monkeypatch.setattr(main, "exiting", lambda: (_ for _ in ()).throw(SystemExit))
    inputs = iter(["3"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))
    try:
        main.main_menu()
    except SystemExit:
        pass
    else:
        raise AssertionError("SystemExit not raised")

