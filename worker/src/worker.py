from flask import Response, request
from pyodide.ffi import run_sync
from workers import wsgi
from app import app


@app.get("/<path:path>")
def serve_asset(path):
    assets = request.environ["workers.env"].ASSETS
    asset_response = run_sync(assets.fetch(f"https://assets.local/{path}"))
    body = run_sync(asset_response.bytes())
    return Response(
        body,
        status=asset_response.status,
        headers=asset_response.headers,
    )


Default = wsgi.entrypoint(app)
