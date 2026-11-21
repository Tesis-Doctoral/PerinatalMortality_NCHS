# -*- coding: utf-8 -*-
"""
nchs_reader.py -- Perinatal mortality, NCHS data

Data adapter for the NCHS public-use Period/Cohort Linked Birth/Infant Death files.
It reads the fixed-width files directly from the downloaded ZIP files (no extraction),
builds each birth cohort as the user guide describes (births of year N joined with the
deaths in years N and N+1 of infants born in N, by cohort sequence number and year of
death) and writes one Parquet file per cohort with the raw codes of the fields used by
the model and the labels.

Field positions come from the record layouts of the user guides 2017/2016 to 2024/2023;
they are identical in all eight releases (only some names change: AGED/AGEDX,
AGER5/AGER5X, AGER22/AGER22X, CO_DODYY/CO_YOD). Positions are 1-based and inclusive,
as in the guides.

No value is recoded here except blanks to missing: the count audit decides how the
"unknown or not stated" codes are handled.
"""
import os
import re
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
# The NCHS files are shared by the neonatal and perinatal repositories and live outside both,
# in a sibling folder NCHS_data/raw; set NCHS_RAW_DIR to use another location.
RAW_DIR = Path(os.environ.get("NCHS_RAW_DIR", ROOT.parent / "NCHS_data" / "raw"))
OUT_DIR = ROOT / "data" / "interim"
COHORTS = list(range(2016, 2024))
CHUNK_RECORDS = 200_000

# ---------------------------------------------------------------------------
# Record layout (birth part, same positions in the denominator and numerator files)
# ---------------------------------------------------------------------------
# name: (start, end, kind)   kind: "int" numeric code, "dec" numeric with decimal point,
#                            "chr" character code kept as text
BIRTH_FIELDS = {
    # birth and residence
    "DOB_YY": (9, 12, "int"), "DOB_MM": (13, 14, "int"), "BFACIL3": (50, 50, "int"),
    "RESTATUS": (104, 104, "int"),
    # mother
    "MAGER": (75, 76, "int"), "MBSTATE_REC": (84, 84, "int"), "MRACEHISP": (117, 117, "int"),
    "DMAR": (120, 120, "int"), "MEDUC": (124, 124, "int"), "WIC": (251, 251, "chr"),
    "PAY_REC": (436, 436, "int"),
    # obstetric history
    "PRIORLIVE": (171, 172, "int"), "PRIORDEAD": (173, 174, "int"), "PRIORTERM": (175, 176, "int"),
    "ILP_R": (214, 216, "int"), "ILLB_R": (198, 200, "int"), "RF_PPB": (318, 318, "chr"), "RF_CESAR": (331, 331, "chr"),
    "RF_CESARN": (332, 333, "int"),
    # current pregnancy
    "PRECARE": (224, 225, "int"), "PREVIS": (238, 239, "int"), "CIG_REC": (269, 269, "chr"),
    "BMI": (283, 286, "dec"), "WTGAIN": (304, 305, "int"),
    "RF_PDIAB": (313, 313, "chr"), "RF_GDIAB": (314, 314, "chr"), "RF_PHYPE": (315, 315, "chr"),
    "RF_GHYPE": (316, 316, "chr"), "RF_EHYPE": (317, 317, "chr"), "RF_INFT": (325, 325, "chr"),
    "IP_GON": (343, 343, "chr"), "IP_SYPH": (344, 344, "chr"), "IP_CHLAM": (345, 345, "chr"),
    "IP_HEPB": (346, 346, "chr"), "IP_HEPC": (347, 347, "chr"),
    # labor and delivery
    "LD_INDL": (383, 383, "chr"), "LD_AUGM": (384, 384, "chr"), "LD_STER": (385, 385, "chr"),
    "LD_ANTB": (386, 386, "chr"), "LD_CHOR": (387, 387, "chr"), "LD_ANES": (388, 388, "chr"),
    "ME_PRES": (401, 401, "int"), "ME_ROUT": (402, 402, "int"), "ME_TRIAL": (403, 403, "chr"),
    "ATTEND": (433, 433, "int"),
    # newborn (known at birth)
    "APGAR5": (444, 445, "int"), "DPLURAL": (454, 454, "int"), "SEX": (475, 475, "chr"),
    "COMBGST_IMP": (488, 488, "chr"), "COMBGEST": (490, 491, "int"),
    "BRTHWGT": (512, 515, "int"), "BWTIMP": (516, 516, "chr"),
    "CA_ANEN": (537, 537, "chr"), "CA_MNSB": (538, 538, "chr"), "CA_CCHD": (539, 539, "chr"),
    "CA_CDH": (540, 540, "chr"), "CA_OMPH": (541, 541, "chr"), "CA_GAST": (542, 542, "chr"),
    "CA_LIMB": (549, 549, "chr"), "CA_CLEFT": (550, 550, "chr"), "CA_CLPAL": (551, 551, "chr"),
    "CA_DOWN": (552, 552, "chr"), "CA_DISOR": (553, 553, "chr"), "CA_HYPO": (554, 554, "chr"),
    # cohort linkage
    "CO_SEQNUM": (365, 371, "int"), "CO_YOD": (372, 375, "int"),
}

