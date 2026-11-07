# The Gambia Health Facility Atlas

An interactive map for exploring health facilities across The Gambia, with separate views of national health-system levels and neonatal care.

**[Explore the atlas on GitHub Pages →](https://drhammadkhan.github.io/gambia-health-facility-atlas/)** · [Sites mirror](https://gambia-health-facility-atlas.aquaantelope.chatgpt.site/)

![JavaScript](https://img.shields.io/badge/JavaScript-vanilla-F7DF1E?logo=javascript&logoColor=black)
![Leaflet](https://img.shields.io/badge/Map-Leaflet-199900?logo=leaflet&logoColor=white)
![Python](https://img.shields.io/badge/Data-Python_3-3776AB?logo=python&logoColor=white)

## What you can explore

- **102 mapped facilities** in the national view, with search and multiple care levels selectable at once.
- **14 neonatal assessment facilities**, classified independently of their general-service level.
- Filters for reported services, neonatal equipment and infrastructure, and published staff counts.
- Facility profiles with dated observations and source links, plus expandable classification and location evidence.
- CSV downloads of filtered facilities and public service/workforce records.

All map circles have the same size. Colour represents the care level in the selected view; selecting a facility adds an outline.

## Run locally

No Node packages, API keys or database are required. With Python 3 installed:

```bash
git clone https://github.com/drhammadkhan/gambia-health-facility-atlas.git
cd gambia-health-facility-atlas
python3 -m http.server 8045 --directory dist
```

Open **http://localhost:8045**. Serve the app over HTTP rather than opening `index.html` directly, because it loads its data with `fetch`.

Leaflet and the data files are bundled. OpenStreetMap tiles and optional web fonts need an internet connection.

## Two different care-level classifications

A hospital's general-service level does **not** establish its neonatal capability.

| View | Classification basis | Current mapped breakdown |
| --- | --- | --- |
| National health facilities | Intended structure in the National Health Sector Strategic Plan 2021–2025, §4.1; historical facility types used where necessary | 88 primary · 7 secondary · 6 tertiary · 1 unclassified |
| Neonatal health facilities | November 2025 assessment context and subsequent clinical clarification by Dr Hammad Khan | 8 primary · 5 secondary · 1 tertiary |

The strategic plan is inconsistent about the placement of minor health centres (§2.7 versus §4.1). The atlas follows §4.1 and records the discrepancy. Historical type-based assignments are provisional, not current verified designations. Njau remains unclassified for general services.

Neonatal secondary units are Bansang, Farafenni, Bwiam, Kanifing and Bundung MCH. EFSTH is tertiary. The remaining eight retained assessment facilities were designated primary neonatal units by Dr Hammad Khan on 5 November 2026. One facility from the original 15-facility assessment was excluded at the dataset owner's request.

## Data and provenance

| Dataset | What it contributes | Important dates and limitations |
| --- | --- | --- |
| [Maina et al., public-sector health facility database](https://pmc.ncbi.nlm.nih.gov/articles/PMC6658526/) | Historical facility inventory and coordinates | Published 2019; 101 Gambian records, plus Njau added from the supplied assessment. Not a current master register. |
| [National Health Sector Strategic Plan 2021–2025](https://extranet.who.int/cpcd/sites/default/files/public_file_repository/GMB_Gambia_National-Health-Sector-Strategic-Plan_2021-2025.pdf) | General care-level framework | §4.1, printed pp.100–102; named hospitals in §2.7.1, p.22. |
| PATG workshop and HF mission reports | Neonatal equipment, infrastructure and mission activity | November 2025; manually transcribed. Original Word/PDF reports are not included in this repository. |
| [National Audit Office EmOC follow-up audit](https://nao.gm/wp-content/uploads/2025/04/FOLLOW-UP-EmOC.pdf) | Services and midwife counts across 13 facilities | Report dated April 2023; observations from December 2022. The URL's 2025 upload path is not the observation date. |
| [National Assembly facility inspection report](https://nawatch.org/wp-content/uploads/2023/04/FINAL-REPORT-OF-THE-SELECT-COMMITTEE-ON-HEALTH.pdf) | Selected facility services and staffing | Visits in June–July 2022; public mirror. |
| Provider websites and attributed media reports | Additional service listings and aggregate staff counts | Dates vary; individual source links and scope are retained in each record. |

The public enrichment, reviewed on **5 November 2026**, contains service records for **22 facilities** and staffing counts for **19**. The complete source catalogue is available in the app's **Data & sources** dialog and in [`dist/public-sources.json`](dist/public-sources.json).

### Interpreting the records

- **“unavailable” for missing information means no record is available.** It is not evidence that the facility lacks that service. Facilities outside the neonatal assessment show a single unavailable assessment entry.
- Service observations describe their source date, not live operational readiness. Undated provider listings are marked unverified.
- Staff figures are published headcounts with a stated scope, not staff per shift or full-time equivalents. Counts of midwives, doctors or all employees are kept distinct; overlapping categories are never summed.
- Staffing norms are reference requirements, separate from observed staff numbers. Conflicting numeric and narrative findings are retained with notes rather than converted into unsupported staffing deficits.
- Phototherapy reported present in the workshop was insufficient. CPAP follows the structured assessment table; conflicting workshop comments remain noted.
- Surgery associated with the November 2025 mission does not establish ongoing surgical availability.
- Some coordinates are approximate locality positions. Private, new, closed, renamed or unmapped facilities may be missing.

This atlas supports planning and exploration; it is not a live referral directory or an authoritative current national facility register.

## Project structure

```text
.
├── build-data.py                 # Rebuilds the app's data and public-record CSV
├── data/
│   ├── public-facilities-2019.geojson  # Preserved historical inventory
│   └── public-enrichment.json    # Dated services, workforce records and sources
├── dist/                        # Complete deployable static app
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   ├── facilities.json           # Merged inventory, classifications and records
│   ├── assessment.json          # Retained neonatal assessment data
│   ├── public-sources.json       # Public source catalogue
│   ├── public-records.csv        # Normalized service/workforce export
│   ├── gambia-boundary.json
│   └── vendor/                  # Bundled Leaflet
└── .openai/hosting.json          # Existing Sites hosting configuration
```

## Update the data

1. Add or correct service and staffing observations in `data/public-enrichment.json`, retaining the source, observation date, scope and any uncertainty.
2. For inventory, care-level or neonatal-assessment changes, update the relevant mappings or transcribed rows in `build-data.py`.
3. Rebuild from the repository root:

   ```bash
   python3 build-data.py
   node --check dist/app.js
   ```

4. Review the resulting diff and inspect the affected facility profiles and filters in the local app. Commit both the source data and generated files.

The data generator uses only Python's standard library. Node.js is optional for the JavaScript syntax check; it is not needed to run the app.

## Hosting

GitHub Pages serves `dist/` at **https://drhammadkhan.github.io/gambia-health-facility-atlas/**. The workflow in `.github/workflows/pages.yml` publishes automatically when `dist/` changes on `main`, or can be run manually from the Actions tab. No build step or deployment secrets are required.

The existing Sites mirror is managed separately; `.openai/hosting.json` retains its project identity. Pushing to GitHub does not update that mirror. The app can also be deployed to any static host by publishing the contents of `dist/`.

## Attribution and reuse

Facility data from Maina et al. are published under **CC BY 4.0**; retain attribution when reusing them. The boundary derives from Natural Earth via [geo-countries](https://github.com/datasets/geo-countries). Basemap tiles are © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright). Leaflet retains its upstream license notice in the bundled files.

Other source documents and websites retain their respective rights. This repository does not grant a blanket license to third-party material, and no project-wide software license has yet been selected.
