import cv2
import numpy as np
import matplotlib.pyplot as plt
import os



def open_image_cyrillic(path: str) -> np.ndarray:
    with open(path, "rb") as f:
        file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)

    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        raise Exception("Изображение не загрузилось")

    return img
def normalize_rgb(img: np.ndarray[np.uint8]) -> np.ndarray:
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb / 255.0
def consecutive_counts_per_row_vectorized(img_normalized):
    diff = img_normalized[:, 1:] != img_normalized[:, :-1]

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
def finish_plotting(ax, img_normalized):
    if ax:
        ax.set_xlim(0,img_normalized.shape[1])
        ax.set_ylim(0, img_normalized.shape[0])
        plt.gca().set_aspect(1.0)
        plt.show()
    print("showing graph:")
def draw_graph(colors_list, counts_list, img_normalized, plot_setting='barh')-> None:
    ax = None
    print("defining subplot")

    print("looping over rows")

    fig, ax = plt.subplots(figsize=(10,10))
    for row_index, (counts, colors) in enumerate(zip(counts_list, colors_list)):

        loading_end = max(img_normalized.shape[0], img_normalized.shape[1])
        if row_index % 10 == 0:
            os.system('cls')
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
                height = 1.0
            )

        elif plot_setting == "barv":
            ax.bar(
                x=np.full_like(counts, row_index),
                height=counts,
                bottom=starts,
                color=colors,
                width=1.0,
                edgecolor=None
            )

    if plot_setting == "barv":
        ax.set_ylim(img_normalized.shape[0], 0)  # Flip Y so top is 0
        ax.set_xlim(0, img_normalized.shape[1])
    else:
        ax.set_ylim(img_normalized.shape[0], 0)  # Flip Y so top is 0
        ax.set_xlim(0, img_normalized.shape[1])

    ax.set_aspect('equal')
    plt.show()

def rotate_image_on_setting(img_normalized, plot_setting):
    assert plot_setting == "barh" or plot_setting == "barv", "assertion error"
    if plot_setting == "barv":
        rotated_image = cv2.rotate(img_normalized, cv2.ROTATE_90_CLOCKWISE)

    elif plot_setting == "barh":
        rotated_image = cv2.flip(cv2.rotate(img_normalized, cv2.ROTATE_180), 1)



    return rotated_image
def resize_image_for_speed(img_normalized: np.ndarray, max_size = 300) -> np.ndarray:
    height, width = img_normalized.shape[:2]
    if max(height, width) <= max_size:
        return img_normalized

    scale_factor = max_size / max(height, width)
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    img_resized = cv2.resize(
        img_normalized,
        (new_width, new_height),  # (width, height)
        interpolation=cv2.INTER_NEAREST_EXACT # best for shrinking
    )

    return img_resized






def main():

    plot_setting = "barv"

    path = r"E:\Загрузки\a6ffe95b222409190cd60e9b165192fb.jpg"
    print("opening image:")
    img = open_image_cyrillic(path)
    print("normalizing image:")
    img_normalized = normalize_rgb(img)

    print("resizing image:")
    img_normalized = resize_image_for_speed(img_normalized)

    print("rotating image:")
    rotated_image = rotate_image_on_setting(img_normalized,plot_setting)

    print("grouping values:")
    counts_list, colors_list  = consecutive_counts_per_row_vectorized(rotated_image)

    print(f"Old image shape: {img.shape[0]}x{img.shape[1]}")
    print(f"New image shape: {rotated_image.shape[0]}x{rotated_image.shape[1]}")



    print("drawing graph:")
    draw_graph(colors_list, counts_list, rotated_image, plot_setting)


    print()


if __name__ == '__main__':
    main()

