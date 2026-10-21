from __future__ import annotations
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data/figure_source'
OUT = ROOT / 'reproduced_figures'
W = 167.0
SOFT, NEUTRAL, HARD = ('#138F8F', '#D5D0C7', '#D94A26')
SSPC = {'SSP1': '#3B8F5A', 'SSP2': '#2F73C5', 'SSP3': '#D19A2A', 'SSP5': '#A43A63'}
LAND = ROOT / 'data/cartography/ne_50m_land.geojson'
plt.rcParams.update({'font.family': 'Arial', 'font.size': 8, 'axes.labelsize': 8, 'axes.titlesize': 8.5, 'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5, 'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none', 'axes.linewidth': 0.55, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.unicode_minus': True, 'text.color': '#222222', 'axes.labelcolor': '#222222', 'xtick.color': '#333333', 'ytick.color': '#333333', 'savefig.facecolor': 'white'})

def read(name):
    p = DATA / name
    return pd.read_csv(p)

def canvas(height):
    f = plt.figure(figsize=(W / 25.4, height / 25.4), dpi=150)
    return (f, height)

def axes(f, height, x, y, w, h):
    return f.add_axes([x / W, y / height, w / W, h / height])

def label(f, height, letter, text, x, y):
    f.text(x / W, y / height, letter, weight='bold', fontsize=10, ha='left', va='baseline')
    f.text((x + 5) / W, y / height, text, fontsize=8.5, ha='left', va='baseline')

