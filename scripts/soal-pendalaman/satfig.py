"""Render Sentinel-2 windows as exam figures."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sat import fetch

CREDIT = "Citra Sentinel-2 L2A (Copernicus/ESA), {date}"


def stretch(a, lo=2, hi=98):
    a = a.astype(np.float32)
    p1, p2 = np.percentile(a[a > 0], [lo, hi]) if (a > 0).any() else (0, 1)
    return np.clip((a - p1) / (p2 - p1 + 1e-6), 0, 1)


def rgb(d, kind="true"):
    if kind == "true":
        im = np.moveaxis(d["visual"], 0, -1).astype(np.float32) / 255.0
        return np.clip(im * 1.15, 0, 1)
    if kind == "false":   # NIR-R-G
        return np.dstack([stretch(d["nir"]), stretch(d["red"]), stretch(d["green"])])
    if kind == "swir":
        return np.dstack([stretch(d["swir16"]), stretch(d["nir"]), stretch(d["red"])])


def ndvi(d):
    n, r = d["nir"], d["red"]
    return (n - r) / (n + r + 1e-6)


def show(name, path, kind="true", title="", labels=None, scale_km=None, ax_fn=None, w=7.5, crop=None):
    d = fetch(name)
    meta = json.loads(str(d["meta"]))
    if kind == "ndvi":
        im = ndvi(d)
    else:
        im = rgb(d, kind)
    km = meta["km"]
    if crop:   # (x0,x1,y0,y1) fractions
        H, W = im.shape[:2]
        x0, x1, y0, y1 = crop
        im = im[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)]
        km = km * (x1 - x0)
    H, W = im.shape[:2]
    fig, ax = plt.subplots(figsize=(w, w * H / W + 0.6))
    if kind == "ndvi":
        m = ax.imshow(im, cmap="RdYlGn", vmin=-0.4, vmax=0.9, extent=(0, km, 0, km * H / W))
        fig.colorbar(m, ax=ax, fraction=0.04, pad=0.02, label="NDVI")
    else:
        ax.imshow(im, extent=(0, km, 0, km * H / W))
    ax.set_xticks([]); ax.set_yticks([])
    for (t, x, y) in (labels or []):
        ax.text(x * km, y * km * H / W, t, fontsize=14, fontweight="bold", color="white", ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.2", fc="#C53030", ec="white", lw=1.2))
    sk = scale_km or {1: 0.2, 2: 0.5}.get(0, None) or round(km / 5, 0) or 1
    x0 = km * 0.05; y0 = km * H / W * 0.05
    ax.plot([x0, x0 + sk], [y0, y0], color="white", lw=5, solid_capstyle="butt")
    ax.plot([x0, x0 + sk], [y0, y0], color="black", lw=2, solid_capstyle="butt")
    ax.text(x0 + sk / 2, y0 + km * H / W * 0.025, f"{sk:g} km".replace(".", ","), color="white", ha="center", fontsize=10, fontweight="bold",
            bbox=dict(fc="black", alpha=0.45, ec="none", pad=1))
    ax.annotate("U", xy=(0.95, 0.95), xytext=(0.95, 0.85), xycoords="axes fraction", ha="center", color="white", fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color="white", lw=2))
    if ax_fn:
        ax_fn(ax, km, km * H / W)
    ax.set_title(title, fontsize=12, fontweight="bold")
    fig.text(0.99, 0.005, CREDIT.format(date=meta["date"]), ha="right", va="bottom", fontsize=7.5, color="#4A5568")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
