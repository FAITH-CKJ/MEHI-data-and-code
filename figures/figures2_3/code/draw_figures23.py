from __future__ import annotations
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Rectangle, PathPatch, Polygon
from matplotlib.offsetbox import AnnotationBbox, DrawingArea
from matplotlib.colors import LinearSegmentedColormap, Normalize, LogNorm
from matplotlib.path import Path as MplPath
import numpy as np
import pandas as pd
HERE = Path(__file__).resolve().parents[1]
SOFT = '#477D9D'
HARD = '#BD5968'
NEUTRAL = '#C7C3B8'
GREEN = '#518E79'
LOSS = '#B89963'
INK = '#203A49'
MUTED = '#76868D'
GRID = '#E6EBEC'
COMPS = {'P': '#497C9D', 'C': '#B46475', 'B': '#BB9655', 'S': '#4B907F'}
FULL = {'NGA': 'Nigeria', 'MEX': 'Mexico', 'THA': 'Thailand', 'PHL': 'Philippines', 'IDN': 'Indonesia', 'MYS': 'Malaysia', 'NZL': 'New Zealand', 'USA': 'United States', 'COL': 'Colombia', 'PAK': 'Pakistan', 'MOZ': 'Mozambique', 'CHN': 'China', 'AUS': 'Australia', 'BHR': 'Bahrain', 'BRA': 'Brazil', 'GIN': 'Guinea', 'SGP': 'Singapore', 'GHA': 'Ghana', 'IND': 'India', 'GLOBAL': 'All locations'}
plt.rcParams.update({'font.family': ['Arial', 'DejaVu Sans'], 'font.size': 8.0, 'axes.labelsize': 8.0, 'axes.titlesize': 8.5, 'xtick.labelsize': 7.4, 'ytick.labelsize': 7.6, 'text.color': INK, 'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK, 'axes.linewidth': 0.55, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.unicode_minus': True, 'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none', 'svg.hashsalt': 'MEHI-Figures23', 'savefig.facecolor': 'white', 'legend.frameon': False})

def read(rel):
    p = DATA / rel
    return pd.read_csv(p, float_precision='round_trip')

def canvas(w, h):
    f = plt.figure(figsize=(w / 25.4, h / 25.4), dpi=160)
    f._mm = (w, h)
    return f

def axmm(f, x, y, w, h):
    fw, fh = f._mm
    return f.add_axes([x / fw, y / fh, w / fw, h / fh])

def txt(f, x, y, s, **kw):
    w, h = f._mm
    return f.text(x / w, y / h, s, **kw)

def title(f, x, y, letter, s):
    txt(f, x, y, letter, fontsize=10, weight='bold')
    txt(f, x + 5, y, s, fontsize=8.7)

def clean(a, grid=None):
    a.tick_params(length=2.2, width=0.5, pad=2)
    if grid:
        a.grid(axis=grid, color=GRID, lw=0.45)
        a.set_axisbelow(True)
    for s in a.spines.values():
        s.set_color('#9AA7AD')

def icon(kind, color=INK, size=19):
    d = DrawingArea(size, size, 0, 0)
    u = size / 24

    def line(xs, ys, c=color, lw=0.85):
        d.add_artist(Line2D(np.asarray(xs) * u, np.asarray(ys) * u, c=c, lw=lw, solid_capstyle='round'))

    def rect(x, y, w, h, fc='none', ec=color):
        d.add_artist(Rectangle((x * u, y * u), w * u, h * u, ec=ec, fc=fc, lw=0.8))
    if kind in ('area', 'edge'):

        def path(verts, codes, **kw):
            d.add_artist(PathPatch(MplPath(np.asarray(verts) * u, codes), **kw))
        d.add_artist(Rectangle((1.5 * u, 2.4 * u), 21 * u, 18.9 * u, fc='#E4F0F3', ec='none'))
        edge = [(9.7, 20.5), (11.2, 19.5), (12.3, 18.5), (11.9, 17.0), (11.6, 15.7), (10.9, 15.0), (11.6, 13.7), (12.6, 12.5), (14.4, 11.9), (13.7, 10.3), (13.0, 9.0), (12.8, 8.0), (13.6, 6.8), (14.7, 5.4), (15.2, 4.4), (15.5, 3.0)]
        path([(2.0, 3.0), (2.0, 20.5)] + edge + [(2.0, 3.0), (2.0, 3.0)], [MplPath.MOVETO, MplPath.LINETO, MplPath.LINETO] + [MplPath.CURVE4] * 15 + [MplPath.LINETO, MplPath.CLOSEPOLY], fc='#D9EBDE' if kind == 'area' else '#E3EEE5', ec='none')
        path([(2, 3), (2, 5.8), (5.2, 6.6), (8.8, 5.6), (11, 5.1), (11, 3), (2, 3)], [MplPath.MOVETO, MplPath.LINETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4, MplPath.LINETO, MplPath.CLOSEPOLY], fc='#E7DCC7', ec='none')
        if kind == 'edge':
            d.add_artist(Rectangle((16.1 * u, 11.9 * u), 6 * u, 8.6 * u, fc='#F3ECE7', ec='none'))
        path(edge, [MplPath.MOVETO] + [MplPath.CURVE4] * 15, fill=False, ec=color if kind == 'edge' else '#75A387', lw=0.95 if kind == 'edge' else 0.7, capstyle='round', joinstyle='round')
        crown = [(4.7, 14.8), (3.6, 15.6), (3.9, 17.1), (5.0, 17.5), (5.3, 19.1), (7.0, 19.4), (8.1, 18.5), (9.5, 18.7), (10.4, 17.2), (9.6, 16.3), (10.0, 15.2), (9.1, 14.1), (8.2, 14.5), (7.0, 13.6), (5.5, 13.8), (4.7, 14.8), (4.7, 14.8)]
        path(crown, [MplPath.MOVETO] + [MplPath.CURVE4] * 15 + [MplPath.CLOSEPOLY], fc='#AED4B9', ec='#6D9C79', lw=0.58, joinstyle='round')
        path([(7.1, 14.0), (7.1, 11.8), (7.1, 10.8), (7.2, 9.4)], [MplPath.MOVETO] + [MplPath.CURVE4] * 3, fill=False, ec='#5F8E70', lw=0.75, capstyle='round')
        for root in [[(7.2, 9.4), (6.2, 8.6), (5.7, 7.5), (4.8, 6.5)], [(7.2, 9.4), (7.8, 8.1), (8.5, 7.3), (9.4, 6.4)], [(7.2, 9.4), (7.1, 8.0), (6.9, 7.3), (6.9, 6.5)]]:
            path(root, [MplPath.MOVETO] + [MplPath.CURVE4] * 3, fill=False, ec='#5F8E70', lw=0.6, capstyle='round')
        if kind == 'edge':
            for x, y, w, h in [(16.7, 12.0, 2.4, 4.3), (19.35, 12.0, 2.1, 6.2)]:
                d.add_artist(Rectangle((x * u, y * u), w * u, h * u, fc='#EDD2D6', ec='#B96D7A', lw=0.5))
            line([15.6, 21.7], [12.0, 12.0], c='#B96D7A', lw=0.55)
        d.add_artist(Rectangle((1.5 * u, 2.4 * u), 21 * u, 18.9 * u, fill=False, ec='#CCD9D4', lw=0.42))
        return d

    def tree(x=6, y=5):
        line([x, x], [y, y + 8])
        line([x - 3, x, x + 3], [y - 1, y + 1, y - 1])
        for dx, dy, rr in [(-2, 9, 3), (2, 10, 3), (0, 12, 3)]:
            d.add_artist(Circle(((x + dx) * u, (y + dy) * u), rr * u, fc='#EDF4F0', ec=color, lw=0.8))

    def building(x=16, y=4):
        rect(x, y, 6, 12, fc='#F7EEEF')
        for dx in [2, 4]:
            for dy in [3, 7]:
                line([x + dx, x + dx], [y + dy, y + dy + 1])
    if kind in ['distance', 'contact']:
        tree(5, 4)
        building(17, 3)
        if kind == 'distance':
            d.add_artist(FancyArrowPatch((9 * u, 7 * u), (17 * u, 7 * u), arrowstyle='<->', mutation_scale=4, lw=0.8, color=color))
        elif kind == 'contact':
            line([10, 17], [9, 9], lw=2.1)
            line([13.5, 13.5], [6.5, 11.5])
        else:
            line([11, 15], [3, 3])
            line([11, 15], [5, 5])
            line([11, 15], [7, 7])
    elif kind == 'built':
        building(3, 4)
        building(13, 4)
        line([1, 22], [3, 3])
    elif kind == 'leaf':
        d.add_artist(Ellipse((12 * u, 13 * u), 14 * u, 9 * u, angle=40, fc='#EDF5F1', ec=color, lw=0.85))
        line([4, 17], [4, 18])
        line([9, 8], [10, 14])
        line([12, 16], [13, 13])
    return d

