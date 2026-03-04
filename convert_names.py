import os
import random
import re

# --- CONFIGURATION ---
# Target counts per Experiment (Total 100 per experiment)
# "30 Asians, 30 Whites, 20 Latinos, 20 Blacks. Half male, half female."
TARGETS = {
    'A': {'F': 15, 'M': 15}, # Asian: 30 total
    'W': {'F': 15, 'M': 15}, # White: 30 total
    'L': {'F': 10, 'M': 10}, # Latino: 20 total
    'B': {'F': 10, 'M': 10}  # Black: 20 total
}

def clean_sort_rename():
    print("--- STARTING SMART BALANCED SORTING ---")
    
    # 1. IDENTIFY UNIQUE FACES
    # We scan for _color.jpg files to find unique identities
    all_files = [f for f in os.listdir('.') if f.endswith('_color.jpg')]
    unique_identities = []

    # Regex to parse CFD filenames
    # Expecting format like: CFD-AF-200-228-N_color.jpg
    # We need to capture the first two letters after "CFD-" (e.g., "AF")
    pattern = re.compile(r"CFD-([A-Z])([A-Z])-.+") 
    
    # Categorize every single face we found
    pool = {
        'A': {'F': [], 'M': []},
        'W': {'F': [], 'M': []},
        'L': {'F': [], 'M': []},
        'B': {'F': [], 'M': []}
    }

    print("Scanning files...")
    for filename in all_files:
        # Get base name (remove _color.jpg)
        base_name = filename.replace('_color.jpg', '')
        
        match = pattern.match(base_name)
        if match:
            race = match.group(1)   # e.g., 'A'
            gender = match.group(2) # e.g., 'F'
            
            if race in pool and gender in pool[race]:
                pool[race][gender].append(base_name)
            else:
                print(f"Warning: Unknown category for {base_name} ({race}-{gender})")
        else:
            print(f"Warning: Could not parse filename {base_name}")

    # 2. SELECT FACES FOR EXPERIMENT 1
    exp1_faces = []
    exp2_faces = []

    print("\nAllocating faces...")
    for race in TARGETS:
        for gender in TARGETS[race]:
            needed = TARGETS[race][gender]
            available = pool[race][gender]
            
            if len(available) < (needed * 2):
                print(f"CRITICAL ERROR: Not enough {race}-{gender} faces!")
                print(f"Need {needed * 2} but only found {len(available)}.")
                return

            # Shuffle to ensure randomness
            random.shuffle(available)
            
            # Take the first slice for Exp 1
            batch1 = available[:needed]
            exp1_faces.extend(batch1)
            
            # Take the second slice for Exp 2
            batch2 = available[needed : needed*2]
            exp2_faces.extend(batch2)
            
            print(f"  {race}-{gender}: Assigned {len(batch1)} to Exp1 and {len(batch2)} to Exp2.")

    # Shuffle the final lists so Race isn't clustered (e.g., all Asians first)
    random.shuffle(exp1_faces)
    random.shuffle(exp2_faces)

    # 3. RENAME AND CLEANUP
    print("\nRenaming files...")
    
    # Process Experiment 1 (ID 001 - 100)
    # KEEP: Color/Grey. DELETE: RG+, RG-
    for i, face_name in enumerate(exp1_faces):
        new_id = str(i + 1).zfill(3)
        
        safe_rename(f"{face_name}_color.jpg", f"face_{new_id}_color.jpg")
        safe_rename(f"{face_name}_grey.jpg",  f"face_{new_id}_grey.jpg")
        
        delete_file(f"{face_name}_rg_plus.jpg")
        delete_file(f"{face_name}_rg_minus.jpg")

    # Process Experiment 2 (ID 101 - 200)
    # KEEP: RG+, RG-. DELETE: Color/Grey
    for i, face_name in enumerate(exp2_faces):
        new_id = str(i + 101).zfill(3)
        
        safe_rename(f"{face_name}_rg_plus.jpg",  f"face_{new_id}_rg_plus.jpg")
        safe_rename(f"{face_name}_rg_minus.jpg", f"face_{new_id}_rg_minus.jpg")
        
        delete_file(f"{face_name}_color.jpg")
        delete_file(f"{face_name}_grey.jpg")

    # Delete any remaining unused files (faces that weren't selected)
    # (Optional, keeps folder clean)
    print("\nCleaning up unused faces...")
    remaining_files = [f for f in os.listdir('.') if f.startswith('CFD-')]
    for f in remaining_files:
        os.remove(f)

    print("\n--- DONE! You now have 400 perfectly balanced images. ---")

def safe_rename(old, new):
    if os.path.exists(old):
        os.rename(old, new)

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

if __name__ == "__main__":
    clean_sort_rename()