# ruff: noqa: INP001, S101 -- Standalone smoke assertions for a running container.
import argparse
import json
import re
from contextlib import closing
from http import HTTPStatus
from http.client import HTTPConnection


def smoke(port: int) -> None:
    with closing(HTTPConnection("127.0.0.1", port, timeout=5)) as connection:

        def get(path: str, expected: HTTPStatus = HTTPStatus.OK) -> tuple[str, bytes]:
            connection.request("GET", path)
            response = connection.getresponse()
            body = response.read()
            assert response.status == expected, (
                f"{path}: HTTP {response.status}, expected {expected}"
            )
            return response.headers.get_content_type(), body

        _, health = get("/api/health")
        assert json.loads(health) == {"status": "ok"}
        content_type, stocks = get("/api/stocks?limit=1")
        page = json.loads(stocks)
        assert content_type == "application/json"
        assert page["items"][0]["symbol"] == "DEMOA"
        assert page["provenance"] == "synthetic-sample"

        content_type, html = get("/")
        assert content_type == "text/html"
        assert b'id="root"' in html
        document = html.decode("utf-8")
        for extension, media_type in (("js", "javascript"), ("css", "text/css")):
            asset = re.search(rf'"(/assets/[^"<>]+\.{extension})"', document)
            assert asset, f"Missing {extension} asset in index.html"
            content_type, body = get(asset[1])
            assert body
            assert media_type in content_type

        content_type, missing = get("/api/missing", HTTPStatus.NOT_FOUND)
        assert content_type == "application/json"
        assert json.loads(missing)["detail"]
        content_type, invalid = get("/api/stocks?limit=0", HTTPStatus.UNPROCESSABLE_CONTENT)
        assert content_type == "application/json"
        assert json.loads(invalid)["detail"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify a running Stock Vision container.")
    parser.add_argument("--port", type=int, default=8000, help="Published localhost port")
    smoke(parser.parse_args().port)
    print("Stock Vision container smoke checks passed.")
