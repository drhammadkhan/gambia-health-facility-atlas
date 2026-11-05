# The Gambia Health Facility Atlas

Static Leaflet webapp. Serve `dist/` using any HTTP server, for example `python3 -m http.server 8045 --directory dist`.

103 records: 101 historical public-sector facilities from the 2019 Maina et al. database, retrieved from its ArcGIS mirror, plus Ahmadiyya and Njau. This is incomplete coverage, not an authoritative current national master register. Fifteen facilities have structured November 2025 PATG assessment data. Unknown services are never inferred from facility type. Source details are included in the app. External OpenStreetMap tiles and optional Google Fonts require internet; facility data, boundary and Leaflet are bundled locally.

`dist/facilities.json` is the editable facility dataset. `dist/assessment.json` preserves the extracted assessment, including CPAP source conflict and phototherapy insufficiency. `build-data.py` documents initial extraction and merging; it uses the preserved source in `data/public-facilities-2019.geojson`. Original source documents have not been altered or uploaded.
