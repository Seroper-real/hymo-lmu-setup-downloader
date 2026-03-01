import logging, sys
from pathlib import Path
from setup_manager import SetupManager
from config import LMU_SETUPS_BASE_PATH, LOG_FORMAT_CONSOLE, LOG_FORMAT_FILE, LOG_LEVEL_CONSOLE, LOG_LEVEL_FILE
from download_manager import DownloadManager
from track_manager import TrackManager
from setup_db import SetupDb

if __name__ == "__main__":
    try:
        ## Start
        def setup_logging():
            levels = logging.getLevelNamesMapping()
            
            lvl_c = levels.get(LOG_LEVEL_CONSOLE.upper(), logging.INFO)
            lvl_f = levels.get(LOG_LEVEL_FILE.upper(), logging.DEBUG)

            logger = logging.getLogger("TrackTitanDownloader")
            logger.setLevel(min(lvl_c, lvl_f))

            # --- Console Handler ---
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(lvl_c)
            console_handler.setFormatter(logging.Formatter(LOG_FORMAT_CONSOLE))

            # --- File Handler ---
            file_handler = logging.FileHandler('app_debug.log', mode='a', encoding='utf-8')
            file_handler.setLevel(lvl_f)
            file_handler.setFormatter(logging.Formatter(LOG_FORMAT_FILE))

            if logger.hasHandlers():
                logger.handlers.clear()
                
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)

            return logger

        log = setup_logging()

        log.info("######################## START ########################")
        if not Path(LMU_SETUPS_BASE_PATH).exists():
            logging.error(f"Folder not exist: {LMU_SETUPS_BASE_PATH}\nCheck value of lmu_base_path in config.json")
            print("Press ENTER for exit")
            input()
            sys.exit(1)

        database = SetupDb()
        track_manager = TrackManager()
        track_map = track_manager.build_tracks_map()
        download_manager = DownloadManager(database=database)
        setup_manager = SetupManager(track_map=track_map,database=database)

        while setups:=download_manager.get_setups_list():
            for setup in setups:
                log.info(f"#################")
                log.info(f"{setup.title}")
                log.info(f"  ID: {setup.id}")
                log.info(f"  Car: {setup.car}")
                log.info(f"  Track: {setup.track}")

                if setup.is_bundle:
                    log.info(f"Skipping bundle.")
                    continue #Non scarichiamo i bundle
                path=download_manager.download(setup)
                
                if path: setup_manager.install_setup(path, setup)

        log.info("######################## FINISH ########################")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR]: {e}")
        print("Check readme for instructions: https://github.com/Seroper-real/hymo-lmu-setup-downloader/blob/main/readme.md")
        print("Istruzioni in italiano: https://github.com/Seroper-real/hymo-lmu-setup-downloader/blob/main/readme.it.md")
        input("\nPress Enter to close...")
        sys.exit(1)