def clean(ax):
    ax.grid(axis='y', color='#E9E9E9', lw=0.45, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(length=2.4, width=0.5, pad=2)
    for sp in ax.spines.values():
        sp.set_color('#999999')

def save(fig, name, height):
    for extension in ['pdf', 'svg', 'png']:
        fig.savefig(OUT / f'{name}.{extension}', dpi=450 if extension == 'pdf' else 300)
    plt.close(fig)

def land(ax, extent=(-177, 180, -40, 36)):
    feats = json.loads(LAND.read_text(encoding='utf-8'))['features']
    patches = []
    for feat in feats:
        geom = feat['geometry']
        polys = [geom['coordinates']] if geom['type'] == 'Polygon' else geom['coordinates']
        for poly in polys:
            arr = np.asarray(poly[0])
            if arr[:, 0].max() < extent[0] or arr[:, 0].min() > extent[1] or arr[:, 1].max() < extent[2] or (arr[:, 1].min() > extent[3]):
                continue
            patches.append(Polygon(arr, closed=True))
    ax.add_collection(PatchCollection(patches, facecolor='#F4F1EA', edgecolor='#BDB7AC', lw=0.25, zorder=1))
    ax.set(xlim=extent[:2], ylim=extent[2:])
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([-120, -60, 0, 60, 120], ['120°W', '60°W', '0°', '60°E', '120°E'])
    ax.set_yticks([-30, 0, 30], ['30°S', '0°', '30°N'])
    ax.set(xlim=extent[:2], ylim=extent[2:])
    ax.grid(color='#EAEAEA', linewidth=0.35, zorder=0)
    ax.tick_params(length=2, width=0.5, pad=1.6, labelsize=7.3)
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_color('#B7B7B0')
        sp.set_linewidth(0.5)

def scenario_weights(maps):
    weight_path = DATA / 'Fig5_2023_external_area_weights.csv.gz'
    w = pd.read_csv(weight_path)
    keys = ['country', 'GRID_ID', 'GRID_UID']
    assert not w.duplicated(keys).any() and (not maps.duplicated(keys).any())
    j = maps.merge(w, on=keys, how='left', validate='one_to_one', indicator=True)
    assert len(j) == 117546 and j._merge.eq('both').all()
    assert j.A_OBS_EXT_M2.notna().all() and j.A_OBS_EXT_M2.ge(0).all()
    return j.drop(columns='_merge')

def draw_scenario_figure():
    traj = read('Fig5_global_trajectory.csv')
    maps = read('Fig5_maps_SSP2_SSP5_2100.csv.gz')
    rank = read('Fig5_country_ranking_all19_SSP235_2100.csv')
    maps = scenario_weights(maps)
    maps['scenario_support_m2'] = maps.A_OBS_EXT_M2.clip(lower=1.0)
    assert len(rank) == 57 and rank.country.nunique() == 19
    assert not rank.duplicated(['country', 'SSP']).any() and rank.Delta_sMEHI.notna().all()
    maps['lon_bin'] = np.floor(maps.lon / 0.5) * 0.5 + 0.25
    maps['lat_bin'] = np.floor(maps.lat / 0.5) * 0.5 + 0.25
    binned = []
    for ssp in ['SSP2', 'SSP5']:
        maps['weighted_value'] = maps[f'Delta_sMEHI_{ssp}'] * maps.scenario_support_m2
        b = maps.groupby(['lon_bin', 'lat_bin'], as_index=False).agg(weighted_sum=('weighted_value', 'sum'), external_support_m2=('scenario_support_m2', 'sum'), n_neighbourhoods=('GRID_UID', 'size'))
        assert b.external_support_m2.gt(0).all()
        b['Delta_sMEHI'] = b.weighted_sum / b.external_support_m2
        b['SSP'] = ssp
        b['year'] = 2100
        binned.append(b)
        target = traj.loc[traj.SSP.eq(ssp) & traj.year.eq(2100), 'Delta_sMEHI'].item()
        aggregate = np.average(maps[f'Delta_sMEHI_{ssp}'], weights=maps.scenario_support_m2)
        assert np.isclose(target, aggregate, rtol=0, atol=1e-10), (ssp, target, aggregate)
    bins = pd.concat(binned, ignore_index=True)
    bins.to_csv(OUT / 'Fig5_spatial_allocation_bins.csv', index=False)
    norm = Normalize(0, np.ceil(bins.Delta_sMEHI.max() * 10) / 10)
    cmap = plt.get_cmap('cividis')
    f, H = canvas(195)
    label(f, H, 'a', 'Global exposure at evaluated SSP years', 5, 188)
    aa = axes(f, H, 18, 156, 132, 27)
    for ssp in ['SSP1', 'SSP2', 'SSP3', 'SSP5']:
        d = traj[traj.SSP.eq(ssp)].sort_values('year')
        aa.plot(d.year, d.Delta_sMEHI, 'o--', color=SSPC[ssp], lw=0.9, ms=4, mec='white', mew=0.5)
        dy = {'SSP1': -0.003, 'SSP2': 0, 'SSP3': 0.002, 'SSP5': 0}[ssp]
        aa.text(2103, d.iloc[-1].Delta_sMEHI + dy, ssp, fontsize=8, color=SSPC[ssp], va='center', weight='bold')
    aa.axhline(0, color='#999999', lw=0.55)
    aa.set(xlim=(2027, 2110), ylim=(0, 0.18), xticks=[2030, 2050, 2070, 2100], yticks=[0, 0.08, 0.16])
    aa.set_xlabel('Evaluated year', labelpad=1)
    aa.set_ylabel('Area-weighted ΔsMEHI', labelpad=3)
    clean(aa)
    for letter, ssp, y in [('b', 'SSP2', 115), ('c', 'SSP5', 76)]:
        ax = axes(f, H, 10, y, 135, 28.74)
        land(ax)
        b = bins[bins.SSP.eq(ssp)]
        ax.scatter(b.lon_bin, b.lat_bin, c=b.Delta_sMEHI, cmap=cmap, norm=norm, s=8.5, marker='o', edgecolor='white', lw=0.18, zorder=3, rasterized=True)
        label(f, H, letter, f'{ssp}, 2100 · conditional spatial allocation', 5, y + 31)
    cax = axes(f, H, 151, 76, 2.5, 67.7)
    cb = f.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax)
    cb.ax.tick_params(labelsize=7.3, length=2, pad=2)
    cb.set_label('ΔsMEHI (0.5° bins)', fontsize=8, labelpad=3)
    f.text(10 / W, 69.5 / H, 'Illustrative local screen · 2023 external-support weights', fontsize=7.3)
    label(f, H, 'd', 'Country/location exposure in 2100', 5, 65)
    ad = axes(f, H, 17, 10, 141, 50)
    order = rank.groupby('country').Delta_sMEHI.max().sort_values(ascending=False).index.tolist()
    ys = np.arange(19)
    for ssp, off in [('SSP2', -0.23), ('SSP3', 0), ('SSP5', 0.23)]:
        v = rank[rank.SSP.eq(ssp)].set_index('country').reindex(order).Delta_sMEHI.to_numpy()
        assert not np.isnan(v).any()
        ad.hlines(ys + off, 0, v, color=SSPC[ssp], lw=1.1, zorder=2)
        zero = np.isclose(v, 0, atol=1e-12)
        ad.scatter(v[~zero], (ys + off)[~zero], s=8, c=SSPC[ssp], edgecolor='white', lw=0.25, zorder=3)
        ad.scatter(v[zero], (ys + off)[zero], s=9, facecolor='white', edgecolor=SSPC[ssp], lw=0.6, zorder=4, clip_on=False)
    ad.set_yticks(ys, order)
    ad.set_ylim(18.7, -0.7)
    ad.set_xlim(-0.006, 0.8)
    ad.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    ad.set_xlabel('Area-weighted ΔsMEHI', labelpad=2)
    ad.tick_params(axis='y', labelsize=7.5, length=0, pad=3)
    ad.grid(axis='x', color='#EAEAEA', lw=0.45)
    ad.set_axisbelow(True)
    handles = [Line2D([0], [0], color=SSPC[s], lw=2, label=s) for s in ['SSP2', 'SSP3', 'SSP5']]
    handles.append(Line2D([0], [0], marker='o', lw=0, mfc='white', mec='#777777', ms=3, label='Zero increment'))
    ad.legend(handles=handles, frameon=False, ncol=4, fontsize=7.2, loc='lower right', bbox_to_anchor=(1, 1.015), handlelength=1, handletextpad=0.4, columnspacing=0.75, borderpad=0)
    save(f, 'Fig5_projected_urban_edge_exposure_R1', H)
