def to_ipwhois_format(data: dict) -> dict:
	"""Convert internal NetRecon IP payload to an ipwho.is-compatible JSON."""
	flag = data.get("flag") or {}
	tz = data.get("timezone") or {}
	conn = data.get("connection") or {}

	# Normalize calling code: "+32" -> "32"
	calling = data.get("calling_code")
	if isinstance(calling, str) and calling.startswith("+"):
		calling_code = calling[1:]
	else:
		calling_code = calling

	# Normalize borders: ["FR", "DE", "LU", "NL"] -> "FR,DE,LU,NL"
	borders = data.get("borders")
	if isinstance(borders, list):
		borders_str = ",".join(borders)
	elif isinstance(borders, str):
		borders_str = borders
	else:
		borders_str = None

	ip_type = data.get("type")
	if isinstance(ip_type, str):
		ip_type = ip_type.upper()

	ipwhois_payload = {
		"ip": data.get("ip"),
		"success": data.get("success"),
		"type": ip_type,
		"continent": data.get("continent"),
		"continent_code": data.get("continent_code"),
		"country": data.get("country"),
		"country_code": data.get("country_code"),
		"region": data.get("region"),
		"region_code": data.get("region_code"),
		"city": data.get("city"),
		"latitude": data.get("latitude"),
		"longitude": data.get("longitude"),
		"is_eu": data.get("is_eu"),
		"postal": data.get("postal"),
		"calling_code": calling_code,
		"capital": data.get("capital"),
		"borders": borders_str,
		"flag": {
			"img": flag.get("svg") or flag.get("png"),
			"emoji": flag.get("emoji"),
			"emoji_unicode": flag.get("emoji_unicode"),
		} if flag else None,
		"connection": {
			"asn": conn.get("asn"),
			"org": conn.get("org"),
			"isp": conn.get("isp"),
			"domain": conn.get("domain"),
		} if conn else None,
		"timezone": tz or None,
	}

	return ipwhois_payload
