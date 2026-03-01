import os, logging
from pathlib import Path
from config import DOWNLOAD_PATH
from setup import Setup
from setup_db import SetupDb
from track_titan_client import TrackTitanClient

log = logging.getLogger("TrackTitanDownloader")

class DownloadManager:
    def __init__(self, database : SetupDb):
        if not DOWNLOAD_PATH:
            raise RuntimeError("Missing DOWNLOAD_PATH")
        os.makedirs(DOWNLOAD_PATH, exist_ok=True)
        self.track_titan_client = TrackTitanClient()
        self.page = 1
        self.page_size = 12
        self.finished = False
        self.already_downloaded : set[str] = set()
        self.already_installed : set[str] = set()
        self.database : SetupDb = database
        self.get_downloaded_setup_uuid()
    
    def get_downloaded_setup_uuid(self) -> None:
        self.already_downloaded.update({
            f[-40:-4]
            for f in os.listdir(DOWNLOAD_PATH)
            if f.endswith(".zip")
            })
                
    def get_setups_list(self) -> list[Setup]:
        if self.finished: return []
        res = self.track_titan_client.get(
            "/v2/games/leMansUltimate/setups",
            params={"page": self.page, "limit": self.page_size}
        )
        setups : list[Setup] = [Setup(setup) for setup in res["data"]["setups"]]
        log.debug(f"PAGE {self.page} found:{len(setups)}")
        self.track_titan_client.human_sleep()
        if len(setups) < self.page_size: self.finished = True
        self.page += 1
        return setups

    def restart_setups_list(self) -> None:
        self.page = 1
        self.finished = False

    def download(self, setup: Setup) -> Path | None:
        if self.database.is_setup_installed_last_version(setup):
            log.info(f"Setup already installed. Skipping")
            return #Setup già scaricato
        
        path = Path(f"{DOWNLOAD_PATH}/{setup.safe_track}-{setup.id}.zip")

        if setup.id not in self.already_downloaded:
            log.debug(f"Downloading setup {setup.id}")
            self.track_titan_client.human_sleep()
            data = self.track_titan_client.download_link(setup.id)
            download_url = data["url"]
            # Scaricare il file
            file_resp = self.track_titan_client.download(download_url)
            with open(path, "wb") as f:
                f.write(file_resp.content)
            log.info(f"Download completed for {setup.id}")
            self.already_downloaded.update(setup.id)
        else:
            log.debug(f"Setup downloaded but not yet installed for {setup.id}")
        return path