# Death part, numerator files only
DEATH_FIELDS = {
    "DOB_YY": (9, 12, "int"), "RESTATUS": (104, 104, "int"),
    "CO_SEQNUM": (365, 371, "int"), "CO_YOD": (372, 375, "int"),
    "AGEDX": (1356, 1358, "int"), "AGER5X": (1359, 1359, "int"), "AGER22X": (1360, 1361, "int"),
    "UCOD": (1368, 1371, "str4"), "DOD_YY": (1672, 1675, "int"),
}

_NAME_YEAR = re.compile(r"^VS(\d{2}|\d{4})LINK", re.IGNORECASE)


def _member_year(name):
    m = _NAME_YEAR.match(name)
    if not m:
        raise ValueError(f"unexpected file name in ZIP: {name}")
    y = int(m.group(1))
    return y + 2000 if y < 100 else y


def cohort_members(cohort, raw_dir=RAW_DIR):
    """ZIP path, denominator member of year `cohort` and numerator members of years
    `cohort` and `cohort + 1`."""
    zpath = Path(raw_dir) / f"{cohort + 1}PE{cohort}CO.zip"
    with zipfile.ZipFile(zpath) as zf:
        names = [i.filename for i in zf.infolist()]
    den = [n for n in names if "DEN" in n.upper() and _member_year(n) == cohort]
    num = sorted(n for n in names if "NUM" in n.upper() and _member_year(n) in (cohort, cohort + 1))
    if len(den) != 1 or len(num) != 2:
        raise ValueError(f"{zpath.name}: expected 1 denominator and 2 numerators, found {den} {num}")
    return zpath, den[0], num


def _record_length(zf, info):
    with zf.open(info) as h:
        first = h.read(4096)
    reclen = first.index(b"\n") + 1
    if info.file_size % reclen:
        raise ValueError(f"{info.filename}: file size is not a multiple of the record length {reclen}")
    return reclen


def _decode(block, fields):
    """Vectorized extraction of the fields from a (records x record_length) uint8 block."""
    out = {}
    for name, (a, b, kind) in fields.items():
        sub = block[:, a - 1:b]
        if kind in ("int", "dec"):
            if kind == "dec":                       # e.g. BMI "23.4": drop the decimal point
                keep = [j for j in range(sub.shape[1]) if j != sub.shape[1] - 2]
                sub = sub[:, keep]
            digits = sub.astype(np.int32) - 48
            isdig = (digits >= 0) & (digits <= 9)
            space = sub == 32
            # padding spaces are allowed (some files write " 002739"); all blank or any other
            # character -> missing
            ok = (isdig | space).all(axis=1) & isdig.any(axis=1)
            val = np.zeros(len(sub), dtype=np.int32)
            for j in range(sub.shape[1]):
                val = np.where(isdig[:, j], val * 10 + digits[:, j], val)
            mask = ~ok
            out[name] = (val, mask, kind)
        else:
            w = sub.shape[1]
            txt = np.ascontiguousarray(sub).view(f"S{w}").ravel()
            out[name] = (txt, None, kind)
    return out


def _read_member(zf, member, fields, chunk_records=CHUNK_RECORDS):
    info = zf.getinfo(member)
    reclen = _record_length(zf, info)
    parts = {k: [] for k in fields}
    n = 0
    with zf.open(info) as h:
        while True:
            buf = h.read(reclen * chunk_records)
            if not buf:
                break
            block = np.frombuffer(buf, dtype=np.uint8).reshape(-1, reclen)
            n += len(block)
            for k, v in _decode(block, fields).items():
                parts[k].append(v)
    if n * reclen != info.file_size:
        raise ValueError(f"{member}: read {n} records, expected {info.file_size // reclen}")
    cols = {}
    for k, (a, b, kind) in fields.items():
        if kind in ("int", "dec"):
            val = np.concatenate([p[0] for p in parts[k]])
            mask = np.concatenate([p[1] for p in parts[k]])
            arr = pd.arrays.IntegerArray(val, mask)
            cols[k] = pd.array(arr, dtype="Int32")
            if kind == "dec":
                cols[k] = pd.array(arr, dtype="Float32") / 10
        else:
            txt = np.concatenate([p[0] for p in parts[k]])
            s = pd.Series(txt.astype(f"U{b - a + 1}")).str.strip()
            cols[k] = pd.Categorical(s.where(s != "", None))
    return pd.DataFrame(cols)


