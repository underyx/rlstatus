import os
import sqlite3

from rlclient import RocketLeagueClient


def main():
    client = RocketLeagueClient()
    call = client.GetPopulationAllPlaylists()
    results = client.request([call])[0]
    rows = [(playlist, players) for playlist, players in results.items()]

    with sqlite3.connect(os.environ['RLSTATUS_DB_URL']) as conn:
        cur = conn.cursor()
        cur.executemany('INSERT INTO population (playlist, players) VALUES (?, ?)', rows)
        conn.commit()

if __name__ == '__main__':
    main()
