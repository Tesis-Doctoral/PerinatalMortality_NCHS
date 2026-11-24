# -*- coding: utf-8 -*-
"""
perinatal_builder.py -- Perinatal mortality, NCHS data

Builds the perinatal population of one delivery year, one row per product of 22 weeks or
more (before the population filter, every record is kept with its flags):

- live-birth component: births of year Y from the linked birth/infant death cohort files,
  with their death at 0 to 6 days (libraries/nchs_reader.py);
- fetal component: fetal deaths delivered in year Y, from the public-use fetal death files
  Fetal<Y>US_COD.zip.

Only the prenatal fields present in BOTH files are kept (outcome card, option A), under the
names of the birth file. Codes are kept as published; the count audit decides how
"unknown" codes are handled. Field positions come from the fetal user guides 2016-2023
(identical for these fields in the 3,052- and 2,653-character layouts).
"""
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from libraries.nchs_reader import RAW_DIR, OUT_DIR, build_cohort, _read_member

FETAL_DIR = RAW_DIR / "fetal"
YEARS = list(range(2016, 2024))

# prenatal fields shared by both files: name -> (birth start, end, kind), (fetal start, end)
SHARED = {
    "MAGER": ((75, 76, "int"), (86, 87)),
    "MRACEHISP": ((117, 117, "int"), (144, 144)),
    "MEDUC": ((124, 124, "int"), (145, 145)),
    "MBSTATE_REC": ((84, 84, "int"), (97, 97)),
    "WIC": ((251, 251, "chr"), (229, 229)),
    "PRIORLIVE": ((171, 172, "int"), (181, 182)),
    "PRIORDEAD": ((173, 174, "int"), (183, 184)),
    "ILLB_R": ((198, 200, "int"), (197, 199)),
    "PRECARE": ((224, 225, "int"), (202, 203)),
    "CIG_REC": ((269, 269, "chr"), (238, 238)),
    "CIG_0": ((253, 254, "int"), (230, 231)),       # cigarettes per day before pregnancy (decision D4)
    "BMI": ((283, 286, "dec"), (245, 248)),
    "RF_PDIAB": ((313, 313, "chr"), (257, 257)),
    "RF_GDIAB": ((314, 314, "chr"), (258, 258)),
    "RF_PHYPE": ((315, 315, "chr"), (259, 259)),
    "RF_GHYPE": ((316, 316, "chr"), (260, 260)),
    "RF_EHYPE": ((317, 317, "chr"), (261, 261)),
    "RF_INFT": ((325, 325, "chr"), (262, 262)),
    "RF_CESAR": ((331, 331, "chr"), (265, 265)),
    "RF_CESARN": ((332, 333, "int"), (266, 267)),
    "DPLURAL": ((454, 454, "int"), (301, 301)),
    "RESTATUS": ((104, 104, "int"), (131, 131)),
    # added for the completed second return (version 2), 2026-11-23: remaining antenatal fields shared by both files
    "MHTR": ((280, 281, "int"), (243, 244)),        # mother's height in inches (99 unknown)
    "CIG_1": ((255, 256, "int"), (232, 233)),       # cigarettes per day, 1st trimester (99 unknown)
    "RF_DRG": ((326, 326, "chr"), (263, 263)),      # fertility-enhancing drugs (Y, N, U; X = no infertility treatment)
    "RF_ART": ((327, 327, "chr"), (264, 264)),      # assisted reproductive technology (Y, N, U; X)
    "SEX": ((475, 475, "chr"), (316, 316)),         # sex of the product (M, F, U)
    "DLMP_MM": ((477, 478, "int"), (318, 319)),     # month of last normal menses (99 unknown)
    "FAGECOMB": ((147, 148, "int"), (177, 178)),    # father's combined age (99 unknown; sensitivity only)
}
LB_FIELDS = {k: v[0] for k, v in SHARED.items()}
LB_FIELDS.update({
    "DOB_YY": (9, 12, "int"), "COMBGEST": (490, 491, "int"), "BRTHWGT": (512, 515, "int"),
    "CO_SEQNUM": (365, 371, "int"), "CO_YOD": (372, 375, "int"),
})
FETAL_FIELDS = {k: (v[1][0], v[1][1], v[0][2]) for k, v in SHARED.items()}
FETAL_FIELDS.update({
    "DOD_YY": (11, 14, "int"), "OE_TABFLG": (10, 10, "chr"),
    "OEGEST_COMB": (340, 341, "int"), "COMBGEST": (331, 332, "int"),
    "DBWT": (349, 352, "int"), "ESTOFD": (357, 357, "chr"),
})
KEEP = ["unit_id", "group_id", "year", "component"] + list(SHARED) + [
    "ga_weeks", "ga_source", "birthweight", "estofd",
    "label_fetal", "label_early_neonatal", "died_first_24h", "label_main", "in_population"]


