from typing import Optional


class Setup:
    def __init__(self,data: dict):
        self.data = data
        self._safe_track = self.track.replace("/", "_").replace("\\", "_").replace("-", "_")

    @property
    def id(self) -> str:
        return self.data["id"]
    
    @property
    def title(self) -> str:
        return self.data["title"]
    
    @property
    def combo(self) -> dict:
        return self.data["setupCombos"][0]
    
    @property
    def car(self) -> str:
        return self.combo["car"]["name"]
    
    @property
    def track(self) -> str:
        return self.combo["track"]["name"]
    
    @property
    def safe_track(self) -> str:
        return self._safe_track

    @safe_track.setter
    def safe_track(self,value: str) -> None:
        self._safe_track = value

    @property
    def hotlap_link(self) -> Optional[str]:
        return self.data["hotlapLink"]
    
    @property
    def last_updated(self) -> int:
        return self.data["lastUpdatedAt"]
    
    @property
    def is_bundle(self) -> bool:
        return self.data["isBundle"]