import numpy as np
from PIL import Image


def split_rgb_channels(image_matrix: np.ndarray) \
        -> tuple[np.ndarray[int], np.ndarray[int], np.ndarray[int]]:
    r = image_matrix[:, :, 0]
    g = image_matrix[:, :, 1]
    b = image_matrix[:, :, 2]

    return r, g, b


def group_image_rows(r: np.ndarray, g: np.ndarray, b: np.ndarray) -> list[tuple[int, int, int]]:
    grouped_rows = []
    for row in range(len(r)):
        grouped_row = []
        for col in range(len(r[row]) - 1):
            if (r[row][col + 1] != r[row][col] or
                    g[row][col + 1] != g[row][col] or
                    b[row][col + 1] != b[row][col]):
                grouped_row.append([
                    r[row][col],
                    g[row][col],
                    b[row][col],
                    col])

        grouped_rows.append(grouped_row)
    else:
        pass

    for row in range(len(grouped_rows)):
        for col in range(len(grouped_rows[row])):
            if col == 0 or grouped_rows[row][col][1] == 0:
                grouped_rows[row][col].append(0)
            else:
                grouped_rows[row][col].append(grouped_rows[row][col][3] - grouped_rows[row][col - 1][3])

    for row in range(len(grouped_rows)):
        for col in range(len(grouped_rows[row])):
            grouped_rows[row][col].pop(3)

    return grouped_rows


def cond_rotate(image_matrix: np.ndarray) -> np.ndarray:
    pass


def rgb_normalize(img_matrix: np.ndarray) -> None:
    # assert isinstance(img_matrix, np.ndarray), "assert error"
    img_matrix[:,:, :3] /= 255.0


def main():
    with Image.open(r"E:\Загрузки\recorder\Downloads\3_809fbf03b62c52b196fba6b1d84a7dfb.jpg") as img:
        img = img.convert("RGB")

        img_data = np.array(img)

        r, g, b = split_rgb_channels(img_data)

        print(r, g, b, sep='\n')

        grouped_rows = group_image_rows(r, g, b)
        # rgb_normalize(grouped_rows)

        print(grouped_rows[0], sep='\n')


if __name__ == '__main__':
    main()