def read_fetal(year, fetal_dir=FETAL_DIR):
    zpath = Path(fetal_dir) / f"Fetal{year}US_COD.zip"
    with zipfile.ZipFile(zpath) as zf:
        members = [i.filename for i in zf.infolist()]
        if len(members) != 1:
            raise ValueError(f"{zpath.name}: expected one data file, found {members}")
        fd = _read_member(zf, members[0], FETAL_FIELDS)
    if not (fd["DOD_YY"] == year).all():
        raise ValueError(f"{zpath.name}: records with a delivery year other than {year}")
    return fd


def build_perinatal(year, raw_dir=RAW_DIR, out_dir=OUT_DIR, verbose=True):
    """Write data/interim/perinatal_<year>.parquet and return aggregate counts."""
    t = time.time()
    lb, lb_summary = build_cohort(year, raw_dir=raw_dir, birth_fields=LB_FIELDS,
                                  return_frame=True, verbose=False)
    lb = lb.assign(year=np.int16(year), component="live_birth",
                   ga_weeks=lb["COMBGEST"], ga_source="COMBGEST", birthweight=lb["BRTHWGT"],
                   estofd=pd.NA, label_fetal=False,
                   label_early_neonatal=lb["label_main"])          # death at 0-6 days

    fd = read_fetal(year, Path(raw_dir) / "fetal")
    fd = fd.assign(year=np.int16(year), component="fetal_death",
                   ga_weeks=fd["OEGEST_COMB"], ga_source="OEGEST_COMB", birthweight=fd["DBWT"],
                   estofd=fd["ESTOFD"].astype("string"), label_fetal=True,
                   label_early_neonatal=False, died_first_24h=False)
    fd.insert(0, "unit_id", np.arange(len(fd), dtype=np.int64) + year * 10_000_000 + 9_000_000)
    fd.insert(1, "group_id", fd["unit_id"])

    df = pd.concat([lb, fd], ignore_index=True)
    df["label_main"] = df["label_fetal"].astype(bool) | df["label_early_neonatal"].astype(bool)
    df["in_population"] = ((df["RESTATUS"] < 4) & df["ga_weeks"].between(22, 47)).fillna(False)
    df["component"] = df["component"].astype("category")
    df["ga_source"] = df["ga_source"].astype("category")
    df = df[KEEP]
    if df["unit_id"].duplicated().any():
        raise ValueError(f"year {year}: duplicated unit_id")

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    final = out_dir / f"perinatal_{year}.parquet"
    tmp = final.with_suffix(".parquet.tmp")
    df.to_parquet(tmp, index=False)
    tmp.replace(final)

    pop = df["in_population"]
    summary = {
        "year": year,
        "live_births": int((df["component"] == "live_birth").sum()),
        "fetal_death_records": int((df["component"] == "fetal_death").sum()),
        "deaths_linked": lb_summary["deaths_linked"],
        "pop_products": int(pop.sum()),
        "pop_live_births": int((pop & (df["component"] == "live_birth")).sum()),
        "pop_fetal_deaths": int((pop & df["label_fetal"]).sum()),
        "pop_early_neonatal_deaths": int((pop & df["label_early_neonatal"]).sum()),
        "pop_perinatal_events": int((pop & df["label_main"]).sum()),
        "pop_ge28_products": int((pop & (df["ga_weeks"] >= 28)).sum()),
        "pop_ge28_events": int((pop & (df["ga_weeks"] >= 28) & df["label_main"]).sum()),
        "seconds": round(time.time() - t),
    }
    if verbose:
        print(summary)
    return summary