def place_icon(a, kind, xy, color=INK, size=19, coords='axes fraction'):
    ab = AnnotationBbox(icon(kind, color, size), xy, xycoords=coords, frameon=False, pad=0, box_alignment=(0.5, 0.5))
    a.add_artist(ab)
    return ab

def out_csv(df, name):
    compression = {'method': 'gzip', 'mtime': 0} if str(name).endswith('.gz') else None
    df.to_csv(SOURCE / name, index=False, float_format='%.17g', compression=compression)

def prepare():
    matched = read('analysis/canonical_matched_support.csv.gz')
    raw = read('figure_source/Fig2_matched_neighbourhoods.csv.gz')
    summary = read('figure_source/Fig2_country_summary.csv')
    paths = read('figure_source/Fig3_area_pMEHI_pathways.csv')
    joint = read('analysis/joint_area_edge_summary.csv')
    cross = read('analysis/joint_area_edge_crosstab.csv')
    annual = read('analysis/classification_sensitivity_inputs_150m.csv.gz')
    expected = read('figure_source/Fig3_global_component_contributions.csv')
    assert len(matched) == len(raw) == 79509 and matched.GU_A3.nunique() == 19
    keys = ['GU_A3', 'GRID_ID']
    assert not matched.duplicated(keys).any()
    assert np.allclose(matched.weight_m2, np.minimum(matched.A_M_2000_m2, matched.A_M_2023_m2), atol=1e-08)
    for code, d in matched.groupby('GU_A3'):
        assert np.allclose(np.sort(d.pMEHI), np.sort(raw.loc[raw.GU_A3.eq(code), 'pMEHI']), atol=1e-14)
    fields = ['P_COMP', 'C_COMP', 'B_COMP', 'S_COMP', 'MEHI']
    for year in [2000, 2023]:
        endpoint = annual.loc[annual.YEAR.eq(year), keys + fields]
        matched = matched.merge(endpoint.rename(columns={c: f'{c}_{year}' for c in fields}), on=keys, how='left', validate='one_to_one')
    assert not matched.isna().any().any()
    assert np.allclose((matched.MEHI_2023 - matched.MEHI_2000) / 2, matched.pMEHI, atol=1e-12)
    con = []
    states = []
    for comp in 'PCBS':
        col = f'{comp}_COMP'
        z = (matched[col + '_2023'] - matched[col + '_2000']) / 8
        matched[comp + '_contribution'] = z
        con.append(dict(component=comp, negative=np.average(np.minimum(z, 0), weights=matched.weight_m2), positive=np.average(np.maximum(z, 0), weights=matched.weight_m2), net=np.average(z, weights=matched.weight_m2)))
    assert np.allclose(matched[[c + '_contribution' for c in 'PCBS']].sum(axis=1), matched.pMEHI, atol=1e-12)
    contributions = pd.DataFrame(con)
    assert np.allclose(contributions.set_index('component').net.reindex(expected.component), expected.value, atol=1e-12)
    for code, d in matched.groupby('GU_A3'):
        for comp in list('PCBS') + ['MEHI']:
            for year in [2000, 2023]:
                col = comp + '_COMP' if len(comp) == 1 else comp
                states.append(dict(GU_A3=code, component=comp, year=year, state=np.average(d[f'{col}_{year}'], weights=d.weight_m2), n=len(d), weight_m2_sum=d.weight_m2.sum()))
    states = pd.DataFrame(states)
    masks = [matched.pMEHI.lt(-0.005), matched.pMEHI.abs().le(0.005), matched.pMEHI.gt(0.005)]
    assert [int(x.sum()) for x in masks] == [35386, 11879, 32244]
    assert int(matched.A_M_2023_m2.ge(matched.A_M_2000_m2).sum()) == 47256
    assert int((matched.A_M_2023_m2.ge(matched.A_M_2000_m2) & masks[2]).sum()) == 17007
    global_row = pd.DataFrame([dict(GU_A3='GLOBAL', country='All locations', common_grid_cells=len(matched), common_neighbourhood_mangrove_area_change_percent=100 * (matched.A_M_2023_m2.sum() / matched.A_M_2000_m2.sum() - 1), pMEHI_aw=np.average(matched.pMEHI, weights=matched.weight_m2), pathway='Global aggregate')])
    comparison = pd.concat([global_row, paths], ignore_index=True).merge(joint.rename(columns={'location_code': 'GU_A3'}), on='GU_A3', validate='one_to_one')
    out_csv(matched, 'Fig23_all_matched_neighbourhoods.csv.gz')
    out_csv(contributions, 'Fig3c_component_gross_and_net.csv')
    out_csv(comparison, 'Fig3ab_country_joint_comparison.csv')
    out_csv(cross, 'Fig3_joint_area_edge_crosstab.csv')
    out_csv(summary, 'Fig2a_country_summary.csv')
    return (matched, summary, comparison, contributions, states)

