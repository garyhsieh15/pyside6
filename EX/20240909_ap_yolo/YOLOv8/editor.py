
import glob
import os
import argparse

def display_file_data(file, data):
    """
    顯示檔案名稱和資料，並將其儲存到 log.txt 檔案中。
    """
    log_file = "log.txt"
    with open(log_file, 'a', encoding='utf-8') as log:
        log.write(f"檔案名稱: {os.path.basename(file)}\n")
        print(f"檔案名稱: {os.path.basename(file)}")
        for item in data:
            log.write(f"{item}\n")
            print(item)
        log.write("\n")
        print()  # 每個檔案之間空一行

def read_first_column_from_txt_files(directory):
    """
    讀取指定目錄下所有的 .txt 檔案，並顯示每一行的第一個欄位資料。
    """
    # 獲取所有的 .txt 檔案
    txt_files = glob.glob(f"{directory}/*.txt")
    
    for file in txt_files:
        data = []
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                # 假設欄位是以空白或逗號分隔
                first_column = line.split()[0] if line.split() else None
                if first_column:
                    data.append(first_column)
        display_file_data(file, data)

def modify_row_data_in_txt_files(directory, modifications):
    """
    修改指定目錄下所有的 .txt 檔案中每一行的第一個欄位資料。
    """
    # 獲取所有的 .txt 檔案
    txt_files = glob.glob(f"{directory}/*.txt")
    
    for file in txt_files:
        modified_lines = []
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                columns = line.split()
                if columns:
                    first_column = columns[0]
                    if first_column.isdigit():
                        index = int(first_column)
                        if index < len(modifications):
                            new_value = modifications[index]
                            if new_value == "":
                                continue  # 刪除該行
                            elif new_value != first_column:
                                columns[0] = new_value
                modified_lines.append(" ".join(columns))
        
        # 將修改後的內容寫回原檔案
        with open(file, 'w', encoding='utf-8') as f:
            for line in modified_lines:
                f.write(line + "\n")

def modify_file_names(directory, name_mapping):
    """
    修改指定目錄下所有檔案的名稱，根據提供的名稱對應表。
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            old_file_path = os.path.join(root, file)
            new_file_name = file
            for old_name, new_name in name_mapping.items():
                new_file_name = new_file_name.replace(old_name, new_name)
            new_file_path = os.path.join(root, new_file_name)
            os.rename(old_file_path, new_file_path)
            print(f"Renamed: {old_file_path} -> {new_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="處理 .txt 檔案中的資料")
    parser.add_argument("--modify-idx", action="store_true", help="修改第一個欄位資料")
    parser.add_argument("--modify-name", action="store_true", help="修改檔案名稱")

    args = parser.parse_args()

    labels_train_folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\labels\train"
    labels_val_folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\labels\val"
    images_train_folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\images\train"
    images_val_folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\images\val"

    #folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\fix\after"
    
    #          index: 0    1    2    3    4    5
    #modifications = ["0", "1", "2", "2", "3", "4"]
    modifications = ["0", "1", "2", "2", "3", ""]
    #modifications = ["0", "1", "2", "2", "", ""]

    if args.modify_idx:
        modify_row_data_in_txt_files(labels_train_folder_path, modifications)
        modify_row_data_in_txt_files(labels_val_folder_path, modifications)
    elif args.modify_name:
        name_mapping = {
            "習志野店": "00",
            "大宮店": "01",
            "松伏店": "02",
            "原町店": "03",
            "黒磯店": "04",
            "大東店": "05",
            "大胡店": "06",
            "佐波東店": "07",
            "邑楽店": "08",
            "静岡羽島": "09",
            "磐田店": "10",
            "カインズ小牧店": "11",
            "カインズ名古屋みなと店": "12",
            # 在這裡添加更多的名稱對應
        }
        modify_file_names(labels_train_folder_path, name_mapping)
        modify_file_names(labels_val_folder_path, name_mapping)
        modify_file_names(images_train_folder_path, name_mapping)
        modify_file_names(images_val_folder_path, name_mapping)
    else:
        read_first_column_from_txt_files(labels_train_folder_path)
        read_first_column_from_txt_files(labels_val_folder_path) 