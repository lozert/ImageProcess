from PIL import Image
from file_loader import get_images, copy_images, save_cropped_image
from crop_image import central_crop, random_crop_with_iou
import os

dir = os.getcwd() 
dir_validate = dir + "/validate" # папка откуда берутся изображения для формирования query and gallery
dir_train = dir + "/train" # Папка откуда берутся данные для train

# Новые папки, куда сохраняться кропнутые изображения
dir_gallery_crop = dir + "/cropped/gallery/" 
dir_train_crop = dir + "/cropped/train/"
dir_query_crop = dir + "/cropped/query/"


coef_crop = 0.5 # коофицент кропа
coef_iou = 0.4 # коофицент пересеченения изображений
image_train = get_images(dir_train)
image_validate = get_images(dir_validate)


count = 0 # так сказать reid чтоб не было одинаковых id у изображений
count_random_crop = 6 # Количество кропов

#train
def train():
    for filename in image_train:
        img = Image.open(filename)
        crop_image, central_bbox = central_crop(img, coef_crop)

        new_name = f"{count}_i1.jpg"
        save_cropped_image(crop_image, dir_train_crop, new_name)
        for i in range(count_random_crop):
            new_name = f"{count}_i{i+2}.jpg"
            random_crop, random_bbox = random_crop_with_iou(img, central_bbox, coef_crop, coef_iou)
            save_cropped_image(random_crop, dir_train_crop, new_name)

        count +=1

#query and gallery 
def query_gallery(count):
    for filename in image_validate:
        img = Image.open(filename)
        crop_image, central_bbox = central_crop(img, coef_crop)

        new_name = f"{count}_i1.jpg"
        save_cropped_image(crop_image, dir_query_crop, new_name)
        for i in range(count_random_crop):
            new_name = f"{count}_i{i+2}.jpg"
            random_crop, random_bbox = random_crop_with_iou(img, central_bbox, coef_crop, coef_iou)
            save_cropped_image(random_crop, dir_gallery_crop, new_name)

        count +=1

query_gallery(count)