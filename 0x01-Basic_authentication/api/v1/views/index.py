#!/usr/bin/env python3
"""Index view for Basic Authentication"""
from flask import abort, jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """GET /api/v1/status"""
    return jsonify({"status": "OK"})


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """Raise a 401 error"""
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """Raise a 403 error"""
    abort(403)


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """GET /api/v1/stats"""
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)
