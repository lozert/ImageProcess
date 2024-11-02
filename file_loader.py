import os
import shutil

def get_images(dir, prefix="*.jpg"):
    image_paths = []
    for file_name in os.listdir(dir):
        image_paths.append(dir + "/" + file_name)
    return image_paths


def copy_images(dir, filename, reid, image_id):
    new_name = f"{reid}_i{image_id}.jpg"
    new_path = os.path.join(dir, new_name)  # Новый путь с новым именем
    shutil.copy2(filename, new_path)


def save_cropped_image(cropped_image, output_dir, new_name):
    """Сохранение кропнутого изображения в новую папку с новым именем."""
    # Проверяем, существует ли директория, если нет — создаем её
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Формируем полный путь для сохранения изображения
    save_path = os.path.join(output_dir, new_name)
    
    # Сохраняем изображение по указанному пути
    cropped_image.save(save_path)