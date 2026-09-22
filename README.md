# Consciousness Capacity Verification — NEWIDEAS-D-25-00768

Independent, dependency-free verification code for the functional consciousness
capacity measure **C(S)** introduced in:

> Kudzai "King" Chakaingesu. *Consciousness as Integrated, Valenced World-Modeling:
> A Non-Anthropocentric Framework for Functional Consciousness Capacity.*
> New Ideas in Psychology. Manuscript **NEWIDEAS-D-25-00768** (under review).

This repository recomputes the paper's scalar capacities from its printed axis
vectors, checks its worked arithmetic and figure coordinates, and records the
provenance and limitations of its inputs. The cryptographic seal fingerprints
the declared package content; it does not establish empirical validity.

---

## 1. What this code establishes

The script `verify_cs.py` implements the listed manuscript equations and runs
five groups of checks. Reported estimates and illustrative diagnostic choices
remain inputs; the package does not reconstruct missing measurements or fitted
E.6 coefficients.

| Part | What it does | Paper reference |
|------|--------------|-----------------|
| A | Recomputes all nine Table 1 capacities as `C = (I·T·R·V)^(1/4)`, including the virus zero vector | Definition D.3; Table 1 (§5.6) |
| B | Confirms the A.1 normalization is invariant to the logarithm base | Definition A.1 (§5.3) |
| C | Exercises conditional proxy diagnostics and shows that no single neuron-count floor fits the declared honeybee and corvid Integration positions | Definitions A.1, E.4, E.5, E.7; §5.3-E.5.1 |
| D | Compares the diagnostic corvid capacity with the reported corvid vector; checks the alternative fish routing value | §5.3-E.5.1; Definition D.3 |
| E | Checks Figure 1 projections and Figure 2 coordinates against the reported vectors; identifies illustrative AI coordinates | Tables 2–3 and Figures 1–2 (§5.6) |

The diagnostic disagreement does not identify unique proxy scores or prove that
the chosen diagnostic ordinals are empirically calibrated. `seal.py` prints a
provenance ledger and builds the content seal only if its ledger checks pass.

---

## 2. Repository contents

```
.
├── verify_cs.py        Arithmetic, conditional diagnostics, and coordinate checks.
├── seal.py             Runner, provenance ledger, and SHA-256 Merkle seal builder.
├── make_data.py        Regenerates data/provenance.json.
├── data/
│   └── provenance.json Inputs, expected results, provenance classes, and limitations.
├── outputs/
│   └── verification_report.txt   Captured output of verify_cs.py.
├── MANIFEST.json       Deterministic per-file SHA-256, sizes, and Merkle root.
├── MERKLE.json         Deterministic Merkle tree and root.
├── requirements.txt    Standard-library dependency declaration.
├── CITATION.cff        Software and article citation.
├── LICENSE             MIT.
└── README.md           This file.
```

---

## 3. Requirements

Python 3.8 or newer. Standard library only. There is nothing to install and no
network access is required.

---

## 4. Running

```bash
python3 make_data.py
python3 seal.py
```

Regenerate provenance after editing `make_data.py`, then run the seal builder.
`seal.py` writes `outputs/verification_report.txt`, `MANIFEST.json`, and
`MERKLE.json`, and prints the ledger. A failed verifier or ledger produces a
nonzero exit status. On a ledger failure the content seals are not replaced;
any existing seal files belong to an earlier run. The captured report is written
before the ledger is checked.

For the numeric report alone, run `python3 verify_cs.py`.

---

## 5. How the code maps to the paper (one to one)

| Code symbol | Manuscript definition | Section |
|-------------|-----------------------|---------|
| `A1_normalize(x, ref)` | A.1, log-plus-one min-max normalization | 5.3 / A |
| `E4_quality(Q)` | E.4, `q = Q/3`, `Q ∈ {0,1,2,3}` | 5.3 / E |
| `E5_axis_raw(proxies)` | E.5, `X_raw = Σ a_j q_j s_j`, `Σ a_j = 1` | 5.3 / E |
| `A1_normalize` at axis level | E.7, `X_t = N(X_raw)` | 5.3 / E |
| `D3_geometric_mean(I,T,R,V)` | D.3, `C = (I·T·R·V)^(1/4)` | 5.3 / D |
| Figure 1 projection | `x_ITR = (I·T·R)^(1/3)`, `y = V` | 5.6 |

All nine Table 1 vectors use D.3. Plants give `0.1257433430 ≈ 0.13` and the
AI reference profile gives `0.1681792831 ≈ 0.17`. The AI value `V = 0.01` is
Convention C.5a's reporting floor, not an additive epsilon or a measured feeling.
The geometric mean retains its zero-product property.

