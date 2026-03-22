import json
import re
from flask import Blueprint, redirect, render_template, request, url_for
from CTFd.utils import get_config, set_config
from CTFd.utils.decorators import admins_only

CONFIG_KEY = "route_manager_redirects"

# Only allow relative paths: must start with / and contain no protocol or
# host component. This prevents open-redirect attacks.
_VALID_PATH_RE = re.compile(r"^/[^\s]*$")
MAX_PATH_LEN = 255


def _is_valid_path(path: str) -> bool:
    """Return True only for safe relative paths."""
    return bool(path and len(path) <= MAX_PATH_LEN and _VALID_PATH_RE.match(path))


def _get_redirects() -> dict:
    raw = get_config(CONFIG_KEY)
    if raw:
        try:
            data = json.loads(raw)
            if not isinstance(data, dict):
                return {}
            # Migration: old entries without the enabled flag → True by default
            for key, entry in list(data.items()):
                if not isinstance(entry, list) or len(entry) < 2:
                    del data[key]
                    continue
                if len(entry) < 3:
                    entry.append(True)
            return data
        except (ValueError, TypeError):
            pass
    return {}


def _save_redirects(redirects: dict) -> None:
    set_config(CONFIG_KEY, json.dumps(redirects))


def load(app):
    bp = Blueprint(
        "route_manager",
        __name__,
        template_folder="templates",
        url_prefix="/plugins/route-manager",
    )

    @bp.route("/", methods=["GET"])
    @admins_only
    def admin_page():
        return render_template("route_manager.html", redirects=_get_redirects())

    @bp.route("/add", methods=["POST"])
    @admins_only
    def add_redirect():
        source = request.form.get("source", "").strip()
        destination = request.form.get("destination", "").strip()

        # Ensure source starts with /
        if source and not source.startswith("/"):
            source = "/" + source

        # Validate both paths: relative only, no external URLs
        if not _is_valid_path(source) or not _is_valid_path(destination):
            return redirect(url_for("route_manager.admin_page"))

        try:
            code = int(request.form.get("code", 302))
            if code not in (301, 302):
                code = 302
        except (ValueError, TypeError):
            code = 302

        redirects = _get_redirects()
        redirects[source] = [destination, code, True]
        _save_redirects(redirects)

        return redirect(url_for("route_manager.admin_page"))

    @bp.route("/toggle", methods=["POST"])
    @admins_only
    def toggle_redirect():
        source = request.form.get("source", "")
        redirects = _get_redirects()
        # Only toggle entries that actually exist — no blind writes
        if source in redirects:
            redirects[source][2] = not redirects[source][2]
            _save_redirects(redirects)
        return redirect(url_for("route_manager.admin_page"))

    @bp.route("/delete", methods=["POST"])
    @admins_only
    def delete_redirect():
        source = request.form.get("source", "")
        redirects = _get_redirects()
        if source in redirects:
            redirects.pop(source)
            _save_redirects(redirects)
        return redirect(url_for("route_manager.admin_page"))

    app.register_blueprint(bp)

    @app.before_request
    def handle_redirects():
        # Never redirect admin or plugin routes to avoid lockout
        if request.path.startswith("/admin") or request.path.startswith("/plugins"):
            return None
        redirects = _get_redirects()
        entry = redirects.get(request.path)
        if entry and entry[2]:  # entry[2] == enabled
            target, code = entry[0], entry[1]
            return redirect(target, code=code)
        return None
