import os
import cv2
import numpy as np
from skimage import color, io, img_as_ubyte

# --- CONFIGURATION ---
INPUT_FOLDER = 'raw_images'
OUTPUT_FOLDER = 'processed_faces'

# Ensure output folder exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Get list of all images
files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(('.jpg', '.png', '.jpeg'))]
print(f"Found {len(files)} images. Processing...")

for filename in files:
    # 1. Load Image (Standard RGB)
    img_path = os.path.join(INPUT_FOLDER, filename)
    img_rgb = io.imread(img_path)

    # Get the base filename without extension (e.g., "CFD-WM-001")
    base_name = os.path.splitext(filename)[0]

    # --- VERSION 1: ORIGINAL COLOR (Just copy/save) ---
    # We save it as standard RGB to ensure format consistency
    save_path = os.path.join(OUTPUT_FOLDER, f"{base_name}_color.jpg")
    io.imsave(save_path, img_rgb)

    # 2. Convert to CIE LAB for manipulation
    # skimage converts images to float64 range [0, 100] for L, [-128, 127] for a/b
    img_lab = color.rgb2lab(img_rgb)

    # --- VERSION 2: GREYSCALE (Exp 1) ---
    # Keep L* (channel 0), Set a* (channel 1) and b* (channel 2) to 0
    lab_grey = img_lab.copy()
    lab_grey[:, :, 1] = 0 # a* = 0
    lab_grey[:, :, 2] = 0 # b* = 0
    
    # Convert back to RGB
    img_grey = color.lab2rgb(lab_grey)
    # Save (img_as_ubyte converts 0-1 float back to 0-255 image)
    io.imsave(os.path.join(OUTPUT_FOLDER, f"{base_name}_grey.jpg"), img_as_ubyte(img_grey))


    # --- VERSION 3: RED-GREEN INCREASED (Exp 2 RG+) ---
    # Multiply a* channel by 1.5
    lab_rg_plus = img_lab.copy()
    lab_rg_plus[:, :, 1] = lab_rg_plus[:, :, 1] * 1.5
    
    # Convert back and Save
    # Note: conversion handles clipping automatically if colors go out of bounds
    img_rg_plus = color.lab2rgb(lab_rg_plus) 
    io.imsave(os.path.join(OUTPUT_FOLDER, f"{base_name}_rg_plus.jpg"), img_as_ubyte(img_rg_plus))


    # --- VERSION 4: RED-GREEN DECREASED (Exp 2 RG-) ---
    # Divide a* channel by 1.5
    lab_rg_minus = img_lab.copy()
    lab_rg_minus[:, :, 1] = lab_rg_minus[:, :, 1] / 1.5
    
    # Convert back and Save
    img_rg_minus = color.lab2rgb(lab_rg_minus)
    io.imsave(os.path.join(OUTPUT_FOLDER, f"{base_name}_rg_minus.jpg"), img_as_ubyte(img_rg_minus))

print("Done! Check the 'processed_faces' folder.")