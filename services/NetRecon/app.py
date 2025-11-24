import os
from flask import Flask, jsonify, request
from geoip_resolver import lookup_ip

from datetime import datetime, timedelta
from config import settings
from formatters import to_ipwhois_format

app = Flask(__name__)


@app.route("/ip/<ip>")
def ip_lookup(ip):
	"""Perform an IP lookup using local GeoLite2 databases.

	Query params:
		raw=1        -> returns internal normalized payload
		compat=ipwhois -> returns ipwho.is compatible payload
	"""
	print(f"[+] Lookup request for IP: {ip}")
	raw = request.args.get("raw", "0").lower() in ("1", "true", "yes")
	compat = request.args.get("compat", "").lower()

	data, err = lookup_ip(ip)
	

	if err == "invalid_ip":
		return jsonify({"error": "invalid_ip", "ip": ip}), 400
	if err == "not_found":
		return jsonify({"error": "ip_not_found", "ip": ip}), 404
	if err and err.startswith("lookup_error"):
		return jsonify({"error": "lookup_failed", "details": err}), 502

	if compat == "ipwhois":
		return jsonify(to_ipwhois_format(data))

	# Raw is currently equal to the normalized output
	return jsonify(data)


if __name__ == "__main__":
	port = settings.port
	# Debug should only be enabled in development
	if DEBUG_MODE:
		app.debug = True
	app.run(host="0.0.0.0", port=port, debug=settings.flask_debug)
