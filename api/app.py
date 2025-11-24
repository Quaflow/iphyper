import os
from flask import Flask, jsonify, request

from geoip_resolver import lookup_ip

app = Flask(__name__)


@app.route('/ip/<ip>')
def ip_lookup(ip):
	"""Lookup IP info using local GeoLite2 DB and return normalized JSON.

	Query param `raw=1` currently returns the same normalized payload
	(ileride dilersen daha detaylı/raw GeoLite2 response da dönebilirsin).
	"""
	raw = request.args.get('raw', '0').lower() in ('1', 'true', 'yes')

	data, err = lookup_ip(ip)

	if err == "invalid_ip":
		return jsonify({'error': 'invalid_ip', 'ip': ip}), 400
	elif err == "not_found":
		return jsonify({'error': 'ip_not_found', 'ip': ip}), 404
	elif err and err.startswith("lookup_error"):
		return jsonify({'error': 'lookup_failed', 'details': err}), 502

	if raw:
		# For now, raw is same as normalized
		return jsonify(data)

	# If you want, you can create an "out" here to exactly mimic ipwho.is.
	# Now lookup_ip already returns a normalized dict.
	return jsonify(data)


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	# You can enable Flask debug locally, disable in production
	app.run(host='0.0.0.0', port=port)
