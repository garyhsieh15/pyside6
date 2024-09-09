from ultralytics import YOLO
import json
import os
import cv2
import base64
import argparse

def save_results_to_txt(results, output_path):
    """
    將原始 YOLOv8 分割結果的資訊儲存到 txt 檔案
    """
    with open(output_path, 'w') as f:
        f.write(str(results))

def display_segmentation_results_info(results):
    """
    顯示 YOLOv8 分割結果的資訊，包含每個類別的名稱
    """
    # 假設 names 字典在 results[0].names 中
    names_dict = results[0].names
    
    # 建立 class_names 對應表
    class_names = {}
    for key, value in names_dict.items():
        class_names[int(key)] = value
    
    for i, result in enumerate(results):
        print(f"Result {i + 1}:")
        for j, (mask, box) in enumerate(zip(result.masks.xy, result.boxes)):
            class_id = int(box.cls)
            # 根據 key 對應到 Class ID
            class_name = class_names.get(class_id, "Unknown")
            print(f"  Object {j + 1}:")
            print(f"    Class ID: {class_id}")
            print(f"    Class Name: {class_name}")
            print(f"    Coordinates: {mask.tolist()}")

def display_detect_results_info(results, class_names):
    """
    顯示 YOLOv8 偵測結果的資訊，包含每個類別的名稱
    """
    for i, result in enumerate(results):
        print(f"Result {i + 1}:")
        for j, box in enumerate(result.boxes):
            class_id = int(box.cls)
            # 根據 key 對應到 Class ID
            class_name = class_names.get(class_id, "Unknown")
            print(f"  Object {j + 1}:")
            print(f"    Class ID: {class_id}")
            print(f"    Class Name: {class_name}")
            print(f"    Coordinates: {box.xyxy.tolist()}")

def convert_image_to_base64(image_path):
    """
    將圖片轉換為 base64 編碼格式
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def convert_to_labelme_format(results, image_path):
    """
    將 YOLOv8 分割結果轉換為 LabelMe 可讀取的 JSON 格式
    """
    # 讀取圖片以獲取其高度和寬度
    image = cv2.imread(image_path)
    image_height, image_width, _ = image.shape

    # 假設 names 字典在 results[0].names 中
    names_dict = results[0].names
    
    # 建立 class_names 對應表
    class_names = {}
    for key, value in names_dict.items():
        class_names[int(key)] = value

    # 將圖片轉換為 base64 編碼格式
    image_data_base64 = convert_image_to_base64(image_path)

    labelme_format = {
        "version": "5.2.1",
        "flags": {},
        "shapes": [],
        "imagePath": os.path.basename(image_path),
        "imageData": image_data_base64,
        "imageHeight": image_height,
        "imageWidth": image_width
    }

    for result in results:
        for mask, box in zip(result.masks.xy, result.boxes):
            class_id = int(box.cls)
            class_name = class_names.get(class_id, "Unknown")
            shape = {
                "label": class_name,
                "points": mask.tolist(),
                "group_id": None,
                "shape_type": "polygon",
                "flags": {}
            }
            labelme_format["shapes"].append(shape)

    return labelme_format

def convert_to_detect_json_format(results, image_path):
    """
    將 YOLOv8 偵測結果轉換為 JSON 格式，參考 20230704_CAINZ習志野店_0005_0005.json 的格式
    """
    # 讀取圖片以獲取其高度和寬度
    image = cv2.imread(image_path)
    image_height, image_width, _ = image.shape

    # 假設 names 字典在 results[0].names 中
    names_dict = results[0].names
    
    # 建立 class_names 對應表
    class_names = {}
    for key, value in names_dict.items():
        class_names[int(key)] = value

    # 將圖片轉換為 base64 編碼格式
    image_data_base64 = convert_image_to_base64(image_path)

    detect_format = {
        "version": "5.2.1",
        "flags": {},
        "shapes": [],
        "imagePath": os.path.basename(image_path),
        "imageData": image_data_base64,
        "imageHeight": image_height,
        "imageWidth": image_width
    }

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            class_name = class_names.get(class_id, "Unknown")
            xyxy = box.xyxy.tolist()[0]  # 將張量轉換為列表並提取第一個元素
            shape = {
                "label": class_name,
                "points": [
                    [xyxy[0], xyxy[1]],
                    [xyxy[2], xyxy[3]]
                ],
                "group_id": None,
                "description": "",
                "shape_type": "rectangle",
                "flags": {}
            }
            detect_format["shapes"].append(shape)

    return detect_format

def save_json(data, output_path):
    """
    將資料儲存為 JSON 檔案
    """
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLOv8 Segmentation to LabelMe Format")
    parser.add_argument("--seg-coord_json", action="store_true", help="Convert segmentation results to LabelMe format")
    parser.add_argument("--seg-coord_info", action="store_true", help="Display segmentation results information")
    parser.add_argument("--detect-coord_info", action="store_true", help="Display detection results information")
    parser.add_argument("--detect-coord_json", action="store_true", help="Convert detection results to JSON format")
    args = parser.parse_args()

    model_path = r'E:\baiV8\ultralytics\runs\train\yolov8l-seg_parking_4_type_random_600_pt\weights\best.pt'
    image_path = r'E:\images_lab\YOLOv7\20240730_parking\datasets\test\20240123_CAINZ大宮店_0008_0006.jpg'
    
    output_json_path = '20240123_CAINZ大宮店_0008_0006.json'
    output_txt_path = 'results.txt'

    model = YOLO(model_path)
    results = model(image_path)

    if args.seg_coord_json:
        # 儲存原始 results 的資訊到 txt 檔案
        save_results_to_txt(results, output_txt_path)

        labelme_data = convert_to_labelme_format(results, image_path)
        save_json(labelme_data, output_json_path)

        print(f"Segmentation results saved to {output_json_path}")
        print(f"Results information saved to {output_txt_path}")

    elif args.seg_coord_info:
        # 顯示分割結果的資訊
        display_segmentation_results_info(results)
    
    elif args.detect_coord_info:
        # 假設 names 字典在 results[0].names 中
        names_dict = results[0].names
        
        # 建立 class_names 對應表
        class_names = {}
        for key, value in names_dict.items():
            class_names[int(key)] = value
        
        # 顯示偵測結果的資訊
        display_detect_results_info(results, class_names)
    
    elif args.detect_coord_json:
        # 轉換偵測結果為 JSON 格式
        detect_data = convert_to_detect_json_format(results, image_path)
        save_json(detect_data, output_json_path)

        print(f"Detection results saved to {output_json_path}")

    else:
        print("Please provide the --seg-coord_json, --seg-coord_info, --detect-coord_info, or --detect-coord_json argument.")