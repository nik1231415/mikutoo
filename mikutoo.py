import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def open_image_cyrillic(path: str) -> np.ndarray:
    """
    Функция открытия картинки с кириллицей.
    Возвращает картинку.
    """
    with open(path, "rb") as f:
        file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img is None:
        raise Exception("Изображение не загрузилось")
    return img
def normalize_rgb(img: np.ndarray) -> np.ndarray:
    """
    Функция нормализации rgb-картинки.
    Возвращает матрицу цветов с нормализованными значениями от 0 до 1
    с правильным положением RGB каналов.
    """
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb / 255.0
def consecutive_counts_per_row_vectorized(img_normalized):
    """
    Функция превращает матрицу RGB цветов и индексов в матрицу цветов и кол-ва пикселей
    (будет интерпретироваться как длина либо ширина столбца).

    Возвращает матрицу счетов и матрицу цветов.
    """
    counts_list = []
    colors_list = []
    for row in img_normalized:
        # Compare each pixel with the previous one
        diff = np.any(row[1:] != row[:-1], axis=1)  # True where color changes
        change_idx = np.flatnonzero(diff) + 1  # indices where color changes
        counts = np.diff(np.r_[0, change_idx, len(row)])  # run lengths
        colors = row[np.r_[0, change_idx]]  # pick the color at start of each run

        counts_list.append(counts)
        colors_list.append(colors)

    return counts_list, colors_list
def draw_graph(colors_list, counts_list, img_normalized, plot_setting='barh') -> None:
    """
    Функция рисования диаграммы в цикле, пока не закончатся строки.
    Так как это медленный процесс, здесь предусмотрена функция уменьшения размера картинки.
    """


    print(f"Drawing graph with setting: {plot_setting}")

    fig, ax = plt.subplots(figsize=(12, 10))

    height, width = img_normalized.shape[:2]
    print(f"Image dimensions: {width}x{height}")

    for row_index, (counts, colors) in enumerate(zip(counts_list, colors_list)):
        if row_index % 10 == 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"plotting row - {row_index}/{len(counts_list)}")

        counts = np.array(counts)
        colors = [tuple(c) for c in colors]
        cum_counts = np.cumsum(counts)
        starts = np.zeros_like(counts)
        starts[1:] = cum_counts[:-1]

        if plot_setting == "barh":

            ax.barh(
                y=np.full_like(counts, row_index),
                width=counts,
                left=starts,
                color=colors,
                edgecolor=None,
                height=0.95
            )
        elif plot_setting == "barv":

            ax.bar(
                x=np.full_like(counts, row_index),
                height=counts,
                bottom=starts,
                color=colors,
                width=0.95,
                edgecolor=None
            )


    if plot_setting == "barh":

        ax.set_xlim(0, width)
        ax.set_ylim(height, 0)

    else:

        ax.set_xlim(0, height)
        ax.set_ylim(0, width)


    ax.set_aspect('equal')
    plt.tight_layout()
    plt.show()
def rotate_image_on_setting(img_normalized, plot_setting):
    """
    Из-за особенности матриц цветов картинки следует повернуть, в зависимости от настройки.
    Эта функция принимает картинку и возвращает ее повернутую версию
    в зависимости от настройки диаграммы.
    """
    assert plot_setting in ["barh", "barv"], "plot_setting must be 'barh' or 'barv'"

    if plot_setting == "barv":

        rotated_image = cv2.rotate(img_normalized, cv2.ROTATE_90_CLOCKWISE)
    else:

        rotated_image = img_normalized.copy()

    return rotated_image
def resize_image_for_speed(img_normalized: np.ndarray, max_size=300) -> np.ndarray:
    """
    Функция циклического уменьшения разрешения картинки, пока ее максимальное измерение не будет
    меньше max_size. Сделано по причине проблем с быстродействием.
    """
    height, width = img_normalized.shape[:2]
    if max(height, width) <= max_size:
        return img_normalized

    scale_factor = max_size / max(height, width)
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    img_resized = cv2.resize(
        img_normalized,
        (new_width, new_height),
        interpolation=cv2.INTER_NEAREST
    )

    return img_resized


def main():

    plot_setting = str(input("Enter plot setting: barv / barh:  "))

    path = input("Enter path to image: ").strip().strip('"').strip("'").lower()

    print("Opening image:")
    img = open_image_cyrillic(path)

    print("Normalizing image:")
    img_normalized = normalize_rgb(img)

    print(f"Original image shape: {img_normalized.shape}")

    print("Resizing image:")
    img_normalized = resize_image_for_speed(img_normalized)

    print(f"Resized image shape: {img_normalized.shape}")

    print("Rotating image based on plot setting:")
    rotated_image = rotate_image_on_setting(img_normalized, plot_setting)
    print(f"Rotated image shape: {rotated_image.shape}")

    print("Grouping consecutive colors:")
    counts_list, colors_list = consecutive_counts_per_row_vectorized(rotated_image)

    print(f"Number of rows processed: {len(counts_list)}")
    print(f"Number of colors per row: {[len(c) for c in colors_list[:5]]}...")

    print("Drawing graph:")
    draw_graph(colors_list, counts_list, rotated_image, plot_setting)

    print("Done!")


if __name__ == '__main__':
    main()