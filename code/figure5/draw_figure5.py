from __future__ import annotations
import argparse, importlib.util
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Ellipse, Rectangle, FancyArrowPatch
from matplotlib.offsetbox import AnnotationBbox, DrawingArea
HERE = Path(__file__).resolve().parents[1]
SOFT = '#497B9F'
HARD = '#BD5A62'
NEUTRAL = '#CCC9C2'
INK = '#233545'
GRID = '#E9ECEC'
COMPS = {'P': '#476F95', 'C': '#AE6772', 'B': '#C29B53', 'S': '#548E83'}
ROUTES = ['proximity_only_route', 'vegetation_buffer_loss_route', 'mixed_route', 'water_edge_narrowing_route', 'built_up_replacement_route', 'tidal_flat_loss_route']
RC = ['#817595', '#669C89', '#C1C0BC', '#5785A4', '#C17170', '#C7A665']
RL = ['Proximity only', 'Vegetation loss', 'Mixed routes', 'Water narrowing', 'Built replacement', 'Tidal-flat loss']
RI = ['distance', 'leaf', 'mixed', 'water', 'built', 'tidal']
plt.rcParams.update({'font.family': ['Arial', 'DejaVu Sans'], 'font.size': 8, 'axes.labelsize': 8, 'axes.titlesize': 8.5, 'xtick.labelsize': 7.3, 'ytick.labelsize': 7.3, 'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none', 'axes.linewidth': 0.55, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.unicode_minus': True, 'text.color': INK, 'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK, 'savefig.facecolor': 'white'})

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
        line([x + 2, x + 2], [y + 3, y + 4])
        line([x + 4, x + 4], [y + 3, y + 4])
        line([x + 2, x + 2], [y + 7, y + 8])
        line([x + 4, x + 4], [y + 7, y + 8])
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
    elif kind == 'tree':
        tree(12, 5)
    return d

def place_icon(ax, kind, xy, color=INK, size=15, coords='axes fraction'):
    a = AnnotationBbox(icon(kind, color, size), xy, xycoords=coords, frameon=False, pad=0, box_alignment=(0.5, 0.5))
    ax.add_artist(a)
    return a

def save(f, name):
    f.canvas.draw()
    for ext in ['pdf', 'svg', 'png']:
        f.savefig(OUT / f'{name}.{ext}', dpi=450 if ext == 'pdf' else 300)
    plt.close(f)
    print('Exported', name, flush=True)

def fig5():
    renderer = HERE / 'support/scenario_figure_helpers.py'
    spec = importlib.util.spec_from_file_location('scenario_renderer', renderer)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.ROOT = DATA.parent
    m.DATA = DATA / 'figure_source'
    m.LAND = DATA / 'cartography/ne_50m_land.geojson'
    m.OUT = OUT
    m.SOFT = SOFT
    m.HARD = HARD
    m.NEUTRAL = NEUTRAL
    m.SSPC = {'SSP1': '#669889', 'SSP2': '#527DA2', 'SSP3': '#BBA061', 'SSP5': '#B96478'}

    def save_with_layout(fig, name, height):
        fig._mm = (167, height)
        for t in fig.findobj(matplotlib.text.Text):
            if t.get_color() in ['#222222', '#333333']:
                t.set_color(INK)
        ia = fig.add_axes([0.74, 184 / height, 0.24, 9 / height])
        ia.set(xlim=(0, 1), ylim=(0, 1))
        ia.axis('off')
        place_icon(ia, 'distance', (0.1, 0.53), INK, 21)
        ia.text(0.24, 0.5, 'Fixed 2023 edge', ha='left', va='center', fontsize=7)
        save(fig, 'Fig5_projected_urban_edge_exposure')
    m.save = save_with_layout
    m.draw_scenario_figure()
    plt.rcParams.update({'font.family': ['Arial', 'DejaVu Sans'], 'text.color': INK, 'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK})

def main():
    global DATA, OUT
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=HERE.parent / 'data')
    parser.add_argument('--out', type=Path, default=HERE / 'figures')
    args = parser.parse_args()
    DATA = args.data
    OUT = args.out
    OUT.mkdir(parents=True, exist_ok=True)
    fig5()
if __name__ == '__main__':
    main()
