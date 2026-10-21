from __future__ import annotations
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Ellipse, PathPatch, Polygon, Rectangle, Wedge
from matplotlib.path import Path as MplPath
import numpy as np
import pandas as pd
from shapely.geometry import box as geo_box, shape as geo_shape
from shapely.ops import unary_union
HERE = Path(__file__).resolve().parents[1]
DATA = HERE.parents[1] / 'data'
OUT, SOURCE = [HERE / n for n in ['figures', 'source_data']]
BINS = SOURCE / 'Fig1_hard_edge_0p5deg_bins.csv'
W, H = (184.0, 240.0)
EXTENT = (-102.0, 180.0, -40.0, 36.0)
FLORIDA_EXTENT = (-82.4, -81.28, 26.0, 27.26)
ZOOM_WIDTH_MM = 16.6595744680851
STAT_INSET_BOUNDS = (62.0, -32.0, 46.0, 19.0)
ZOOM_MARK_AREA = 4.0
INK, SECONDARY = ('#233441', '#64717A')
LAND_FILL, LAND_EDGE, OCEAN = ('#EFEEE8', '#BAC3C5', '#F5F9FB')
MEHI_BOUNDS = np.array([-1, -0.8, -0.75, -0.7, -0.675, -0.65, -0.625, -0.6, -0.575, -0.55, -0.525, -0.5, -0.475, -0.45, -0.4, -0.33, 0, 0.33])
RAW_MEHI_COLORS = ['#011959', '#0c2f5d', '#114160', '#154f62', '#1e5d62', '#2f675c', '#447052', '#5b7745', '#747e38', '#8f862d', '#ad8c2d', '#ca923c', '#e39754', '#f59f74', '#fdaa97', '#fdb5b8', '#fcc0d8', '#faccfa']
MEHI_COLORS = RAW_MEHI_COLORS[:-1]
RAW_MEHI_BOUNDS = np.r_[MEHI_BOUNDS, 1.0]
HARD_BOUNDS = np.array([0, 0.025, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 10, 25, 100])
HARD_COLORS = ['#011959', '#0d325e', '#124561', '#185562', '#26635f', '#3c6d56', '#577647', '#737e38', '#91862d', '#b38e2f', '#d29343', '#ed9a62', '#fba689', '#fdb2af', '#fcbfd3', '#faccfa']
POINT_EDGE = '#536777'
STATE_COLORS = ['#18658C', '#947334', '#A63734']
GEOGRAPHIC_INSETS = []
LAND_GEOMETRY = None
plt.rcParams.update({'font.family': ['Arial', 'DejaVu Sans'], 'font.size': 8, 'axes.labelsize': 7.5, 'axes.titlesize': 8.5, 'xtick.labelsize': 7, 'ytick.labelsize': 7, 'text.color': INK, 'axes.labelcolor': INK, 'xtick.color': SECONDARY, 'ytick.color': SECONDARY, 'axes.linewidth': 0.5, 'axes.unicode_minus': True, 'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none', 'svg.hashsalt': 'MEHI-Figure1', 'savefig.facecolor': 'white'})

def read(relative):
    path = DATA / relative
    return pd.read_csv(path, float_precision='round_trip')

def axes(fig, x, y, w, h):
    return fig.add_axes([x / W, y / H, w / W, h / H])

def base_map(ax, land, show_longitudes, extent=EXTENT):
    patches = []
    for feat in land['features']:
        geom = feat['geometry']
        polygons = [geom['coordinates']] if geom['type'] == 'Polygon' else geom['coordinates']
        for polygon in polygons:
            arr = np.asarray(polygon[0])
            if arr[:, 0].max() < extent[0] or arr[:, 0].min() > extent[1] or arr[:, 1].max() < extent[2] or (arr[:, 1].min() > extent[3]):
                continue
            patches.append(Polygon(arr, closed=True))
    ax.set_facecolor(OCEAN)
    ax.add_collection(PatchCollection(patches, facecolor=LAND_FILL, edgecolor=LAND_EDGE, lw=0.28, zorder=1))
    ax.set(xlim=extent[:2], ylim=extent[2:])
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([-90, -30, 30, 90, 150], ['90°W', '30°W', '30°E', '90°E', '150°E'] if show_longitudes else [''] * 5)
    ax.set_yticks([-30, 0, 30], ['30°S', '0°', '30°N'])
    ax.grid(color='#DDE6EA', linewidth=0.28, alpha=0.65, zorder=0)
    ax.tick_params(length=1.8, width=0.45, pad=1.7, labelsize=7.2)
    if not show_longitudes:
        ax.tick_params(axis='x', length=0)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('#BBC1C4')
        spine.set_linewidth(0.5)

def plot_bins(ax, frame, kind):
    if kind == 'MEHI':
        ax.scatter(frame.bin_lon, frame.bin_lat, c=frame.mean_MEHI, s=18, cmap=ListedColormap(MEHI_COLORS), norm=BoundaryNorm(MEHI_BOUNDS, len(MEHI_COLORS)), edgecolors=POINT_EDGE, linewidths=0.22, alpha=1, zorder=3)
    else:
        zero = frame.hard_area_share_percent.eq(0)
        ax.scatter(frame.loc[zero, 'bin_lon'], frame.loc[zero, 'bin_lat'], s=18, facecolors='none', edgecolors='#A4AFB4', linewidths=0.48, zorder=2.5)
        ax.scatter(frame.loc[~zero, 'bin_lon'], frame.loc[~zero, 'bin_lat'], s=18, c=frame.loc[~zero, 'hard_area_share_percent'], cmap=ListedColormap(HARD_COLORS), norm=BoundaryNorm(HARD_BOUNDS, len(HARD_COLORS)), edgecolors=POINT_EDGE, linewidths=0.22, zorder=3)

