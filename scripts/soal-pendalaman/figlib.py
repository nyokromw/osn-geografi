"""Shared figure helpers for OSNGEO Soal Pendalaman Materi images."""
import json, os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch, Rectangle, Circle, FancyBboxPatch, Ellipse
from matplotlib.collections import PatchCollection

HERE = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(HERE, "geo")

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.labelsize": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

C = dict(blue="#2B6CB0", lblue="#90CDF4", green="#2F855A", lgreen="#9AE6B4", red="#C53030",
         lred="#FEB2B2", orange="#DD6B20", yellow="#D69E2E", gray="#4A5568", lgray="#CBD5E0",
         brown="#8B5A2B", sand="#E9D8A6", sea="#DCEFFB", land="#F3EBD3", purple="#6B46C1", teal="#2C7A7B")
SERIES = [C["blue"], C["orange"], C["green"], C["red"], C["purple"], C["teal"], C["yellow"], C["gray"]]

BULAN = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
BULAN3 = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


def new(w=8, h=4.6):
    fig, ax = plt.subplots(figsize=(w, h))
    return fig, ax


def blank(w=8, h=4.6, xlim=(0, 100), ylim=(0, 60)):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def _idfmt(v, pos=None):
    if abs(v - round(v)) < 1e-9:
        v = int(round(v))
        return f"{v:,}".replace(",", ".") if abs(v) >= 10000 else str(v).replace("-", "−")
    return (f"{v:.6g}").replace(".", ",").replace("-", "−")


def save(fig, path, source=None):
    from matplotlib.ticker import ScalarFormatter, FuncFormatter
    for ax in fig.get_axes():
        for axis in (ax.xaxis, ax.yaxis):
            if type(axis.get_major_formatter()) is ScalarFormatter:
                axis.set_major_formatter(FuncFormatter(_idfmt))
    if source:
        fig.text(0.99, 0.005, source, ha="right", va="bottom", fontsize=8, color="#718096")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def arrow(ax, x1, y1, x2, y2, color="#2D3748", lw=2, ms=16, style="-|>", ls="-", **kw):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms, color=color, lw=lw, linestyle=ls, **kw)
    ax.add_patch(a)
    return a


def box(ax, x, y, w, h, text, fc="#EDF2F7", ec="#4A5568", fs=11, bold=False, tc="#1A202C", r=0.6):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.2,rounding_size={r}", fc=fc, ec=ec, lw=1.4)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", wrap=True)
    return p


def label(ax, x, y, t, fs=12, c="#1A202C", bold=True, bg=None, **kw):
    bbox = dict(boxstyle="round,pad=0.25", fc=bg, ec="none") if bg else None
    ax.text(x, y, t, fontsize=fs, color=c, fontweight="bold" if bold else "normal", ha="center", va="center",
            bbox=bbox, **kw)


def table(data, headers, path, title=None, col_w=None, fs=12, w=8, row_h=0.42, highlight=None):
    nrow = len(data) + 1
    h = row_h * nrow + (0.6 if title else 0.2)
    fig, ax = plt.subplots(figsize=(w, h))
    ax.axis("off")
    tb = ax.table(cellText=[[str(c) for c in r] for r in data], colLabels=headers, loc="center",
                  cellLoc="center", colWidths=col_w)
    tb.auto_set_font_size(False); tb.set_fontsize(fs); tb.scale(1, 1.55)
    for (r, c), cell in tb.get_celld().items():
        cell.set_edgecolor("#A0AEC0")
        if r == 0:
            cell.set_facecolor("#2D3748"); cell.set_text_props(color="white", fontweight="bold")
        elif r % 2 == 0:
            cell.set_facecolor("#F7FAFC")
        if highlight and (r, c) in highlight:
            cell.set_facecolor("#FEFCBF")
    if title:
        ax.set_title(title, pad=6)
    save(fig, path)


def climograph(T, P, path, title="", ylimT=None, ylimP=None):
    fig, ax = new(8, 4.6)
    x = np.arange(12)
    ax.bar(x, P, color=C["lblue"], edgecolor=C["blue"], label="Curah hujan (mm)")
    ax.set_ylabel("Curah hujan (mm)", color=C["blue"])
    ax.set_xticks(x); ax.set_xticklabels(BULAN3)
    if ylimP: ax.set_ylim(*ylimP)
    ax2 = ax.twinx()
    ax2.plot(x, T, color=C["red"], marker="o", lw=2.2, label="Suhu (°C)")
    ax2.set_ylabel("Suhu (°C)", color=C["red"])
    ax2.spines["top"].set_visible(False)
    if ylimT: ax2.set_ylim(*ylimT)
    ax.set_title(title)
    save(fig, path)


