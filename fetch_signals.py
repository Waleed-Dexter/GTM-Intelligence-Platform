import re, hashlib, datetime as dt
from pathlib import Path
import pandas as pd
import feedparser, yaml

OUT_CSV = "signals_template.csv"

def normalize_text(s): 
    return re.sub(r"\s+", " ", str(s or "")).strip()

def row_key(url, title):
    h = hashlib.sha256((normalize_text(url) + "|" + normalize_text(title)).encode("utf-8")).hexdigest()
    return h[:16]

def is_match(title_snippet, include, exclude):
    text = title_snippet.lower()
    if include and not any(k.lower() in text for k in include):
        return False
    if exclude and any(k.lower() in text for k in exclude):
        return False
    return True

def parse_date(entry):
    try:
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            return dt.date(*entry.published_parsed[:3]).isoformat()
    except Exception:
        pass
    return dt.date.today().isoformat()

def collect_from_feed(url, limit):
    parsed = feedparser.parse(url)
    entries = parsed.entries[:limit] if limit else parsed.entries
    out = []
    for e in entries:
        title = normalize_text(getattr(e, "title", ""))
        link  = normalize_text(getattr(e, "link", ""))
        desc  = normalize_text(getattr(e, "summary", getattr(e, "description", "")))
        date  = parse_date(e)
        source= normalize_text(getattr(e, "source", {}).get("title", "")) or normalize_text(parsed.feed.get("title", ""))
        out.append({"date": date, "source": source, "title": title, "url": link, "snippet": desc})
    return out

def main():
    cfg = yaml.safe_load(Path("sources.yml").read_text(encoding="utf-8"))
    include = cfg.get("keywords", {}).get("include", [])
    exclude = cfg.get("keywords", {}).get("exclude", [])
    feeds   = cfg.get("feeds", [])
    limit   = int(cfg.get("max_items_per_feed", 25))

    rows, seen = [], set()
    for feed in feeds:
        try:
            for item in collect_from_feed(feed, limit):
                hay = f"{item['title']} {item['snippet']}"
                if not is_match(hay, include, exclude):
                    continue
                key = row_key(item["url"], item["title"])
                if key in seen:
                    continue
                seen.add(key)
                rows.append(item)
        except Exception as e:
            print(f"[warn] feed failed: {feed} -> {e}")

    df = pd.DataFrame(rows).drop_duplicates(subset=["url","title"])
    if "date" in df.columns:
        df = df.sort_values("date", ascending=False)
    df = df.head(25)

    cols = ["date","source","title","url","snippet"]
    for c in cols:
        if c not in df.columns: df[c] = ""
    df = df[cols]
    df.to_csv(OUT_CSV, index=False)
    print(f"Wrote {OUT_CSV} with {len(df)} rows.")

if __name__ == "__main__":
    main()