def geographic_inset(ax, land, frame, raw, kind, letter):
    width = ZOOM_WIDTH_MM / (162 / 282)
    height = width * (FLORIDA_EXTENT[3] - FLORIDA_EXTENT[2]) / (FLORIDA_EXTENT[1] - FLORIDA_EXTENT[0])
    ia = ax.inset_axes([-99, -37, width, height], transform=ax.transData)
    base_map(ia, land, False, FLORIDA_EXTENT)
    ia.set_xticks([])
    ia.set_yticks([])
    ia.grid(False)
    ia.set(xlim=FLORIDA_EXTENT[:2], ylim=FLORIDA_EXTENT[2:])
    for side in ia.spines.values():
        side.set_color('#83949D')
        side.set_linewidth(0.5)
    x0, x1, y0, y1 = FLORIDA_EXTENT
    selected = raw[raw.lon.between(x0, x1) & raw.lat.between(y0, y1)].copy()
    original_coordinates = selected[['lon', 'lat']].to_numpy().copy()
    selected['bin_ix'] = np.floor(selected.lon / 0.5).astype(int)
    selected['bin_iy'] = np.floor(selected.lat / 0.5).astype(int)
    selected = selected.merge(frame[['bin_ix', 'bin_iy', 'mean_MEHI', 'hard_area_share_percent']], on=['bin_ix', 'bin_iy'], how='left', sort=False, validate='many_to_one')
    assert np.array_equal(selected[['lon', 'lat']].to_numpy(), original_coordinates)
    assert not selected[['mean_MEHI', 'hard_area_share_percent']].isna().any().any()
    if kind == 'MEHI':
        ia.scatter(selected.lon, selected.lat, c=selected.mean_MEHI, s=ZOOM_MARK_AREA, cmap=ListedColormap(MEHI_COLORS), norm=BoundaryNorm(MEHI_BOUNDS, len(MEHI_COLORS)), edgecolors=POINT_EDGE, linewidths=0.1, rasterized=True, zorder=3)
    else:
        zero = selected.hard_area_share_percent.eq(0)
        ia.scatter(selected.loc[zero, 'lon'], selected.loc[zero, 'lat'], s=ZOOM_MARK_AREA, facecolors='none', edgecolors='#A4AFB4', linewidths=0.1, rasterized=True, zorder=2.5)
        ia.scatter(selected.loc[~zero, 'lon'], selected.loc[~zero, 'lat'], s=ZOOM_MARK_AREA, c=selected.loc[~zero, 'hard_area_share_percent'], cmap=ListedColormap(HARD_COLORS), norm=BoundaryNorm(HARD_BOUNDS, len(HARD_COLORS)), edgecolors=POINT_EDGE, linewidths=0.1, rasterized=True, zorder=3)
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, ec='#5E747F', lw=0.5, zorder=2))
    star = ax.text(-78.2, 30.7, '*', fontsize=8.5, ha='left', va='bottom', color='#4F6773', zorder=5)
    ia.text(0.92, 0.85, '*', fontsize=8.5, ha='center', va='bottom', color='#4F6773', transform=ia.transAxes)
    GEOGRAPHIC_INSETS.append((letter, ax, ia, star, selected))

def forest_icon(ax, x, y, scale=1):
    tr = ax.transAxes
    trunk = '#796049'
    leaf_colors = ['#327453', '#4A9769', '#6AA375', '#388662', '#287B59']
    verts = [(x - 0.012 * scale, y), (x - 0.01 * scale, y + 0.11 * scale), (x + 0.004 * scale, y + 0.18 * scale), (x + 0.011 * scale, y + 0.04 * scale), (x + 0.015 * scale, y)]
    ax.add_patch(PathPatch(MplPath(verts, [1, 3, 3, 3, 3]), fill=False, ec=trunk, lw=0.85, transform=tr, clip_on=False))
    for dx, bend in [(-0.04, -0.018), (0.046, 0.022)]:
        ax.add_patch(PathPatch(MplPath([(x, y + 0.035 * scale), (x + bend * scale, y), (x + dx * scale, y - 0.02 * scale)], [1, 3, 3]), fill=False, ec=trunk, lw=0.65, transform=tr, clip_on=False))
    for leaf, (xx, yy, ww, hh, angle) in zip(leaf_colors, [(-0.033, 0.145, 0.102, 0.145, 22), (0.03, 0.16, 0.102, 0.16, -18), (0, 0.215, 0.115, 0.15, 4), (-0.065, 0.115, 0.084, 0.1, 30), (0.071, 0.124, 0.083, 0.11, -26)]):
        ax.add_patch(Ellipse((x + xx * scale, y + yy * scale), ww * scale, hh * scale, angle=angle, fc=leaf, ec='white', lw=0.2, transform=tr, clip_on=False))

