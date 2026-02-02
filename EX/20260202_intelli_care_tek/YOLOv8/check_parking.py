import os

#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\20230704_CAINZ習志野店_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\CAINZ_原町店_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\CAINZ磐田店_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\CAINZ静岡羽島PlanALL_P1_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\CAINZ静岡羽島PlanALL_P2_Image"
#folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\カインズ小牧店_Image"
folder_path = r"E:\images_lab\YOLOv7\20240730_parking\datasets\Parking20240730\カインズ名古屋みなと店_Image"


def compare_file_names(path1, path2):
    def get_base_names(path):
        return {os.path.splitext(file)[0] for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))}
    
    base_names1 = get_base_names(path1)
    base_names2 = get_base_names(path2)
    
    diff1 = base_names1 - base_names2
    diff2 = base_names2 - base_names1
    
    return diff1, diff2

def display_comparison_results():

    # create folder to cut and convert.
    train_images_path = os.path.join(folder_path, "images_NEW", "train")
    val_images_path = os.path.join(folder_path, "images_NEW", "val")

    train_labels_path = os.path.join(folder_path, "labels_NEW", "train")
    val_labels_path = os.path.join(folder_path, "labels_NEW", "val")

    # Display comparison results
    diff1, _ = compare_file_names(train_images_path, train_labels_path)
    diff2, _ = compare_file_names(val_images_path, val_labels_path)

    print(folder_path)
    
    if not diff1 and not diff2:
        print("\nAll files match between train_images_path and train_labels_path, and between val_images_path and val_labels_path.")
    else:
        # Display side-by-side comparison for train images and train labels
        print("\nFiles in train_images_path but not in train_labels_path:")
        for file in diff1:
            print(file)

        # Display side-by-side comparison for val images and val labels
        print("\nFiles in val_images_path but not in val_labels_path:")
        for file in diff2:
            print(file)


# Example usage:
display_comparison_results()