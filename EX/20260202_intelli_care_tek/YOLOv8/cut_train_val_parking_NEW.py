"""
1. cut and then convert.
2. continue
"""

import os
import json
import shutil
import random
import argparse
from json_to_txt_parking import convert_polygon_json_to_yolo_txt

# here
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\20230704_CAINZ習志野店_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\CAINZ_原町店_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\CAINZ_黒磯店_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\CAINZ大東店_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\CAINZ大胡店_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\CAINZ大宮店_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\CAINZ佐波東店_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\CAINZ邑楽店_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\CAINZ松伏店_Image"
folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\CAINZ静岡羽島PlanALL_P1_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\CAINZ静岡羽島PlanALL_P2_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\CAINZ磐田店_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\カインズ小牧店_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\カインズ名古屋みなと店_Image"

# here. remove data to yolo training path
folder_src_yolo_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730"
folder_tgt_yolo_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets"

# create folder to cut and convert.
train_images_path = os.path.join(folder_path, "images_NEW", "train")
val_images_path = os.path.join(folder_path, "images_NEW", "val")
other_images_path = os.path.join(folder_path, "images_NEW", "other")

train_labels_path = os.path.join(folder_path, "labels_NEW", "train")
val_labels_path = os.path.join(folder_path, "labels_NEW", "val")


# move folder for training path of YOLO.
train_images_yolo_path = os.path.join(folder_tgt_yolo_path, "images", "train")
val_images_yolo_path = os.path.join(folder_tgt_yolo_path, "images", "val")
train_labels_yolo_path = os.path.join(folder_tgt_yolo_path, "labels", "train")
val_labels_yolo_path = os.path.join(folder_tgt_yolo_path, "labels", "val")


def create_or_reset_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return None

def generate_file_lists(folder_path):
    json_list = []
    images_list = []

    for file in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file)):
            if file.endswith('.json'):
                json_list.append(file)
            elif file.endswith(('.png', '.jpg', '.jpeg')):
                images_list.append(file)

    return json_list, images_list

def extract_unique_labels(json_list, folder_path):
    unique_labels = set()
    for json_file in json_list:
        file_path = os.path.join(folder_path, json_file)
        data = read_json_file(file_path)
        if data and 'shapes' in data:
            for shape in data['shapes']:
                if 'label' in shape:
                    unique_labels.add(shape['label'])
    return unique_labels

def count_labels(json_list, folder_path):
    label_counts = {}
    for json_file in json_list:
        file_path = os.path.join(folder_path, json_file)
        data = read_json_file(file_path)
        if data and 'shapes' in data:
            for shape in data['shapes']:
                if 'label' in shape:
                    label = shape['label']
                    if label in label_counts:
                        label_counts[label] += 1
                    else:
                        label_counts[label] = 1
    return label_counts

def display_file_info(json_list, images_list):
    print(f"Number of JSON files: {len(json_list)}")
    print(f"Number of image files: {len(images_list)}")
    label_counts = count_labels(json_list, folder_path)
    print(f"Label counts: {label_counts}")

def split_and_save_json_files(json_list, train_labels_path, val_labels_path, ratio=0.8):
    random.shuffle(json_list)
    split_index = int(len(json_list) * ratio)
    train_json_list = json_list[:split_index]
    val_json_list = json_list[split_index:]

    for json_file in train_json_list:
        shutil.copy(os.path.join(folder_path, json_file), train_labels_path)
        convert_polygon_json_to_yolo_txt(os.path.join(train_labels_path, json_file), train_labels_path)

    for json_file in val_json_list:
        shutil.copy(os.path.join(folder_path, json_file), val_labels_path)
        convert_polygon_json_to_yolo_txt(os.path.join(val_labels_path, json_file), val_labels_path)

    return train_json_list, val_json_list

