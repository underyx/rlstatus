import os
import sqlite3
from datetime import datetime

from rlclient import RocketLeagueClient


def main():
    client = RocketLeagueClient()
    call = client.GetPopulationAllPlaylists()
    results = client.request([call])[0]
    timestamp = datetime.now()
    rows = [(timestamp, playlist, players) for playlist, players in results.items()]

    with sqlite3.connect(os.environ['RLSTATUS_DB_URL']) as conn:
        cur = conn.cursor()
        cur.executemany(
            'INSERT INTO population (timestamp, playlist, players) VALUES (?, ?, ?)',
            rows,
        )
        conn.commit()

if __name__ == '__main__':
    main()