def city_icon(ax, x, y, scale=1):
    tr, color = (ax.transAxes, STATE_COLORS[2])
    for fill, (xx, yy, ww, hh) in zip(['#C87959', '#963F4C', '#B95B4B'], [(-0.082, 0, 0.063, 0.19), (-0.014, 0, 0.072, 0.28), (0.062, 0, 0.052, 0.15)]):
        ax.add_patch(Rectangle((x + xx * scale, y + yy * scale), ww * scale, hh * scale, fc=fill, ec='white', lw=0.25, transform=tr, clip_on=False))
        for yc in np.arange(0.04, hh - 0.025, 0.065):
            ax.add_patch(Rectangle((x + (xx + 0.018) * scale, y + yc * scale), 0.013 * scale, 0.024 * scale, fc='#F9F2E8', ec='none', transform=tr, clip_on=False))
    ax.plot([x - 0.093 * scale, x + 0.13 * scale], [y - 0.009 * scale] * 2, color=color, lw=0.65, transform=tr, clip_on=False)

def location_tile(ax, x, y, width, height, color):
    tr = ax.transAxes
    points = np.array([[0, 0.1], [0.33, 0], [0.66, 0.15], [1, 0.05], [1, 0.95], [0.66, 1], [0.33, 0.85], [0, 0.95]])
    points = points * np.array([width, height]) + np.array([x, y])
    ax.add_patch(Polygon(points, closed=True, fc=color, ec=OCEAN, lw=0.22, transform=tr, clip_on=False))
    for xx, ya, yb in [(0.33, 0, 0.85), (0.66, 0.15, 1)]:
        ax.plot([x + width * xx] * 2, [y + height * ya, y + height * yb], color='white', lw=0.24, alpha=0.8, transform=tr, clip_on=False)
    path = MplPath([(x, y + height * 0.4), (x + width * 0.28, y + height * 0.66), (x + width * 0.54, y + height * 0.42), (x + width, y + height * 0.66)], [1, 4, 4, 4])
    ax.add_patch(PathPatch(path, fill=False, ec='white', lw=0.25, transform=tr, clip_on=False))

