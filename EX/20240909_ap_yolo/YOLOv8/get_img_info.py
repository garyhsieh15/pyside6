from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image_path):
    """
    获取图片的 EXIF 数据
    """
    image = Image.open(image_path)
    exif_data = image._getexif()
    if exif_data is not None:
        return {TAGS.get(tag): value for tag, value in exif_data.items()}
    else:
        return {}

def get_image_info(image_path):
    """
    获取手机拍摄照片时的相关数据
    """
    exif_data = get_exif_data(image_path)
    image_info = {}

    # 获取影像大小
    with Image.open(image_path) as img:
        image_info['Image Size'] = img.size

    # 获取焦距、曝光时间、光圈值等信息
    if 'FocalLength' in exif_data:
        image_info['Focal Length'] = exif_data['FocalLength']
    if 'ExposureTime' in exif_data:
        image_info['Exposure Time'] = exif_data['ExposureTime']
    if 'FNumber' in exif_data:
        image_info['Aperture'] = exif_data['FNumber']
    if 'ISOSpeedRatings' in exif_data:
        image_info['ISO'] = exif_data['ISOSpeedRatings']
    if 'Model' in exif_data:
        image_info['Camera Model'] = exif_data['Model']
    if 'DateTime' in exif_data:
        image_info['Date Time'] = exif_data['DateTime']

    return image_info

# 测试
image_path = r'E:\images_lab\YOLOv7\20240730_parking\datasets\test\IMG20240826154747.jpg'
image_info = get_image_info(image_path)
for key, value in image_info.items():
    print(f"{key}: {value}")