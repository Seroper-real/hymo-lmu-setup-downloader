from typing import Any, Optional
import requests, time, random, logging
from config import BASE_URL, ACCESS_TOKEN_LIST, ACCESS_TOKEN_DOWNLOAD, CONSUMER_ID, USER_ID

log = logging.getLogger("TrackTitanDownloader")

class TrackTitanClient:
    def __init__(self):
        if not BASE_URL:
            raise RuntimeError("Missing BASE_URL")
        if not ACCESS_TOKEN_LIST:
            raise RuntimeError("Missing ACCESS_TOKEN_LIST")
        if not ACCESS_TOKEN_DOWNLOAD:
            raise RuntimeError("Missing ACCESS_TOKEN_DOWNLOAD")
        if not CONSUMER_ID:
            raise RuntimeError("Missing CONSUMER_ID")
        if not USER_ID:
            raise RuntimeError("Missing USER_ID")

    def get(self, path: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        url = f"{BASE_URL}{path}"
        r = requests.get(url, params=params, headers={
            "Authorization": f"{ACCESS_TOKEN_LIST}",
            "Accept": "application/json, text/plain, */*",
            "x-consumer-id": f"{CONSUMER_ID}"
        })
        r.raise_for_status()
        return r.json()

    def download_link(self, setup_id: str) -> dict[str, Any]:
        url = f"{BASE_URL}/v1/user/{USER_ID}/setup/{setup_id}/download"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": f"{ACCESS_TOKEN_DOWNLOAD}",
            "x-consumer-id": f"{CONSUMER_ID}"
        }
        # POST without body (curl -X POST with content-length: 0)
        response = requests.post(url, headers=headers, data=None)
        response.raise_for_status()
        log.debug(response.json())
        return response.json()
    
    def download(self, url: str) -> requests.Response:
        response = requests.get(url)
        response.raise_for_status()
        return response

    def human_sleep(self, avg: float = 2.5, jitter: float = 1.0) -> None:
        delay = max(0.2, random.gauss(avg, jitter))
        time.sleep(delay)
