"""
Export CFD 3.0 Norming Data to face_actual_ages.csv for the experiment scoring system.

Requires: pip install pandas openpyxl

Usage:
  1. Put "CFD 3.0 Norming Data and Codebook.xlsx" in the parent folder (YB_survey).
  2. From Project folder: python scripts/export_norming_to_face_ages.py

  If you have data/face_order.txt (one CFD model ID per line, line 1 = face_001 ... line 200 = face_200),
  the script will produce data/face_actual_ages.csv. Otherwise it only produces data/cfd_norming_ages.csv.
"""

import os
import sys

try:
    import pandas as pd
except ImportError:
    print("Please install pandas: pip install pandas openpyxl")
    sys.exit(1)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
PARENT_DIR = os.path.dirname(PROJECT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
XLSX_PATH = os.path.join(PARENT_DIR, "CFD 3.0 Norming Data and Codebook.xlsx")
FACE_ORDER_PATH = os.path.join(DATA_DIR, "face_order.txt")
CFD_NORMING_CSV = os.path.join(DATA_DIR, "cfd_norming_ages.csv")
FACE_AGES_CSV = os.path.join(DATA_DIR, "face_actual_ages.csv")


def find_age_column(df):
    for c in df.columns:
        if c and "age" in str(c).lower():
            return c
    return None


def find_id_column(df):
    for c in df.columns:
        s = str(c).lower()
        if "target" in s or "model" in s or "id" in s or "face" in s:
            return c
    return df.columns[0]


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.isfile(XLSX_PATH):
        print("Not found:", XLSX_PATH)
        print("Put CFD 3.0 Norming Data and Codebook.xlsx in the YB_survey folder.")
        sys.exit(1)
    print("Reading", XLSX_PATH)
    xl = pd.ExcelFile(XLSX_PATH)
    sheet = xl.sheet_names[0]
    df = pd.read_excel(xl, sheet_name=sheet)
    age_col = find_age_column(df)
    id_col = find_id_column(df)
    if age_col is None:
        print("No age column found. Columns:", list(df.columns))
        sys.exit(1)
    norm = df[[id_col, age_col]].dropna()
    norm.columns = ["cfd_model", "actual_age"]
    norm["cfd_model"] = norm["cfd_model"].astype(str).str.strip()
    norm["actual_age"] = pd.to_numeric(norm["actual_age"], errors="coerce")
    norm = norm.dropna(subset=["actual_age"])
    norm.to_csv(CFD_NORMING_CSV, index=False)
    print("Wrote", CFD_NORMING_CSV)
    age_by_model = dict(zip(norm["cfd_model"], norm["actual_age"].astype(int)))
    if os.path.isfile(FACE_ORDER_PATH):
        with open(FACE_ORDER_PATH, "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
        rows = []
        for i, cfd_id in enumerate(lines[:200]):
            face_id = str(i + 1).zfill(3)
            age = age_by_model.get(cfd_id.strip()) or age_by_model.get(cfd_id.strip() + "-N")
            rows.append((face_id, age if age is not None else ""))
        with open(FACE_AGES_CSV, "w", encoding="utf-8") as f:
            f.write("face_id,actual_age\n")
            for fid, a in rows:
                f.write(f"{fid},{a}\n")
        print("Wrote", FACE_AGES_CSV)
    else:
        print("No data/face_order.txt. Create it (one CFD model per line, order face_001..face_200) to generate face_actual_ages.csv.")


if __name__ == "__main__":
    main()
