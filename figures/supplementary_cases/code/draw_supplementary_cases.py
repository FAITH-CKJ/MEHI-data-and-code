from __future__ import annotations
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
REGIONS = ('R02', 'R04', 'R08')
YEARS = (2000, 2010, 2020, 2023)
mpl.rcParams.update({'font.family': 'Arial', 'font.sans-serif': ['Arial', 'DejaVu Sans'], 'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none', 'axes.linewidth': 0.8, 'savefig.dpi': 450})
REGION_META = {'R02': {'country': 'United States', 'code': 'USA', 'direction': 'softening', 'mean_pmehi': -0.49766532468091806, 'mehi_2000': 0.2303775384557037, 'mehi_2023': -0.7649531109061326, 'n_grid': 56}, 'R04': {'country': 'Thailand', 'code': 'THA', 'direction': 'hardening', 'mean_pmehi': 0.35138798019360495, 'mehi_2000': -0.5715317637029416, 'mehi_2023': 0.1312441966842682, 'n_grid': 51}, 'R08': {'country': 'Australia', 'code': 'AUS', 'direction': 'softening', 'mean_pmehi': -0.2969677173848612, 'mehi_2000': -0.373070636045225, 'mehi_2023': -0.9670060708149474, 'n_grid': 64}}

def panel_title(ax, label: str, title: str, subtitle: str | None=None) -> None:
    ax.text(-0.005, 1.065, label, transform=ax.transAxes, ha='left', va='bottom', fontsize=10.5, fontweight='bold')
    ax.text(0.075, 1.065, title, transform=ax.transAxes, ha='left', va='bottom', fontsize=10.5, fontweight='bold')
    if subtitle:
        ax.text(0.075, 1.012, subtitle, transform=ax.transAxes, ha='left', va='bottom', fontsize=7.6, color='#4d4d4d')

def draw_region(region: str, out_dir: Path) -> dict[str, Path]:
    meta = REGION_META[region]
    fig = plt.figure(figsize=(11.2, 8.45), constrained_layout=False)
    grid = fig.add_gridspec(2, 3, left=0.045, right=0.982, top=0.83, bottom=0.12, wspace=0.125, hspace=0.255, width_ratios=[1.0, 1.0, 1.07])
    fig.text(0.045, 0.965, f"{region} {meta['country']} ({meta['code']}) | {meta['direction']} pMEHI case", ha='left', va='top', fontsize=15, fontweight='bold')
    fig.text(0.045, 0.925, f"Mean MEHI 2000 = {meta['mehi_2000']:.3f}; mean MEHI 2023 = {meta['mehi_2023']:.3f}; mean pMEHI = {meta['mean_pmehi']:.3f}; n = {meta['n_grid']} common 150 m cells", ha='left', va='top', fontsize=9.2, color='#333333')
    fig.text(0.045, 0.894, 'Landsat RGB panels provide visual context; MEHI and pMEHI maps show quantified 150 m edge-neighbourhood structure.', ha='left', va='top', fontsize=8.4, color='#555555')
    layout = [('a', '2000 Landsat RGB', 'remote sensing context', load_rgb(region, 2000), grid[0, 0]), ('b', '2010 Landsat RGB', 'remote sensing context', load_rgb(region, 2010), grid[0, 1]), ('c', '2023 MEHI', 'edge-hardening index', load_map(region, 'MEHI'), grid[0, 2]), ('d', '2020 Landsat RGB', 'remote sensing context', load_rgb(region, 2020), grid[1, 0]), ('e', '2023 Landsat RGB', 'remote sensing context', load_rgb(region, 2023), grid[1, 1]), ('f', 'pMEHI, 2000-2023', 'common-cell change', load_map(region, 'pMEHI'), grid[1, 2])]
    for label, title, subtitle, arr, cell in layout:
        ax = fig.add_subplot(cell)
        ax.imshow(arr)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_linewidth(0.75)
            spine.set_color('#222222')
        panel_title(ax, label, title, subtitle)
    fig.text(0.045, 0.055, 'Caption: Six-panel case synthesis for a selected pMEHI region. Panels a, b, d and e show four evaluated Landsat RGB context years; panel c shows 2023 MEHI; panel f shows pMEHI for common 2000-2023 cells. Map colours follow the source MEHI and pMEHI scales.', ha='left', va='bottom', fontsize=8.4, color='#303030', wrap=True)
    figures = out_dir / 'figures'
    figures.mkdir(parents=True, exist_ok=True)
    stem = f'{region}_six_panel_remote_sensing_MEHI_pMEHI_synthesis_highres'
    paths: dict[str, Path] = {}
    for ext in ('pdf',):
        p = figures / f'{stem}.{ext}'
        if ext == 'tif':
            fig.savefig(p, dpi=450, pil_kwargs={'compression': 'tiff_lzw'})
        else:
            fig.savefig(p, dpi=450)
        paths[ext] = p
    plt.close(fig)
    return paths
ROOT = Path(__file__).resolve().parents[1]

def load_rgb(region, year):
    im = Image.open(ROOT / 'source_images' / region / f'{region}_{year}_RGB.tif').convert('RGB')
    im = ImageOps.autocontrast(im, cutoff=0.15)
    return np.asarray(ImageEnhance.Sharpness(ImageEnhance.Contrast(im).enhance(1.05)).enhance(1.25))

def load_map(region, kind):
    name = f'{region}_MEHI_2023_map.png' if kind == 'MEHI' else f'{region}_pMEHI_2000_2023_map.png'
    im = Image.open(ROOT / 'source_images' / region / name).convert('RGB')
    return np.asarray(im.crop((0, 68, im.size[0], im.size[1] - 8)))
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'reproduced')
    args = parser.parse_args()
    for region in REGIONS:
        draw_region(region, args.output_dir)
