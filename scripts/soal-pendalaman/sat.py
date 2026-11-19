"""Fetch real Sentinel-2 L2A windows (Copernicus open data via AWS Earth Search) and cache as npz."""
import os, sys, json
import numpy as np
import rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform as wtransform
from pystac_client import Client

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "sat")
os.makedirs(CACHE, exist_ok=True)
API = "https://earth-search.aws.element84.com/v1"
os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
os.environ.setdefault("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".tif")

SITES = {
    "batur": (115.375, -8.255, 13),
    "bromo": (112.955, -7.935, 11),
    "jakarta": (106.83, -6.19, 10),
    "karawang": (107.33, -6.22, 7),
    "mahakam": (117.45, -0.62, 36),
    "krakatau": (105.423, -6.102, 9),
    "lapindo": (112.712, -7.527, 5),
    "batanghari": (103.55, -1.62, 16),
    "pari": (106.615, -5.862, 6),
    "soetta": (106.655, -6.126, 7),
    "sawit": (101.47, 0.42, 9),
    "segara": (108.95, -7.70, 22),
}


def read_win(href, lon, lat, km, out_shape=None):
    with rasterio.open(href) as ds:
        xs, ys = wtransform("EPSG:4326", ds.crs, [lon], [lat])
        h = km * 500
        win = from_bounds(xs[0] - h, ys[0] - h, xs[0] + h, ys[0] + h, ds.transform)
        kw = dict(window=win, boundless=True, fill_value=0)
        if out_shape:
            kw["out_shape"] = out_shape
        return ds.read(**kw)


def fetch(name, n_try=8, max_cloud=15, dates="2022-01-01/2025-10-31"):
    out = os.path.join(CACHE, name + ".npz")
    if os.path.exists(out):
        return dict(np.load(out))
    lon, lat, km = SITES[name]
    cl = Client.open(API)
    items = list(cl.search(collections=["sentinel-2-l2a"], intersects=dict(type="Point", coordinates=[lon, lat]), datetime=dates,
                           query={"eo:cloud_cover": {"lt": max_cloud}}, max_items=60).items())
    items.sort(key=lambda it: it.properties.get("eo:cloud_cover", 100))
    px = int(min(1200, km * 100))
    best = None
    for it in items[:n_try]:
        try:
            vis = read_win(it.assets["visual"].href, lon, lat, km, out_shape=(3, px, px))
        except Exception as e:
            print("  fail", e); continue
        valid = (vis.sum(0) > 0).mean()
        bright = ((vis.astype(int).sum(0) > 600)).mean()
        score = bright + (1 - valid) * 5
        print(f"  {it.id} cc={it.properties.get('eo:cloud_cover'):.1f} valid={valid:.2f} bright={bright:.3f}")
        if best is None or score < best[0]:
            best = (score, it, vis)
        if score < 0.01:
            break
    score, it, vis = best
    bands = {}
    for b in ["red", "green", "nir", "swir16"]:
        bands[b] = read_win(it.assets[b].href, lon, lat, km, out_shape=(1, px, px))[0].astype(np.float32)
    np.savez_compressed(out, visual=vis, **bands, meta=np.array(json.dumps(dict(id=it.id, date=it.properties["datetime"][:10], lon=lon, lat=lat, km=km))))
    print(name, it.id, "score", score)
    return dict(np.load(out))


if __name__ == "__main__":
    for n in (sys.argv[1:] or SITES):
        print(n); fetch(n)
