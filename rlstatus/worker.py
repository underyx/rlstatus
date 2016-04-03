import os
import sqlite3
import logging

from rlclient import RocketLeagueClient

LOG = logging.getLogger(__name__)


def main():
    client = RocketLeagueClient()
    calls = [client.GetPopulationAllPlaylists()]
    while True:
        try:
            results = client.request(calls)[0]
            rows = [(playlist, players) for playlist, players in results.items()]

            with sqlite3.connect(os.environ['RLSTATUS_DB_URL']) as conn:
                cur = conn.cursor()
                LOG.info('saving %s rows into database', len(rows))
                cur.executemany('INSERT INTO population (playlist, players) VALUES (?, ?)', rows)
                conn.commit()
        except:
            LOG.exception('unhandled error')

        LOG.info('population collection done, sleeping for %s seconds', int(os.getenv('RLSTATUS_CHECK_INTERVAL', '60')))


if __name__ == '__main__':
    main()
