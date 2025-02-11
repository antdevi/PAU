from flask import Blueprint, send_from_directory

server_bp = Blueprint('server', __name__)

# ✅ Route to serve revision.html at /revision.html
@server_bp.route("/revision.html")
def serve_revision():
    return send_from_directory("public/templates", "revision.html")
