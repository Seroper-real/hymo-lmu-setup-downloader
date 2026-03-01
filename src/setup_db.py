import json
import logging
from pathlib import Path
import sqlite3
import time
from config import DB_PATH
from setup import Setup

log = logging.getLogger("TrackTitanDownloader")

class SetupDb:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS installed_setups (
                    setup_id TEXT PRIMARY KEY,
                    track TEXT,
                    car TEXT,
                    install_date INTEGER,
                    setup_last_update INTEGER,
                    hotlap_link TEXT,
                    api_data TEXT,
                    file_names TEXT
                )
            """)
             
    def is_setup_installed_last_version(self, setup: Setup) -> bool:
        cursor = self.conn.execute("SELECT 1 FROM installed_setups WHERE setup_id = ? and setup_last_update >= ?", (setup.id, setup.last_updated))
        try:
            return cursor.fetchone() is not None
        finally:
            cursor.close

    def add_installed_setup(self, setup: Setup, file_names: list[Path]) -> None:
        with self.conn:
            query = """
                    INSERT INTO installed_setups (setup_id, track, car, install_date, setup_last_update, hotlap_link, api_data, file_names)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(setup_id) DO UPDATE SET
                        track = excluded.track,
                        car = excluded.car,
                        install_date = excluded.install_date,
                        setup_last_update = excluded.setup_last_update,
                        hotlap_link = excluded.hotlap_link,
                        api_data = excluded.api_data,
                        file_names = excluded.file_names
                    """
            self.conn.execute(query, (setup.id, setup.track, setup.car, int(time.time()*1000), setup.last_updated, setup.hotlap_link, json.dumps(setup.data),json.dumps([file.name for file in file_names])))

    def fetch_setup_files(self,setup_id: str) -> list[str]:
        cursor = self.conn.cursor()
        query = "SELECT file_names FROM installed_setups WHERE setup_id = ?"
        try:
            cursor.execute(query,(setup_id,))
            row = cursor.fetchone()
            if row and row[0]:
                return json.loads(row[0])
            return []
        except Exception as e:
            log.error(f"Error fetching files for {setup_id}: {e}")
            return []
        finally:
            cursor.close()
