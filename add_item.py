#!/usr/bin/env python3
"""편 추가: 썸네일을 줄여 img/ 에 복사하고 data/items.json 맨 앞에 추가(같은 id면 덮어씀).
사용: python add_item.py --id ep04 --date 2026-11-28 --title "제목" --keyword 키워드 \
        --cover "C:/경로/cover.jpg" --product "상품명" --url "https://link.coupang.com/a/..." [--reel URL] [--note 메모]
"""
import argparse, json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
DEFAULT_URL = "https://influencers.coupang.com/s/temfind"

def main():
    a = argparse.ArgumentParser()
    a.add_argument("--id", required=True)
    a.add_argument("--date", required=True)
    a.add_argument("--title", required=True)
    a.add_argument("--keyword", required=True)
    a.add_argument("--cover", required=True)
    a.add_argument("--product", required=True)
    a.add_argument("--url", default=DEFAULT_URL)
    a.add_argument("--reel", default="")
    a.add_argument("--note", default="")
    g = a.parse_args()

    im = Image.open(g.cover).convert("RGB")
    w = 480
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    out = ROOT / "img" / f"{g.id}.jpg"
    q = 85
    while True:
        im.save(out, "JPEG", quality=q, optimize=True)
        if out.stat().st_size <= 200_000 or q <= 40:
            break
        q -= 5

    f = ROOT / "data" / "items.json"
    data = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {"items": []}
    item = {"id": g.id, "date": g.date, "title": g.title, "keyword": g.keyword,
            "thumb": f"img/{g.id}.jpg", "reel": g.reel,
            "products": [{"name": g.product, "url": g.url, "note": g.note}]}
    data["items"] = [i for i in data["items"] if i["id"] != g.id] + [item]
    data["items"].sort(key=lambda i: (i["date"], i["id"]), reverse=True)  # 최신 날짜, 같은 날은 id 큰 것이 위
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK {g.id}: {out.name} {out.stat().st_size//1024}KB, 총 {len(data['items'])}편")

if __name__ == "__main__":
    sys.exit(main())
