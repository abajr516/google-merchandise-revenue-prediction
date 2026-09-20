from pathlib import Path
import shutil
import subprocess
import zipfile


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

FILES = [
    "train_v2.csv",
    "test_v2.csv",
]

MIN_FREE_GB = 45


# --------------------------------------------------
# Check available storage
# --------------------------------------------------

def check_storage():
    total, used, free = shutil.disk_usage(DATA_DIR)

    free_gb = free / (1024 ** 3)

    print(f"Available disk space: {free_gb:.1f} GB")

    if free_gb < MIN_FREE_GB:
        raise RuntimeError(
            f"Not enough free disk space. "
            f"This project requires at least {MIN_FREE_GB} GB of free space."
        )

    print("Storage check passed.")


# --------------------------------------------------
# Download a file from Kaggle
# --------------------------------------------------

def download_file(filename):
    csv_path = DATA_DIR / filename
    zip_path = DATA_DIR / f"{filename}.zip"

    # If the extracted file already exists, do nothing.
    if csv_path.exists():
        print(f"{filename} already exists. Skipping download.")
        return

    # If the ZIP already exists, don't download it again.
    if zip_path.exists():
        print(f"{zip_path.name} already exists. Skipping download.")
        return

    print(f"Downloading {filename}...")

    try:
        subprocess.run(
            [
                "kaggle",
                "competitions",
                "download",
                "-c",
                "ga-customer-revenue-prediction",
                "-f",
                filename,
                "-p",
                str(DATA_DIR),
            ],
            check=True,
        )
    except FileNotFoundError:
        raise RuntimeError(
            "Kaggle CLI was not found. "
            "Make sure the project environment is activated and "
            "the kaggle package is installed."
        )
    except subprocess.CalledProcessError:
        raise RuntimeError(
            "Kaggle download failed. "
            "Make sure you have configured Kaggle authentication."
        )


# --------------------------------------------------
# Extract a downloaded ZIP
# --------------------------------------------------

def extract_file(filename):
    csv_path = DATA_DIR / filename
    zip_path = DATA_DIR / f"{filename}.zip"

    # If already extracted, nothing to do.
    if csv_path.exists():
        print(f"{filename} is already extracted.")
        return

    if not zip_path.exists():
        raise FileNotFoundError(
            f"Could not find {zip_path.name}."
        )

    print(f"Extracting {zip_path.name}...")

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(DATA_DIR)

    if not csv_path.exists():
        raise RuntimeError(
            f"Extraction completed, but {filename} was not found."
        )

    print(f"Successfully extracted {filename}.")


# --------------------------------------------------
# Remove ZIP files after successful extraction
# --------------------------------------------------

def remove_zip(filename):
    zip_path = DATA_DIR / f"{filename}.zip"

    if zip_path.exists():
        zip_path.unlink()
        print(f"Removed {zip_path.name}.")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Google Analytics Customer Revenue Prediction")
    print("Dataset setup")
    print("--------------------------------------------")

    # If both files are already present, don't require
    # a storage check or download anything.
    if all((DATA_DIR / filename).exists() for filename in FILES):
        print("Both required dataset files already exist.")
        print("No download or extraction is needed.")
        return

    check_storage()

    for filename in FILES:
        download_file(filename)
        extract_file(filename)
        remove_zip(filename)

    print("--------------------------------------------")
    print("Dataset setup complete.")
    print(f"Files are located in: {DATA_DIR}")


if __name__ == "__main__":
    main()