def pyramid(groups, male, female, path, title="", unit="%", xmax=None, legend_loc="upper right"):
    fig, ax = new(7.5, 5.2)
    y = np.arange(len(groups))
    ax.barh(y, [-m for m in male], color=C["blue"], label="Laki-laki")
    ax.barh(y, female, color=C["red"], alpha=0.85, label="Perempuan")
    ax.set_yticks(y); ax.set_yticklabels(groups, fontsize=10)
    xm = xmax or max(max(male), max(female)) * 1.15
    ax.set_xlim(-xm, xm)
    ticks = np.linspace(-xm, xm, 5)
    ax.set_xticks(ticks); ax.set_xticklabels([f"{abs(t):.0f}" for t in ticks])
    ax.set_xlabel(f"Persentase penduduk ({unit})" if unit == "%" else unit)
    ax.axvline(0, color="#2D3748", lw=0.8)
    ax.legend(loc=legend_loc, frameon=False, fontsize=10)
    ax.set_title(title)
    save(fig, path)


# ---------------------------------------------------------------- maps
_cache = {}


def _load(name):
    if name not in _cache:
        _cache[name] = json.load(open(os.path.join(GEO, name)))
    return _cache[name]


def _polys(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"]]
    if geom["type"] == "MultiPolygon":
        return geom["coordinates"]
    return []


def draw_geo(ax, features, fc=C["land"], ec="#8D7B5A", lw=0.5, colors=None, key="name"):
    for f in features:
        col = fc
        if colors is not None:
            col = colors.get(f["properties"].get(key), fc)
        for poly in _polys(f["geometry"]):
            ring = np.array(poly[0])
            ax.add_patch(Polygon(ring, closed=True, fc=col, ec=ec, lw=lw))


def world_features():
    return _load("countries50.geojson")["features"]


def indonesia_map(ax=None, extent=(94, 142, -11.5, 6.8), colors=None, neighbors=True, w=10, h=4.6,
                  grid=True, fc=C["land"]):
    """Draw Indonesia (provinces) with optional per-province colors."""
    fig = None
    if ax is None:
        fig, ax = plt.subplots(figsize=(w, h))
    ax.set_facecolor(C["sea"])
    if neighbors:
        feats = [f for f in world_features() if f["properties"].get("ADM0_A3") != "IDN"]
        draw_geo(ax, feats, fc="#EDEDED", ec="#B5B5B5", lw=0.4)
    draw_geo(ax, _load("idn_prov.geojson")["features"], fc=fc, ec="#7A6A4F", lw=0.4, colors=colors)
    ax.set_xlim(extent[0], extent[1]); ax.set_ylim(extent[2], extent[3]); ax.set_aspect("equal")
    if grid:
        ax.set_xticks(range(int(math.ceil(extent[0] / 5) * 5), int(extent[1]) + 1, 5))
        ax.set_xticklabels([f"{t}°BT" for t in ax.get_xticks().astype(int)], fontsize=8)
        yt = [t for t in range(-10, 11, 5) if extent[2] <= t <= extent[3]]
        ax.set_yticks(yt)
        ax.set_yticklabels([("0°" if t == 0 else f"{abs(t)}°{'LU' if t > 0 else 'LS'}") for t in yt], fontsize=8)
        ax.grid(color="white", lw=0.6, alpha=0.8)
        for s in ax.spines.values():
            s.set_visible(True); s.set_color("#718096")
    else:
        ax.set_xticks([]); ax.set_yticks([])
    return fig, ax


def world_map(ax=None, extent=(-180, 180, -60, 80), colors=None, w=10, h=5, key="ADM0_A3", fc=C["land"]):
    fig = None
    if ax is None:
        fig, ax = plt.subplots(figsize=(w, h))
    ax.set_facecolor(C["sea"])
    draw_geo(ax, world_features(), fc=fc, ec="#9C8E70", lw=0.3, colors=colors, key=key)
    ax.set_xlim(extent[0], extent[1]); ax.set_ylim(extent[2], extent[3]); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(True); s.set_color("#718096")
    return fig, ax


def legend_patches(ax, items, loc="lower left", title=None, fs=9, ncol=1):
    from matplotlib.patches import Patch
    hs = [Patch(fc=c, ec="#555", label=l) for l, c in items]
    ax.legend(handles=hs, loc=loc, fontsize=fs, title=title, title_fontsize=fs, framealpha=0.92, ncol=ncol)


def north_arrow(ax, x, y, size=0.06):
    ax.annotate("U", xy=(x, y), xytext=(x, y - size), xycoords="axes fraction", textcoords="axes fraction",
                ha="center", va="center", fontsize=12, fontweight="bold",
                arrowprops=dict(facecolor="black", width=3, headwidth=10))


def scalebar(ax, x, y, length, text, h=None):
    h = h or length * 0.04
    ax.add_patch(Rectangle((x, y), length / 2, h, fc="black", ec="black"))
    ax.add_patch(Rectangle((x + length / 2, y), length / 2, h, fc="white", ec="black"))
    ax.text(x + length / 2, y + h * 2.2, text, ha="center", va="bottom", fontsize=9)


# ---------------------------------------------------------------- terrain
def terrain(n=200, peaks=((0.5, 0.5, 1.0, 0.18),), base=0.0, tilt=(0, 0), ridge=None):
    """Synthetic elevation field on unit square; peaks=(x,y,h,sigma)."""
    x = np.linspace(0, 1, n); X, Y = np.meshgrid(x, x)
    Z = np.full_like(X, base) + tilt[0] * X + tilt[1] * Y
    for (px, py, h, s) in peaks:
        Z += h * np.exp(-((X - px) ** 2 + (Y - py) ** 2) / (2 * s ** 2))
    if ridge:
        for (x0, y0, x1, y1, h, s) in ridge:
            # distance to segment
            dx, dy = x1 - x0, y1 - y0
            t = np.clip(((X - x0) * dx + (Y - y0) * dy) / (dx * dx + dy * dy), 0, 1)
            d2 = (X - (x0 + t * dx)) ** 2 + (Y - (y0 + t * dy)) ** 2
            Z += h * np.exp(-d2 / (2 * s ** 2))
    return X, Y, Z


def contour_map(X, Y, Z, path, interval, index_every=5, points=None, title="", fill=True, unit="m",
                river=None, w=7, h=6, extra=None, show_labels=True):
    fig, ax = plt.subplots(figsize=(w, h))
    lv = np.arange(math.floor(Z.min() / interval) * interval, Z.max() + interval, interval)
    if fill:
        ax.contourf(X, Y, Z, levels=lv, cmap="YlGn_r", alpha=0.35)
    cs = ax.contour(X, Y, Z, levels=lv, colors="#8B5A2B", linewidths=0.7)
    idx = [l for l in lv if round(l / interval) % index_every == 0]
    cs2 = ax.contour(X, Y, Z, levels=idx, colors="#6B3E12", linewidths=1.6)
    if show_labels:
        ax.clabel(cs2, fmt=lambda v: f"{v:.0f}", fontsize=9)
    if river:
        ax.plot(*river, color=C["blue"], lw=2.2)
    if points:
        for name, (px, py) in points.items():
            ax.plot(px, py, "o", ms=7, color=C["red"], mec="white", mew=1.2, zorder=5)
            ax.text(px + 0.015, py + 0.015, name, fontsize=13, fontweight="bold", zorder=6,
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))
    if extra:
        extra(ax)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(True)
    ax.set_title(title)
    save(fig, path)
    return lv


