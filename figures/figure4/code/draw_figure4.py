from __future__ import annotations
import argparse
import shutil
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from matplotlib.offsetbox import AnnotationBbox, DrawingArea
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Rectangle
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
HERE = Path(__file__).resolve().parents[1]
INK = '#233545'
SOFT = '#497B9F'
HARD = '#BD5A62'
GRID = '#E9ECEC'
ROUTES = ['proximity_only_route', 'vegetation_buffer_loss_route', 'mixed_route', 'water_edge_narrowing_route', 'built_up_replacement_route', 'tidal_flat_loss_route']
ROUTE_COLORS = ['#817595', '#669C89', '#C1C0BC', '#5785A4', '#C17170', '#C7A665']
ROUTE_LABELS = ['Proximity only', 'Vegetation loss', 'Mixed routes', 'Water narrowing', 'Built replacement', 'Tidal-flat loss']
ROUTE_ICONS = ['distance', 'leaf', 'mixed', 'water', 'built', 'tidal']
SOURCE_FILES = ['Fig4_transition_matrix.csv', 'Fig4_global_route_shares.csv', 'Fig4_country_route_shares.csv', 'Fig4_country_association.csv']
COUNTRY_ORDER = ['USA', 'MYS', 'NGA', 'AUS', 'BRA', 'THA', 'IDN', 'NZL', 'GIN', 'COL', 'PAK', 'CHN', 'PHL', 'MEX', 'IND', 'MOZ', 'SGP', 'BHR', 'GHA']
plt.rcParams.update({'font.family': ['Arial', 'DejaVu Sans'], 'font.size': 8, 'axes.labelsize': 8, 'axes.titlesize': 8.5, 'xtick.labelsize': 7.3, 'ytick.labelsize': 7.3, 'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none', 'axes.linewidth': 0.55, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.unicode_minus': True, 'text.color': INK, 'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK, 'savefig.facecolor': 'white', 'legend.frameon': False, 'svg.hashsalt': 'MEHI-Figures23'})

def read_source(name):
    path = DATA / 'figure_source' / name
    target = SOURCE / name
    shutil.copyfile(path, target)
    return pd.read_csv(path, float_precision='round_trip')

def canvas(w, h):
    f = plt.figure(figsize=(w / 25.4, h / 25.4), dpi=160)
    f._mm = (w, h)
    return f

def axmm(f, x, y, w, h):
    fw, fh = f._mm
    return f.add_axes([x / fw, y / fh, w / fw, h / fh])

def txt(f, x, y, value, **kw):
    w, h = f._mm
    return f.text(x / w, y / h, value, **kw)

def title(f, x, y, letter, value):
    txt(f, x, y, letter, fontsize=10, weight='bold')
    txt(f, x + 5, y, value, fontsize=8.6)

def clean(ax, axis='x'):
    ax.tick_params(length=2.4, width=0.55, pad=2)
    ax.grid(axis=axis, color=GRID, lw=0.5)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color('#8E999F')

def icon(kind, color=INK, size=15):
    d = DrawingArea(size, size, 0, 0)
    lw = 0.85
    s = size / 24

    def line(x, y, c=color, w=lw):
        d.add_artist(Line2D(np.asarray(x) * s, np.asarray(y) * s, c=c, lw=w, solid_capstyle='round'))

    def rect(x, y, w, h, fc='none'):
        d.add_artist(Rectangle((x * s, y * s), w * s, h * s, ec=color, fc=fc, lw=lw))

    def tree(x=7, y=6):
        line([x, x], [y, y + 9])
        line([x - 3, x, x + 3], [y - 1, y + 1, y - 1])
        for dx, dy, r in [(-2, 9, 3), (2, 10, 3), (0, 12, 3.2)]:
            d.add_artist(Circle(((x + dx) * s, (y + dy) * s), r * s, fc='white', ec=color, lw=lw))

    def building(x=15, y=5):
        rect(x, y, 6, 12)
        for dx in [2, 4]:
            for dy in [3, 7]:
                line([x + dx, x + dx], [y + dy, y + dy + 1])
    if kind in ['distance', 'contact']:
        tree(5, 5)
        building(17, 4)
        if kind == 'distance':
            d.add_artist(FancyArrowPatch((9 * s, 7 * s), (17 * s, 7 * s), arrowstyle='<->', mutation_scale=4, lw=lw, color=color))
        else:
            line([10, 17], [10, 10], w=2.4)
            line([13.5, 13.5], [7.5, 12.5])
    elif kind == 'built':
        building(3, 4)
        building(13, 4)
        line([1, 22], [3, 3])
    elif kind == 'leaf':
        d.add_artist(Ellipse((12 * s, 13 * s), 14 * s, 9 * s, angle=40, fc='white', ec=color, lw=lw))
        line([4, 17], [4, 18])
        line([9, 8], [10, 14])
        line([12, 16], [13, 13])
    elif kind == 'water':
        for y in [6, 11, 16]:
            x = np.linspace(2, 22, 50)
            line(x, y + 1.3 * np.sin((x - 2) * np.pi / 7))
    elif kind == 'tidal':
        for y in [5, 10, 15]:
            line([2, 7, 11, 16, 22], [y, y, y + 1, y + 1, y])
        for x, y in [(5, 19), (12, 19), (18, 20)]:
            d.add_artist(Circle((x * s, y * s), 0.6 * s, fc=color, ec='none'))
    elif kind == 'mixed':
        for x, y in [(4, 4), (14, 4), (4, 14), (14, 14)]:
            rect(x, y, 6, 6, fc='white')
    return d

