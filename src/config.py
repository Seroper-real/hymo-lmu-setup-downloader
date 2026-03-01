import os
import json
from pathlib import Path
import sys
from dotenv import load_dotenv
from utils import get_path

try:
    # Load .env
    load_dotenv(get_path(".env"))

    # Load config.json
    CONFIG_FILE = get_path("config/config.json")
    if not CONFIG_FILE.exists():
        raise RuntimeError("Missing config.json")

    with CONFIG_FILE.open(encoding="utf-8") as f:
        _config = json.load(f)

    # Load db
    DB_PATH = get_path("data/hymo_lmu_sm.db")
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # ===== LOGGING CONFIG =====
    _log_cfg = _config.get("logging", {})

    # Console config
    LOG_LEVEL_CONSOLE = _log_cfg.get("console", {}).get("level", "INFO")
    LOG_FORMAT_CONSOLE = _log_cfg.get("console", {}).get("format", "%(message)s")

    # File config
    LOG_LEVEL_FILE = _log_cfg.get("file", {}).get("level", "DEBUG")
    LOG_FORMAT_FILE = _log_cfg.get("file", {}).get("format", "%(asctime)s - %(levelname)s - %(message)s")

    # ===== ENV =====
    ACCESS_TOKEN_LIST = os.getenv("ACCESS_TOKEN_LIST")
    ACCESS_TOKEN_DOWNLOAD = os.getenv("ACCESS_TOKEN_DOWNLOAD")
    USER_ID = os.getenv("USER_ID")

    if not all([ACCESS_TOKEN_LIST, ACCESS_TOKEN_DOWNLOAD, USER_ID]):
        raise RuntimeError("Missing auth values in .env")

    # ===== JSON =====
    BASE_URL = _config["network"]["base_url"]
    CONSUMER_ID = _config["network"]["consumer_id"]
    PAGE_SIZE = _config["network"]["page_size"]
    MIN_DELAY = _config["network"]["min_delay"]
    MAX_DELAY = _config["network"]["max_delay"]

    DOWNLOAD_PATH = get_path(_config["paths"]["download"]["base_path"])
    CLEAN_DOWNLOAD = _config["paths"]["download"]["clean_download_after_copy"]

    OVERWRITE : bool = _config["paths"]["setups"]["overwrite"]
    DELETE_PREVIOUS_VERSION : bool = _config["paths"]["setups"]["delete_previous_version"]
    LMU_SETUPS_BASE_PATH = get_path(_config["paths"]["setups"]["lmu_base_path"])

    SETUP_FILE_EXTENSIONS: set[str] = {
        ext.lower()
        for ext in _config["paths"]["setups"]["file_extensions"]
    }

    REMOTE_TRACKS_ENABLED=_config["remote_tracks"]["enabled"]
    REMOTE_TRACKS_TIMEOUT=_config["remote_tracks"]["timeout"]
    REMOTE_TRACKS_URL=_config["remote_tracks"]["url"]

    # ===== Folders =====
    Path(DOWNLOAD_PATH).mkdir(parents=True, exist_ok=True)
except Exception as e:
    print(f"\n[ERROR]: {e}")
    input("\nPress Enter to close...")
    sys.exit(1)