def export(f, name):
    f.canvas.draw()
    for ext in ['pdf', 'svg', 'png']:
        f.savefig(OUT / f'{name}.{ext}', dpi=450 if ext == 'pdf' else 400)
    plt.close(f)
    print('Exported', name, flush=True)

def figure2(m, summary):
    f = canvas(174, 194)
    title(f, 4, 187, 'a', 'Local edge-change distributions')
    txt(f, 169, 187, '79,509 matched neighbourhoods', ha='right', fontsize=7.8, color=MUTED)
    edges = np.arange(-1.0125, 1.01251, 0.025)
    order = summary.GU_A3.tolist()
    bins = []
    support = []
    rng = np.random.default_rng(10023)
    for j, code in enumerate(order):
        row, col = divmod(j, 4)
        x, y = (11 + col * 40.5, 160 - row * 21.5)
        a = axmm(f, x, y, 34.5, 16.2)
        s = m.loc[m.GU_A3.eq(code), 'pMEHI'].to_numpy()
        r = summary.loc[summary.GU_A3.eq(code)].iloc[0]
        base = np.zeros(len(edges) - 1)
        for lab, mask, color in [('softening', s < -0.005, SOFT), ('near_neutral', np.abs(s) <= 0.005, NEUTRAL), ('hardening', s > 0.005, HARD)]:
            h, _ = np.histogram(s[mask & (s != 0)], bins=edges)
            pct = 100 * h / len(s)
            a.stairs(base + pct, edges, baseline=base, fill=True, color=color, alpha=0.82, lw=0.35)
            for left, right, n, p in zip(edges[:-1], edges[1:], h, pct):
                bins.append(dict(GU_A3=code, direction=lab, bin_left=left, bin_right=right, n_nonzero=int(n), share_all_country_cells_percent=p))
            base += pct
        zz = 100 * np.count_nonzero(s == 0) / len(s)
        a.vlines(0, 0, zz, color='#93897A', lw=1.0, zorder=6)
        a.axvline(0, lw=0.4, color='#B1B7B7', zorder=0)
        a.axhline(0, lw=0.4, color='#BCC5C7', zorder=1)
        a.plot([s.min(), s.max()], [-3.8, -3.8], color='#CBD3D6', lw=0.65, zorder=2)
        a.plot([r.weighted_p25, r.weighted_p75], [-3.8, -3.8], color=INK, lw=1.25, zorder=3)
        a.scatter(r.weighted_median_pMEHI, -3.8, s=8, fc='white', ec=INK, lw=0.6, zorder=4)
        if len(s) < 100:
            cols = np.where(s < -0.005, SOFT, np.where(s > 0.005, HARD, NEUTRAL))
            a.scatter(s, -7 + rng.uniform(-0.5, 0.5, len(s)), s=3.7, c=cols, lw=0, zorder=4)
        a.set(xlim=(-1, 1), ylim=(-8.5, 31), xticks=[-1, 0, 1], yticks=[0, 15, 30])
        a.set_xticklabels(['−1', '0', '1'] if row == 4 else [])
        a.set_yticklabels(['0', '15', '30'] if col == 0 else [])
        a.tick_params(axis='both', length=1.6, width=0.45, pad=1.4, labelsize=7.2)
        if col != 0:
            a.tick_params(axis='y', length=0)
        if row != 4:
            a.tick_params(axis='x', length=0)
        a.spines['left'].set_visible(col == 0)
        a.spines['bottom'].set_visible(False)
        a.spines['left'].set_color('#BEC6C9')
        a.text(0, 1.04, FULL[code] + ('†' if len(s) < 100 else ''), transform=a.transAxes, fontsize=7.8, ha='left', va='bottom', weight='medium')
        a.text(1, 1.045, f'n={len(s):,}', transform=a.transAxes, fontsize=7.2, ha='right', va='bottom', color=MUTED)
        support.append(dict(GU_A3=code, n=len(s), strict_zero_n=int(np.count_nonzero(s == 0)), strict_zero_percent=zz, min=float(s.min()), max=float(s.max())))
    txt(f, 3.0, 125, 'Neighbourhoods per bin (%)', rotation=90, ha='center', va='center', fontsize=7.8)
    txt(f, 79, 64, 'pMEHI (2000–2023)', ha='center', fontsize=8)
    key = axmm(f, 133, 69, 35, 23)
    key.axis('off')
    key.text(0.02, 1.02, 'All locations', fontsize=7.5, color=MUTED, transform=key.transAxes)
    shares = [100 * m.pMEHI.lt(-0.005).mean(), 100 * m.pMEHI.abs().le(0.005).mean(), 100 * m.pMEHI.gt(0.005).mean()]
    for k, (co, lab, pct) in enumerate(zip([SOFT, NEUTRAL, HARD], ['Softening', 'Near-neutral', 'Hardening'], shares)):
        key.add_patch(Rectangle((0.02, 0.8 - k * 0.17), 0.07, 0.07, color=co, transform=key.transAxes, lw=0))
        key.text(0.14, 0.835 - k * 0.17, lab, fontsize=7.3, va='center', transform=key.transAxes)
        key.text(1, 0.835 - k * 0.17, f'{pct:.1f}%', ha='right', fontsize=7.3, va='center', color=co if co != NEUTRAL else '#887F70', transform=key.transAxes)
    key.plot([0.02, 0.12], [0.27, 0.27], c=INK, lw=1.1, transform=key.transAxes)
    key.plot([0.07], [0.27], marker='o', mfc='white', mec=INK, ms=2.6, mew=0.6, transform=key.transAxes)
    key.text(0.18, 0.27, 'Median / IQR', fontsize=7.4, va='center', transform=key.transAxes)
    key.text(0.02, 0.05, '† All cells also shown', fontsize=7.2, color=MUTED, transform=key.transAxes)
    out_csv(pd.DataFrame(bins), 'Fig2a_country_histograms_nonzero.csv')
    out_csv(pd.DataFrame(support), 'Fig2a_country_support.csv')
    s = m.pMEHI.to_numpy()
    neg = np.minimum(s, 0).mean()
    pos = np.maximum(s, 0).mean()
    net = s.mean()
    title(f, 4, 56, 'b', 'Paired MEHI endpoint values')
    joint_edges = np.linspace(-1, 1, 81)
    counts, xed, yed = np.histogram2d(m.MEHI_2000.to_numpy(), m.MEHI_2023.to_numpy(), bins=(joint_edges, joint_edges))
    counts = counts.astype(np.int64)
    assert counts.sum() == len(m)
    joint_source = pd.DataFrame([dict(MEHI_2000_left=xed[i], MEHI_2000_right=xed[i + 1], MEHI_2023_left=yed[j], MEHI_2023_right=yed[j + 1], n=int(counts[i, j])) for i in range(80) for j in range(80)])
    out_csv(joint_source, 'Fig2b_full_support_joint_frequency.csv')
    marginal_2000 = counts.sum(axis=1)
    marginal_2023 = counts.sum(axis=0)
    assert np.array_equal(marginal_2000, np.histogram(m.MEHI_2000.to_numpy(), bins=xed)[0])
    assert np.array_equal(marginal_2023, np.histogram(m.MEHI_2023.to_numpy(), bins=yed)[0])
    assert marginal_2000.sum() == marginal_2023.sum() == len(m)
    marginal_source = pd.DataFrame([dict(year=year, bin_left=edges_[i], bin_right=edges_[i + 1], n=int(n), share_all_matched_cells_percent=100 * n / len(m)) for year, edges_, values in [(2000, xed, marginal_2000), (2023, yed, marginal_2023)] for i, n in enumerate(values)])
    out_csv(marginal_source, 'Fig2b_endpoint_marginal_histograms.csv')
    cm = LinearSegmentedColormap.from_list('joint_frequency', ['#E8E5F6', '#C3B9E8', '#8C7DD0', '#594AA9', '#29266C'])
    cm.set_bad('white')
    b = axmm(f, 19, 11, 34, 34)
    z = np.ma.masked_where(counts.T == 0, counts.T)
    mesh = b.pcolormesh(xed, yed, z, cmap=cm, norm=LogNorm(vmin=1, vmax=int(counts.max())), shading='flat', rasterized=True)
    for boundary in (-0.33, 0.33):
        b.axvline(boundary, color='#71878D', lw=0.7, ls=(0, (2, 2)), zorder=3)
        b.axhline(boundary, color='#71878D', lw=0.7, ls=(0, (2, 2)), zorder=3)
    b.plot([-1, 1], [-1, 1], color=HARD, lw=0.75, alpha=0.88, zorder=3)
    b.set(xlim=(-1, 1), ylim=(-1, 1), xticks=[-1, 0, 1], yticks=[-1, 0, 1])
    b.set_xlabel('MEHI 2000', fontsize=7.6, labelpad=4)
    b.set_ylabel('MEHI 2023', fontsize=7.6, labelpad=1)
    clean(b)
    marginal_ceiling = 1.04 * 100 * max(marginal_2000.max(), marginal_2023.max()) / len(m)
    top = axmm(f, 19, 46, 34, 5)
    top.stairs(100 * marginal_2000 / len(m), xed, fill=True, fc='#786AB9', ec='#594AA9', lw=0.45)
    top.set(xlim=(-1, 1), ylim=(0, marginal_ceiling))
    top.axis('off')
    right = axmm(f, 54, 11, 5, 34)
    right.stairs(100 * marginal_2023 / len(m), yed, orientation='horizontal', fill=True, fc='#786AB9', ec='#594AA9', lw=0.45)
    right.set(xlim=(0, marginal_ceiling), ylim=(-1, 1))
    right.axis('off')
    for boundary in (-0.33, 0.33):
        top.axvline(boundary, color='#71878D', lw=0.65, ls=(0, (2, 2)), zorder=3)
        right.axhline(boundary, color='#71878D', lw=0.65, ls=(0, (2, 2)), zorder=3)
    cbax = axmm(f, 60.5, 11, 2.1, 34)
    cb = f.colorbar(mesh, cax=cbax, ticks=[1, 10, 100, 1000, int(counts.max())])
    cb.ax.set_yticklabels(['1', '10', '100', '1k', f'{counts.max():,}'])
    cb.ax.tick_params(labelsize=7, length=1.5, width=0.45, pad=1.5)
    cb.outline.set_linewidth(0.4)
    txt(f, 63.5, 47, 'n / bin', fontsize=7.2, color=MUTED)
    title(f, 74, 56, 'c', 'Change by initial state')
    c = axmm(f, 82, 26, 86, 25)
    state = np.where(m.MEHI_2000.to_numpy() < -0.33, 0, np.where(m.MEHI_2000.to_numpy() > 0.33, 2, 1))
    curves = []
    groups = []
    for k, (label, color) in enumerate([('Soft', SOFT), ('Mixed', '#A78B58'), ('Hard', HARD)]):
        vals = np.sort(s[state == k])
        unique, frequency = np.unique(vals, return_counts=True)
        cumulative = np.cumsum(frequency)
        c.step(np.r_[-1, unique, 1], np.r_[0, cumulative / len(vals), 1], where='post', color=color, lw=1.5, label=label, zorder=3)
        category = [int(np.sum(vals < -0.005)), int(np.sum(np.abs(vals) <= 0.005)), int(np.sum(vals > 0.005))]
        groups.append(dict(state_2000=label, n=len(vals), softening_n=category[0], near_neutral_n=category[1], hardening_n=category[2], softening_percent=100 * category[0] / len(vals), near_neutral_percent=100 * category[1] / len(vals), hardening_percent=100 * category[2] / len(vals)))
        curves.extend((dict(state_2000=label, pMEHI=float(value), at_value_n=int(fr), cumulative_n=int(cum), cumulative_percent=100 * cum / len(vals), denominator_n=len(vals)) for value, fr, cum in zip(unique, frequency, cumulative)))
    out_csv(pd.DataFrame(groups), 'Fig2c_initial_state_change_shares.csv')
    out_csv(pd.DataFrame(curves), 'Fig2c_full_empirical_CDF.csv.gz')
    c.axvline(0, color='#8C9DA2', lw=0.55, ls=(0, (2, 2)))
    c.set(xlim=(-1, 1), ylim=(0, 1), xticks=[-1, -0.5, 0, 0.5, 1], yticks=[0, 0.5, 1])
    c.set_xticklabels(['−1', '−0.5', '0', '0.5', '1'])
    c.set_yticklabels(['0', '0.5', '1'])
    c.set_xlabel('pMEHI (2000–2023)', fontsize=7.6, labelpad=4)
    c.set_ylabel('Cumulative share', fontsize=7.6, labelpad=1)
    clean(c, grid='y')
    txt(f, 81, 13.7, '2000 class (n)', fontsize=7.0, color=MUTED)
    txt(f, 168, 13.7, 'Change-class share (%)', ha='right', fontsize=7.0, color=MUTED)
    for i, (row, color) in enumerate(zip(groups, [SOFT, '#A78B58', HARD])):
        yy = 9.4 - i * 4.0
        txt(f, 81, yy + 1.6, row['state_2000'], fontsize=7.2, color=color, weight='bold', va='center')
        txt(f, 104, yy + 1.6, f"{row['n']:,}", ha='right', va='center', fontsize=7.0, color=MUTED)
        bar = axmm(f, 107, yy, 61, 3.2)
        bar.set(xlim=(0, 100), ylim=(0, 1))
        bar.axis('off')
        left = 0
        for share, fill, txt_color in [(row['softening_percent'], SOFT, 'white'), (row['near_neutral_percent'], '#D7D4CD', INK), (row['hardening_percent'], HARD, 'white')]:
            bar.add_patch(Rectangle((left, 0), share, 1, fc=fill, ec='white', lw=0.65))
            if share >= 10:
                bar.text(left + share / 2, 0.5, f'{share:.1f}', ha='center', va='center', fontsize=7.0, color=txt_color, weight='medium')
            left += share
        assert np.isclose(left, 100, atol=1e-10)
    h = m.loc[m.pMEHI.gt(0.005)].copy()
    for year in [2000, 2023]:
        h[f'state_{year}'] = np.where(h[f'MEHI_{year}'] < -0.33, 0, np.where(h[f'MEHI_{year}'] > 0.33, 2, 1))
    mat = pd.crosstab(h.state_2000, h.state_2023).reindex(index=range(3), columns=range(3), fill_value=0).to_numpy()
    assert mat.tolist() == [[23978, 4649, 669], [0, 1906, 736], [0, 0, 306]]
    pct = mat / len(h) * 100
    same = np.trace(mat) / len(h) * 100
    assert abs(same - 81.2244) < 0.0001
    out_csv(pd.DataFrame([dict(negative=neg, positive=pos, net=net, mean_absolute_pMEHI=np.abs(s).mean(), n=len(s))]), 'Fig2b_equal_cell_gross_net.csv')
    out_csv(pd.DataFrame([dict(state_2000=['soft', 'mixed', 'hard'][i], state_2023=['soft', 'mixed', 'hard'][j], n=int(mat[i, j]), share_all_hardening_percent=pct[i, j], denominator_n=len(h)) for i in range(3) for j in range(3)]), 'Fig2c_hardening_state_transitions.csv')
    export(f, 'Fig2_pMEHI_trajectories')

