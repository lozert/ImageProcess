import random
from PIL import Image, ImageDraw

def central_crop(img, coef_crop=0.5):
    """Центральный кроп изображения."""
    img_width, img_height = img.size
    crop_height, crop_width = img_height * coef_crop, img_width * coef_crop
    
    left = (img_width - crop_width) // 2
    top = (img_height - crop_height) // 2
    right = (img_width + crop_width) // 2
    bottom = (img_height + crop_height) // 2
    
    img_cropped = img.crop((left, top, right, bottom))
    
    return img_cropped, (left, top, right, bottom)


def _compute_intersection_area(box1, box2):
    """Вычисляет площадь пересечения двух прямоугольников."""
    left1, top1, right1, bottom1 = box1
    left2, top2, right2, bottom2 = box2
    
    inter_left = max(left1, left2)
    inter_top = max(top1, top2)
    inter_right = min(right1, right2)
    inter_bottom = min(bottom1, bottom2)
    
    if inter_right > inter_left and inter_bottom > inter_top:
        return (inter_right - inter_left) * (inter_bottom - inter_top)
    else:
        return 0

def random_crop_with_iou(img, central_box, coef_crop=0.5, coef_iou=0.4):
    """Рандомный кроп с точным пересечением в 40% с центральным кропом."""
    img_width, img_height = img.size
    crop_height, crop_width = img_height * coef_crop, img_width * coef_crop

    # Координаты центрального кропа
    left_central, top_central, right_central, bottom_central = central_box
    central_width = right_central - left_central
    central_height = bottom_central - top_central

    # Площадь центрального кропа
    central_area = central_width * central_height

    # Целевая площадь пересечения
    target_intersection_area = central_area * coef_iou

    while True:
        # Генерация случайных координат для рандомного кропа
        left = random.uniform(0, img_width - crop_width)
        top = random.uniform(0, img_height - crop_height)
        right = left + crop_width
        bottom = top + crop_height

        random_box = (left, top, right, bottom)

        # Площадь пересечения случайного и центрального кропа
        intersection_area = _compute_intersection_area(random_box, central_box)

        # Если площадь пересечения примерно равна 40%, возвращаем случайный кроп
        if abs(intersection_area - target_intersection_area) / target_intersection_area < 0.05:
            img_cropped = img.crop(random_box)
            return img_cropped, random_box
    
    

def draw_boxes_on_image(img, boxes, colors):
    """Добавляет прямоугольники на изображение."""
    draw = ImageDraw.Draw(img)
    
    for box, color in zip(boxes, colors):
        left, top, right, bottom = box
        draw.rectangle([left, top, right, bottom], outline=color, width=3)
    
    return img

# Проверочный запуск
if __name__ == "__main__":
    import os
    work_dir = os.getcwd()
    img_dir = work_dir + "/reid_dataset/validate/0_image_083.jpg"
    coef_crop = 0.5
    coef_iou = 0.4

    image = Image.open(img_dir)

    # Центральный кроп
    central_crop_img, central_box = central_crop(image, coef_crop)
    print(f"Central crop box: {central_box}")

    # Рандомный кроп с нужным IoU
    random_crop_img, random_box = random_crop_with_iou(image, central_box, coef_crop, coef_iou)
    print(f"Random crop box: {random_box}")



    # Отображение изображения с нарисованными прямоугольниками
    image_with_boxes = image.copy()
    image_with_boxes = draw_boxes_on_image(image_with_boxes, [central_box, random_box], ['red', 'blue'])

    image_with_boxes.show()  # Показываем изображение с прямоугольниками
