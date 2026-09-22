#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seal.py  ---  NEWIDEAS-D-25-00768 verification package: run + seal

One command does everything:
  1. Runs verify_cs.py and captures its EXACT output to outputs/verification_report.txt
  2. Prints a provenance-mapped verification ledger (every headline number tied to
     its provenance class and its location in the manuscript, via data/provenance.json)
  3. Computes SHA-256 of the declared package files + the captured report
  4. Builds a real binary SHA-256 Merkle tree over those hashes and writes a single
     Merkle root fingerprint for the declared content (MERKLE.json + MANIFEST.json)

The content seal excludes incidental files and build time. Re-running builds a
new seal; authenticating a prior package requires an independently retained root
and manifest. A matching seal proves byte integrity, not empirical validity.

Dependencies: Python 3.8+ standard library only.
"""
import hashlib, json, subprocess, sys, math, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# artifacts produced by THIS script are not themselves sealed (they would be circular)
SEALED_FILES = (
    "CITATION.cff", "LICENSE", "README.md", "data/provenance.json",
    "make_data.py", "outputs/verification_report.txt", "requirements.txt",
    "seal.py", "verify_cs.py",
)

# --- mirrors of the paper's equations, used ONLY to print the ledger ---------
# Identical by construction to verify_cs.py (Definitions A.1, D.1, D.3). The full
# verbatim verify_cs.py report is also captured and sealed, so any divergence is visible.
def _A1(x, ref):
    lg = lambda v: math.log1p(v)
    lo, hi = min(map(lg, ref)), max(map(lg, ref))
    return 0.0 if hi == lo else (lg(x) - lo) / (hi - lo)
def _D3(I, T, R, V):           return (I * T * R * V) ** 0.25

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def collect_files():
    missing = [rel for rel in SEALED_FILES if not (ROOT / rel).is_file()]
    if missing:
        raise FileNotFoundError("Missing required sealed files: " + ", ".join(missing))
    return sorted(SEALED_FILES)

def merkle_root(leaf_hex_list):
    """Binary SHA-256 Merkle tree.
    leaves = SHA-256(file_content) digests (raw bytes), ordered by sorted relpath.
    parent = SHA-256(left || right). Odd node at a level is duplicated.
    Returns (root_hex, levels_hex) where levels_hex[0] are the leaves.
    """
    if not leaf_hex_list:
        return sha256_bytes(b""), [[]]
    level = [bytes.fromhex(h) for h in leaf_hex_list]
    levels = [[h.hex() for h in level]]
    while len(level) > 1:
        if len(level) % 2 == 1:
            level = level + [level[-1]]            # duplicate last
        nxt = [hashlib.sha256(level[i] + level[i + 1]).digest()
               for i in range(0, len(level), 2)]
        levels.append([h.hex() for h in nxt])
        level = nxt
    return level[0].hex(), levels

# ---------------------------------------------------------------------------
def main():
    bar = "=" * 78
    print(bar); print("NEWIDEAS-D-25-00768  VERIFICATION PACKAGE  ---  RUN + SEAL"); print(bar)

    # 1. run the canonical verifier, capture output deterministically
    res = subprocess.run([sys.executable, str(ROOT / "verify_cs.py")],
                         capture_output=True, text=True)
    if res.returncode != 0:
        print("verify_cs.py FAILED:\n", res.stderr); sys.exit(1)
    report = res.stdout
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "verification_report.txt").write_text(report, encoding="utf-8")
    print("\n[1] verify_cs.py executed cleanly; report captured -> outputs/verification_report.txt")

    # 2. provenance-mapped ledger
    prov = json.loads((ROOT / "data" / "provenance.json").read_text(encoding="utf-8"))
    t1 = prov["table1_published"]
    print("\n[2] VERIFICATION LEDGER  (published value  vs  recomputed via paper's equations)")
    print("    class P=PUBLISHED  paper: Table 1, \u00a75.6   equation: D.3 (I*T*R*V)^(1/4)")
    print(f"    {'entity':<11}{'I':>5}{'T':>5}{'R':>5}{'V':>6}{'pubC':>7}{'recomp':>8}  verdict")
    allok = True
    for name in ["Humans","Corvids","Octopus","Fish","Honeybees","Plants","Bacteria","Viruses","AI (LLM)"]:
        r = t1[name]; I,T,R,V,C = r["I"],r["T"],r["R"],r["V"],r["C"]
        raw = _D3(I,T,R,V)
        val = raw; ok = round(val,2) == C
        verdict = "MATCH (D.3)" if ok else "MISMATCH"
        allok = allok and ok
        print(f"    {name:<11}{I:>5.2f}{T:>5.2f}{R:>5.2f}{V:>6.2f}{C:>7.2f}{val:>8.4f}  {verdict}")
    # the A.1 anchor (raven), tied to the worked example
    ref = [1.0e6,1.0e7,5.0e8,1.2e9,1.6e10]; raven = _A1(1.2e9, ref)
    print(f"    A.1 anchor: N(raven=1.2e9 | bee,fish,octopus,raven,human) = {raven:.4f}"
          f"  (paper \u00a75.3-E.5.1: \u2248 0.73)  {'MATCH' if round(raven,2)==0.73 else 'CHECK'}")
    print(f"    --> all published Table 1 capacities reproduced: {allok}")
    capacities_ok = allok
    figure1_ok = True
    figure2_ok = True
    for point in prov["figure1"]["points"]:
        if point["class"] == "ILLUSTRATIVE":
            print(f"    Figure 1: {point['label']} ({point['x']:.2f}, {point['V']:.2f}) retained illustrative input")
            continue
        r = t1[point["entity"]]
        x_itr = (r["I"] * r["T"] * r["R"]) ** (1/3)
        ok = math.isclose(x_itr, point["x"], rel_tol=1e-12) and round(x_itr, 2) == point["printed_x"] and r["V"] == point["V"]
        figure1_ok = figure1_ok and ok
    for point in prov["figure2"]["points"]:
        r = t1[point["entity"]]
        figure2_ok = figure2_ok and (r["I"], r["V"]) == (point["I"], point["V"])
    anchor_ok = round(raven, 2) == 0.73
    allok = capacities_ok and figure1_ok and figure2_ok and anchor_ok
    print(f"    --> Figure 1 formula-derived coordinates reproduced: {figure1_ok}")
    print(f"    --> Figure 2 coordinates reproduced: {figure2_ok}")

    # provenance class census
    print("\n[2b] PROVENANCE CENSUS (what kind of number each input is)")
    se = prov["sourced_empirical"]; ec = prov["evidence_coded"]
    n_pub = len([k for k in t1 if not k.startswith('_')])
    census = {}
    for group, records in se.items():
        if group.startswith("_"):
            continue
        for key, record in records.items():
            if key.startswith("_"):
                continue
            category = record.get("_class", "UNCLASSIFIED")
            census[category] = census.get(category, 0) + 1
    print(f"    PUBLISHED (paper inputs/results) . {n_pub} entity vectors (Table 1)")
    for category, count in sorted(census.items()):
        print(f"    {category:<33} {count} records")
    print("    EVIDENCE_CODED: G/B ordinals, criterion counts, Q tiers, 3 horizon choices.")
    print("    These choices lack a supplied calibration dataset; diagnostic use only.")
    print("    Table 1 capacities and figure projections do not derive from those choices.")
    print("    AI profile: illustrative reference case, not a measurement of 2026 AI.")
    if "known_manuscript_inconsistencies" in prov:
        ki = prov["known_manuscript_inconsistencies"]
        print(f"    note: manuscript rounding corrections synchronized: "
              f"honeybee prose {ki['honeybee_C']['prose']} vs {ki['honeybee_C']['table1_and_calc']}; "
              f"octopus prose {ki['octopus_C']['prose']} vs {ki['octopus_C']['table1_and_calc']}")

    if not allok:
        print("\nVERIFICATION: FAIL; content seals were not regenerated.")
        return 1

    # 3. hash every file
    print("\n[3] SHA-256 OF EACH PACKAGE FILE")
    files = collect_files()
    manifest_files = []
    for rel in files:
        b = (ROOT / rel).read_bytes()
        h = sha256_bytes(b)
        manifest_files.append({"path": rel, "bytes": len(b), "sha256": h})
        print(f"    {h}  {rel}")

    # 4. Merkle tree over the per-file content hashes (ordered by sorted path)
    leaves = [f["sha256"] for f in manifest_files]
    root, levels = merkle_root(leaves)
    built = datetime.datetime.now(datetime.timezone.utc).isoformat()

    manifest = {
        "manuscript": prov["_meta"]["manuscript"]["number"],
        "title": prov["_meta"]["manuscript"]["title"],
        "merkle_algorithm": "SHA-256 binary Merkle; leaves=SHA-256(file content) ordered by sorted POSIX relpath; parent=SHA-256(left||right); odd node duplicated",
        "merkle_root": root,
        "file_count": len(manifest_files),
        "files": manifest_files,
        "verification": {
            "all_table1_capacities_reproduced": capacities_ok,
            "figure1_formula_coordinates_reproduced": figure1_ok,
            "figure2_coordinates_reproduced": figure2_ok,
            "A1_raven_anchor": round(raven, 6),
            "report": "outputs/verification_report.txt"
        }
    }
    (ROOT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    (ROOT / "MERKLE.json").write_text(json.dumps({
        "merkle_root": root,
        "algorithm": manifest["merkle_algorithm"],
        "leaf_count": len(leaves),
        "levels": levels,
        "ordered_leaves": [{"path": f["path"], "leaf_sha256": f["sha256"]} for f in manifest_files]
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n[4] MERKLE SEAL")
    print(f"    build UTC    : {built} (run metadata; outside content seal)")
    print(f"    files sealed : {len(manifest_files)}")
    print(f"    tree height  : {len(levels)} levels")
    print(f"    MERKLE ROOT  : {root}")
    print(f"    written      : MANIFEST.json, MERKLE.json")
    print("\n" + bar)
    print("VERIFICATION: PASS" if allok else "VERIFICATION: FAIL")
    print("To reproduce: retain this root independently, re-run, and compare the content seal.")
    print(bar)
    return 0

if __name__ == "__main__":
    sys.exit(main())
