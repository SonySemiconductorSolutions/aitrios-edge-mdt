import os
import tarfile
import time
import urllib.request
import shutil
from pathlib import Path

# Directories and URLs
script_dir = os.path.dirname(os.path.abspath(__file__))
imagenet_dir = os.path.join(script_dir, 'imagenet')
val_dir = os.path.join(imagenet_dir, 'val')
val_tar_file = os.path.join(imagenet_dir, 'ILSVRC2012_img_val.tar')
urls = [
    "https://image-net.org/data/ILSVRC/2012/ILSVRC2012_devkit_t12.tar.gz",
    "https://image-net.org/data/ILSVRC/2012/ILSVRC2012_img_val.tar"
]
labels_url = "https://raw.githubusercontent.com/tensorflow/models/master/research/slim/datasets/imagenet_2012_validation_synset_labels.txt"
labels_file = os.path.join(val_dir, 'imagenet_2012_validation_synset_labels.txt')

def download_file(url, dest):
    if not os.path.exists(dest):
        print(f"Downloading {url} to {dest}")
        start_time = time.time()
        urllib.request.urlretrieve(url, dest)
        end_time = time.time()
        print(f"Downloaded {url} in {end_time - start_time:.2f} seconds.")
    else:
        print(f"File {dest} already exists.")


def download_ds():
    if not os.path.isdir(imagenet_dir):
        os.makedirs(imagenet_dir)

    for url in urls:
        filename = os.path.join(imagenet_dir, os.path.basename(url))
        download_file(url, filename)

def extract_tar(tar_path, extract_to):
    print(f"Extracting {tar_path} to {extract_to}")
    start_time = time.time()
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(path=extract_to)
    end_time = time.time()
    print(f"Extracted {tar_path} in {end_time - start_time:.2f} seconds.")

def organize_validation_images():
    # Ensure validation directory exists
    if not os.path.exists(val_dir):
        os.makedirs(val_dir)

    # Extract validation images
    if os.path.exists(val_tar_file):
        extract_tar(val_tar_file, val_dir)

    # Download validation labels
    download_file(labels_url, labels_file)

    # Copy devkit file
    devkit_tar_path = os.path.join(imagenet_dir, "ILSVRC2012_devkit_t12.tar.gz")
    devkit_dest_path = os.path.join(val_dir, "ILSVRC2012_devkit_t12.tar.gz")

    if os.path.exists(devkit_tar_path):
        print(f"Linking {devkit_tar_path} to {devkit_dest_path}")
        if not os.path.exists(devkit_dest_path):  # Avoid errors if the link already exists
            os.symlink(devkit_tar_path, devkit_dest_path)
        else:
            print(f"Symlink already exists: {devkit_dest_path}")

    # Copy validation tar file
    val_tar_dest_path = os.path.join(val_dir, "ILSVRC2012_img_val.tar")

    if os.path.exists(val_tar_file):
        print(f"Linking {val_tar_file} to {val_tar_dest_path}")
        if not os.path.exists(val_tar_dest_path):  # Check if the link already exists
            os.symlink(val_tar_file, val_tar_dest_path)
        else:
            print(f"Symlink already exists: {val_tar_dest_path}")

    # Organize images by label
    with open(labels_file, 'r') as labels_f:
        labels = labels_f.read().splitlines()

    image_files = sorted(Path(val_dir).glob("*.JPEG"))

    if len(image_files) != len(labels):
        print("Error: Mismatch between number of images and labels")
        return

    print("Organizing images into subdirectories...")
    for image_file, label in zip(image_files, labels):
        label_dir = os.path.join(val_dir, label)
        os.makedirs(label_dir, exist_ok=True)
        shutil.move(str(image_file), os.path.join(label_dir, image_file.name))

    # Clean up
    if os.path.exists(labels_file):
        os.remove(labels_file)


def get_ds_path():
    download_ds()

    if not os.path.exists(val_dir) or not any(Path(val_dir).iterdir()):
        organize_validation_images()

    return val_dir

if __name__ == "__main__":
    dataset_path = get_ds_path()
    print(f"Dataset is available at: {dataset_path}")