import os
import json

def convert_polygon_json_to_yolo_txt(json_file_path, unified_dir):
    if not os.path.exists(unified_dir):
        os.makedirs(unified_dir)
    
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    img_width = data['imageWidth']
    img_height = data['imageHeight']
    
    yolo_format_lines = []

    for shape in data['shapes']:
        label = shape['label']
        if label == 'linearcrack':
            label = '0'
        elif label == 'blur':
            label = '1'
        elif label == 'alligator':
            label = '2'
        elif label == 'briscrack':
            label = '3'
        elif label == 'pothole':
            label = '4'
        elif label == 'kurumadome':
            label = '5'
        points = shape['points']
        
        normalized_points = ' '.join([f"{x/img_width} {y/img_height}" for x, y in points])
        yolo_format_line = f"{label} {normalized_points}"
        yolo_format_lines.append(yolo_format_line)
    
    txt_file_name = os.path.basename(json_file_path).replace('.json', '.txt')
    txt_file_path = os.path.join(unified_dir, txt_file_name)
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        for line in yolo_format_lines:
            txt_file.write(line + '\n')

def convert_folder_json_to_yolo_txt(unified_dir):
    for filename in os.listdir(unified_dir):
        if filename.endswith('.json'):
            json_file_path = os.path.join(unified_dir, filename)
            convert_polygon_json_to_yolo_txt(json_file_path, unified_dir)

# Example usage
if __name__ == "__main__":
    #train_labels_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\カインズ名古屋みなと店_Image\labels_NEW\train"
    #val_labels_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\カインズ名古屋みなと店_Image\labels_NEW\val"

    train_labels_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\fix\train"
    val_labels_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\fix\val"

    convert_folder_json_to_yolo_txt(train_labels_path)
    convert_folder_json_to_yolo_txt(val_labels_path)