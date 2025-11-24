import json
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR / "data" / "country_meta.json"
RESTCOUNTRIES_URL = "https://restcountries.com/v3.1/all"


def _country_code_to_emoji(cc: str | None) -> str | None:
	"""Convert ISO2 country code to flag emoji."""
	if not cc or len(cc) != 2:
		return None
	try:
		base = 0x1F1E6
		first = base + (ord(cc[0].upper()) - ord("A"))
		second = base + (ord(cc[1].upper()) - ord("A"))
		return chr(first) + chr(second)
	except Exception:
		return None


def _emoji_to_unicode_codes(emoji: str | None) -> str | None:
	"""Convert emoji string to unicode code representation (e.g. U+1F1E7 U+1F1EA)."""
	if not emoji:
		return None
	return " ".join(f"U+{ord(ch):04X}" for ch in emoji)


def fetch_countries():
	"""Fetch raw country data from RestCountries API."""
	resp = requests.get(
		RESTCOUNTRIES_URL,
		params={
			"fields": "cca2,cca3,name,capital,idd,borders",
		},
		timeout=15,
	)
	resp.raise_for_status()
	return resp.json()


def build_alpha3_to_alpha2_map(raw_countries) -> dict:
	"""Build a mapping from ISO3 (cca3) to ISO2 (cca2) codes."""
	mapping: dict = {}
	for c in raw_countries:
		cca2 = c.get("cca2")
		cca3 = c.get("cca3")
		if cca2 and cca3:
			mapping[cca3.upper()] = cca2.upper()
	return mapping


def build_country_meta(raw_countries, alpha3_to_alpha2: dict) -> dict:
	"""Build country metadata dict keyed by ISO2 (cca2)."""
	meta: dict = {}

	for c in raw_countries:
		code = c.get("cca2")
		if not code:
			continue

		code = code.upper()

		# Name
		name_data = c.get("name") or {}
		name = name_data.get("common") or name_data.get("official") or code

		# Capital: usually a list; take the first if present
		capitals = c.get("capital") or []
		capital = capitals[0] if capitals else None

		# Calling code: idd: { root: "+32", suffixes: [""] } etc.
		idd = c.get("idd") or {}
		root = idd.get("root")
		suffixes = idd.get("suffixes") or []
		if root and suffixes:
			calling_code = f"{root}{suffixes[0]}"
		elif root:
			calling_code = root
		else:
			calling_code = None

		# Borders: convert ISO3 to ISO2 using the mapping
		borders_iso3 = c.get("borders") or []
		borders_iso2 = [
			alpha3_to_alpha2.get(b.upper(), b.upper()) for b in borders_iso3
		]

		# Flag URLs + emoji
		cc_lower = code.lower()
		emoji = _country_code_to_emoji(code)
		emoji_unicode = _emoji_to_unicode_codes(emoji)

		flag = {
			"emoji": emoji,
			"emoji_unicode": emoji_unicode,
			"svg": f"https://flagcdn.com/{cc_lower}.svg",
		}

		meta[code] = {
			"name": name,
			"calling_code": calling_code,
			"capital": capital,
			"borders": borders_iso2,
			"flag": flag,
		}

	return meta


def main():
	"""Fetch, build and write country metadata file."""
	print("[*] Fetching country data from RestCountries...")
	countries = fetch_countries()
	print(f"[+] Received {len(countries)} raw country entries.")

	alpha3_to_alpha2 = build_alpha3_to_alpha2_map(countries)
	print(f"[+] Built alpha3->alpha2 mapping for {len(alpha3_to_alpha2)} codes.")

	meta = build_country_meta(countries, alpha3_to_alpha2)
	print(f"[+] Built metadata for {len(meta)} countries.")

	OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

	with OUTPUT_PATH.open("w", encoding="utf-8") as f:
		json.dump(meta, f, ensure_ascii=False, indent=2)

	print(f"[+] Written country_meta.json to: {OUTPUT_PATH}")


if __name__ == "__main__":
	main()
