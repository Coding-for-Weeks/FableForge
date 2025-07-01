import sys
from pathlib import Path

# Ensure the stub and src directories are on the import path for tests
root = Path(__file__).resolve().parents[1]
stub = root / "tests" / "stubs"
if str(stub) not in sys.path:
    sys.path.insert(0, str(stub))

src = root / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))