def evidence_inset(ax, letter, evidence):
    bounds = (62.0, -34.0, 46.0, 17.0) if letter == 'd' else STAT_INSET_BOUNDS
    ia = ax.inset_axes(bounds, transform=ax.transData)
    ia.set_facecolor(OCEAN)
    ia.tick_params(axis='both', length=1.4, width=0.4, pad=1.1, labelsize=7)
    for side in ['top', 'right', 'left', 'bottom']:
        ia.spines[side].set_visible(False)
    title = ''
    subtitle = ''
    if letter == 'a':
        rows = evidence['relative']
        vals = rows.relative_share_change_percent.to_numpy()
        ia.set(xlim=(-0.45, 2.45), ylim=(-30, 155), xticks=[], yticks=[0, 120])
        ia.spines['left'].set_visible(True)
        ia.spines['left'].set_color('#A3B1B9')
        ia.spines['left'].set_linewidth(0.4)
        ia.spines['left'].set_bounds(0, 120)
        ia.axhline(0, color='#A7B4BC', lw=0.55, zorder=1)
        for i, (name, value, color) in enumerate(zip(['Soft', 'Mixed', 'Hard'], vals, STATE_COLORS)):
            ia.plot([i, i], [0, value], color=color, lw=1.15, zorder=2)
            ia.scatter(i, value, s=18, color=color, edgecolors='white', linewidths=0.45, zorder=3)
            label_y = 15 if i == 0 else value - 5 if i == 2 else value + 12
            ia.text(i - 0.05 if i == 2 else i, label_y, f'{value:+.2f}'.replace('-', '−'), fontsize=7.1, ha='right' if i == 2 else 'center', va='top' if i == 2 else 'bottom', color=color)
            x = (i + 0.45) / 2.9
            if i == 0:
                forest_icon(ia, x, -0.04, 0.33)
            elif i == 1:
                forest_icon(ia, x - 0.025, -0.04, 0.25)
                city_icon(ia, x + 0.018, -0.04, 0.24)
            else:
                city_icon(ia, x, -0.04, 0.33)
            ia.text(x, -0.2, name, fontsize=7, ha='center', va='center', transform=ia.transAxes)
        title = 'Relative change (%)'
    elif letter == 'b':
        rows = evidence['country']
        n_up = int(rows.delta_hard_share_pp.gt(0).sum())
        n_down = int(rows.delta_hard_share_pp.lt(0).sum())
        ia.set(xlim=(0, 1), ylim=(0, 1), xticks=[], yticks=[])
        for i in range(19):
            row, col = divmod(i, 5)
            location_tile(ia, 0.015 + col * 0.081, 0.69 - row * 0.205, 0.064, 0.16, STATE_COLORS[2] if i < n_up else STATE_COLORS[0])
        for yy, n, direction, color in [(0.68, n_up, '↑', STATE_COLORS[2]), (0.27, n_down, '↓', STATE_COLORS[0])]:
            ia.text(0.58, yy, f'{direction} {n}', fontsize=11, weight='bold', va='center', color=color, transform=ia.transAxes)
        title = 'Hard-share direction'
    elif letter == 'c':
        rows = evidence['concentration'].query('top_k == 5').sort_values('year')
        vals = rows.share_of_hard_area_percent.to_numpy()
        wmm, hmm = (STAT_INSET_BOUNDS[2] * 162 / 282, STAT_INSET_BOUNDS[3] * 162 / 282)
        ia.set(xlim=(0, wmm), ylim=(0, hmm), xticks=[], yticks=[])
        for xx, year, value, color in zip([5.6, wmm - 5.6], [2000, 2023], vals, [STATE_COLORS[0], STATE_COLORS[2]]):
            centre = (xx, 5.25)
            radius = 5.1
            thick = 0.85
            ia.add_patch(Wedge(centre, radius, 0, 360, width=thick, fc='#DCE5E7', ec='none'))
            ia.add_patch(Wedge(centre, radius, 90 - value / 100 * 360, 90, width=thick, fc=color, ec=OCEAN, lw=0.35))
            ia.text(xx, 5.25, f'{value:.2f}%', fontsize=7.0, ha='center', va='center', color=color, weight='bold')
            ia.text(xx, -1.5, str(year), fontsize=7.0, ha='center', va='center')
        title = 'Top 5 share'
    else:
        rows = evidence['robustness']
        vals = rows.delta_hard_share_pp.to_numpy()
        ia.set(xlim=(-1.1, 1.8), ylim=(-0.7, 2.55), xticks=[0, 0.75, 1.5], yticks=[])
        ia.spines['bottom'].set_visible(True)
        ia.spines['bottom'].set_color('#8A979E')
        ia.spines['bottom'].set_linewidth(0.4)
        ia.spines['bottom'].set_bounds(0, 1.5)
        for yy, name, row in zip([1.8, 0.8, -0.2], ['Mapped', 'Pooled', 'By year'], rows.itertuples()):
            before, after = (row.hard_share_2000_percent, row.hard_share_2023_percent)
            ia.plot([before, after], [yy, yy], color='#7F8F99', lw=0.85, zorder=1)
            ia.scatter(before, yy, s=18, facecolors=OCEAN, edgecolors=STATE_COLORS[0], linewidths=0.7, zorder=3)
            ia.scatter(after, yy, s=18, facecolors=STATE_COLORS[2], edgecolors='white', linewidths=0.35, zorder=4)
            ia.text(-1.06, yy, name, fontsize=7.0, va='center')
        ia.scatter(0.025, 1.05, s=13, facecolors=OCEAN, edgecolors=STATE_COLORS[0], linewidths=0.65, transform=ia.transAxes, clip_on=False)
        ia.text(0.068, 1.05, '2000', fontsize=7, va='center', transform=ia.transAxes)
        ia.scatter(0.32, 1.05, s=13, facecolors=STATE_COLORS[2], edgecolors='white', linewidths=0.3, transform=ia.transAxes, clip_on=False)
        ia.text(0.36, 1.05, '2023', fontsize=7, va='center', transform=ia.transAxes)
        title = 'Hard share (%)'
    title_x = -8 / STAT_INSET_BOUNDS[2] if letter in ['a', 'b'] else 0
    title_y = 1.2 if letter == 'd' else 1.0 - 0.4 / (STAT_INSET_BOUNDS[3] * 162 / 282)
    ia.text(title_x, title_y, title, ha='left', va='bottom', transform=ia.transAxes, fontsize=7.2)
    if subtitle:
        ia.text(0, 1.07, subtitle, ha='left', va='bottom', transform=ia.transAxes, fontsize=7.0, color=SECONDARY)

def color_key(fig, bounds, colors, y, kind):
    x0, width, height = (39.0, 134.0, 2.5)
    n = len(colors)
    for i, col in enumerate(colors):
        fig.add_artist(Rectangle(((x0 + width * i / n) / W, y / H), width / n / W, height / H, fc=col, ec='white', lw=0.35, transform=fig.transFigure))
    for i, value in enumerate(bounds):
        xx = x0 + width * i / n
        label = f'{value:g}'.replace('-', '−')
        tick = fig.text(xx / W, (y - 1.5) / H, label, ha='center', va='top', fontsize=7.2)
    if kind == 'MEHI':
        fig.text(11 / W, (y + 0.55) / H, 'Mean MEHI', fontsize=8, va='center')
    else:
        fig.text(11 / W, (y + 2.0) / H, 'Hard-edge', fontsize=7.4, va='center')
        fig.text(11 / W, (y - 1.0) / H, 'area (%)', fontsize=7.4, va='center')
        fig.text(40 / W, 3.5 / H, '○  Zero hard-edge area', color=SECONDARY, fontsize=7)
        fig.text(173 / W, 3.5 / H, 'Main maps: 0.5° bin centres', color=SECONDARY, fontsize=7, ha='right')