---

## 6. Provenance of every number (read this before citing any value)

`data/provenance.json` distinguishes the following input and output statuses.
Its historical `sourced_empirical` container contains mixed classes; each record
has its own explicit class, which the printed census counts.

| Class | Meaning |
|-------|---------|
| PUBLISHED | Reported axis inputs and capacities; capacities are recalculated from the inputs. |
| SOURCED_EMPIRICAL | Manuscript quantities attributed to named empirical sources; no underlying experiment is replicated here. |
| MANUSCRIPT_APPROXIMATION | Approximate manuscript counts, including honeybee and total octopus neurons. |
| DIAGNOSTIC_ASSUMPTION | The retained fish `10⁷` neuron input has no supplied species-specific calibration; it does not establish an adult fish count or range. |
| DERIVED_ESTIMATE | The rounded octopus central-plus-optic estimate derived from a qualitative proportion. |
| MANUSCRIPT_LOWER_BOUND | The honeybee 12-hour manuscript lower bound; the cited study does not measure that exact interval. |
| SOURCE_UNRESOLVED | A retained input whose exact study attribution still requires resolution. |
| EVIDENCE_CODED | Existing illustrative diagnostic ordinals, quality tiers, criterion counts, and horizon choices. |
| ILLUSTRATIVE | Retained plotting coordinates without empirical calibration. |
| COMPUTED | Values produced by the declared equations and figure projection. |

The G/B ordinal values, quality tiers, valence counts, and illustrative horizons
of 14 days, 180 days, and 30 years have no supplied numerical calibration dataset
or item-level coding record. They remain explicitly conditional diagnostic
inputs, not recovered E.6 coefficients. None generates the published Table 1
vectors. The diagnostic corvid Integration depends on the G/B/Q assignments and
equal proxy weights. The separate diagnostic corvid capacity uses neuron-only
Integration, the chosen caching horizon and temporal reference set, criterion-count
Valence, and the paper's Routing value.

The existing `AI (LLM)` and `Current LLMs` labels denote the manuscript's
illustrative reference profile `(0.80, 0.20, 0.50, 0.01)`. They are not a
measurement of all AI systems in 2026. Contemporary capability results do not
by themselves supply calibrated replacements on this paper's axes.

Honeybee and octopus prose capacities have been synchronized to `0.29` and
`0.66`. All nine scalar capacities now match the printed vectors under D.3.

---

## 7. Cryptographic integrity

`seal.py` seals exactly nine required content files: `CITATION.cff`, `LICENSE`,
`README.md`, `data/provenance.json`, `make_data.py`,
`outputs/verification_report.txt`, `requirements.txt`, `seal.py`, and
`verify_cs.py`. Missing required files fail the build. Incidental files such as
`.DS_Store`, caches, and version-control metadata are outside this declared scope;
they are neither deleted nor authenticated by the seal.

`MANIFEST.json` lists each sealed path, size, and SHA-256 digest. `MERKLE.json`
records the tree and root. The two seal files are excluded from their own tree to
avoid circular hashing. Build time is printed only as run metadata, outside the
deterministic content seal.

Each leaf is `SHA-256(file content)`, ordered by sorted POSIX relative path.
Each parent is `SHA-256(left ‖ right)` over raw 32-byte digests; an odd node is
duplicated. The top node is the root. The manifest binds the listed paths to
the digests; the root itself summarizes the ordered content digests.

To authenticate a received package, retain a trusted root and manifest independently,
compare the received files with that manifest, and independently rebuild the tree.
Running `seal.py` rebuilds the seal for the files currently present; it does not
authenticate them against a previously trusted fingerprint. Re-running after a
change therefore cannot establish that the original package was unchanged.

Hashes prove integrity relative to a trusted reference. They do not prove a
scientific claim, validate an assumption, or independently establish a publication
date or priority claim.

---

## 8. Reproducibility

The calculations use fixed inputs without randomness or network data. On the
tested runtime, repeated runs reproduce the report, manifest, and Merkle tree
byte-for-byte, even when unrelated OS metadata changes. Floating-point library
differences across runtimes can affect formatted last digits; cross-platform
identity must be checked rather than assumed.

---

## 9. Citation

See `CITATION.cff`. Please cite both the article and this repository.

Repository: https://github.com/KudzaiKing1/Consciousness-as-Integrated-Valenced-World-Modeling-Code-

---

## 10. License

MIT. See `LICENSE`.
