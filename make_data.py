#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_data.py  ---  emits data/provenance.json
This data-authoring script records capacity inputs and computes figure projections;
it records, for every number that appears in verify_cs.py, what the number is,
which provenance class it belongs to, the exact source, and where it lives in
the manuscript NEWIDEAS-D-25-00768. Run once; the JSON is the artifact.
"""
import json, pathlib

PROV = {
  "_meta": {
    "file": "provenance.json",
    "purpose": "1:1 provenance for every numeric input/output used by verify_cs.py.",
    "manuscript": {
      "number": "NEWIDEAS-D-25-00768",
      "title": "Consciousness as Integrated, Valenced World-Modeling: A Non-Anthropocentric Framework for Functional Consciousness Capacity",
      "author": "Kudzai \u201cKing\u201d Chakaingesu",
      "journal": "New Ideas in Psychology"
    },
    "provenance_classes": {
      "PUBLISHED":        "A value reported in the manuscript itself (Table 1 axis scores and C(S)). These are the paper's results.",
      "SOURCED_EMPIRICAL":"A manuscript-reported quantity attributed to a named empirical source; this package does not replicate the underlying experiment.",
      "MANUSCRIPT_APPROXIMATION":"An approximate manuscript input, not an exact study measurement.",
      "DIAGNOSTIC_ASSUMPTION":"A retained illustrative diagnostic input without a supplied empirical calibration or exact species-specific measurement.",
      "DERIVED_ESTIMATE":"A rounded estimate derived from a qualitative manuscript proportion, not a directly measured count.",
      "MANUSCRIPT_LOWER_BOUND":"A manuscript lower-bound input, not an exactly measured experimental interval.",
      "SOURCE_UNRESOLVED":"A retained manuscript input whose exact study attribution requires resolution.",
      "EVIDENCE_CODED":   "An existing illustrative diagnostic choice. No supplied data matrix, coding protocol, inter-rater record, or fitted coefficients calibrate its exact numerical value. Used in Parts C/D only, not to derive Table 1.",
      "ILLUSTRATIVE":     "A retained plotting coordinate, not a measured or fitted axis estimate.",
      "COMPUTED":         "A value produced by the paper's equations (A.1, D.3, E.4, E.5, E.7) or Figure 1 projection inside the script."
    }
  },

  "equation_map": [
    {"code": "A1_normalize", "paper": "Definition A.1 (Universal Normalization)", "section": "5.3 / Part A", "note": "log(1+x) then min-max over the reference set R; invariant to log base."},
    {"code": "E4_quality",   "paper": "Definition E.4 (Evidence-Quality Weighting), q=Q/3", "section": "5.3 / Part E", "note": "Q in {0,1,2,3} quality tier from Definition E.1."},
    {"code": "E5_axis_raw",  "paper": "Definition E.5 (Axis Raw Construction / Empirical Allocation Law)", "section": "5.3 / Part E", "note": "X_raw = sum_j a_j q_j s_j, a_j>=0, sum a_j = 1 (simplex)."},
    {"code": "A1_normalize (axis-level)", "paper": "Definition E.7 (Axis Normalization)", "section": "5.3 / Part E", "note": "X_t = N(X_raw) across the clade reference set."},
    {"code": "D3_geometric_mean", "paper": "Definition D.3 (Geometric-Mean Specialization), C=(I*T*R*V)^(1/4)", "section": "5.3 / Part D", "note": "alpha=beta=gamma=delta=1 specialization of D.1."},
    {"code": "x_itr", "paper": "Figure 1 visualization coordinate, x_ITR=(I*T*R)^(1/3)", "section": "5.6 / Table 2 and Figure 1", "note": "Projection only, not an alternative capacity law; C=x_ITR^(3/4)*V^(1/4)."}
  ],

  "table1_published": {
    "_class": "PUBLISHED",
    "_paper_location": "Table 1, \u00a75.6 (Summary Tables and Figures)",
    "_note": "Axis scores are evidence-anchored first-pass estimates. Every reported C(S) is the geometric mean (D.3) of the printed axis scores. AI V=0.01 is the reporting-floor convention C.5a, not an additive safeguard or an observed affective state.",
    "Humans":    {"I":0.95,"T":0.90,"R":0.92,"V":0.88,"C":0.91},
    "Corvids":   {"I":0.70,"T":0.65,"R":0.70,"V":0.70,"C":0.69},
    "Octopus":   {"I":0.68,"T":0.70,"R":0.74,"V":0.55,"C":0.66},
    "Fish":      {"I":0.40,"T":0.40,"R":0.30,"V":0.60,"C":0.41},
    "Honeybees": {"I":0.35,"T":0.25,"R":0.40,"V":0.20,"C":0.29},
    "Plants":    {"I":0.20,"T":0.25,"R":0.10,"V":0.05,"C":0.13},
    "Bacteria":  {"I":0.05,"T":0.03,"R":0.04,"V":0.02,"C":0.03},
    "Viruses":   {"I":0.00,"T":0.00,"R":0.00,"V":0.00,"C":0.00,
                  "_note":"Domain constraint (Definition C.6); the zero vector is included in the Part A arithmetic verification."},
    "AI (LLM)":  {"I":0.80,"T":0.20,"R":0.50,"V":0.01,"C":0.17, "_status":"ILLUSTRATIVE_REFERENCE_PROFILE", "_note":"Retained reference case for the manuscript; not an empirically calibrated measurement of 2026 AI systems. I/T/R have no supplied fitted proxy dataset; V=0.01 is Convention C.5a."}
  },

  "sourced_empirical": {
    "_class": "MIXED_PROVENANCE",
    "_note": "The historical container name is retained; each record has its own explicit provenance class.",
    "neuron_counts": {
      "_unit": "neurons",
      "_use": "Integration proxy s_neuron via A.1; reference set R for normalization.",
      "honeybee_1e6":   {"_class": "MANUSCRIPT_APPROXIMATION", "value": 1.0e6,  "paper": "\u00a75.4.1 (\u2018~1 million neurons\u2019); reference set in \u00a75.3-E.5.1", "source": "manuscript-stated (\u00a75.4.1: 'a brain of only ~1 million neurons')"},
      "fish_1e7":       {"_class": "DIAGNOSTIC_ASSUMPTION", "value": 1.0e7,  "paper": "Diagnostic reference set in \u00a75.3-E.5.1; \u00a75.4.4 does not report a measured adult 10M count.", "source": "Retained illustrative diagnostic assumption of 10 million neurons; no source calibrates this exact species-specific value. It is not evidence for an adult 1-10M range."},
      "octopus_total_5e8": {"_class": "MANUSCRIPT_APPROXIMATION", "value": 5.0e8, "paper": "\u00a75.4.2 (\u2018roughly 500 million neurons in Octopus vulgaris\u2019 [8]); reference set in \u00a75.3-E.5.1", "source": "manuscript ref [8] (Natural History Museum 2023)"},
      "octopus_central_optic_2e8": {"_class": "DERIVED_ESTIMATE", "value": 2.0e8, "paper": "derived from \u00a75.4.2 (\u2018about 2/3 of neurons reside in the arms\u2019 \u2192 ~1/3 central+optic \u2248 167M)", "source": "derived from manuscript \u00a75.4.2 only", "class_override": "DERIVED (computed from the manuscript qualitative 2/3-in-arms statement; not a measurement and not a stated figure)"},
      "raven_1.2e9":    {"_class": "SOURCED_EMPIRICAL", "value": 1.2e9,  "paper": "\u00a75.3-E.5.1 and \u00a75.4.3 (\u2018~1.2 \u00d7 10^9 pallial neurons\u2019 [4])", "source": "manuscript ref [4] (Olkowicz et al. 2016, PNAS)"},
      "human_cortex_1.6e10": {"_class": "SOURCED_EMPIRICAL", "value": 1.6e10, "paper": "\u00a72.5 (\u2018about 16 billion \u2026 in the cerebral cortex\u2019 [32]); reference set in \u00a75.3-E.5.1", "source": "manuscript ref [32] (Herculano-Houzel 2009). Note: Azevedo et al. 2009 is the primary source for this count but is NOT in the manuscript reference list, so it is not claimed."}
    },
    "temporal_horizons": {
      "_unit": "seconds (converted from the stated horizon)",
      "_use": "Temporal-depth proxy s_T via A.1.",
      "bee_12h":        {"_class": "MANUSCRIPT_LOWER_BOUND", "value_s": 43200,    "stated": "\u2265 12 hours location memory", "paper": "\u00a75.4.1 (\u2018at least 12+ hours\u2019)", "source": "Manuscript ref [60], Van Nest, Otto & Moore (2018), https://doi.org/10.1242/jeb.187336. The study reports location/time memories and revisits on subsequent days, not an exactly measured 12 h interval.", "class_override": "MANUSCRIPT_LOWER_BOUND: 43200 seconds retains the manuscript's 12 h lower bound as the diagnostic input; it is not a verbatim study measurement."},
      "fish_12d":       {"_class": "SOURCED_EMPIRICAL", "value_s": 1036800,  "stated": "reinforced visual-pattern memory tested after 12 days", "paper": "\u00a75.4.4, ref [16] (12-day retention test)", "source": "Ingraham, Anderson, Hurd & Hamilton (2016), Frontiers in Behavioral Neuroscience 10:157, https://doi.org/10.3389/fnbeh.2016.00157. Observed retention after the tested delay, not a maximum fish memory span."},
      "corvid_plan_17h":{"_class": "SOURCED_EMPIRICAL", "value_s": 61200,    "stated": "17 hours flexible planning", "paper": "\u00a75.3-E.5.1 and \u00a75.4.3 (\u2018planning up to 17 hours ahead \u2026 [6]\u2019)", "source": "manuscript ref [6] (Kabadayi & Osvath 2017, Science)"}
    },
    "pci": {
      "_use": "Convergent-validity anchor cited in \u00a76.5; not an input to C(S).",
      "PCI_star_0.31":  {"_class": "SOURCED_EMPIRICAL", "value": 0.31,  "paper": "\u00a76.5 (\u2018empirical cutoff, PCI* = 0.31\u2019)", "source": "manuscript refs [44,45,46] (Casali 2013; Casarotto 2016; Comolatti 2019)"},
      "sensitivity_94_7": {"_class": "SOURCED_EMPIRICAL", "value": 0.947, "paper": "\u00a76.5 (\u201894.7% sensitivity\u2019)", "source": "manuscript refs [44,45,46]"},
      "benchmark_n_150":  {"_class": "SOURCED_EMPIRICAL", "value": 150, "paper": "\u00a76.5 (\u2018benchmark population of 150 \u2026 subjects\u2019)", "source": "manuscript refs [44,45,46]"},
      "_note_on_code_annotations": "Earlier the code SOURCES string listed '94.7% on 81 DOC' and '92% on n=24'. Those granular figures come from the underlying PCI literature (Casarotto 2016; Casali 2013) but are NOT stated in manuscript \u00a76.5. They were removed from the code; only the manuscript-stated figures (PCI*=0.31, 94.7% sensitivity, n=150) are retained."
    }
  },

  "evidence_coded": {
    "_class": "EVIDENCE_CODED",
    "_warning": "These retained choices are not direct measurements or fitted estimates. The package supplies no numerical calibration data for their exact values. They exercise Parts C/D conditionally and do not derive any Table 1 value.",
    "integration_proxy_G_workspace": {
      "_definition": "global-broadcasting / workspace-like dynamics proxy (Definition C.1 G_workspace), in [0,1]",
      "values": {"Honeybees":0.45,"Fish":0.35,"Octopus(total)":0.55,"Corvids":0.75,"Humans":0.95},
      "basis": "Illustrative ordinal assignment; no study-to-score calibration, coding record, or evidence of target independence is supplied."
    },
    "integration_proxy_B_crossmodal": {
      "_definition": "cross-modal binding proxy (Definition C.1 B_crossmodal), in [0,1]",
      "values": {"Honeybees":0.40,"Fish":0.45,"Octopus(total)":0.65,"Corvids":0.70,"Humans":0.95},
      "basis": "Illustrative ordinal assignment; no study-to-score calibration or coding record is supplied."
    },
    "valence_criteria_count": {
      "_definition": "count of satisfied valence criteria out of 7 (nociceptors, central processing, harm/reward trade-off, long-term avoidance, pharmacological modulation, conditioned place aversion, complex/social affect)",
      "values": {"Honeybees":4,"Fish":6,"Octopus":6,"Corvids":7,"Humans":7},
      "basis": "Illustrative criterion counts informed by pain-criteria literature; no species-by-criterion evidence matrix or documented coding process is supplied."
    },
    "quality_tiers_Q": {
      "_definition": "Definition E.1 evidence tier Q in {0,1,2,3}; q=Q/3 (Definition E.4)",
      "values": {"neuron_counts": 3, "G_workspace_nonhuman": 2, "B_crossmodal_nonhuman": 2, "human_all": 3, "corvid_G": 3},
      "basis": "Illustrative tier assignment using the E.1 rubric; no item-level evidence grading record is supplied."
    },
    "horizon_estimates": {
      "_warning": "Representative horizons used in Part C that are estimates, not verbatim manuscript figures.",
      "T_octopus_14d": {"value_s": 1209600, "manuscript_says": "\u2018retain those memories for weeks\u2019 (\u00a75.4.2, ref [9]); \u2018days-to-weeks\u2019", "status": "14 d (=2 weeks) is a representative concretization of \u2018weeks\u2019, not a stated figure"},
      "T_corvid_cache_180d": {"value_s": 15552000, "manuscript_says": "\u2018cache \u2026 over a season and recover them weeks later\u2019; \u2018seasonal caching\u2019 (\u00a75.4.3, ref [34])", "status": "180 d is a representative seasonal span; the manuscript states seasonal caching with weeks-scale recovery, not 180 d"},
      "T_human_30y": {"value_s": 946080000, "manuscript_says": "multi-decade planning (qualitative)", "status": "Illustrative 30-year choice; no experiment establishes this exact value or its conservativeness."}
    }
  },

  "code_source_annotation_corrections": {
    "_date": "2026-06-08",
    "_scope": "Historical annotation-only correction record, not a description of subsequent revisions: ONLY descriptive SOURCES annotation strings in verify_cs.py were corrected. No computed value, equation, axis score, or program output changed; the verification report is byte-identical before and after.",
    "removed_because_not_in_manuscript": [
      "human: 'Azevedo et al. 2009' (manuscript cites only Herculano-Houzel 2009, ref [32])",
      "honeybee: '~960k' (manuscript states '~1 million')",
      "octopus total: 'OIST 2020' and 'Young' (manuscript cites ref [8] Natural History Museum 2023)",
      "octopus central: '40-45M central + 120-180M optic; Nature Lab Animal 2014' (reclassified DERIVED from the manuscript 2/3-in-arms statement)",
      "PCI: '94.7% on 81 DOC' and '92% on n=24' (manuscript 6.5 states only 0.31, 94.7% sensitivity, n=150)"
    ],
    "reclassified": [
      "octopus central+optic ~2.0e8: SOURCED_EMPIRICAL -> DERIVED"
    ],
    "marked_as_estimate_in_code": [
      "T_octopus ~14 d (manuscript: 'weeks')",
      "T_corvid_cache ~180 d (manuscript: 'seasonal caching ... recovered weeks later')",
      "T_human ~30 yr (conservative)"
    ]
  },
  "known_manuscript_inconsistencies": {
    "_note": "The authorized manuscript corrections synchronize these prose values with Table 1 and D.3.",
    "honeybee_C": {"prose": 0.29, "table1_and_calc": 0.29, "exact": 0.2892507609, "fix": "prose synchronized to 0.29 in \u00a75.4.1"},
    "octopus_C":  {"prose": 0.66, "table1_and_calc": 0.66, "exact": 0.6634379959, "fix": "prose synchronized to 0.66 in \u00a75.4.2"}
  }
}

PROV["figure1"] = {
    "_paper_location": "Table 2 and Figure 1, \u00a75.6",
    "_equation": "x_ITR=(I*T*R)^(1/3), y=V; C=x_ITR^(3/4)*V^(1/4)",
    "_note": "Projection of reported inputs, not a second capacity law. Current LLMs is the illustrative AI reference profile; the other AI coordinates and risk band are also illustrative, not empirically validated measurements or thresholds.",
    "points": [
        {"label": label, "entity": entity, "class": "COMPUTED", "x": (PROV["table1_published"][entity]["I"] * PROV["table1_published"][entity]["T"] * PROV["table1_published"][entity]["R"]) ** (1/3), "printed_x": printed_x, "V": PROV["table1_published"][entity]["V"]}
        for label, entity, printed_x in [("Plants","Plants",0.17),("Honeybees","Honeybees",0.33),("Fish","Fish",0.36),("Octopus","Octopus",0.71),("Corvids","Corvids",0.68),("Humans","Humans",0.92)]
    ] + [
        {"label": "Early automation", "class": "ILLUSTRATIVE", "x": 0.10, "printed_x": 0.10, "V": 0.05},
        {"label": "Classical ML", "class": "ILLUSTRATIVE", "x": 0.35, "printed_x": 0.35, "V": 0.06},
        {"label": "Current LLMs", "entity": "AI (LLM)", "class": "COMPUTED", "x": (0.80*0.20*0.50) ** (1/3), "printed_x": 0.43, "V": 0.01},
        {"label": "Speculative advanced AI", "class": "ILLUSTRATIVE", "x": 0.90, "printed_x": 0.90, "V": 0.08}
    ]
}
PROV["figure2"] = {
    "_paper_location": "Figure 2, \u00a75.6",
    "_equation": "x=I, y=V",
    "_note": "The seven plotted points are unchanged; Table 3 lists the five points other than Plants and Honeybees.",
    "points": [
        {"label": label, "entity": entity, "class": "PUBLISHED", "I": PROV["table1_published"][entity]["I"], "V": PROV["table1_published"][entity]["V"]}
        for label, entity in [("Plants","Plants"),("Honeybees","Honeybees"),("Fish","Fish"),("Octopus","Octopus"),("Corvids","Corvids"),("Humans","Humans"),("Current LLMs","AI (LLM)")]
    ]
}
PROV["verification_scope"] = {
    "recomputed": "Nine Table 1 capacities; A.1 log-base invariance; reported corvid floor solutions, ratio, diagnostic I, diagnostic C and capacity difference; alternative fish C; seven formula-derived Figure 1 coordinates and seven Figure 2 coordinates.",
    "inputs_not_rederived": "Reported axis estimates, literature measurements, evidence-coded diagnostic inputs, illustrative coordinates, and the AI reporting-floor convention.",
    "not_claimed": "Complete E.6 coefficient fits, time-series capacity estimates, uncertainty estimates, literature-study replication, or empirical validation."
}
PROV["reported_numeric_checks"] = {
    "_class": "COMPUTED",
    "_paper_location": "\u00a75.3-E.5.1; \u00a75.4 capacity calculations; \u00a75.6 Table 1",
    "_note": "Expected displayed precision is verified against the equations. These checks do not infer new empirical inputs or uniquely identify E.6 coefficients.",
    "capacity_closures": {"Humans":0.9121350693,"Corvids":0.6871505037,"Octopus":0.6634379959,"Fish":0.4119534288,"Honeybees":0.2892507609,"Plants":0.1257433430,"Bacteria":0.0330975092,"Viruses":0.0,"AI (LLM)":0.1681792831},
    "raven_normalized": 0.7324198983,
    "bee_floor_neurons": 5447.083,
    "corvid_floor_neurons": 2846584.253,
    "floor_ratio": 522.589,
    "corvid_diagnostic_I": 0.6663420214,
    "corvid_diagnostic_T": 0.5889485796,
    "corvid_diagnostic_C": 0.7412827403,
    "corvid_C_difference": 0.0541322367,
    "fish_alternative_R": 0.35,
    "fish_alternative_rounded_C": 0.43
}

out = pathlib.Path(__file__).resolve().parent / "data" / "provenance.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(PROV, indent=2, ensure_ascii=False), encoding="utf-8")
print("wrote", out, "(", out.stat().st_size, "bytes )")
