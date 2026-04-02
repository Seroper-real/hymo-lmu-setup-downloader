import json
import unicodedata
import requests
import logging
from config import REMOTE_TRACKS_ENABLED, REMOTE_TRACKS_TIMEOUT, REMOTE_TRACKS_URL
from utils import get_path

log = logging.getLogger("TrackTitanDownloader")

class TrackManager:

    def __init__(self):
        self.tracks_json_path = get_path("config/tracks.json")
        self.track_map: dict[str, str] = self.build_tracks_map()
        pass

    def _normalize_track(self, track: str) -> str:
        return unicodedata.normalize("NFC", track).lower().strip()

    def _load_local_tracks(self) -> dict | None:
        if self.tracks_json_path.exists():
            with open(self.tracks_json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else: return None

    def _load_remote_tracks(self) -> dict | None:
        if REMOTE_TRACKS_ENABLED:
            try:
                response = requests.get(REMOTE_TRACKS_URL, timeout=REMOTE_TRACKS_TIMEOUT)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                log.error(f"Cannot download tracks file from Github. Error: {e}")
        return None

    def build_tracks_map(self) -> dict:
        self.local_json = self._load_local_tracks()
        self.remote_json = self._load_remote_tracks()
        
        local_version: int = (self.local_json or {}).get("version", -1)
        remote_version: int = (self.remote_json or {}).get("version", -1)
        
        if self.remote_json is not None and remote_version > local_version:
            log.info(f"Using remote tracks mapping file (version {remote_version})")
            tracks_data = self.remote_json.get("tracks", [])
            log.info(f"Overriding local tracks.json with newer version: {remote_version}")
            with open(self.tracks_json_path, "w", encoding="utf-8") as f:
                json.dump(self.remote_json, f, indent=4)
        elif self.local_json is not None:
            log.info(f"Using local tracks mapping file (version {local_version})")
            tracks_data = self.local_json.get("tracks", [])
        else:
            raise RuntimeError("No tracks mapping file found. Both local and remote files are missing or inaccessible.")
        
        return {
            self._normalize_track(tt_name).lower(): track["lmu_folder_name"]
            for track in tracks_data
            for tt_name in track["tt_folder_name"]
        }
    
    def get_track_folder_name(self, track:str) -> str | None:
         return self.track_map.get(self._normalize_track(track).lower())