def component_glyph(component, color):
    drawing = DrawingArea(22, 18, 0, 0)
    sx, sy = 22 / 36, 18 / 28
    def rect(x, y, width, height, alpha=0.0, outline=True, dashed=False):
        if alpha:
            drawing.add_artist(Rectangle((x*sx, y*sy), width*sx, height*sy, facecolor=color, edgecolor='none', alpha=alpha))
        if outline:
            drawing.add_artist(Rectangle((x*sx, y*sy), width*sx, height*sy, facecolor='none', edgecolor=color, linewidth=0.55, linestyle=(0,(1.3,1.2)) if dashed else '-'))
    def line(x1,y1,x2,y2,lw=0.65,alpha=1):
        drawing.add_artist(Line2D([x1*sx,x2*sx],[y1*sy,y2*sy],color=color,linewidth=lw,alpha=alpha,solid_capstyle='round'))
    def forest():
        points=np.array([(2,4),(2,23),(5,25),(8,23),(10,24),(12,20),(10,17),(12,13),(10,9),(12,4)])
        drawing.add_artist(Polygon(points*[sx,sy],closed=True,facecolor=color,edgecolor='none',alpha=0.16))
        drawing.add_artist(Polygon(points*[sx,sy],closed=True,facecolor='none',edgecolor=color,linewidth=0.65,joinstyle='round'))
        line(5,8,5,19,0.55)
        line(5,13,8,16,0.55)
        line(5,16,3.5,18,0.55)
    def building():
        rect(26,6,7,16,0.22)
        rect(23,6,3,10,0.12)
        line(29,10,30,10,0.8)
        line(29,15,30,15,0.8)
    if component=='P':
        forest();building()
        drawing.add_artist(FancyArrowPatch((12*sx,12*sy),(22*sx,12*sy),arrowstyle='<->',mutation_scale=3.5,linewidth=0.65,color=color,shrinkA=0,shrinkB=0))
    elif component=='C':
        rect(8,2,27,24,0.07,dashed=True)
        forest();building()
        rect(8.5,6,2.5,14,0.35,outline=False)
    elif component=='B':
        forest()
        for row in range(3):
            for col in range(3):
                occupied=(row,col) in {(0,0),(0,1),(1,0),(1,2),(2,2)}
                rect(15+col*6.3,4+row*7.0,5.0,5.7,0.65 if occupied else 0.06)
    elif component=='S':
        forest()
        rect(15,3,19,22,0,True)
        rect(15,3,6,22,0.18,False)
        rect(27,3,7,22,0.18,False)
        for y in [8,14,20]:
            line(15,y,21,y,0.55)
            line(27,y,34,y,0.55)
        rect(21,3,6,22,0,True,True)
    return drawing