def interval_tables(frame, column, bounds, colors, kind):
    result = []
    for year, group in frame.groupby('year', sort=False):
        values = group[column].to_numpy()
        for i, color in enumerate(colors):
            mask = (values >= bounds[i]) & (values < bounds[i + 1] if i < len(colors) - 1 else values <= bounds[i + 1])
            if kind == 'hard':
                mask &= values > 0
            weights = group['area_weight'] if 'area_weight' in group else group['area_weight_sum_m2']
            result.append({'variable': kind, 'year': int(year), 'lower': bounds[i], 'upper': bounds[i + 1], 'left_inclusive': kind != 'hard' or i > 0, 'upper_inclusive': i == len(colors) - 1, 'hex_color': color, 'support_count': int(mask.sum()), 'support_kind': '150m neighbourhood' if column == 'MEHI' else '0.5 degree bin', 'area_weight_m2': float(weights.to_numpy()[mask].sum())})
        if kind == 'hard':
            mask = values == 0
            result.append({'variable': kind, 'year': int(year), 'lower': 0, 'upper': 0, 'left_inclusive': True, 'upper_inclusive': True, 'hex_color': 'hollow', 'support_count': int(mask.sum()), 'support_kind': '0.5 degree bin', 'area_weight_m2': float(group.loc[mask, 'area_weight_sum_m2'].sum())})
    return result

def verify(maps, bins, hist):
    assert len(maps) == 233008 and len(bins) == 214
    assert not maps[['MEHI', 'lon', 'lat', 'area_weight']].isna().any().any()
    assert maps.MEHI.between(-1, 1).all() and maps.area_weight.ge(0).all()
    assert maps.lon.between(EXTENT[0], EXTENT[1]).all() and maps.lat.between(EXTENT[2], EXTENT[3]).all()
    for year, group in maps.groupby('year', sort=False):
        b = bins[bins.year.eq(year)]
        s = hist[hist.year.eq(year)]
        assert len(group) == s.grid_count.sum() == b.n_grid.sum()
        assert np.isclose(group.area_weight.sum(), b.area_weight_sum_m2.sum(), rtol=1e-14)
        hard_area = group.loc[group.MEHI.gt(0.33), 'area_weight'].sum()
        assert np.isclose(hard_area, b.hard_area_m2.sum(), rtol=1e-14)
        fallback = group.area_weight.mask(group.area_weight.eq(0), 1).to_numpy()
        recalculated, _ = np.histogram(group.MEHI, np.r_[s.MEHI_bin_left.to_numpy(), s.MEHI_bin_right.iloc[-1]], weights=fallback)
        assert np.allclose(recalculated, s.area_weight_sum, rtol=1e-10, atol=1e-05)
        assert np.allclose(b.hard_area_share_percent, 100 * b.hard_area_m2 / b.area_weight_sum_m2, atol=1e-12, rtol=0)
        derived = group.assign(bin_ix=np.floor(group.lon / 0.5).astype(int), bin_iy=np.floor(group.lat / 0.5).astype(int), mehi_area=group.MEHI * group.area_weight).groupby(['bin_ix', 'bin_iy']).agg(area=('area_weight', 'sum'), mehi_area=('mehi_area', 'sum')).reset_index()
        checked = b.merge(derived, on=['bin_ix', 'bin_iy'], validate='one_to_one')
        assert len(checked) == len(b)
        assert np.allclose(checked.mean_MEHI, checked.mehi_area / checked.area, rtol=0, atol=2e-14)
        assert b.mean_MEHI.between(MEHI_BOUNDS[0], MEHI_BOUNDS[-1]).all()
        overlap = group.lon.between(49, 106) & group.lat.between(-40, -3)
        assert overlap.sum() == 0, 'Move inset to keep every mapped observation visible'

def raw_area_histograms(maps, archived):
    tables = []
    for year, group in maps.groupby('year', sort=False):
        h = archived[archived.year.eq(year)].copy()
        edges = np.r_[h.MEHI_bin_left.to_numpy(), h.MEHI_bin_right.iloc[-1]]
        raw, _ = np.histogram(group.MEHI, bins=edges, weights=group.area_weight)
        counts, _ = np.histogram(group.MEHI, bins=edges)
        assert np.array_equal(counts, h.grid_count)
        assert np.isclose(raw.sum(), group.area_weight.sum(), rtol=1e-13)
        old_percent = h.area_weight_sum.to_numpy() / h.area_weight_sum.sum() * 100
        raw_percent = raw / raw.sum() * 100
        assert raw_percent.max() < 15
        h['archived_area_weight_sum'] = h.area_weight_sum
        h['area_weight_sum'] = raw
        h['raw_minus_archived_percent'] = raw_percent - old_percent
        tables.append(h)
    return pd.concat(tables, ignore_index=True)

def annual_claim_series(annual, archived):
    records = []
    assert len(annual) == 474003
    assert annual.MEHI.between(-1, 1).all() and annual.area_weight.ge(0).all()
    for year, d in annual.groupby('year', sort=True):
        accepted = archived[archived.year.eq(year)].iloc[0]
        assert len(d) == accepted.n_grid
        area = d.area_weight.sum()
        mean = float(np.average(d.MEHI, weights=d.area_weight))
        hard = float(d.loc[d.MEHI.gt(0.33), 'area_weight'].sum() / area * 100)
        fallback = d.area_weight.mask(d.area_weight.eq(0), 1)
        old_mean = float(np.average(d.MEHI, weights=fallback))
        old_hard = float(np.average(d.MEHI.gt(0.33), weights=fallback) * 100)
        assert np.isclose(old_mean, accepted.area_weighted_MEHI_mean, rtol=0, atol=2e-14)
        assert np.isclose(old_hard, accepted.hard_urban_edge_area_share_percent, rtol=0, atol=2e-13)
        assert f'{mean:.3f}' == f'{accepted.area_weighted_MEHI_mean:.3f}'
        assert f'{hard:.2f}' == f'{accepted.hard_urban_edge_area_share_percent:.2f}'
        records.append({'year': int(year), 'n_grid': len(d), 'n_zero_area': int(d.area_weight.eq(0).sum()), 'area_weight_sum_m2': float(area), 'area_weighted_MEHI_mean': mean, 'hard_area_share_percent': hard, 'archived_area_weighted_MEHI_mean': float(accepted.area_weighted_MEHI_mean), 'archived_hard_area_share_percent': float(accepted.hard_urban_edge_area_share_percent), 'raw_minus_archived_mean': mean - float(accepted.area_weighted_MEHI_mean), 'raw_minus_archived_hard_share_pp': hard - float(accepted.hard_urban_edge_area_share_percent)})
    series = pd.DataFrame(records)
    assert series.area_weighted_MEHI_mean.lt(-0.33).all()
    series.to_csv(SOURCE / 'Fig1_annual_hard_share_and_mean_MEHI.csv', index=False)
    return series

