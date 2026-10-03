import datetime
import json
import os
import re
import subprocess
import urllib.request

SP = os.path.dirname(os.path.abspath(__file__))
today = datetime.date.today().isoformat()
since = (datetime.date.today() - datetime.timedelta(days=365)).isoformat()


def gh(path, paginate_count=False):
    r = subprocess.run(["gh", "api", "-i", path], capture_output=True, text=True, encoding="utf-8")
    head, _, body = (
        r.stdout.partition("\r\n\r\n") if "\r\n\r\n" in r.stdout else r.stdout.partition("\n\n")
    )
    return head, body


def jgh(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8")
    try:
        return json.loads(r.stdout)
    except Exception:
        return None


def count(path):
    sep = "&" if "?" in path else "?"
    head, body = gh(path + sep + "per_page=1")
    m = re.search(r'page=(\d+)>; rel="last"', head)
    if m:
        return int(m.group(1))
    try:
        return len(json.loads(body))
    except Exception:
        return None


def pypi(name):
    try:
        d = json.load(urllib.request.urlopen(f"https://pypi.org/pypi/{name}/json", timeout=30))
        rel = d["releases"]
        dates = sorted(min(f["upload_time"] for f in fs)[:10] for v, fs in rel.items() if fs)
        return {
            "latest": d["info"]["version"],
            "n_releases": len(dates),
            "first": dates[0] if dates else None,
            "last": dates[-1] if dates else None,
            "releases_last_12m": sum(1 for x in dates if x >= since),
            "requires_python": d["info"].get("requires_python"),
        }
    except Exception as e:
        return {"err": str(e)}


def dl(name):
    try:
        return json.load(
            urllib.request.urlopen(f"https://pypistats.org/api/packages/{name}/recent", timeout=30)
        )["data"]
    except Exception as e:
        return {"err": str(e)}


repos = {
    "DBCI": ("DeepPSP/DBCI", "diff-binom-confint"),
    "binomial_cis": ("TRI-ML/binomial_cis", "binomial-cis"),
    "pynomial": ("Silver-Creek/pynomial", "pynomial"),
    "binoculars": ("nolanbconaway/binoculars", "binoculars"),
    "confseq": ("gostevehoward/confseq", "confseq"),
    "statsmodels": ("statsmodels/statsmodels", "statsmodels"),
    "astropy": ("astropy/astropy", "astropy"),
    "scipy": ("scipy/scipy", "scipy"),
    "DescTools": ("AndriSignorell/DescTools", None),
    "binomcikit": ("pranava-ba/binomcikit", "binomcikit"),
}
out = {"measured": today, "since": since, "repos": {}}
for k, (r, pk) in repos.items():
    j = jgh(f"repos/{r}") or {}
    e = {
        "repo": r,
        "stars": j.get("stargazers_count"),
        "forks": j.get("forks_count"),
        "watchers": j.get("subscribers_count"),
        "open_issues_plus_prs": j.get("open_issues_count"),
        "license": (j.get("license") or {}).get("spdx_id"),
        "created": (j.get("created_at") or "")[:10],
        "pushed": (j.get("pushed_at") or "")[:10],
        "archived": j.get("archived"),
        "size_kb": j.get("size"),
        "default_branch": j.get("default_branch"),
    }
    e["commits_12m"] = count(f"repos/{r}/commits?since={since}T00:00:00Z")
    e["contributors"] = count(f"repos/{r}/contributors?anon=1")
    e["tags"] = count(f"repos/{r}/tags")
    e["gh_releases"] = count(f"repos/{r}/releases")
    for state in ("open", "closed"):
        s = jgh(f"search/issues?q=repo:{r}+type:issue+state:{state}&per_page=1")
        e[f"issues_{state}"] = (s or {}).get("total_count")
        s = jgh(f"search/issues?q=repo:{r}+type:pr+state:{state}&per_page=1")
        e[f"prs_{state}"] = (s or {}).get("total_count")
    top = jgh(f"repos/{r}/contributors?per_page=1") or []
    e["top_contrib_commits"] = top[0]["contributions"] if top else None
    if pk:
        e["pypi"] = pypi(pk)
        e["downloads"] = dl(pk)
    out["repos"][k] = e
    print(k, e["stars"], e["commits_12m"], e["contributors"], flush=True)
json.dump(out, open(os.path.join(SP, "data", "activity.json"), "w"), indent=1)
