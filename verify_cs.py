#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EMPIRICAL + MATHEMATICAL VERIFICATION OF C(S)  ---  NEWIDEAS-D-25-00768
Author of paper: Kudzai "King" Chakaingesu

GROUND RULES (per author):
  * Use ONLY the paper's own equations: A.1, E.3, E.4, E.5, E.7, D.3.
  * No external consciousness metric is substituted. No fake functions.
  * Source annotations, manuscript approximations, and illustrative diagnostic
    choices are distinguished; those choices have no supplied calibration data.
  * The author's MATH and published axis VALUES are not changed; this script
    (a) verifies the arithmetic, and (b) exercises diagnostic proxy calculations
    without claiming unique recovery of the published axis estimates.
"""

import math

# ----------------------------------------------------------------------------
# 0. THE PAPER'S EQUATIONS, IMPLEMENTED VERBATIM
# ----------------------------------------------------------------------------

def A1_normalize(x, ref_values, base=math.e):
    """Definition A.1 (Universal Normalization).
        N(x) = [log(1+x) - min_r log(1+x_r)] / [max_r log(1+x_r) - min_r log(1+x_r)]
    Implemented exactly. NOTE: invariant to log base (proved in invariance check).
    ref_values = the reference set R of raw observables {x_r} for this axis/proxy.
    """
    lg = (lambda v: math.log(1.0 + v, base))
    lo = min(lg(r) for r in ref_values)
    hi = max(lg(r) for r in ref_values)
    if hi == lo:
        return 0.0
    return (lg(x) - lo) / (hi - lo)

def E4_quality(Q):
    """Definition E.4: q_j = Q_j / 3,  Q in {0,1,2,3}."""
    return Q / 3.0

def E5_axis_raw(proxies):
    """Definition E.5: X_raw = sum_j a_j * q_j * s_j ,  a_j>=0 , sum a_j = 1.
    proxies = list of (a_j, q_j, s_j).
    """
    assert abs(sum(a for a, _, _ in proxies) - 1.0) < 1e-9, "weights must sum to 1 (E.5 simplex)"
    return sum(a * q * s for (a, q, s) in proxies)

def D3_geometric_mean(I, T, R, V):
    """Definition D.3 (unweighted geometric mean): C = (I*T*R*V)^(1/4)."""
    return (I * T * R * V) ** 0.25

# ============================================================================
# PART A.  VERIFY THE PUBLISHED TABLE 1 ARITHMETIC EXACTLY (pure math, no data)
# ============================================================================
print("="*78)
print("PART A  ---  EXACT RECOMPUTATION OF TABLE 1 VIA D.3  (I*T*R*V)^(1/4)")
print("="*78)

table1 = {
    # entity:        (I,    T,    R,    V,    published_C)
    "Humans":        (0.95, 0.90, 0.92, 0.88, 0.91),
    "Corvids":       (0.70, 0.65, 0.70, 0.70, 0.69),
    "Octopus":       (0.68, 0.70, 0.74, 0.55, 0.66),
    "Fish":          (0.40, 0.40, 0.30, 0.60, 0.41),
    "Honeybees":     (0.35, 0.25, 0.40, 0.20, 0.29),
    "Plants":        (0.20, 0.25, 0.10, 0.05, 0.13),
    "Bacteria":      (0.05, 0.03, 0.04, 0.02, 0.03),
    "Viruses":       (0.00, 0.00, 0.00, 0.00, 0.00),
    "AI (LLM)":      (0.80, 0.20, 0.50, 0.01, 0.17),
}
capacity_closures = {
    "Humans": 0.9121350693, "Corvids": 0.6871505037, "Octopus": 0.6634379959,
    "Fish": 0.4119534288, "Honeybees": 0.2892507609, "Plants": 0.1257433430,
    "Bacteria": 0.0330975092, "Viruses": 0.0000000000, "AI (LLM)": 0.1681792831,
}

print(f"{'Entity':<12}{'I':>5}{'T':>6}{'R':>6}{'V':>6}{'  recomputed':>16}{'  published':>12}{'  status':>10}")
flags = []
for name,(I,T,R,V,pub) in table1.items():
    c = D3_geometric_mean(I,T,R,V)
    assert abs(c - capacity_closures[name]) < 5e-11, name
    diff = c - pub
    status = "MATCH" if abs(round(c,2)-pub) <= 0.005 else "FLAG"
    if status == "FLAG":
        flags.append((name, I,T,R,V, round(c,4), pub))
    print(f"{name:<12}{I:>5.2f}{T:>6.2f}{R:>6.2f}{V:>6.2f}{c:>16.10f}{pub:>12.2f}{status:>10}")

print("\n--- Rows whose printed C(S) differs from the geometric mean of the printed inputs ---")
for (name,I,T,R,V,c,pub) in flags:
    print(f"  {name}: inputs ({I},{T},{R},{V}) -> raw geom mean = {c}, but table prints {pub}")
if not flags:
    print("  None; all nine Table 1 capacities match D.3.")
assert not flags, "Table 1 capacity mismatch"


# ============================================================================
# PART B.  A.1 IS INVARIANT TO LOG BASE  (so 'log' ambiguity is harmless)
# ============================================================================
print("\n"+"="*78)
print("PART B  ---  A.1 LOG-BASE INVARIANCE CHECK")
print("="*78)
ref = [1e6, 1e7, 5e8, 1.2e9, 1.6e10]
x = 1.2e9
for b,label in [(math.e,"ln"),(10,"log10"),(2,"log2")]:
    normalized = A1_normalize(x, ref, base=b)
    print(f"  N(raven) with base {label:<6}= {normalized:.10f}")
    assert abs(normalized - 0.7324198983) < 5e-11
print("  -> identical: min-max ratio cancels the 1/ln(base) factor. 'log' base is immaterial.")


# ============================================================================
# PART C.  DIAGNOSTIC AXIS CALCULATIONS FROM SOURCED AND EVIDENCE-CODED INPUTS
# ============================================================================
print("\n"+"="*78)
print("PART C  ---  DIAGNOSTIC AXIS CALCULATIONS (not recovery of published estimates)")
print("="*78)

SOURCES = {
 # SOURCE ANNOTATIONS: cited quantities, manuscript approximations, and representative inputs.
 "neurons_human_cortex":"1.6e10 cortical; manuscript 2.5 ('roughly 86 billion neurons [32], about 16 billion of which are in the cerebral cortex'); ref [32] Herculano-Houzel 2009",
 "neurons_raven_pallium":"1.2e9 pallial; manuscript 5.3-E.5.1 and 5.4.3; ref [4] Olkowicz et al. 2016 (PNAS)",
 "neurons_octopus_total":"5.0e8 total; manuscript 5.4.2 ('roughly 500 million neurons in Octopus vulgaris'); ref [8]",
 "neurons_fish_repr":"1.0e7 retained illustrative diagnostic assumption; no species-specific measurement or calibrated adult fish count is supplied for this value; the manuscript does not claim a supported adult 1-10M range",
 "neurons_bee":"1.0e6 whole brain; manuscript 5.4.1 ('a brain of only ~1 million neurons')",
 "T_bee":"12 h is the manuscript 5.4.1 lower-bound input ('at least 12+ hours'); ref [60] Van Nest et al. 2018 reports location/time memories and revisits on subsequent days, not an exactly measured 12 h interval",
 "T_fish":"12 d retention; manuscript 5.4.4; ref [16] Ingraham, Anderson, Hurd & Hamilton 2016, Frontiers in Behavioral Neuroscience 10:157, doi:10.3389/fnbeh.2016.00157; reinforced visual-pattern memory tested after 12 d, not a maximum memory span",
 "T_corvid_plan":"17 h flexible planning; manuscript 5.3-E.5.1 and 5.4.3; ref [6] Kabadayi & Osvath 2017",
 "PCI":"PCI*=0.31; effectively perfect sensitivity/specificity on the n=150 benchmark; 94.7% sensitivity in severe brain injury; manuscript 6.5; refs [44,45,46] Casali 2013 / Casarotto 2016 / Comolatti 2019",
 # DERIVED: computed from a qualitative manuscript statement; NOT a stated number.
 "neurons_octopus_central":"~2.0e8 central+optic, DERIVED from manuscript 5.4.2 ('about 2/3 of neurons reside in the arms', so ~1/3 central+optic); supplementary anchor, NOT a stated figure",
 # ESTIMATE: representative value; the manuscript gives only a qualitative horizon (no day count).
 "T_octopus":"~14 d (=2 weeks): ESTIMATE; manuscript 5.4.2 says 'retain those memories for weeks'",
 "T_corvid_cache":"~180 d: ESTIMATE (representative seasonal span); manuscript 5.4.3 says 'seasonal caching ... recovered weeks later'",
 "T_human":"~30 yr: ILLUSTRATIVE ESTIMATE; manuscript describes multi-decade planning qualitatively, with no calibration of this exact value",
}

# ---- C.1  INTEGRATION via declared neuron-count inputs (mixed provenance) ----
print("\n[C.1] INTEGRATION axis, neuron-count proxy s_neurons = A.1(neurons)")
neuron_ref = [1.0e6, 1.0e7, 5.0e8, 1.2e9, 1.6e10]   # bee, fish, octopus_total, raven, human cortex
I_neuron = {
 "Honeybees": 1.0e6,
 "Fish":      1.0e7,
 "Octopus(central+optic)": 2.0e8,
 "Octopus(total)":         5.0e8,
 "Corvids":   1.2e9,
 "Humans":    1.6e10,
}
pub_I = {"Honeybees":0.35,"Fish":0.40,"Octopus(central+optic)":0.68,"Octopus(total)":0.68,"Corvids":0.70,"Humans":0.95}
print(f"  reference set R (neurons): {neuron_ref}")
print(f"  {'system':<26}{'neurons':>12}{'s_neuron(A.1)':>15}{'published I':>13}")
for k,v in I_neuron.items():
    s = A1_normalize(v, neuron_ref)
    print(f"  {k:<26}{v:>12.3g}{s:>15.3f}{pub_I[k]:>13.2f}")

print("\n  Finding: neuron-count alone reproduces the UPPER range well")
print("    corvid 0.732 vs 0.70 ; human 1.000 vs 0.95 ; octopus(total) 0.642 vs 0.68")
print("  but pins bee=0.000 and fish=0.238 (they are near the floor on raw count).")

# Is there ANY single floor that reproduces BOTH bee=0.35 and corvid=0.70? Solve.
print("\n  [C.1b] Does a single reference floor reproduce bee=0.35 AND corvid=0.70?")
def floor_for_target(x, target, ceiling=1.6e10):
    # solve A.1(x)=target for the lower bound m_min (natural log)
    Lx, Lc = math.log(1+x), math.log(1+ceiling)
    # target = (Lx - L)/(Lc - L) -> L = (Lx - target*Lc)/(1-target)
    L = (Lx - target*Lc)/(1-target)
    return math.exp(L)-1
f_bee = floor_for_target(1.0e6, 0.35)
f_cor = floor_for_target(1.2e9, 0.70)
print(f"     floor that makes bee=0.35  : {f_bee:,.3f} neurons")
print(f"     floor that makes corvid=0.70: {f_cor:,.3f} neurons")
print(f"     ratio of the two floors   : {f_cor / f_bee:,.3f}")
assert round(f_bee, 3) == 5447.083
assert round(f_cor, 3) == 2846584.253
assert round(f_cor / f_bee, 3) == 522.589
print("     -> the two required floors differ by orders of magnitude, so NO single")
print("        neuron-count floor fits both declared positions. Additional proxies are")
print("        required to reproduce those positions under the stated implementation.")
print("        This does not uniquely identify proxy assignments or E.6 coefficients.")

# ---- full 3-proxy E.5 for Integration (neuron = hard; G,B = evidence-coded) --
print("\n[C.1c] E.5 diagnostic with 3 proxies (G/B and Q are uncalibrated illustrative choices)")
# evidence-coded G_workspace, B_crossmodal in [0,1]; illustrative choices without a supplied calibration dataset
G_raw = {"Honeybees":0.45,"Fish":0.35,"Octopus(total)":0.55,"Corvids":0.75,"Humans":0.95}
B_raw = {"Honeybees":0.40,"Fish":0.45,"Octopus(total)":0.65,"Corvids":0.70,"Humans":0.95}
# quality tiers Q (E.1): neuron counts Tier3; G,B mostly Tier2 (behavioral+mechanistic), human Tier3
Q_neuron = {"Honeybees":3,"Fish":3,"Octopus(total)":3,"Corvids":3,"Humans":3}
Q_G      = {"Honeybees":2,"Fish":2,"Octopus(total)":2,"Corvids":3,"Humans":3}
Q_B      = {"Honeybees":2,"Fish":2,"Octopus(total)":2,"Corvids":2,"Humans":3}
sysset = ["Honeybees","Fish","Octopus(total)","Corvids","Humans"]
Gref = [G_raw[s] for s in sysset]; Bref=[B_raw[s] for s in sysset]
print(f"  {'system':<16}{'s_neur':>8}{'s_G':>7}{'s_B':>7}{'X_raw(E.5)':>12}{'X_t(E.7)':>10}{'pub I':>7}")
Xraw_store={}
for s in sysset:
    s_n = A1_normalize(I_neuron[s], neuron_ref)
    s_G = A1_normalize(G_raw[s], Gref)
    s_B = A1_normalize(B_raw[s], Bref)
    # equal weights a_j = 1/3 (the minimal-family / D.3-consistent choice; pipeline may fit E.6)
    proxies = [(1/3, E4_quality(Q_neuron[s]), s_n),
               (1/3, E4_quality(Q_G[s]),      s_G),
               (1/3, E4_quality(Q_B[s]),      s_B)]
    Xraw = E5_axis_raw(proxies)
    Xraw_store[s]=Xraw
    print(f"  {s:<16}{s_n:>8.3f}{s_G:>7.3f}{s_B:>7.3f}{Xraw:>12.4f}", end="")
    # placeholder for E.7 printed after we have all X_raw
    print()
# E.7 normalizes X_raw across the clade reference set
Xrefs=list(Xraw_store.values())
print("  --- after E.7 axis normalization X_t = A.1(X_raw) across the set ---")
for s in sysset:
    Xt = A1_normalize(Xraw_store[s], Xrefs)
    print(f"    {s:<16} X_t = {Xt:.3f}   (published I = {pub_I[s]:.2f})")
I_diagnostic = A1_normalize(Xraw_store["Corvids"], Xrefs)
print(f"  Corvid diagnostic I = {I_diagnostic:.10f}; published I = 0.70")
assert abs(I_diagnostic - 0.6663420214) < 5e-11

# ---- C.2  TEMPORAL DEPTH via planning/memory horizon (log seconds) ----------
print("\n[C.2] TEMPORAL DEPTH axis, horizon proxy s_T = A.1(seconds)")
T_secs = {
 "Honeybees": 12*3600,            # 12 h
 "Fish":      12*86400,           # 12 d  (Ingraham et al. 2016)
 "Octopus":   14*86400,           # ~14 d retention
 "Corvids(plan 17h)": 17*3600,    # 17 h  (Kabadayi 2017)
 "Corvids(cache 180d)": 180*86400,# seasonal caching
 "Humans":    30*365*86400,       # ~30 y
}
T_ref = [12*3600, 12*86400, 14*86400, 180*86400, 30*365*86400]
pub_T={"Honeybees":0.25,"Fish":0.40,"Octopus":0.70,"Corvids(plan 17h)":0.65,"Corvids(cache 180d)":0.65,"Humans":0.90}
print(f"  {'system':<22}{'seconds':>13}{'s_T(A.1)':>11}{'pub T':>8}")
for k,v in T_secs.items():
    print(f"  {k:<22}{v:>13.3g}{A1_normalize(v,T_ref):>11.3f}{pub_T[k]:>8.2f}")
print("  Finding: this horizon-only normalization does not preserve all Table 1 ordering.")
print("  The corvid diagnostic uses the illustrative 180-day caching horizon")
print("  (0.59) not the 17h planning horizon (0.04); octopus on pure retention (0.33)")
print("  sits below the paper's 0.70 estimate. These horizon choices do not reconstruct it.")

# ---- C.3  VALENCE via satisfied-criteria count ------------------------------
print("\n[C.3] VALENCE axis, criteria-count proxy s_V = A.1(#criteria of 7)")
# criteria: nociceptors, central proc, harm/reward tradeoff, long-term avoidance,
#           pharmacological modulation, conditioned place aversion, complex/social affect
V_count = {"Honeybees":4.0,"Fish":6.0,"Octopus":6.0,"Corvids":7.0,"Humans":7.0}
V_ref=list(V_count.values())
pub_V={"Honeybees":0.20,"Fish":0.60,"Octopus":0.55,"Corvids":0.70,"Humans":0.88}
print(f"  {'system':<12}{'criteria/7':>12}{'s_V(A.1)':>11}{'pub V':>8}")
for k,v in V_count.items():
    print(f"  {k:<12}{v:>12.1f}{A1_normalize(v,V_ref):>11.3f}{pub_V[k]:>8.2f}")
print("  Finding: criteria-count anchors the floor (bee low) and ceiling (human top)")
print("  but compresses fish/octopus/corvid near 1.0; published values use finer")
print("  affective-richness gradation, consistent with V's multi-criterion definition.")

# ============================================================================
# PART D.  ASSEMBLE C(S) FROM INDEPENDENT AXES vs PUBLISHED  (corvid worked ex)
# ============================================================================
print("\n"+"="*78)
print("PART D  ---  CORVID WORKED EXAMPLE, NOW NUMERIC (Integration), + C(S)")
print("="*78)
I_cor = A1_normalize(1.2e9, neuron_ref)         # neuron proxy only
T_cor = A1_normalize(180*86400, T_ref)          # caching horizon
V_cor = A1_normalize(7.0, V_ref)                # criteria
R_cor_pub = 0.70                                 # R kept from paper (softest to source)
C_cor = D3_geometric_mean(I_cor, T_cor, R_cor_pub, V_cor)
print(f"  Corvid (diagnostic, neuron/horizon/criteria + paper's R):")
print(f"    I={I_cor:.10f}  T={T_cor:.10f}  R={R_cor_pub:.2f}(paper)  V={V_cor:.10f}")
print(f"    C(corvid) = (I*T*R*V)^(1/4) = {C_cor:.10f}   | published C = 0.69")
published_corvid_C = D3_geometric_mean(0.70,0.65,0.70,0.70)
print(f"  Published corvid vector C: {published_corvid_C:.10f} (rounded, 0.69)")
print(f"  Diagnostic minus reported-vector C: {C_cor - published_corvid_C:.10f}")
assert abs(I_cor - 0.7324198983) < 5e-11
assert abs(T_cor - 0.5889485796) < 5e-11
assert abs(C_cor - 0.7412827403) < 5e-11
assert abs(C_cor - published_corvid_C - 0.0541322367) < 5e-11
fish_alternative_C = D3_geometric_mean(0.40,0.40,0.35,0.60)
print(f"  Fish with the stated alternative R=0.35: C={fish_alternative_C:.10f}, rounded {fish_alternative_C:.2f}")
assert round(fish_alternative_C, 2) == 0.43

print("\n"+"="*78)
print("PART E  ---  FIGURE COORDINATES FROM THE REPORTED TABLE 1 VECTORS")
print("="*78)
table2 = [
    ("Plants", "Plants", 0.17, 0.05),
    ("Honeybees", "Honeybees", 0.33, 0.20),
    ("Fish", "Fish", 0.36, 0.60),
    ("Octopus", "Octopus", 0.71, 0.55),
    ("Corvids", "Corvids", 0.68, 0.70),
    ("Humans", "Humans", 0.92, 0.88),
    ("Early automation", None, 0.10, 0.05),
    ("Classical ML", None, 0.35, 0.06),
    ("Current LLMs", "AI (LLM)", 0.43, 0.01),
    ("Speculative advanced AI", None, 0.90, 0.08),
]
print("  Figure 1 / Table 2: x_ITR=(I*T*R)^(1/3), y=V; x_ITR is not C(S).")
for label, entity, printed_x, printed_v in table2:
    if entity is None:
        print(f"    {label:<24} x={printed_x:.2f}  V={printed_v:.2f}  ILLUSTRATIVE (not empirical)")
    else:
        I,T,R,V,pub = table1[entity]
        x_itr = (I*T*R) ** (1/3)
        assert round(x_itr, 2) == printed_x and V == printed_v, label
        assert math.isclose(x_itr ** 0.75 * V ** 0.25, D3_geometric_mean(I,T,R,V), rel_tol=1e-12), label
        print(f"    {label:<24} x={x_itr:.12f}  printed={printed_x:.2f}  V={V:.2f}  MATCH")
print("  The orange risk band is illustrative; its boundary is not a validated threshold.")
figure2 = [
    ("Plants", "Plants", 0.20, 0.05),
    ("Honeybees", "Honeybees", 0.35, 0.20),
    ("Fish", "Fish", 0.40, 0.60),
    ("Octopus", "Octopus", 0.68, 0.55),
    ("Corvids", "Corvids", 0.70, 0.70),
    ("Humans", "Humans", 0.95, 0.88),
    ("Current LLMs", "AI (LLM)", 0.80, 0.01),
]
print("  Figure 2: the seven plotted (I,V) coordinates are unchanged.")
for label, entity, printed_i, printed_v in figure2:
    I,T,R,V,pub = table1[entity]
    assert (I,V) == (printed_i,printed_v), label
    print(f"    {label:<24} I={I:.2f}  V={V:.2f}  MATCH")
print("  Table 3 lists five of these points; Plants and Honeybees appear only in Figure 2.")
print("  Verification scope: arithmetic from reported vectors, diagnostic calculations, and figure coordinates.")
print("  Axis estimates, cited quantities, illustrative choices, and the AI V=0.01 convention are inputs.")
print("  AI (LLM) / Current LLMs denotes an illustrative reference profile, not a 2026 measurement.")
print("  Complete E.6 fits, uncertainty estimates, and empirical validation are not supplied or claimed.")

print("\nDONE.")
