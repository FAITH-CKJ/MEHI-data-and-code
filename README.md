# MEHI data and code

Data and code for *Urban hardening of mangrove edges extends beyond forest loss*.

**Release: [v1.3.1](https://github.com/FAITH-CKJ/MEHI-data-and-code/releases/tag/v1.3.1).**

Download [MEHI_data_and_code_v1.3.1.zip](https://github.com/FAITH-CKJ/MEHI-data-and-code/releases/download/v1.3.1/MEHI_data_and_code_v1.3.1.zip), or clone this repository. The ZIP and repository contain the same files. Four annual land-cover mosaics are separate assets on the release page.

## Contents

| Directory | Contents |
|---|---|
| `code/` | MEHI calculation, classifier training and inference, sensitivity analysis, transition routes and scenarios |
| `data/` | Annual and matched neighbourhood records, training and validation inputs, figure source data and analytical summaries |
| `figures/` | Drawing programs, regional image crops, case membership and display-window data |
| `metadata/` | Bounds, coordinate systems and checksums of the four spatial assets |
| `workflow/` | Variable definitions, figure-source mapping, methods and third-party data sources |

The data cover 2000, 2010, 2020 and 2023: 474,003 neighbourhood-year records, 79,509 matched neighbourhoods, 42,795 training records and 10,657 validation records. The release includes seven trained classifiers. Annual and matched samples have distinct inclusion rules, documented in `data/dictionaries/DATA_DICTIONARY.md`.

## Setup

Use Python 3.11. Run commands from the repository root.

```text
python -m pip install -r code/requirements.txt
```

Tables are supplied as CSV or gzip-compressed CSV, spatial geometry as GeoJSON, and the seven checkpoints as PyTorch `.pth` files. The programs read these files directly. `SHA256SUMS.txt` lists file checksums. Variable definitions and inclusion rules are in `data/dictionaries/DATA_DICTIONARY.md`; spatial, classifier and scenario input schemas are in `workflow/INPUT_SCHEMAS.md`.

## Analyses

```text
python code/evaluate_map_validation.py
python code/analyze_routes.py
python code/sensitivity/recompute_sensitivity.py
python code/evaluate_temporal_uncertainty.py
python code/summarize_joint_area_edge.py
python code/scenario/run_scenario_projection.py self-test
python code/scenario/run_scenario_projection.py run-all --config config.json
python code/build_figure5_source.py
python code/landcover_classifier/inference_ensemble.py --self-test
```

Generated results are written to `output/` or `reproduced/`. `code/landcover_classifier/README.md` describes training and inference. Validation data were also used for checkpoint selection; final-map accuracy is calculated on 9,811 unique covered coordinate-year points. Outside-map and duplicate records remain identified separately.

## Figures

```text
python figures/figure1/code/draw_figure1.py --out reproduced_figures/figure1/figures --sources reproduced_figures/figure1/source_data
python figures/figures2_3/code/draw_figures23.py --out reproduced_figures/figures2_3/figures --sources reproduced_figures/figures2_3/source_data
python figures/figure4/code/draw_figure4.py --out reproduced_figures/figure4/figures --sources reproduced_figures/figure4/source_data
python code/figure5/draw_figure5.py --out reproduced_figures/figure5
python figures/supplementary_cases/code/draw_supplementary_cases.py --output-dir reproduced_figures/cases
```

Figure 3c reports signed component means as percentages of the sum of absolute gross contributions across all four components in each geographic row, using minimum-endpoint mangrove-area weights. Each component has its own horizontal range. Open circles, filled circles and diamonds show negative gross, positive gross and net contributions; colours and vector symbols identify P, C, B and S. Figure 3b shows conditional class composition without numerical labels inside the bars. Figure 4 uses a compact panel layout and one-decimal route labels; sample sizes and thresholds are given in the article captions. The drawing programs export the original-unit and relative component tables, normalization checks and axis ranges.

These programs reproduce main Figures 1–5 and Supplementary Figures 4–9. Figure 1 and Figure 2/3 source tables are generated from the retained inputs. Supplementary Figures 2–3 have numerical source tables; main Figure 6 is a conceptual diagram and Supplementary Figure 1 is a geographic locator. See `workflow/FIGURE_DATA_MAP.md` for the full mapping.

## Spatial construction and sources

The numerical analyses use the included tables. Full spatial construction additionally requires ArcGIS Pro and the four annual mosaic assets, described in `metadata/spatial_release_assets.json` and `workflow/EXTERNAL_DATA.md`. Run `python code/spatial/build_mehi_arcpy.py --help` for its arguments. Provider products, versions, DOI records and scene identifiers are listed in `workflow/THIRD_PARTY_SOURCES.md`.

## Citation and licences

Cao, K., Shen, X., Luo, X., Li, W. & Li, R. *Urban hardening of mangrove edges extends beyond forest loss: data and code*. Version 1.3.1 (2026). https://github.com/FAITH-CKJ/MEHI-data-and-code/releases/tag/v1.3.1

Machine-readable citations are in `CITATION.cff` and `CITATION_DATA.cff`. Code uses the MIT licence (`LICENSE`); the authors' data and model parameters use CC BY 4.0 (`LICENSE_DATA.txt`). Third-party material retains its original terms. See `THIRD_PARTY_NOTICES.md` for the figure colour-map attribution.

Corresponding author: Ruili Li, https://orcid.org/0009-0001-9166-2469.