def derive_inset_evidence(annual, bins, error_table, series):
    endpoints = annual[annual.year.isin([2000, 2023])].copy()
    relative = []
    for state, mask in [('soft', endpoints.MEHI.lt(-0.33)), ('mixed', endpoints.MEHI.between(-0.33, 0.33)), ('hard', endpoints.MEHI.gt(0.33))]:
        totals = endpoints.groupby('year').area_weight.sum()
        areas = endpoints[mask].groupby('year').area_weight.sum()
        shares = areas / totals * 100
        relative.append({'state': state, 'area_2000_m2': float(areas[2000]), 'area_2023_m2': float(areas[2023]), 'annual_total_area_2000_m2': float(totals[2000]), 'annual_total_area_2023_m2': float(totals[2023]), 'share_2000_percent': float(shares[2000]), 'share_2023_percent': float(shares[2023]), 'share_ratio_2023_to_2000': float(shares[2023] / shares[2000]), 'relative_share_change_percent': float(100 * (shares[2023] / shares[2000] - 1))})
    relative = pd.DataFrame(relative)
    assert np.allclose(relative[['share_2000_percent', 'share_2023_percent']].sum(), 100)
    relative.to_csv(SOURCE / 'Fig1_class_share_relative_change.csv', index=False)
    endpoints['hard_area_m2'] = endpoints.area_weight * endpoints.MEHI.gt(0.33)
    country = endpoints.groupby(['GU_A3', 'year']).agg(n_grid=('MEHI', 'size'), area_weight_m2=('area_weight', 'sum'), hard_area_m2=('hard_area_m2', 'sum')).reset_index()
    country['hard_area_share_percent'] = country.hard_area_m2 / country.area_weight_m2 * 100
    wide = country.pivot(index='GU_A3', columns='year', values='hard_area_share_percent')
    wide.columns = ['share_2000_percent', 'share_2023_percent']
    wide['delta_hard_share_pp'] = wide.share_2023_percent - wide.share_2000_percent
    wide['direction'] = np.sign(wide.delta_hard_share_pp).astype(int)
    wide = wide.reset_index()
    assert len(wide) == 19 and wide.delta_hard_share_pp.gt(0).sum() == 12 and (wide.delta_hard_share_pp.lt(0).sum() == 7)
    country.to_csv(SOURCE / 'Fig1_country_hard_share_annual_support.csv', index=False)
    wide.to_csv(SOURCE / 'Fig1_country_hard_share_direction.csv', index=False)
    ranked, summaries = ([], [])
    for year, group in bins.groupby('year', sort=True):
        order = group.sort_values('hard_area_m2', ascending=False, kind='stable').copy()
        order['rank_by_hard_area'] = np.arange(1, len(order) + 1)
        order['annual_hard_area_m2'] = order.hard_area_m2.sum()
        order['annual_mangrove_area_m2'] = order.area_weight_sum_m2.sum()
        order['hard_area_contribution_percent'] = order.hard_area_m2 / order.hard_area_m2.sum() * 100
        order['mangrove_area_contribution_percent'] = order.area_weight_sum_m2 / order.area_weight_sum_m2.sum() * 100
        order['cumulative_hard_area_percent'] = order.hard_area_contribution_percent.cumsum()
        order['top5'] = order.rank_by_hard_area.le(5)
        ranked.append(order)
        for top_k in [5, 10, 20]:
            part = order.iloc[:top_k]
            summaries.append({'year': int(year), 'top_k': top_k, 'n_observed_bins': len(order), 'share_of_hard_area_percent': float(part.hard_area_contribution_percent.sum()), 'share_of_mangrove_area_percent': float(part.mangrove_area_contribution_percent.sum()), 'hard_area_m2': float(part.hard_area_m2.sum()), 'mangrove_area_m2': float(part.area_weight_sum_m2.sum())})
    concentration = pd.DataFrame(summaries)
    pd.concat(ranked).to_csv(SOURCE / 'Fig1_ranked_hard_area_bins.csv', index=False)
    concentration.to_csv(SOURCE / 'Fig1_spatial_concentration_summaries.csv', index=False)
    robust = []
    for scenario in ['observed', 'pooled_composition', 'year_specific_composition']:
        rows = error_table[error_table.scenario.eq(scenario)].set_index('year')
        for year in [2000, 2023]:
            s = series[series.year.eq(year)].iloc[0]
            assert int(rows.loc[year, 'grid_count']) == int(s.n_grid)
            assert np.isclose(rows.loc[year, 'observed_mangrove_weight_m2'], s.area_weight_sum_m2, rtol=1e-13)
        robust.append({'scenario': scenario, 'hard_share_2000_percent': float(rows.loc[2000, 'hard_edge_share_percent']), 'hard_share_2023_percent': float(rows.loc[2023, 'hard_edge_share_percent']), 'delta_hard_share_pp': float(rows.loc[2023, 'hard_edge_share_percent'] - rows.loc[2000, 'hard_edge_share_percent']), 'scope': str(rows.loc[2000, 'scope'])})
    robustness = pd.DataFrame(robust)
    assert robustness.delta_hard_share_pp.gt(0).all()
    robustness.to_csv(SOURCE / 'Fig1_classification_error_share_increase.csv', index=False)
    return {'relative': relative, 'country': wide, 'concentration': concentration, 'robustness': robustness}

