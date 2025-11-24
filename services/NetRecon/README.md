# NetRecon – IP Intelligence Service (GeoLite2-based)

NetRecon is a lightweight, high-performance IP intelligence API powered by Flask and MaxMind's GeoLite2 databases.  
It acts as a fast, local alternative to external IP lookup services such as ipwho.is, while also being extensible for future modules (Nmap scans, threat intelligence, recon tools, etc.).

---

## 🚀 Features

- Full IP information lookup using local GeoLite2 databases
- Normalized JSON response including:
  - Continent, country, region, city
  - Latitude / longitude
  - Timezone
  - Postal code
  - Custom country metadata (calling code, capital, borders, flag icons)
  - Connection info (ASN, ISP, route) via GeoLite2-ASN
- Simple HTTP endpoint:  
  **`GET /ip/<ip>?raw=1`**
- Fully Dockerized
- Extensible architecture for future recon modules

---

## 📦 Requirements

- **Python 3.9+**
- MaxMind GeoLite2 databases:
  - `GeoLite2-City.mmdb`
  - `GeoLite2-ASN.mmdb`
- Python dependencies (from `requirements.txt`):
  - `Flask`
  - `geoip2`
  - `gunicorn` (for production)
  - `requests` (optional, used for metadata generator)

---

## 📁 Project Structure

```text
NetRecon/
├─ app.py
├─ geoip_resolver.py
├─ requirements.txt
├─ generate_country_meta.py
└─ data/
   ├─ GeoLite2-City.mmdb
   ├─ GeoLite2-ASN.mmdb
   └─ country_meta.json
```


## 🐋 Docker Usage

  ```
  docker build -t net-recon .
  ```

  - **This will:**
    - Install dependencies
    - Copy the source code
    - Package the MaxMind databases (if present in data/)
    - Configure Gunicorn as the WSGI server

  - **Run the Container**
    ```
    docker run -p 5000:5000 netrecon
    ```

    - **Example Usage:**
      ```
      curl "http://localhost:5000/ip/8.8.8.8"
      ```
