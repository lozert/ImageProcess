import os
import glob 
import random
import shutil

image_paths = []

path = "G:/ИИ/Датасеты/Reidentification/датасет/microscope-x100-nails/2_default"

work_dir = os.getcwd()
dataset = "/reid_dataset"
upload_dirs = ["/train", "/test", "/validate"]
storage_ratios = [0.8, 0.1, 0.1]

assert len(storage_ratios) == len(upload_dirs)

for dir_name in os.listdir(path):
    image_paths.extend(glob.glob(os.path.join(path + "/" + dir_name, "*.jpg")))

random.shuffle(image_paths)


sum_ratios = 0
len_images = len(image_paths)


for index in range(len(upload_dirs)):
    upload_storage = work_dir + dataset + upload_dirs[index] #куда изображения закинуть
    
    #TODO: Будут ошибки, когда захотим поделить датасет немного в другом соотношенни
    images = image_paths[ int(len_images * sum_ratios) : int(len_images * (sum_ratios + storage_ratios[index])) ]
    sum_ratios += storage_ratios[index]

    for count, filename in enumerate(images):
        # Формируем новое имя файла
        new_name = f"{count}_{os.path.basename(filename)}"  # Добавляем префикс к имени
        new_path = os.path.join(upload_storage, new_name)  # Новый путь с новым именем
        shutil.copy2(filename, new_path)  # Копируем файл с сохранением метаданных
     

        