def place_icon(ax, kind, xy, color=INK, size=15):
    obj = AnnotationBbox(icon(kind, color, size), xy, xycoords='axes fraction', frameon=False, pad=0, box_alignment=(0.5, 0.5))
    ax.add_artist(obj)
    return obj

def export(f, name):
    f.canvas.draw()
    for ext in ['pdf', 'svg', 'png']:
        f.savefig(OUT / f'{name}.{ext}', dpi=400)
    plt.close(f)
    print('Exported', name, flush=True)

def draw():
    transition = read_source(SOURCE_FILES[0])
    routes = read_source(SOURCE_FILES[1]).set_index('route')
    country = read_source(SOURCE_FILES[2])
    assoc = read_source(SOURCE_FILES[3])
    mat = transition.pivot(index='from_code', columns='to_code', values='share_of_all_transition_percent').reindex(index=range(1, 7), columns=range(1, 7))
    assert mat.shape == (6, 6) and np.isclose(mat.values.sum(), 100)
    assert len(assoc) == 19 and set(assoc.GU_A3) == set(COUNTRY_ORDER)
    f = canvas(174, 149)
    title(f, 4, 143, 'a', 'Endpoint land-cover transitions')
    a = axmm(f, 27, 94, 42, 42)
    cm = LinearSegmentedColormap.from_list('sand_copper', ['#FAF6EC', '#F2DFB7', '#D9A570', '#AB6952', '#794544'])
    im = a.imshow(mat, cmap=cm, vmin=0, vmax=32, aspect='equal', interpolation='nearest')
    for i in range(6):
        for j in range(6):
            v = mat.iloc[i, j]
            label = '<0.1' if 0 < v < 0.1 else f'{v:.1f}'
            a.text(j, i, label, ha='center', va='center', fontsize=7.2, color='white' if v > 19 else INK)
    a.set_xticks(range(6), ['Mang.', 'Flat', 'Veg.', 'Water', 'Built', 'Other'])
    a.set_yticks(range(6), ['Mangrove', 'Tidal flat', 'Other vegetation', 'Water', 'Built-up', 'Other'])
    a.tick_params(length=0, pad=3, labelsize=7.1)
    a.set_xlabel('2023 class', labelpad=2)
    a.set_ylabel('2000 class', labelpad=2)
    for spine in a.spines.values():
        spine.set_visible(False)
    for z in np.arange(0.5, 6):
        a.axhline(z, lw=0.35, color='white')
        a.axvline(z, lw=0.35, color='white')
    cb = f.colorbar(im, cax=axmm(f, 73, 94, 2.5, 42))
    cb.set_ticks([0, 10, 20, 30])
    cb.ax.tick_params(labelsize=7, length=2, pad=2)
    cb.set_label('Mapped transition area (%)', fontsize=7.3, labelpad=3)
    title(f, 92, 143, 'b', 'Global positive-change routes')
    b = axmm(f, 126, 94, 43, 42)
    for i, (route, color, label, kind) in enumerate(zip(ROUTES, ROUTE_COLORS, ROUTE_LABELS, ROUTE_ICONS)):
        value = float(routes.loc[route, 'share_of_hardening_weight_percent'])
        b.barh(i, value, height=0.59, color=color, lw=0)
        b.text(value + 1, i, f'{value:.1f}', va='center', fontsize=7.4)
        y = 94 + 42 * (5.65 - i) / 6.3
        txt(f, 103, y, label, va='center', fontsize=7.3)
        place_icon(b, kind, ((97.5 - 126) / 43, (5.65 - i) / 6.3), color, 15)
    b.set(xlim=(0, 66), ylim=(5.65, -0.65), xticks=[0, 20, 40, 60], yticks=[])
    b.set_xlabel('Mangrove-area weight (%)', labelpad=2)
    b.spines['left'].set_visible(False)
    clean(b)
    title(f, 4, 80, 'c', 'Country/location route mixtures')
    table = country.pivot(index='GU_A3', columns='route', values='share_of_country_hardening_weight_percent').reindex(columns=ROUTES).fillna(0)
    table = table.reindex(COUNTRY_ORDER)
    assert table.shape == (19, 6) and np.allclose(table.sum(axis=1), 100)
    for k, (x, codes) in enumerate([(18, COUNTRY_ORDER[:10]), (102, COUNTRY_ORDER[10:])]):
        c = axmm(f, x, 49, 67, 28)
        subset = table.loc[codes]
        left = np.zeros(len(subset))
        for route, color in zip(ROUTES, ROUTE_COLORS):
            c.barh(np.arange(len(subset)), subset[route], left=left, color=color, height=0.7, lw=0)
            left += subset[route].to_numpy()
        c.set(yticks=range(len(subset)), yticklabels=codes, ylim=(9.35, -0.65), xlim=(0, 100), xticks=[0, 50, 100])
        c.tick_params(axis='y', length=0, labelsize=7.0, pad=2.3)
        c.tick_params(axis='x', length=2, pad=2, labelsize=7.0)
        c.spines['left'].set_visible(False)
        c.spines['bottom'].set_color('#9BA6AA')
    txt(f, 90, 42.4, 'Share of country/location hardening weight (%)', fontsize=7.2, ha='center')
    for i, (color, label) in enumerate(zip(ROUTE_COLORS, ROUTE_LABELS)):
        x = [8, 35, 63, 90, 118, 146][i]
        f.add_artist(Rectangle((x / 174, 38.1 / 149), 1.9 / 174, 1.5 / 149, transform=f.transFigure, fc=color, ec='none'))
        txt(f, x + 3, 38.5, label, fontsize=7.0)
    title(f, 4, 34, 'd', 'Soft-cover replacement and edge change')
    d = axmm(f, 18, 8, 151, 23)
    d.axhline(0, c='#AFB8BA', lw=0.55)
    d.axvline(0, c='#AFB8BA', lw=0.55)
    offsets = {'AUS': (3, -9), 'BHR': (2, -11), 'BRA': (-10, -10), 'CHN': (4, 1), 'COL': (-13, 5), 'GHA': (-5, -11), 'GIN': (-18, 2), 'IDN': (-20, 2), 'IND': (-8, -9), 'MEX': (-10, 5), 'MOZ': (-7, 8), 'MYS': (3, 6), 'NGA': (-8, 6), 'NZL': (-8, 5), 'PAK': (-11, -10), 'PHL': (-8, 5), 'SGP': (-10, -10), 'THA': (-7, 6), 'USA': (-12, -10)}
    for row in assoc.itertuples():
        x = row.soft_buffer_to_built_share_changed_area * 100
        y = row.country_weighted_mean_pMEHI
        d.scatter(x, y, s=17, c=HARD if y > 0.005 else SOFT if y < -0.005 else '#97988F', ec='white', lw=0.4, zorder=3)
        d.annotate(row.GU_A3, (x, y), xytext=offsets[row.GU_A3], textcoords='offset points', fontsize=7, arrowprops=dict(arrowstyle='-', color='#A1AAAD', lw=0.3, shrinkB=3), zorder=4)
    rho = float(spearmanr(assoc.soft_buffer_to_built_share_changed_area, assoc.country_weighted_mean_pMEHI).statistic)
    d.set(xlim=(-0.3, 5.65), ylim=(-0.19, 0.23), xticks=[0, 1, 2, 3, 4, 5], yticks=[-0.1, 0, 0.1])
    d.tick_params(labelsize=7, length=2, pad=2)
    d.set_xlabel('Soft cover → built land (% of changed area)', labelpad=2)
    d.set_ylabel('pMEHI', labelpad=3)
    d.text(0.01, 0.98, f'Spearman ρ = {rho:.2f}', transform=d.transAxes, va='top', fontsize=7.2)
    export(f, 'Fig4_soft_buffer_replacement')

def main():
    global DATA, OUT, SOURCE
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=HERE.parents[1] / 'data')
    parser.add_argument('--out', type=Path, default=HERE / 'figures')
    parser.add_argument('--sources', type=Path, default=HERE / 'source_data')
    args = parser.parse_args()
    DATA, OUT, SOURCE = (args.data, args.out, args.sources)
    for folder in [OUT, SOURCE]:
        folder.mkdir(parents=True, exist_ok=True)
    draw()
if __name__ == '__main__':
    main()
