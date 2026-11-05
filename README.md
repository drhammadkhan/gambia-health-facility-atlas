# The Gambia Health Facility Atlas

Static Leaflet app. Serve `dist/` over HTTP, e.g. `python3 -m http.server 8045 --directory dist`.

102 facilities: 101 records from the historical Maina et al. public-sector database plus Njau. The neonatal view contains 14 retained workshop assessment facilities; one facility was removed from the app dataset at the owner's request. The original source documents still cover 15 facilities and have not been edited. The general-services view contains all 102 records. Coverage is incomplete, not a current authoritative register.

Separate general and neonatal classification fields include source evidence. General grouping follows strategic plan section 4.1, with discrepancies against section 2.7 disclosed in the app. Six named general/teaching hospitals are tertiary; seven major/district records are secondary; 88 historical clinics/minor centres are provisionally primary; Njau is unclassified. Neonatal levels follow Dr Hammad Khan’s classifications: eight primary, five secondary and EFSTH tertiary. The eight previously unclassified assessment facilities were designated primary on 5 November 2026. General-service levels are separate.

`build-data.py` regenerates `dist/facilities.json` and `dist/assessment.json` from the preserved source `data/public-facilities-2019.geojson` and transcribed report data. Excluded facility data have been removed from the generator and generated files. CSV exports include both classifications. All map circles have radius 7; selection uses an outline only. Leaflet, the boundary and facility data are bundled; OpenStreetMap tiles and optional fonts require internet.