def iso_map(path, centers, title="", unit="mb", interval=4, points=None, extent=(0, 1, 0, 1), base=1012, w=8,
            h=5.5, labels=None, extra=None):
    """centers: list of (x, y, amplitude(mb), sigma, label)"""
    x = np.linspace(extent[0], extent[1], 300); y = np.linspace(extent[2], extent[3], 220)
    X, Y = np.meshgrid(x, y)
    Z = np.full_like(X, float(base))
    for (cx, cy, a, s, *_r) in centers:
        Z += a * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * s ** 2))
    fig, ax = plt.subplots(figsize=(w, h))
    lv = np.arange(math.floor(Z.min() / interval) * interval, Z.max() + interval, interval)
    cs = ax.contour(X, Y, Z, levels=lv, colors="#2D3748", linewidths=1.0)
    ax.clabel(cs, fmt=lambda v: f"{v:.0f}", fontsize=9)
    for (cx, cy, a, s, *rest) in centers:
        if rest and rest[0]:
            ax.text(cx, cy, rest[0], fontsize=20, fontweight="bold", ha="center", va="center",
                    color=C["red"] if a < 0 else C["blue"])
    if points:
        for name, (px, py) in points.items():
            ax.plot(px, py, "o", ms=7, color="black")
            ax.text(px + 0.012, py + 0.012, name, fontsize=13, fontweight="bold")
    if extra:
        extra(ax)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect("equal")
    for s in ax.spines.values():
        s.set_visible(True)
    ax.set_title(title)
    save(fig, path)
    return Z


