from dataclasses import dataclass
import json
import logging
from pathlib import Path
import sqlite3
import time
from config import DB_PATH
from setup import Setup

log = logging.getLogger("TrackTitanDownloader")

@dataclass
class InstalledSetup:
    setup_id: str
    track: str
    car: str
    install_date: int
    setup_last_update: int
    hotlap_link: str
    api_data: dict
    file_names: list[str]
    track_found: bool
    installation_base_path: str | None
    installation_folder: str | None

    @staticmethod
    def from_row(row: tuple) -> "InstalledSetup":
        return InstalledSetup(
            setup_id=row[0],
            track=row[1],
            car=row[2],
            install_date=row[3],
            setup_last_update=row[4],
            hotlap_link=row[5],
            api_data=json.loads(row[6]) if row[6] else {},
            file_names=json.loads(row[7]) if row[7] else [],
            track_found=bool(row[8]),
            installation_base_path=row[9],
            installation_folder=row[10]
        )
    
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
                    file_names TEXT,
                    track_found INTEGER,
                    installation_base_path TEXT,
                    installation_folder TEXT
                )
            """)
            # Migration 1: add track_found to existing installations
            try:
                self.conn.execute("ALTER TABLE installed_setups ADD COLUMN track_found INTEGER")
            except sqlite3.OperationalError:
                pass
            # Migration 2: add installation_base_path and installation_folder
            try:
                self.conn.execute("ALTER TABLE installed_setups ADD COLUMN installation_base_path TEXT")
            except sqlite3.OperationalError:
                pass
            try:
                self.conn.execute("ALTER TABLE installed_setups ADD COLUMN installation_folder TEXT")
            except sqlite3.OperationalError:
                pass


    def is_setup_installed_last_version(self, setup: Setup) -> bool:
        cursor = self.conn.execute("SELECT 1 FROM installed_setups WHERE setup_id = ? and setup_last_update >= ?", (setup.id, setup.last_updated))
        try:
            return cursor.fetchone() is not None
        finally:
            cursor.close


    def add_installed_setup(self, setup: Setup, file_names: list[Path], track_found: bool, installation_dir: Path) -> None:
        with self.conn:
            query = """
                    INSERT INTO installed_setups (setup_id, track, car, install_date, setup_last_update, hotlap_link, api_data, file_names, track_found, installation_base_path, installation_folder)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(setup_id) DO UPDATE SET
                        track = excluded.track,
                        car = excluded.car,
                        install_date = excluded.install_date,
                        setup_last_update = excluded.setup_last_update,
                        hotlap_link = excluded.hotlap_link,
                        api_data = excluded.api_data,
                        file_names = excluded.file_names,
                        track_found = excluded.track_found,
                        installation_base_path = excluded.installation_base_path,
                        installation_folder = excluded.installation_folder
                    """
            self.conn.execute(query, (
                setup.id, setup.track, setup.car, int(time.time()*1000), setup.last_updated,
                setup.hotlap_link, json.dumps(setup.data), json.dumps([file.name for file in file_names]),
                int(track_found), str(installation_dir.parent), installation_dir.name
            ))

    def update_installed_setup(self, setup: InstalledSetup) -> None:
        with self.conn:
            query = """
                    UPDATE installed_setups SET
                        track = ?,
                        car = ?,
                        install_date = ?,
                        setup_last_update = ?,
                        hotlap_link = ?,
                        api_data = ?,
                        file_names = ?,
                        track_found = ?,
                        installation_base_path = ?,
                        installation_folder = ?
                    WHERE setup_id = ?
                    """
            self.conn.execute(query, (
                setup.track, setup.car, setup.install_date, setup.setup_last_update,
                setup.hotlap_link, json.dumps(setup.api_data), json.dumps(setup.file_names),
                int(setup.track_found), setup.installation_base_path, setup.installation_folder,
                setup.setup_id
            ))

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


    def is_track_found(self, setup_id: str) -> bool:
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT track_found FROM installed_setups WHERE setup_id = ?", (setup_id,))
            row = cursor.fetchone()
            if row is None:
                return False
            return bool(row[0])
        except Exception as e:
            log.error(f"Error fetching track_found for {setup_id}: {e}")
            return False
        finally:
            cursor.close()

    def fetch_tracks_not_found(self) -> list[InstalledSetup]:
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM installed_setups WHERE track_found = 0 OR track_found IS NULL")
            return [InstalledSetup.from_row(row) for row in cursor.fetchall()]
        except Exception as e:
            log.error(f"Error fetching unresolved tracks: {e}")
            return []
        finally:
            cursor.close()