def figure3(m, comparison, contributions, states):
    f = canvas(174, 174)
    title(f, 4, 168, 'a', 'Area and edge change')
    title(f, 101, 168, 'b', 'Conditional edge change')
    order = ['GLOBAL'] + comparison.loc[comparison.GU_A3.ne('GLOBAL')].sort_values('hardening_percent_within_nondecreasing_cells', ascending=False).GU_A3.tolist()
    comp = comparison.set_index('GU_A3').loc[order]
    y = np.arange(len(order))
    y0, hh = (90, 66)
    a1 = axmm(f, 14, y0, 40, hh)
    a2 = axmm(f, 61, y0, 36, hh)
    b = axmm(f, 101, y0, 68, hh)
    for a in [a1, a2, b]:
        a.axhspan(-0.48, 0.48, fc='#EEF3F1', zorder=0)
        for i in range(1, len(order)):
            a.axhline(i, color=GRID, lw=0.4, zorder=0)
        a.axhline(0.6, color='#BBC8C5', lw=0.6, zorder=1)
        a.set(ylim=(19.65, -0.75), yticks=y)
        a.tick_params(axis='y', length=0)
        a.spines['left'].set_visible(False)
    a1.set_yticklabels(['All'] + [c for c in order[1:]], fontsize=7.7)
    a1.tick_params(axis='y', pad=2.4)
    a2.set_yticklabels([])
    b.set_yticklabels([])
    av = comp.common_neighbourhood_mangrove_area_change_percent.to_numpy()
    ev = comp.pMEHI_aw.to_numpy()
    a1.axvline(0, color='#96A6A5', lw=0.55, zorder=1)
    a1.barh(y, av, height=0.55, color=np.where(av >= 0, GREEN, LOSS), zorder=2)
    a1.set(xlim=(-30, 110), xticks=[-25, 0, 50, 100])
    a1.set_xticklabels(['−25', '0', '50', '100'])
    a1.set_xlabel('Area change (%)', fontsize=7.8, labelpad=3)
    a2.axvspan(-0.005, 0.005, fc=NEUTRAL, alpha=0.28, zorder=0)
    a2.axvline(0, color='#9DA8AC', lw=0.55, zorder=1)
    a2.barh(y, ev, height=0.55, color=[HARD if v > 0.005 else SOFT if v < -0.005 else '#A7A398' for v in ev], zorder=2)
    a2.scatter(ev, y, s=5, c=[HARD if v > 0.005 else SOFT if v < -0.005 else '#A7A398' for v in ev], lw=0, zorder=3)
    a2.set(xlim=(-0.145, 0.155), xticks=[-0.1, 0, 0.1])
    a2.set_xticklabels(['−0.1', '0', '0.1'])
    a2.set_xlabel('pMEHI', fontsize=7.8, labelpad=3)
    cross = pd.read_csv(SOURCE / 'Fig3_joint_area_edge_crosstab.csv').set_index(['location_code', 'area_direction', 'edge_direction'])
    area_groups = ['persistence_or_gain', 'loss']
    edge_groups = ['softening', 'near_neutral', 'hardening']
    matrix = []
    b.set(xlim=(0, 70), xticks=[0, 31, 39, 70])
    b.set_xticklabels(['0', '100%', '0', '100%'], fontsize=7.0)
    b.tick_params(axis='x', length=0, pad=3)
    b.set_yticklabels([])
    b.spines['left'].set_visible(False)
    b.spines['bottom'].set_visible(False)
    for i, code in enumerate(order):
        for k, area_group in enumerate(area_groups):
            start = 0.0 if k == 0 else 39.0
            left = start
            hardening = None
            group_total = 0.0
            for edge_group in edge_groups:
                r = cross.loc[code, area_group, edge_group]
                pct = float(r.percent_within_area_direction_cells)
                co = {'softening': SOFT, 'near_neutral': '#CBC9C0', 'hardening': HARD}[edge_group]
                if pct > 0:
                    b.add_patch(Rectangle((left, i - 0.29), 31 * pct / 100, 0.58, fc=co, ec='white', lw=0.28, zorder=3))
                left += 31 * pct / 100
                group_total += pct
                if edge_group == 'hardening':
                    hardening = pct
                matrix.append(dict(GU_A3=code, area_direction=area_group, edge_direction=edge_group, n=int(r.n), weight_m2=float(r.weight_m2), share_within_area_direction_cells_percent=pct, share_within_area_direction_weight_percent=float(r.percent_within_area_direction_weight)))
            assert np.isclose(group_total, 100, atol=1e-08)
    b.axhline(0.5, color='#889DA0', lw=0.85, zorder=5)
    b.text(15.5, 1.075, 'No net area loss', transform=b.get_xaxis_transform(), ha='center', va='bottom', fontsize=7.4)
    b.text(54.5, 1.075, 'Area loss', transform=b.get_xaxis_transform(), ha='center', va='bottom', fontsize=7.4)
    for a in [a1, a2]:
        clean(a)
        a.tick_params(axis='y', length=0)
    place_icon(a1, 'area', (0.08, 1.09), GREEN, 15)
    a1.text(0.18, 1.09, 'Area', transform=a1.transAxes, va='center', fontsize=8.2)
    place_icon(a2, 'edge', (0.08, 1.09), HARD, 15)
    a2.text(0.2, 1.09, 'Edge', transform=a2.transAxes, va='center', fontsize=8.2)
    txt(f, 104, 83, '■', fontsize=8.5, color=SOFT)
    txt(f, 108, 83, 'Softening', fontsize=7.2, color=MUTED)
    txt(f, 126, 83, '■', fontsize=8.5, color='#CBC9C0')
    txt(f, 130, 83, 'Near-neutral', fontsize=7.2, color=MUTED)
    txt(f, 151, 83, '■', fontsize=8.5, color=HARD)
    txt(f, 155, 83, 'Hardening', fontsize=7.2, color=MUTED)
    out_csv(pd.DataFrame(matrix), 'Fig3b_joint_condition_matrix.csv')
    title(f, 4, 79, 'c', 'Relative component contributions')
    contrib_rows = []
    for code in order:
        group = m if code == 'GLOBAL' else m.loc[m.GU_A3.eq(code)]
        ww = group.weight_m2.to_numpy()
        for cc in 'PCBS':
            z = group[f'{cc}_contribution'].to_numpy()
            neg = float(np.average(np.minimum(z, 0), weights=ww))
            pos = float(np.average(np.maximum(z, 0), weights=ww))
            net = float(np.average(z, weights=ww))
            assert np.isclose(neg + pos, net, atol=1e-14)
            contrib_rows.append(dict(GU_A3=code, component=cc, negative=neg, positive=pos, net=net, n=len(group), weight_m2_sum=float(ww.sum()), n_negative=int((z < 0).sum()), n_zero=int((z == 0).sum()), n_positive=int((z > 0).sum())))
    conc = pd.DataFrame(contrib_rows).set_index(['GU_A3', 'component'])
    for cc in 'PCBS':
        assert np.isclose(conc.loc[('GLOBAL', cc), 'net'], contributions.set_index('component').loc[cc, 'net'], atol=1e-13)
    assert conc.negative.min() > -0.08 and conc.positive.max() < 0.08
    out_csv(pd.DataFrame(contrib_rows), 'Fig3c_country_component_gross_net.csv')
    absolute = conc.copy()
    denom = (conc.positive - conc.negative).groupby(level='GU_A3').sum()
    assert np.isfinite(denom).all() and (denom > 0).all()
    for name in ['negative', 'positive', 'net']:
        conc[name] = 100 * conc[name] / conc.index.get_level_values('GU_A3').map(denom).to_numpy()
    assert np.allclose((conc.positive - conc.negative).groupby(level='GU_A3').sum(), 100, atol=1e-10)
    assert np.allclose(conc.negative + conc.positive, conc.net, atol=1e-11)
    result = conc.reset_index()
    result['denominator_absolute_contribution'] = result.GU_A3.map(denom)
    result = result.rename(columns={x: x + '_percent' for x in ['negative', 'positive', 'net']})
    out_csv(result, 'Fig3c_relative_component_contributions.csv')
    expected = comp.pMEHI_aw.reindex(denom.index)
    reconstructed = absolute.net.groupby(level='GU_A3').sum().reindex(denom.index)
    assert np.allclose(reconstructed, expected, atol=1e-13)
    audit = dict(rows=20, components_per_row=4, matched_neighbourhoods=len(m), denominator_min=float(denom.min()), denominator_max=float(denom.max()), max_gross_closure_error=float(abs((conc.positive-conc.negative).groupby(level='GU_A3').sum()-100).max()), max_absolute_reconstruction_error=float(abs(reconstructed-expected).max()))
    (SOURCE / 'Fig3c_display_validation.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')
    for x,marker,filled,label in [(102,'o',False,'− gross'),(129,'o',True,'+ gross'),(156,'D',True,'net')]:
        f.add_artist(Line2D([x/174],[80/174],transform=f.transFigure,marker=marker,markersize=3.3,markerfacecolor=INK if filled else 'white',markeredgecolor=INK,markeredgewidth=0.7,linestyle='none'))
        txt(f,x+2.5,80,label,fontsize=7.0,color=INK,va='center')
    axis_ranges = []
    for j, cc in enumerate('PCBS'):
        c = axmm(f, 14 + j * 40, 9, 35, 62)
        c.axhspan(-0.48, 0.48, fc='#EDF3F1', zorder=0)
        c.axvline(0, color='#A8B5B7', lw=0.55, zorder=1)
        for i, code in enumerate(order):
            q = conc.loc[code, cc]
            c.axhline(i, color=GRID, lw=0.3, zorder=0)
            c.hlines(i, q.negative, q.positive, color=COMPS[cc], alpha=0.45, lw=1.2, zorder=2)
            c.scatter(q.negative, i, s=11, facecolors='white', edgecolors=COMPS[cc], lw=0.8, zorder=3)
            c.scatter(q.positive, i, s=12, c=COMPS[cc], ec='white', lw=0.25, zorder=3)
            c.scatter(q.net, i, s=12, marker='D', c=INK, ec='white', lw=0.2, zorder=4)
        c.axhline(0.5, color='#99AAA9', lw=0.7, zorder=5)
        values = conc.xs(cc, level='component')[['negative', 'positive', 'net']].to_numpy()
        value_min, value_max = min(0.0, float(values.min())), max(0.0, float(values.max()))
        span = value_max - value_min
        rounding = 10.0 if span >= 100 else 5.0 if span >= 20 else 1.0
        lower = np.floor((value_min - 0.05 * span) / rounding) * rounding
        upper = np.ceil((value_max + 0.05 * span) / rounding) * rounding
        target = span / 4
        magnitude = 10 ** np.floor(np.log10(target))
        step = next(x for x in [1, 2, 2.5, 4, 5, 10] if x >= target / magnitude) * magnitude
        ticks = np.arange(np.ceil(lower / step), np.floor(upper / step) + 1) * step
        assert lower < value_min <= 0 <= value_max < upper
        axis_ranges.append(dict(component=cc,observed_min_percent=value_min,observed_max_percent=value_max,xlim_percent=[float(lower),float(upper)],ticks_percent=ticks.tolist(),all_60_points_within_axis=True))
        c.set(xlim=(lower, upper), ylim=(19.5, -0.5), xticks=ticks, yticks=range(20))
        c.set_xticklabels([f'{x:g}'.replace('-', '−') for x in ticks], fontsize=7.2)
        c.set_yticklabels(['All'] + order[1:] if j == 0 else [], fontsize=7.5)
        c.tick_params(axis='y', length=0, pad=2.5)
        c.tick_params(axis='x', length=1.5, pad=2)
        c.spines['left'].set_visible(False)
        c.spines['bottom'].set_color('#ABB8BC')
        header_x=14+j*40
        f.add_artist(AnnotationBbox(component_glyph(cc,COMPS[cc]),((header_x+4)/174,74.2/174),xycoords='figure fraction',frameon=False,pad=0,box_alignment=(0.5,0.5)))
        txt(f,header_x+9.2,74.2,{'P':'P · proximity','C':'C · contact','B':'B · built-up','S':'S · soft-buffer'}[cc],fontsize=7.8,color=COMPS[cc],va='center')
    (SOURCE / 'Fig3c_axis_ranges.json').write_text(json.dumps(axis_ranges, indent=2), encoding='utf-8')
    txt(f, 90, 2.0, 'Share of total absolute component change (%)', fontsize=7.4, ha='center', color=MUTED)
    export(f, 'Fig3_area_component_pathways')

