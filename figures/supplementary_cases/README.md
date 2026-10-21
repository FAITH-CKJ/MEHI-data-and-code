# Supplementary Figures 4–6: regional image and MEHI sources

R02, R04 and R08 correspond to Supplementary Figures 4, 5 and 6. The source
rasters are the inputs used by the supplied drawing program to reconstruct
the six-panel examples.
The four RGB panels for each case are 512 × 512, three-band Landsat views
in EPSG:4326. Their actual acquisition dates, scene IDs, collection and
scene-wide cloud-cover metadata are recorded per case. These display images
are separate from the multi-date predictor composites used for classification.
USGS Landsat source data are public domain; attribution is retained.

## Analysis cluster and display window

The annotated means summarize selected change clusters of 56, 51 and 64
neighbourhoods. They use minimum endpoint mangrove-area weights. The maps
show larger surrounding windows containing 432, 857 and 818 matched
neighbourhoods, respectively. Do not calculate the annotated cluster means
from all rows in the display windows.

Clusters were selected from the upper/lower 5% tails of all 79,509 pMEHI
records, grouped by GU_A3, change direction and 5-km bins of the recorded
Mollweide centroids (floor(x/5000), floor(y/5000)). The published cluster
membership CSVs retain exact GRID_IDs and source values. The GeoJSON polygons
are display windows, not cluster boundaries. Annual window CSVs include all
available year-specific neighbourhoods and retain their original membership.

`selection_score` is a ranking score calculated as abs(mean_pMEHI)*100 +
min(n,50)*0.7 + a country/location bonus (2 for USA/MYS/AUS/BRA, 8 otherwise).
It measures cluster size and change magnitude for case selection. Scene
acquisition and cloud-cover metadata describe the imagery separately.

Run from the package root:

```text
python figures/supplementary_cases/code/draw_supplementary_cases.py
```

This rebuilds the six-panel PDFs from the original image crops, applying the
same brightness/contrast adjustments, map cropping and layout as the paper.
