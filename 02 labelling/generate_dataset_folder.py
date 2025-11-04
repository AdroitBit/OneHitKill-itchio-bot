import os
from datetime import datetime

def create_dataset_folder(base_dir="datasets"):
    """Create a new timestamped folder for this dataset session."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f"dataset_{timestamp}"
    path = os.path.join(base_dir, folder_name)
    os.makedirs(path, exist_ok=True)
    return path

def create_class_folders(dataset_folder, classes):
    """Create class subfolders inside the dataset folder."""
    for cla in classes:
        class_path = os.path.join(dataset_folder, cla)
        os.makedirs(class_path, exist_ok=True)
    print(f"[INFO] Created {len(classes)} class folders in {dataset_folder}")

# Define your element and weakpoint pairs
pair_element = ["none", "robot", "dark", "fire", "ice"]
pair_weakpoint = ["none", "side", "center", "rock", "head"]

# Generate class names
classes = [
    "no_monster",
    *["{}_{}".format(e, w) for e in pair_element for w in pair_weakpoint]
]

if __name__ == "__main__":
    # Move to script directory (optional but clean)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"[WORKDIR] {os.getcwd()}")

    # Step 1: Create dataset folder
    dataset_folder = create_dataset_folder(base_dir="datasets")

    # Step 2: Create class folders
    create_class_folders(dataset_folder, classes)

    # Step 3: Print summary
    print("\n[CLASSES]")
    for idx, cla in enumerate(classes):
        print(f"{idx:02d}: {cla}")
    print(f"\n[DATASET READY] {dataset_folder}")
