# Norming data for scoring

The experiment can show each participant a **score** at the end (average error vs. actual ages, % within 5 years) if it finds actual ages for the faces.

## Option A: Use the CFD norming file (recommended)

1. Place **"CFD 3.0 Norming Data and Codebook.xlsx"** in the **YB_survey** folder (parent of Project).

2. Install dependencies and run the export script from the **Project** folder:
   ```bash
   pip install pandas openpyxl
   python scripts/export_norming_to_face_ages.py
   ```
   This creates **cfd_norming_ages.csv** (all CFD models and their ages).

3. **To get automatic face_actual_ages.csv** (so the experiment can score):
   - Create **data/face_order.txt** with one CFD model ID per line, in order:
     - Line 1 = the CFD model used for **face_001**
     - Line 2 = face_002, … line 200 = face_200  
   - Re-run the script. It will generate **face_actual_ages.csv** from the norming data.

   If you no longer have the exact order (e.g. from when you ran `convert_names.py`), you can build **face_actual_ages.csv** manually (see Option B).

## Option B: Manual face_actual_ages.csv

Create **data/face_actual_ages.csv** with a header and one row per face:

```csv
face_id,actual_age
001,28
002,34
...
200,41
```

- **face_id**: 001, 002, … 200 (three digits).
- **actual_age**: age from the CFD norming data (or your own records) for that face.

You can look up ages from **cfd_norming_ages.csv** (after running the script once) and type them into **face_actual_ages.csv** in the same order as your experiment faces.

## If no norming file is used

If **data/face_actual_ages.csv** is missing or empty, the end screen will not show a score; the rest of the experiment (and CSV download) works as usual.