def build_cohort(cohort, raw_dir=RAW_DIR, out_dir=OUT_DIR, verbose=True, birth_fields=None, return_frame=False):
    """Build one birth cohort and write data/interim/cohort_<year>.parquet.
    Returns a dict of aggregate counts (no record-level data). With return_frame=True
    nothing is written and (frame, summary) is returned; birth_fields selects the birth
    fields to read (default: BIRTH_FIELDS)."""
    t = time.time()
    zpath, den_name, num_names = cohort_members(cohort, raw_dir)
    with zipfile.ZipFile(zpath) as zf:
        births = _read_member(zf, den_name, birth_fields or BIRTH_FIELDS)
        deaths = pd.concat([_read_member(zf, m, DEATH_FIELDS) for m in num_names], ignore_index=True)

    n_deaths_file = len(deaths)
    # guide: keep deaths of infants born in the cohort year to US residents
    deaths = deaths[(deaths["DOB_YY"] == cohort) & (deaths["RESTATUS"] < 4)]
    deaths = deaths.dropna(subset=["CO_SEQNUM", "CO_YOD"])
    if deaths.duplicated(["CO_SEQNUM", "CO_YOD"]).any():
        raise ValueError(f"cohort {cohort}: duplicated linkage keys in the numerator files")
    deaths = deaths.drop(columns=["DOB_YY", "RESTATUS"]).rename(
        columns={"AGEDX": "d_age_days", "AGER5X": "d_ager5", "AGER22X": "d_ager22",
                 "UCOD": "d_ucod", "DOD_YY": "d_year"})

    births.insert(0, "cohort", np.int16(cohort))
    births.insert(0, "unit_id", np.arange(len(births), dtype=np.int64) + cohort * 10_000_000)
    births.insert(1, "group_id", births["unit_id"])     # no mother identifier in the public files
    keyed = births["CO_SEQNUM"].notna() & births["CO_YOD"].notna()
    merged = births.merge(deaths, how="left", on=["CO_SEQNUM", "CO_YOD"], indicator=True)
    merged.loc[~keyed.to_numpy(), "_merge"] = "left_only"
    if len(merged) != len(births):
        raise ValueError(f"cohort {cohort}: the join changed the number of births")

    died = merged["_merge"].eq("both")
    age = merged["d_age_days"]
    merged["died_infant"] = died
    merged["label_main"] = died & age.le(6).fillna(False)                         # 0-6 days
    merged["label_neonatal"] = died & age.le(27).fillna(False)                    # 0-27 days
    merged["died_first_24h"] = died & merged["d_ager5"].isin([1, 2]).fillna(False)  # < 24 hours
    merged["label_day1_6"] = died & merged["d_ager5"].eq(3).fillna(False)         # 1-6 days
    merged = merged.drop(columns=["_merge"])

    not_found = len(deaths) - int(died.sum())
    if not_found > 0.01 * len(deaths):
        raise ValueError(f"cohort {cohort}: {not_found} of {len(deaths)} deaths did not join a birth")

    if not return_frame:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        final = out_dir / f"cohort_{cohort}.parquet"
        tmp = final.with_suffix(".parquet.tmp")
        merged.to_parquet(tmp, index=False)       # write to a temporary name first, so an interrupted
        tmp.replace(final)                        # run never leaves a corrupted cohort file

    summary = {
        "cohort": cohort,
        "births": len(births),
        "births_us_resident": int((births["RESTATUS"] < 4).sum()),
        "births_with_link_key": int(keyed.sum()),
        "deaths_in_numerator_files": n_deaths_file,
        "deaths_of_cohort_us_resident": len(deaths),
        "deaths_linked": int(died.sum()),
        "deaths_not_found_in_births": len(deaths) - int(died.sum()),
        "early_neonatal_0_6d": int(merged["label_main"].sum()),
        "neonatal_0_27d": int(merged["label_neonatal"].sum()),
        "died_first_24h": int(merged["died_first_24h"].sum()),
        "seconds": round(time.time() - t),
    }
    if verbose:
        print(summary)
    if return_frame:
        return merged, summary
    return summary
