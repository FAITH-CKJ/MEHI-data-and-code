# External data products

| Product | Version / years | Role | Persistent identifier or access route |
|---|---|---|---|
| Global Mangrove Watch | v3.0; multi-epoch mangrove extent, 1996-2020 | Primary mangrove envelope and extent comparison | DOI: https://doi.org/10.5281/zenodo.6894273 |
| HGMF | 2020; 10 m global mangrove forest map | Alternative mangrove envelope | DOI: https://doi.org/10.7910/DVN/PKAN93 |
| GWL_FCS30 | 2020; 30 m, mangrove class 185 | Supporting mangrove-domain product recorded in the original study documentation | https://doi.org/10.5281/zenodo.7340516; product article https://doi.org/10.5194/essd-15-265-2023 |
| USGS Landsat 5 Collection 2 Tier 1 Level-2 | 2000 and 2010 composites | Surface reflectance, land-surface temperature and QA inputs | Earth Engine ID `LANDSAT/LT05/C02/T1_L2`; https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT05_C02_T1_L2 |
| USGS Landsat 7 Collection 2 Tier 1 Level-2 | Gap filling where required | Surface reflectance, land-surface temperature and QA inputs | Earth Engine ID `LANDSAT/LE07/C02/T1_L2`; https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C02_T1_L2 |
| USGS Landsat 8 Collection 2 Tier 1 Level-2 | 2020 and 2023 composites | Surface reflectance, land-surface temperature and QA inputs | Earth Engine ID `LANDSAT/LC08/C02/T1_L2`; https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2 |
| Global Urban Boundaries | 2018; polygons derived from 30 m GAIA | Urban-domain definition | iEarth DataHub record: https://data-starcloud.pcl.ac.cn/iearthdata/14; product paper DOI: https://doi.org/10.1088/1748-9326/ab9be3 |
| Gao-Pesaresi SSP urban fraction | Version 1.00; 2020-2100 | Scenario urban-fraction increments | https://doi.org/10.7927/1Z4R-EZ63 |

Supplementary Notes 1 and 2 provide the analytical variables, temporal alignment, scenario lookup structure, projection and spatial construction details. Provider-managed files should retain their original names and checksums when used for a full rerun.

The four coastal polygon mosaics are public as separate v1.3.1
release assets. Their 20 core Shapefile components contain 1,134,839,452 bytes.
They preserve the original geometry, land-cover class and country/location
code. The release manifest records component hashes, field definitions,
feature counts, coordinate systems, bounds and download links.

The larger spatial production archive, including upstream imagery and
intermediate production files, exceeds 1 TB according to the study archive
record. It is available through the corresponding author, Ruili Li
(liruili@pkusz.edu.cn), who coordinates transfer. The four mosaics, original
predictor sample tables and adopted analytical inputs do not require this
larger archive to be requested separately.

## Case imagery and geographic attribution

The Supplementary Figure 4–6 RGB crops use USGS Landsat Collection 2
Level-2 scenes accessed through the Planetary Computer `landsat-c2-l2`
collection. Per-case metadata record each actual acquisition date, item ID
and scene-wide cloud cover, including Landsat 9 where selected for a context
panel. Those context panels are distinct from classifier predictor composites.
Landsat data remain public domain wherever hosted:
https://www.usgs.gov/faqs/are-landsat-data-cloud-still-considered-be-within-public-domain .
Use and redistribution guidance:
https://www.usgs.gov/faqs/are-there-any-restrictions-use-or-redistribution-landsat-data .

Geographic reporting codes and base-map shapes retain Natural Earth attribution
and public-domain status: https://www.naturalearthdata.com/about/terms-of-use/ .
Other provider-managed products retain their provider terms; the authors'
data licence does not relicense third-party products.
