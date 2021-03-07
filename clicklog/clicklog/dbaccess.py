import psycopg2
from uuid import uuid4
import time
import json
from datetime import datetime, timezone
from tzlocal import get_localzone
from dateutil.parser import parse as parsedatetime
import logging

log = logging.getLogger("dbaccess")

class DBConn:
    __slots__ = ["conn", "log"]

    def __init__(self, host:str, port:int, password:str):
        retry = 3
        self.conn = None
        log.info(f"Connecting to {host}:{port}")
        while self.conn is None:
            try:
                self.conn = psycopg2.connect(dbname="clicknow", host=host, port=port, user="postgres", password=password)
            except psycopg2.OperationalError:
                log.warning("Retry to connect")
                time.sleep(1)
                retry -=1
                if retry == 0:
                    log.error("Cannot connect to DB")
                    raise Exception("Cannot connect to DB")

    def add_clicklog_entry(self, token:str, source:str, headers:{str:str}):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO clicklog (id, ts, token, source, headers) values(%s,%s,%s,%s,%s)",
                       (str(uuid4()), datetime.now(timezone.utc),  token, source, json.dumps(headers))
                       )
        self.conn.commit()
        cursor.close()

    def show_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM clicklog")
        for i in cursor.fetchall():
            print(f"{i[1].astimezone(get_localzone())} {i[3]} {i[2]} {i[4]}")


def test():
    conn = DBConn()
    conn.add_clicklog_entry("aaa", "127.0.0.1:8080", {"a":1, "b":2})
    conn.show_data()

