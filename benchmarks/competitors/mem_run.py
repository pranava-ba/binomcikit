import json
import os
import subprocess
import sys

SP = os.path.dirname(os.path.abspath(__file__))
rows = []
cases = [
    ("binomcikit.ci", 10000),
    ("binomcikit.limits", 10000),
    ("statsmodels", 10000),
    ("astropy", 10000),
    ("DBCI", 1000),
    ("binoculars", 1000),
    ("scipy", 1000),
]
for method in ("wilson", "exact"):
    for pkg, n in cases:
        if pkg == "astropy" and method == "exact":
            continue
        r = subprocess.run(
            [sys.executable, os.path.join(SP, "mem_child.py"), pkg, method, str(n)],
            capture_output=True,
            text=True,
        )
        line = [l for l in r.stdout.splitlines() if l.startswith("{")]
        if line:
            rows.append(json.loads(line[-1]))
            print(line[-1], flush=True)
        else:
            print("FAIL", pkg, method, r.stderr[-200:])
json.dump(rows, open(os.path.join(SP, "data", "memory.json"), "w"), indent=1)