def supplementary9(states, comparison):
    f = canvas(174, 107)
    title(f, 4, 100, 'a', 'Fixed-neighbourhood component states, 2000 and 2023')
    txt(f, 107, 92, '○ 2000', fontsize=7.5, color=MUTED)
    txt(f, 143, 92, '● 2023', fontsize=7.5)
    order = ['GLOBAL'] + comparison.loc[comparison.GU_A3.ne('GLOBAL')].sort_values('hardening_percent_within_nondecreasing_cells', ascending=False).GU_A3.tolist()
    country_order = order[1:]
    for j, cc in enumerate(list('PCBS') + ['MEHI']):
        d = axmm(f, 28 + j * 28.3, 13, 24.7, 71)
        d.axvline(0, color='#BDC8CB', lw=0.6, ls=(0, (2, 2)))
        for i, code in enumerate(country_order):
            v = states.loc[states.GU_A3.eq(code) & states.component.eq(cc)].set_index('year').state
            co = HARD if v[2023] > v[2000] else SOFT
            d.axhline(i, color=GRID, lw=0.4, zorder=0)
            d.plot([v[2000], v[2023]], [i, i], c=co, lw=1.25, zorder=2)
            d.scatter(v[2000], i, s=14, fc='white', ec=co, lw=0.7, zorder=3)
            d.scatter(v[2023], i, s=14, fc=co, ec='white', lw=0.3, zorder=4)
        d.set(xlim=(-1.05, 1.05), ylim=(18.5, -0.5), xticks=[-1, 0, 1], yticks=range(19))
        d.set_yticklabels(country_order if j == 0 else [], fontsize=7.6)
        d.set_xticklabels(['−1', '0', '1'], fontsize=7.4)
        d.tick_params(axis='y', length=0, pad=3)
        d.tick_params(axis='x', length=2, pad=2)
        d.spines['left'].set_visible(False)
        d.spines['bottom'].set_color('#ABB7BC')
        d.set_title({'P': 'P · proximity', 'C': 'C · contact', 'B': 'B · built-up', 'S': 'S · soft-buffer', 'MEHI': 'MEHI'}[cc], fontsize=8.0, pad=4, color=COMPS.get(cc, INK))
    txt(f, 97, 4.5, 'Component / index state (fixed cells, fixed area weights)', ha='center', fontsize=7.5, color=MUTED)
    out_csv(states, 'Supplementary_Fig9_paired_component_states.csv')
    export(f, 'Supplementary_Fig9_paired_component_states')

