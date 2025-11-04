import os
from glob import glob
from PIL import Image

# ==== CONFIG ====
# Define your fixed ROI here (x, y, width, height)

ROI = (750, 200, 1100, 500)  # Example: left=100, top=100, right=500, bottom=400
# Note: In PIL.crop, the box format is (left, top, right, bottom)

OVERWRITE = False  # Set True to replace original images

# ==================
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    dataset_folder = "datasets/dataset_2025-11-03_17-45-40"
    output_folder = dataset_folder + "_cropped"

    # Create output folder if not overwriting
    if not OVERWRITE:
        os.makedirs(output_folder, exist_ok=True)

    # Find all images recursively
    exts = ("*.png", "*.jpg", "*.jpeg")
    image_paths = []
    for ext in exts:
        image_paths.extend(glob(os.path.join(dataset_folder, "**", ext), recursive=True))

    print(f"[INFO] Found {len(image_paths)} images")

    for img_path in image_paths:
        try:
            img = Image.open(img_path)
            cropped = img.crop(ROI)  # Crop using fixed region

            if OVERWRITE:
                save_path = img_path
            else:
                # Preserve class folder structure
                rel_path = os.path.relpath(img_path, dataset_folder)
                save_path = os.path.join(output_folder, rel_path)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)

            cropped.save(save_path)
            print(f"[CROPPED] {save_path}")
        except Exception as e:
            print(f"[ERROR] {img_path} -> {e}")

    print("\n✅ Cropping completed.")
    if not OVERWRITE:
        print(f"[OUTPUT] Cropped dataset saved to: {output_folder}")
