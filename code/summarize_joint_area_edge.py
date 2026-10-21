from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reproduced/analysis'
OUT.mkdir(parents=True, exist_ok=True)
f = pd.read_csv(ROOT / 'data/analysis/canonical_matched_support.csv.gz')
assert len(f) == 79509 and (not f.duplicated(['GU_A3', 'GRID_ID']).any())
assert (f[['A_M_2000_m2', 'A_M_2023_m2', 'weight_m2']] > 0).all().all()
f['area_direction'] = np.where(f.A_M_2023_m2 >= f.A_M_2000_m2, 'persistence_or_gain', 'loss')
f['edge_direction'] = np.where(f.pMEHI > 0.005, 'hardening', np.where(f.pMEHI < -0.005, 'softening', 'near_neutral'))
rows = []
summaries = []
for code, g in [('GLOBAL', f), *list(f.groupby('GU_A3', sort=True))]:
    total_n = len(g)
    total_w = float(g.weight_m2.sum())
    nonloss = g[g.area_direction.eq('persistence_or_gain')]
    joint = nonloss[nonloss.edge_direction.eq('hardening')]
    for area in ['persistence_or_gain', 'loss']:
        a = g[g.area_direction.eq(area)]
        for edge in ['hardening', 'near_neutral', 'softening']:
            q = a[a.edge_direction.eq(edge)]
            w = float(q.weight_m2.sum())
            rows.append({'location_code': code, 'area_direction': area, 'edge_direction': edge, 'n': len(q), 'weight_m2': w, 'percent_all_cells': 100 * len(q) / total_n, 'percent_all_weight': 100 * w / total_w, 'percent_within_area_direction_cells': 100 * len(q) / len(a) if len(a) else np.nan, 'percent_within_area_direction_weight': 100 * w / a.weight_m2.sum() if a.weight_m2.sum() else np.nan})
    summaries.append({'location_code': code, 'all_n': total_n, 'area_nondecreasing_n': len(nonloss), 'area_nondecreasing_hardening_n': len(joint), 'joint_percent_all_cells': 100 * len(joint) / total_n, 'hardening_percent_within_nondecreasing_cells': 100 * len(joint) / len(nonloss) if len(nonloss) else None, 'joint_percent_all_weight': 100 * joint.weight_m2.sum() / total_w, 'hardening_percent_within_nondecreasing_weight': 100 * joint.weight_m2.sum() / nonloss.weight_m2.sum() if nonloss.weight_m2.sum() else None})
pd.DataFrame(rows).to_csv(OUT / 'joint_area_edge_crosstab.csv', index=False)
pd.DataFrame(summaries).to_csv(OUT / 'joint_area_edge_summary.csv', index=False)
print(f'Joint area and edge summaries: {len(f):,} matched neighbourhoods.')
