# Third-party public data used in the MEHI study

Names and versions refer to the products actually used. Provider DOI records
identify source data; related article DOIs are labelled separately.

Project release: https://github.com/FAITH-CKJ/MEHI-data-and-code/releases/tag/v1.3.1

## 1. Global Mangrove Watch (1996–2020) Version 3.0 Dataset

Version / coverage used: 3.0; 1996–2020
Role: Primary mangrove envelope for the 2-km urban interface, sample-domain definition and coverage analysis; also baseline in alternative-envelope sensitivity.
Original data DOI / access: https://doi.org/10.5281/zenodo.6894273

## 2. Global Urban Boundaries (GUB), 2018 layer

Version / coverage used: 2018 polygon layer
Role: Urban polygon layer; boundaries >100 km² buffered by 2 km to define the direct urban–mangrove interface.
Original data DOI / access: https://data-starcloud.pcl.ac.cn/iearthdata/14
Related product paper: https://doi.org/10.1088/1748-9326/ab9be3

## 3. USGS Landsat 5 TM Collection 2 Level-2

Version / coverage used: Collection 2 Level-2; Tier 1 Earth Engine collection for 2000/2010 classification composites. One R08 2010 contextual case item is Tier 2; provider processing subversion not recorded.
Role: Main spectral/thermal/QA observations for 2000 and 2010 annual land-cover mosaics; RGB context in regional cases.
Original data DOI / access: https://doi.org/10.5066/P9IAXOVV
Collection access: https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT05_C02_T1_L2
Case-image access: https://planetarycomputer.microsoft.com/dataset/group/landsat

## 4. USGS Landsat 7 ETM+ Collection 2 Tier 1 Level-2

Version / coverage used: Collection 2 Level-2, Tier 1
Role: Gap-filling observations in annual mosaics; R08 2000 regional RGB case uses LE07_L2SP_089079_20001008_02_T1.
Original data DOI / access: https://doi.org/10.5066/P9C7I13B
Collection access: https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C02_T1_L2
Case-image access: https://planetarycomputer.microsoft.com/dataset/group/landsat

## 5. USGS Landsat 8 OLI/TIRS Collection 2 Tier 1 Level-2

Version / coverage used: Collection 2 Level-2, Tier 1
Role: Main observations for 2020/2023 annual classification mosaics and most 2020/2023 regional RGB panels.
Original data DOI / access: https://doi.org/10.5066/P9OGBGM6
Collection access: https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2
Case-image access: https://planetarycomputer.microsoft.com/dataset/group/landsat

## 6. GWL_FCS30 global 30 m wetland map, 2020

Version / coverage used: 2020 product, Zenodo record v1; mangrove class 185.
Role: Supporting mangrove-domain product recorded for mangrove and land-cover harmonization; exact pixel-level contribution is not separately traced in the portable numerical package.
Original data DOI / access: https://doi.org/10.5281/zenodo.7340516

## 7. High-resolution Global Mangrove Forests (HGMF_2020)

Version / coverage used: 2020 map, 10 m; no further release number recorded
Role: Alternative mangrove envelope in dataset-sensitivity analysis, evaluated against GMW v3 and their union; not the primary annual MEHI mosaic.
Original data DOI / access: https://doi.org/10.7910/DVN/PKAN93

## 8. Global 1-km Downscaled Urban Land Extent Projection and Base Year Grids by SSP Scenarios, 2000–2100

Version / coverage used: Version 1.00. The study uses SSP1, SSP2, SSP3 and SSP5 scenario urban fractions, 2020 alignment and 2030/2050/2070/2100 targets.
Role: External future urban-fraction pressure field for Fig. 5 scenario calculations.
Original data DOI / access: https://doi.org/10.7927/1Z4R-EZ63
Provider page: https://sedac.ciesin.columbia.edu/data/set/ssp-1-km-downscaled-urban-land-extent-projection-base-year-ssp-2000-2100

## 9. USGS Landsat 9 OLI/TIRS Collection 2 Level-2

Version / coverage used: Collection 2 Level-2, R02 2023 selected item is Tier 1 (LC09_L2SP_017041_20230218_02_T1); tier identified by the scene ID
Role: R02 2023 RGB context panel in Supplementary Figure 4; not a Landsat 9 input to the four-date classifier composites.
Original data DOI / access: https://doi.org/10.5066/P9OGBGM6
Collection access: https://planetarycomputer.microsoft.com/dataset/group/landsat

## 10. Natural Earth 1:50m land polygons

Version / coverage used: 1:50m land theme; the source release number of the retained GeoJSON is not recorded.
Role: Land basemap for figure production. Geographic join fields are also credited to Natural Earth; their administrative theme and version are not recorded.
Original data DOI / access: https://www.naturalearthdata.com/downloads/50m-physical-vectors/50m-land/

## Case-scene access and reuse

USGS Collection 2 Level-2 products were accessed through Google Earth Engine
for classification and the Microsoft Planetary Computer landsat-c2-l2 STAC
collection for case imagery. These are access platforms for the products above.
All 12 case acquisition dates and scene identifiers remain in
figures/supplementary_cases/source_data/R02_imagery_metadata.json,
R04_imagery_metadata.json and R08_imagery_metadata.json.

Landsat original citation guidance:
https://www.usgs.gov/landsat-missions/landsat-collection-2-level-2-science-products

Natural Earth reuse terms: https://www.naturalearthdata.com/about/terms-of-use/
Third-party material retains its provider terms.
