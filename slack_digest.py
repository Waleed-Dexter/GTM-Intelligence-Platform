import os, pandas as pd
from pathlib import Path
import requests

WEBHOOK = os.environ.get("SLACK_WEBHOOK_URL")
if not WEBHOOK:
    raise SystemExit("Missing SLACK_WEBHOOK_URL environment variable.")

out_dir = Path("out")
sc = out_dir / "signals_classified.csv"
cc = out_dir / "category_counts.csv"

if not sc.exists():
    raise SystemExit("signals_classified.csv not found. Run GTM_Intel_Task2.py first.")

cat_top = ""
if cc.exists():
    cat_df = pd.read_csv(cc).sort_values("count", ascending=False).head(3)
    cat_top = ", ".join([f"{r['category']} ({r['count']})" for _, r in cat_df.iterrows()])

df = pd.read_csv(sc).head(3)
lines = [":newspaper: *GTM Intel — Revolut (daily)*"]
if cat_top:
    lines.append(f"_Top categories:_ {cat_top}")
for _, r in df.iterrows():
    lines.append(f"• {r['date']} — *{r['title']}*  ({r['source']})\n  {r['url']}")

resp = requests.post(WEBHOOK, json={"text": "\n".join(lines)}, timeout=10)
resp.raise_for_status()
print("Slack digest posted.")
