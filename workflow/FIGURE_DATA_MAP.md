# Figure and data sources

Paths are relative to the repository root. Source filenames use the figure numbers in the article. Drawing programs read the supplied CSV, gzip-compressed CSV and GeoJSON files directly.

| Figure | Inputs and program |
|---|---|
| Main 1 and Supplementary 7 | Annual records in `data/analysis/`, annual state maps in `data/figure_source/` and the retained `figures/figure1/source_data/Fig1_hard_edge_0p5deg_bins.csv`. Run `figures/figure1/code/draw_figure1.py`. |
| Main 2–3 and Supplementary 8–9 | `data/analysis/canonical_matched_support.csv.gz`, annual records and the source summaries in `data/figure_source/`. Run `figures/figures2_3/code/draw_figures23.py`; it creates the joined record table and panel source tables. |
| Main 4 | `data/figure_source/Fig4_transition_matrix.csv`, `Fig4_global_route_shares.csv`, `Fig4_country_route_shares.csv` and `Fig4_country_association.csv`. Run `figures/figure4/code/draw_figure4.py`. Neighbourhood-level route data are in `data/supporting/Fig4_grid_route_classification.csv.gz`. |
| Main 5 | `data/figure_source/Fig5_global_trajectory.csv`, `Fig5_country_ranking_all19_SSP235_2100.csv`, `Fig5_maps_SSP2_SSP5_2100.csv.gz`; backtests and uncertainty summaries are in `data/supporting/`. Run `code/figure5/draw_figure5.py`. Scenario inputs and commands are documented in the root README. |
| Main 6 | Conceptual diagram in the article. |
| Supplementary 1 | Geographic locator in the Supplementary Information; annual coordinates and the four mosaic assets define analytical coverage. |
| Supplementary 2 | `data/supporting/dataset_sensitivity_summary.csv`. |
| Supplementary 3 | `data/supplementary/SuppFig3_scale_sensitivity_source.csv`, `data/supporting/MEHI_scale_sensitivity.csv` and `MEHI_scale_agreement_summary.csv`. |
| Supplementary 4–6 | R02, R04 and R08 source images, 56/51/64 selected-cluster records, four annual display-window tables per case, matched-window tables and scene metadata under `figures/supplementary_cases/`. Run its `code/draw_supplementary_cases.py`. |

For main Figure 3c, `Fig3c_country_component_gross_net.csv` contains the original-unit component means and `Fig3c_relative_component_contributions.csv` contains the displayed percentages and their common within-row denominator. `Fig3c_display_validation.json` records gross-sum closure and reconstruction of pMEHI, and `Fig3c_axis_ranges.json` records the four displayed horizontal ranges. These outputs are generated from all 79,509 matched neighbourhoods by the Figure 2/3 program.

The drawing programs export panel source tables alongside figures. Finished figures and complete captions are supplied in the article and Supplementary Information.

`GU_A3` and `GRID_ID` jointly identify neighbourhoods; annual joins also require `YEAR`. Final-map validation contains 9,811 unique covered coordinate-year pairs, 654 outside-map entries and 192 repeated entries. Inputs, weights and sample definitions are detailed in `data/dictionaries/DATA_DICTIONARY.md` and `workflow/INPUT_SCHEMAS.md`.

The four land-cover mosaics use EPSG:4326. Spatial analysis uses Mollweide (ESRI:54009). Classes are 1 mangrove, 2 tidal flat, 3 non-mangrove vegetation, 4 water, 5 built-up and 6 other. Analytical areas in square metres are calculated from projected geometry. Spatial file hashes, bounds, counts and CRS are in `metadata/spatial_release_assets.json`.