def supplementary_distributions(histogram, series, cmap, norm):
    width, height = (167.0, 170.0)
    fig = plt.figure(figsize=(width / 25.4, height / 25.4), dpi=300)
    fig.text(23 / width, 166 / height, 'Annual MEHI distributions', fontsize=10, weight='bold')
    source_tables = []
    for idx, (year, y) in enumerate(zip([2000, 2010, 2020, 2023], [127, 91, 55, 19])):
        ax = fig.add_axes([23 / width, y / height, 136 / width, 28 / height])
        h = histogram[histogram.year.eq(year)].copy()
        s = series[series.year.eq(year)].iloc[0]
        h['area_share_percent'] = h.area_weight_sum / h.area_weight_sum.sum() * 100
        assert h.grid_count.sum() == s.n_grid
        assert np.isclose(h.area_share_percent.sum(), 100)
        for left, right, fill in [(-1, -0.33, '#F2F6F8'), (-0.33, 0.33, '#F7F4EE'), (0.33, 1, '#FAF1F1')]:
            ax.axvspan(left, right, color=fill, lw=0, zorder=0)
        ax.bar(h.MEHI_bin_left, h.area_share_percent, width=0.025, align='edge', color=cmap(norm(h.MEHI_bin_mid)), edgecolor='none', zorder=2)
        for threshold in [-0.33, 0.33]:
            ax.axvline(threshold, lw=0.55, color='#A8B4BA', zorder=3)
        ax.plot([s.area_weighted_MEHI_mean] * 2, [0, 12.8], lw=0.8, color=INK, ls=(0, (2, 1)), zorder=4)
        ax.text(0.37, 10.7, f'Mean {s.area_weighted_MEHI_mean:.3f}'.replace('-', '−'), fontsize=8.5)
        ax.set(xlim=(-1, 1), ylim=(0, 15), xticks=[-1, -0.5, 0, 0.5, 1], yticks=[0, 5, 10, 15])
        if idx < 3:
            ax.set_xticklabels([])
        else:
            ax.set_xlabel('MEHI', fontsize=9, labelpad=3)
        ax.tick_params(length=2, width=0.5, pad=2, labelsize=8)
        ax.grid(axis='y', color='#DCE4E8', lw=0.35, zorder=1)
        ax.set_axisbelow(True)
        for side in ['top', 'right']:
            ax.spines[side].set_visible(False)
        for side in ['bottom', 'left']:
            ax.spines[side].set_color('#8C9AA2')
            ax.spines[side].set_linewidth(0.5)
        fig.text(17 / width, (y + 30.8) / height, chr(97 + idx), fontsize=10, weight='bold')
        fig.text(23 / width, (y + 30.8) / height, str(year), fontsize=9, weight='bold')
        fig.text(159 / width, (y + 30.8) / height, f'n = {int(s.n_grid):,}', ha='right', fontsize=8.5)
        if idx == 0:
            for x, name in [(-0.665, 'Soft-buffered'), (0, 'Mixed'), (0.665, 'Hard urban')]:
                ax.text(x, 13.9, name, ha='center', va='center', fontsize=8.3, color=SECONDARY)
        source_tables.append(h)
    fig.text(5 / width, 87 / height, 'Mangrove area per 0.025 MEHI bin (%)', fontsize=9, rotation=90, ha='center', va='center')
    fig.text(159 / width, 3.0 / height, 'Common axes · raw mangrove-area weights · dashed line: annual mean', fontsize=8, ha='right', color=SECONDARY)
    name = 'Supp_Fig_annual_MEHI_distributions'
    for extension, dpi in [('.pdf', 600), ('.svg', 600), ('.png', 350)]:
        fig.savefig(OUT / (name + extension), dpi=dpi)
    plt.close(fig)
    pd.concat(source_tables).to_csv(SOURCE / (name + '.csv'), index=False)

def save(fig):
    name = 'Fig1_MEHI_state'
    fig.canvas.draw()
    for extension, dpi in [('.pdf', 600), ('.svg', 600), ('.png', 350)]:
        fig.savefig(OUT / (name + extension), dpi=dpi)
    plt.close(fig)
    print('Exported', name, flush=True)

