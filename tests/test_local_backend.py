import os
import sys
import http.server
import threading
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend import db, api


def test_sqlite_db_initializes():
    db.init_db()
    conn = db.get_connection() if hasattr(db, "get_connection") else None
    if conn is not None:
        conn.close()


def test_local_http_server_serves_index():
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), api.ApiHandler)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    try:
        res = urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=5)
        assert res.status == 200
        html = res.read().decode("utf-8", errors="ignore")
        assert "<html" in html.lower()
    finally:
        httpd.shutdown()
        httpd.server_close()