def supplementary8(m, summary):
    f = canvas(174, 118)
    title(f, 4, 111, 'a', 'Magnitude of opposing changes')
    title(f, 96, 111, 'b', 'Country/location medians')
    a = axmm(f, 17, 71, 67, 31)
    s = m.pMEHI.to_numpy()
    curves = []
    for direction, mask, co, sign in [('softening', s < -0.005, SOFT, -1), ('hardening', s > 0.005, HARD, 1)]:
        z, cnt = np.unique(np.abs(s[mask]), return_counts=True)
        remaining = cnt.sum() - np.cumsum(cnt)
        x = np.r_[0.005, z, 1.0]
        y = np.r_[cnt.sum(), remaining, 0] / len(s) * 100
        a.fill_between(x, 0, sign * y, color=co, alpha=0.23, step='post', lw=0)
        a.step(x, sign * y, where='post', c=co, lw=1.0)
        curves.extend([dict(direction=direction, absolute_pMEHI_cutoff=xx, share_all_matched_cells_percent=yy) for xx, yy in zip(x, y)])
        assert y[-1] == 0 and np.all(np.diff(y) <= 1e-12)
    a.axhline(0, c='#93A4AB', lw=0.55)
    a.text(0.43, 26, 'Hardening', color=HARD, fontsize=7.7)
    a.text(0.43, -32, 'Softening', color=SOFT, fontsize=7.7)
    a.set(xlim=(0, 1), ylim=(-48, 48), xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[-40, -20, 0, 20, 40])
    a.set_yticklabels(['40', '20', '0', '20', '40'])
    a.set_xlabel('Absolute pMEHI cutoff', labelpad=2)
    a.set_ylabel('Cells above cutoff (%)', labelpad=2)
    clean(a, 'y')
    b = axmm(f, 113, 17, 51, 86)
    b.axvspan(-0.005, 0.005, fc=NEUTRAL, alpha=0.3, zorder=0)
    b.axvline(0, color='#9DA9AE', lw=0.55)
    for i, r in summary.reset_index(drop=True).iterrows():
        co = HARD if r.weighted_median_pMEHI > 0.005 else SOFT if r.weighted_median_pMEHI < -0.005 else '#A0988A'
        b.hlines(i, r.weighted_p25, r.weighted_p75, color='#BAC4C8', lw=1.1)
        b.scatter(r.weighted_median_pMEHI, i, s=19, fc=co, ec='white', lw=0.4, zorder=3)
    b.set(ylim=(18.6, -0.6), xlim=(-0.225, 0.215), xticks=[-0.2, -0.1, 0, 0.1, 0.2], yticks=range(19), yticklabels=summary.GU_A3.tolist())
    b.set_xlabel('pMEHI median and IQR', labelpad=3)
    b.tick_params(axis='y', length=0, labelsize=7.8)
    b.spines['left'].set_visible(False)
    clean(b)
    title(f, 4, 55, 'c', 'All matched state transitions')
    c = axmm(f, 26, 14, 39, 32)
    states = []
    for year in [2000, 2023]:
        v = m[f'MEHI_{year}'].to_numpy()
        states.append(np.where(v < -0.33, 0, np.where(v > 0.33, 2, 1)))
    mat = pd.crosstab(states[0], states[1]).reindex(index=range(3), columns=range(3), fill_value=0).to_numpy()
    assert mat.tolist() == [[63974, 4652, 669], [4354, 3703, 736], [333, 532, 556]]
    pct = mat / len(m) * 100
    cm = LinearSegmentedColormap.from_list('full_transitions', ['#F2F5F2', '#C2D8CC', '#548C79'])
    c.imshow(pct, cmap=cm, norm=Normalize(0, 85), aspect='auto', interpolation='nearest')
    for i in range(3):
        for j in range(3):
            c.text(j, i, f'{mat[i, j]:,}\n{pct[i, j]:.1f}%', ha='center', va='center', fontsize=7.4, linespacing=1.15, color='white' if pct[i, j] > 50 else INK)
        c.add_patch(Rectangle((i - 0.46, i - 0.46), 0.92, 0.92, fill=False, ec=GREEN, lw=0.7))
    c.set(xticks=range(3), yticks=range(3), xticklabels=['Soft', 'Mixed', 'Hard'], yticklabels=['Soft', 'Mixed', 'Hard'])
    c.tick_params(length=0, pad=3, labelsize=7.5)
    for sp in c.spines.values():
        sp.set_visible(False)
    c.set_xlabel('2023 state', labelpad=3)
    c.set_ylabel('2000 state', labelpad=3)
    txt(f, 71, 36, 'n=79,509', fontsize=7.6, color=MUTED)
    txt(f, 71, 27, 'Count', fontsize=7.6)
    txt(f, 71, 23, 'Cell share', fontsize=7.6)
    txt(f, 71, 19, '(%)', fontsize=7.6)
    out_csv(pd.DataFrame(curves), 'Supplementary_Fig8a_magnitude_exceedance.csv.gz')
    out_csv(pd.DataFrame([dict(state_2000=['soft', 'mixed', 'hard'][i], state_2023=['soft', 'mixed', 'hard'][j], n=int(mat[i, j]), share_all_matched_cells_percent=pct[i, j], denominator_n=len(m)) for i in range(3) for j in range(3)]), 'Supplementary_Fig8c_all_state_transitions.csv')
    export(f, 'Supplementary_Fig8_local_change_diagnostics')

def main():
    global DATA, OUT, SOURCE
    p = argparse.ArgumentParser()
    p.add_argument('--data', type=Path, default=HERE.parents[1] / 'data')
    p.add_argument('--out', type=Path, default=HERE / 'figures')
    p.add_argument('--sources', type=Path, default=HERE / 'source_data')
    p.add_argument('--figures', nargs='+', choices=['2', '3', 'S8', 'S9'], default=['2', '3', 'S8', 'S9'])
    a = p.parse_args()
    DATA = a.data
    OUT = a.out
    SOURCE = a.sources
    for folder in [OUT, SOURCE]:
        folder.mkdir(parents=True, exist_ok=True)
    m, summary, comparison, contributions, states = prepare()
    if '2' in a.figures:
        figure2(m, summary)
    if '3' in a.figures:
        figure3(m, comparison, contributions, states)
    if 'S8' in a.figures:
        supplementary8(m, summary)
    if 'S9' in a.figures:
        supplementary9(states, comparison)
if __name__ == '__main__':
    main()