def lines(xs, series, path, title="", xlabel="", ylabel="", legend=True, markers=True, ylim=None, hline=None,
          xticks=None, annotate=None, w=8, h=4.4, legend_loc="best"):
    fig, ax = new(w, h)
    for i, (name, ys) in enumerate(series.items()):
        ax.plot(xs, ys, marker="o" if markers else None, ms=4, lw=2.2, color=SERIES[i % 8], label=name)
    if hline is not None:
        ax.axhline(hline, color="#718096", lw=1, ls="--")
    if ylim: ax.set_ylim(*ylim)
    if xticks is not None: ax.set_xticks(xticks)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.set_title(title)
    ax.grid(axis="y", color="#E2E8F0")
    if legend and len(series) > 1: ax.legend(frameon=False, loc=legend_loc)
    if annotate: annotate(ax)
    save(fig, path)


def bars(cats, series, path, title="", ylabel="", xlabel="", stacked=False, horizontal=False, values=False,
         ylim=None, w=8, h=4.4, colors=None, legend_loc="best", fmt="{:g}", rot=0, hline=None):
    fig, ax = new(w, h)
    n = len(series); x = np.arange(len(cats)); width = 0.8 / (1 if stacked else n)
    bottom = np.zeros(len(cats))
    for i, (name, ys) in enumerate(series.items()):
        col = (colors[i] if colors else SERIES[i % 8])
        ys = np.array(ys, dtype=float)
        if horizontal:
            pos = x if stacked else x - 0.4 + width * (i + 0.5)
            b = ax.barh(pos, ys, height=width, left=bottom if stacked else None, color=col, label=name)
        else:
            pos = x if stacked else x - 0.4 + width * (i + 0.5)
            b = ax.bar(pos, ys, width=width, bottom=bottom if stacked else None, color=col, label=name)
        if values:
            ax.bar_label(b, labels=[(_idfmt(v) if fmt == "{:g}" else fmt.format(v).replace(".", ",")) for v in ys], fontsize=9, padding=2,
                         label_type="center" if stacked else "edge")
        if stacked: bottom += ys
    if horizontal:
        ax.set_yticks(x); ax.set_yticklabels(cats); ax.set_xlabel(ylabel); ax.invert_yaxis()
        ax.grid(axis="x", color="#E2E8F0")
    else:
        ax.set_xticks(x); ax.set_xticklabels(cats, rotation=rot, ha="right" if rot else "center")
        ax.set_ylabel(ylabel); ax.set_xlabel(xlabel); ax.grid(axis="y", color="#E2E8F0")
    ax.set_axisbelow(True)
    if hline is not None: ax.axhline(hline, color="#718096", ls="--", lw=1)
    if ylim: (ax.set_xlim if horizontal else ax.set_ylim)(*ylim)
    if n > 1: ax.legend(frameon=False, loc=legend_loc)
    ax.set_title(title)
    save(fig, path)


def scatter(points, path, title="", xlabel="", ylabel="", labels=True, fit=False, w=7.5, h=5, quad=None):
    fig, ax = new(w, h)
    xs = [p[1] for p in points]; ys = [p[2] for p in points]
    ax.scatter(xs, ys, s=60, color=C["blue"], edgecolor="white", zorder=3)
    if labels:
        for n, x, y in points:
            ax.annotate(n, (x, y), xytext=(5, 5), textcoords="offset points", fontsize=11, fontweight="bold")
    if fit:
        m, b = np.polyfit(xs, ys, 1); xx = np.linspace(min(xs), max(xs), 10)
        ax.plot(xx, m * xx + b, "--", color=C["gray"])
    if quad:
        ax.axvline(quad[0], color="#A0AEC0", lw=1); ax.axhline(quad[1], color="#A0AEC0", lw=1)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.set_title(title); ax.grid(color="#EDF2F7")
    save(fig, path)
