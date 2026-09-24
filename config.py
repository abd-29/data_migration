from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent

LOG_DIR = ROOT_DIR / "logs"
LOG_FILE = LOG_DIR / "migration.log"

print(ROOT_DIR)
print(LOG_DIR)
print(LOG_FILE)