def main():
    global DATA, OUT, SOURCE, BINS, LAND_GEOMETRY
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=DATA)
    parser.add_argument('--out', type=Path, default=OUT)
    parser.add_argument('--sources', type=Path, default=SOURCE)
    parser.add_argument('--bins', type=Path, default=BINS)
    args = parser.parse_args()
    DATA, OUT, SOURCE, BINS = [p.resolve() for p in [args.data, args.out, args.sources, args.bins]]
    for directory in [OUT, SOURCE]:
        directory.mkdir(parents=True, exist_ok=True)
    maps = read('figure_source/Fig1_edge_state_maps_2000_2023.csv.gz')
    hist = read('figure_source/Fig1_annual_MEHI_histogram.csv')
    archived_summary = read('figure_source/Fig1_annual_MEHI_summary.csv')
    error_table = read('analysis/annual_error_sensitivity.csv')
    annual = read('analysis/classification_sensitivity_inputs_150m.csv.gz').rename(columns={'YEAR': 'year', 'A_M_M2': 'area_weight'})
    bins = pd.read_csv(BINS, float_precision='round_trip')
    land_path = DATA / 'cartography/ne_50m_land.geojson'
    land = json.loads(land_path.read_text(encoding='utf8'))
    ocean_region = geo_box(30, -40, 120, 20)
    LAND_GEOMETRY = unary_union([geo_shape(f['geometry']).intersection(ocean_region) for f in land['features']])
    verify(maps, bins, hist)
    hist = raw_area_histograms(annual, hist)
    series = annual_claim_series(annual, archived_summary)
    evidence = derive_inset_evidence(annual, bins, error_table, series)
    raw_cm = ListedColormap(RAW_MEHI_COLORS)
    raw_norm = BoundaryNorm(RAW_MEHI_BOUNDS, len(RAW_MEHI_COLORS))
    supplementary_distributions(hist, series, raw_cm, raw_norm)
    fig = plt.figure(figsize=(W / 25.4, H / 25.4), dpi=300)
    for letter, year, kind, y, title_y in [('a', 2000, 'MEHI', 187, 233.5), ('b', 2023, 'MEHI', 137, 183.5), ('c', 2000, 'hard', 74, 120.5), ('d', 2023, 'hard', 24, 70.5)]:
        ax = axes(fig, 11, y, 162, 162 * (EXTENT[3] - EXTENT[2]) / (EXTENT[1] - EXTENT[0]))
        base_map(ax, land, letter in ['b', 'd'])
        b = bins[bins.year.eq(year)]
        plot_bins(ax, b, kind)
        geographic_inset(ax, land, b, maps[maps.year.eq(year)], kind, letter)
        evidence_inset(ax, letter, evidence)
        fig.text(5 / W, title_y / H, letter, fontsize=10.5, weight='bold', va='baseline')
        fig.text(11 / W, title_y / H, ('Area-weighted mean MEHI' if kind == 'MEHI' else 'Hard-edge area share') + f' · {year}', fontsize=9, va='baseline')
    color_key(fig, MEHI_BOUNDS, MEHI_COLORS, 128, 'MEHI')
    color_key(fig, HARD_BOUNDS, HARD_COLORS, 14.4, 'hard')
    clean_columns = ['year', 'location_code', 'GRID_ID', 'GRID_UID', 'lon', 'lat', 'MEHI', 'MEHI_class', 'area_weight']
    maps[clean_columns].to_csv(SOURCE / 'Fig1_MEHI_map_points.csv.gz', index=False, compression={'method': 'gzip', 'mtime': 0})
    zoom_columns = ['year', 'location_code', 'GRID_ID', 'GRID_UID', 'lon', 'lat', 'bin_ix', 'bin_iy', 'MEHI', 'area_weight', 'mean_MEHI', 'hard_area_share_percent']
    pd.concat([selected[zoom_columns] for letter, _, _, _, selected in GEOGRAPHIC_INSETS if letter in ['a', 'b']]).to_csv(SOURCE / 'Fig1_Florida_zoom_raw_points.csv.gz', index=False, compression={'method': 'gzip', 'mtime': 0})
    palette_rows = interval_tables(bins, 'mean_MEHI', MEHI_BOUNDS, MEHI_COLORS, 'mean_MEHI')
    palette_rows += interval_tables(bins, 'hard_area_share_percent', HARD_BOUNDS, HARD_COLORS, 'hard')
    palette_table = pd.DataFrame(palette_rows)
    for year in [2000, 2023]:
        for variable, table, weight_field in [('mean_MEHI', bins, 'area_weight_sum_m2'), ('hard', bins, 'area_weight_sum_m2')]:
            support = palette_table[palette_table.year.eq(year) & palette_table.variable.eq(variable)]
            source = table[table.year.eq(year)]
            assert support.support_count.sum() == len(source)
            assert np.isclose(support.area_weight_m2.sum(), source[weight_field].sum(), rtol=1e-13)
    palette_table.to_csv(SOURCE / 'Fig1_color_boundaries_and_support.csv', index=False)
    pd.DataFrame(interval_tables(annual, 'MEHI', RAW_MEHI_BOUNDS, RAW_MEHI_COLORS, 'raw_MEHI')).to_csv(SOURCE / 'Supp_Fig_MEHI_color_boundaries_and_support.csv', index=False)
    save(fig)
if __name__ == '__main__':
    main()
