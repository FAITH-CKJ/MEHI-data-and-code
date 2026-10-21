from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'output'
SOURCE = ROOT / 'data' / 'figure_source'
GEOMETRY = ROOT / 'data' / 'scenario' / 'map_geometry.csv.gz'

def main() -> None:
    SOURCE.mkdir(parents=True, exist_ok=True)
    global_table = pd.read_csv(OUTPUT / 'future_global_smehi_summary.csv')
    country_table = pd.read_csv(OUTPUT / 'future_country_smehi_summary.csv')
    trajectory = global_table.copy()
    trajectory.insert(0, 'panel', 'a')
    trajectory['n_countries'] = 19
    trajectory['hard_edge_fraction_change_pp'] = 100.0 * (trajectory['hard_edge_fraction_future'] - trajectory['hard_edge_fraction_2023'])
    trajectory['mean_Delta_sMEHI_area_weighted'] = trajectory['Delta_sMEHI']
    trajectory['soft_to_mixed_or_hard_share_percent'] = 100.0 * trajectory['soft_to_mixed_or_hard_share']
    trajectory['method_tier'] = 'country_aggregated_150m_area_conserving_exposure_screen'
    trajectory = trajectory.sort_values(['SSP', 'year'])
    trajectory.to_csv(SOURCE / 'Fig5_global_trajectory.csv', index=False)
    ranking = country_table.loc[country_table['year'].eq(2100) & country_table['SSP'].isin(['SSP2', 'SSP3', 'SSP5'])].copy()
    ranking['hard_edge_fraction'] = ranking['hard_edge_fraction_future']
    ranking['rank_by_max_SSP235'] = ranking.groupby('country')['Delta_sMEHI'].transform('max').rank(method='dense', ascending=False).astype(int)
    ranking['is_zero_or_no_change'] = np.isclose(ranking['Delta_sMEHI'], 0.0, atol=1e-12)
    ranking['method_tier'] = 'country_aggregated_150m_area_conserving_exposure_screen'
    ranking = ranking[['country', 'SSP', 'year', 'n_grids', 'Delta_sMEHI', 'hard_edge_fraction', 'soft_to_mixed_or_hard_share', 'unmet_allocation_percent', 'method_tier', 'rank_by_max_SSP235', 'is_zero_or_no_change']].sort_values(['country', 'SSP'])
    assert len(ranking) == 57 and ranking['country'].nunique() == 19
    ranking.to_csv(SOURCE / 'Fig5_country_ranking_all19_SSP235_2100.csv', index=False)
    geometry = pd.read_csv(GEOMETRY)[['country', 'GRID_UID', 'GRID_ID', 'lon', 'lat', 'year']]
    assert len(geometry) == 117546 and (not geometry.duplicated(['country', 'GRID_UID', 'GRID_ID']).any())
    grid = pd.read_csv(OUTPUT / 'future_grid_smehi_summary.csv.gz')
    assert len(grid) == 117546 * 16
    for ssp in ('SSP2', 'SSP5'):
        subset = grid.loc[grid['SSP'].eq(ssp) & grid['year'].eq(2100), ['country', 'GRID_UID', 'edge_grid_id', 'Delta_sMEHI', 'sMEHI', 'hard_edge_future_flag']].rename(columns={'edge_grid_id': 'GRID_ID', 'Delta_sMEHI': f'Delta_sMEHI_{ssp}', 'sMEHI': f'sMEHI_{ssp}', 'hard_edge_future_flag': f'hard_edge_future_flag_{ssp}'})
        geometry = geometry.merge(subset, on=['country', 'GRID_UID', 'GRID_ID'], how='left', validate='one_to_one', indicator=True)
        assert geometry['_merge'].eq('both').all()
        geometry = geometry.drop(columns='_merge')
        weight = grid.loc[grid['SSP'].eq(ssp) & grid['year'].eq(2100), 'observed_external_support_m2']
        assert np.isclose(np.average(subset[f'Delta_sMEHI_{ssp}'], weights=weight), trajectory.loc[trajectory['SSP'].eq(ssp) & trajectory['year'].eq(2100), 'Delta_sMEHI'].item(), atol=1e-12)
    geometry.to_csv(SOURCE / 'Fig5_maps_SSP2_SSP5_2100.csv.gz', index=False, compression='gzip')
    print('Figure 5 source tables written to', SOURCE)
if __name__ == '__main__':
    main()