def split_and_save_images(images_list, train_json_list, val_json_list, train_images_path, val_images_path, other_images_path):
    train_json_base_names = {os.path.splitext(json_file)[0] for json_file in train_json_list}
    val_json_base_names = {os.path.splitext(json_file)[0] for json_file in val_json_list}

    train_images_list = [img for img in images_list if os.path.splitext(img)[0] in train_json_base_names]
    val_images_list = [img for img in images_list if os.path.splitext(img)[0] in val_json_base_names]
    unmatched_images = [img for img in images_list if os.path.splitext(img)[0] not in train_json_base_names and os.path.splitext(img)[0] not in val_json_base_names]

    for image_file in train_images_list:
        shutil.copy(os.path.join(folder_path, image_file), train_images_path)

    for image_file in val_images_list:
        shutil.copy(os.path.join(folder_path, image_file), val_images_path)

    for image_file in unmatched_images:
        shutil.copy(os.path.join(folder_path, image_file), other_images_path)

def list_nth_level_directories(base_path, tgt_path, n):
    """
    List the names of directories at the nth level under the base_path.
    """
    current_level_dirs = [base_path]
    for _ in range(n):
        next_level_dirs = []
        for dir_path in current_level_dirs:
            try:
                with os.scandir(dir_path) as entries:
                    for entry in entries:
                        if entry.is_dir():
                            next_level_dirs.append(entry.path)
            except PermissionError:
                continue
        current_level_dirs = next_level_dirs

    # Check and create required directories
    required_dirs = [
        os.path.join(tgt_path, "images", "train"),
        os.path.join(tgt_path, "images", "val"),
        os.path.join(tgt_path, "labels", "train"),
        os.path.join(tgt_path, "labels", "val")
    ]

    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    # Copy files from images_NEW to target directories
    for dir_path in current_level_dirs:
        if os.path.basename(dir_path) == "images_NEW":
            for subdir in ["other", "train"]:
                subdir_path = os.path.join(dir_path, subdir)
                if os.path.exists(subdir_path):
                    for file in os.listdir(subdir_path):
                        if file.endswith(('.png', '.jpg', '.jpeg')):
                            shutil.copy(os.path.join(subdir_path, file), os.path.join(tgt_path, "images", "train"))
            val_subdir_path = os.path.join(dir_path, "val")
            if os.path.exists(val_subdir_path):
                for file in os.listdir(val_subdir_path):
                    if file.endswith(('.png', '.jpg', '.jpeg')):
                        shutil.copy(os.path.join(val_subdir_path, file), os.path.join(tgt_path, "images", "val"))

        elif os.path.basename(dir_path) == "labels_NEW":
            train_subdir_path = os.path.join(dir_path, "train")
            if os.path.exists(train_subdir_path):
                for file in os.listdir(train_subdir_path):
                    if file.endswith('.txt'):
                        shutil.copy(os.path.join(train_subdir_path, file), os.path.join(tgt_path, "labels", "train"))
            val_subdir_path = os.path.join(dir_path, "val")
            if os.path.exists(val_subdir_path):
                for file in os.listdir(val_subdir_path):
                    if file.endswith('.txt'):
                        shutil.copy(os.path.join(val_subdir_path, file), os.path.join(tgt_path, "labels", "val"))

    return [os.path.basename(dir_path) for dir_path in current_level_dirs]

def main():
    parser = argparse.ArgumentParser(description="Process some images and JSON files.")
    parser.add_argument('--get-info', action='store_true', help='Display file information')
    parser.add_argument('--split', action='store_true', help='Split and save images and JSON files')
    parser.add_argument('--merge-unclear', action='store_true', help='Merge unclear option')
    parser.add_argument('-dl', type=int, help='Depth level to search for directories')

    args = parser.parse_args()

    json_list, images_list = generate_file_lists(folder_path)

    if args.get_info:
        display_file_info(json_list, images_list)
    elif args.split:
        create_or_reset_folder(train_images_path)
        create_or_reset_folder(val_images_path)
        create_or_reset_folder(other_images_path)
        create_or_reset_folder(train_labels_path)
        create_or_reset_folder(val_labels_path)
        
        train_json_list, val_json_list = split_and_save_json_files(json_list, train_labels_path, val_labels_path)
        split_and_save_images(images_list, train_json_list, val_json_list, train_images_path, val_images_path, other_images_path)
    elif args.merge_unclear and args.dl is not None:
        directories = list_nth_level_directories(folder_src_yolo_path, folder_tgt_yolo_path, args.dl)
        print(f"Directories at level {args.dl} under {folder_src_yolo_path}:")
        for directory in directories:
            print(directory)
    else:
        print("No valid action provided. Use --get-info or --split")

if __name__ == "__main__":
    main()