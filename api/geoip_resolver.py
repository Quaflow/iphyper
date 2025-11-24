import json
from pathlib import Path
import ipaddress
import geoip2.database
import geoip2.errors

BASE_DIR = Path(__file__).resolve().parent

GEOIP_CITY_DB_PATH = BASE_DIR / "data" / "GeoLite2-City.mmdb"
GEOIP_ASN_DB_PATH = BASE_DIR / "data" / "GeoLite2-ASN.mmdb"
COUNTRY_META_PATH = BASE_DIR / "data" / "country_meta.json"

city_reader = geoip2.database.Reader(str(GEOIP_CITY_DB_PATH))
asn_reader = geoip2.database.Reader(str(GEOIP_ASN_DB_PATH))

try:
	with open(COUNTRY_META_PATH, encoding="utf-8") as f:
		COUNTRY_META = json.load(f)
except FileNotFoundError:
	COUNTRY_META = {}

def lookup_ip(ip: str):
	# IP format kontrolü
	try:
		ip_obj = ipaddress.ip_address(ip)
	except ValueError:
		return None, "invalid_ip"

	# CITY lookup
	try:
		c = city_reader.city(ip)
	except geoip2.errors.AddressNotFoundError:
		return None, "not_found"
	except Exception as e:
		return None, f"lookup_error:{e}"

	continent_name = c.continent.names.get("en") if c.continent else None
	country_name = c.country.names.get("en") if c.country else None
	region = c.subdivisions.most_specific
	city_name = c.city.names.get("en") if c.city else None

	data = {
		"ip": ip,
		"success": True,
		"type": "ipv4" if isinstance(ip_obj, ipaddress.IPv4Address) else "ipv6",
		"continent": continent_name,
		"continent_code": c.continent.code if c.continent else None,
		"country": country_name,
		"country_code": c.country.iso_code if c.country else None,
		"region": region.names.get("en") if region and region.names else None,
		"region_code": region.iso_code if region else None,
		"city": city_name,
		"latitude": c.location.latitude,
		"longitude": c.location.longitude,
		"is_eu": getattr(c.country, "is_in_european_union", None),
		"postal": c.postal.code if c.postal else None,
		# country_meta ile doldurulacak alanlar için şimdilik None
		"calling_code": None,
		"capital": None,
		"borders": None,
		"flag": None,
		# birazdan ASN lookup ile doldurulacak
		"connection": None,
		"timezone": c.location.time_zone,
	}

	cc = data["country_code"]
	if cc and cc in COUNTRY_META:
		meta = COUNTRY_META[cc]
		data["calling_code"] = meta.get("calling_code")
		data["capital"] = meta.get("capital")
		data["borders"] = meta.get("borders")
		
		flag_meta = meta.get("flag")
		if flag_meta:
			data["flag"] = {
				"emoji": flag_meta.get("emoji"),
				"svg": flag_meta.get("svg"),
				"png": flag_meta.get("png"),
			}

	connection = _lookup_connection(ip)
	if connection:
		data["connection"] = connection

	return data, None


def _lookup_connection(ip: str):
	try:
		a = asn_reader.asn(ip)
	except geoip2.errors.AddressNotFoundError:
		return None
	except Exception:
		return None

	# GeoLite2-ASN'de genelde:
	# - autonomous_system_number
	# - autonomous_system_organization
	# - network (IP range)
	asn = a.autonomous_system_number
	org = a.autonomous_system_organization
	network = str(a.network)  # örn: "1.1.1.0/24"

	connection = {
		"asn": asn,
		"org": org,
		"isp": org,
		"route": network,
	}

	return connection
