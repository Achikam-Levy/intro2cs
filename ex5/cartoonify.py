import math
import copy
import sys
from sys import argv

import ex5_helper


def separate_channels(image):
    """

    :param image: 3d image
    :return: new separate_channels image
    """
    new_image = []
    channels = image[0][0]
    columns = image[0]
    for k in range(len(channels)):
        new_image.append([])
        for i in range(len(image)):
            new_image[k].append([])
            for j in range(len(columns)):
                new_image[k][i].append(image[i][j][k])
    return new_image


def combine_channels(channels):
    """

    :param channels: separate_channels image
    :return: new combine_channels image
    """
    combine_image = []
    for i in range(len(channels[0])):  # runs to 2
        combine_image.append([])
        for k in range(len(channels[0][0])):  # runs to 1
            combine_image[i].append([])
            for j in range(len(channels)):  # runs to 3
                combine_image[i][k].append(channels[j][i][k])
    return combine_image


def color_avarage(pixel):
    """

    :param pixel: pixel
    :return: avarage_pixel
    """
    pixel[0] = pixel[0] * 0.299
    pixel[1] = pixel[1] * 0.587
    pixel[2] = pixel[2] * 0.114
    avarage_pixel = pixel[0] + pixel[1] + pixel[2]
    return round(avarage_pixel)


def RGB2grayscale(colored_image):
    """

    :param colored_image: colored image
    :return: grey image
    """
    new_colored_image = copy.deepcopy(colored_image)
    new_colored_image = new_colored_image
    columns = new_colored_image[0]
    for row in range(len(new_colored_image)):
        for column in range(len(columns)):
            new_colored_image[row][column] = color_avarage(
                new_colored_image[row][column])
    return new_colored_image


def blur_kernel(size):
    """

    :param size: number for size
    :return: list for blur
    """
    global new_lst
    for i in range(size):
        new_lst = []
        in_new_lst = []
        for r in range(size):
            in_new_lst.append(1 / (size ** 2))
            new_lst.append(in_new_lst)
    return new_lst


def new_matrix(kernel):
    """

    :param kernel: size for kernel
    :return: flat matrix for kernel
    """
    flat_matrix = []
    for i in range(len(kernel)):
        for r in range(len(kernel)):
            flat_matrix.append(kernel[i][r])
    return flat_matrix


def apply_kernel(image, kernel):
    """

    :param image: image
    :param kernel: the kernel function
    :return: nwe kerneld image
    """
    new_image = copy.deepcopy(image)
    flat_matrix = new_matrix(kernel)
    r = ((len(kernel)) // 2)
    for row1 in range(len(new_image)):
        for num1 in range(len(new_image[0])):
            current = image[row1][num1]
            sum_pix = 0
            empty_matrix = []
            for row in range(row1-r, row1 + r+1):
                for num in range(num1-r, num1+r+1):
                        if (row > (len(new_image)-1) or row < 0
                                or num > len(new_image[0])-1 or num < 0):
                            empty_matrix.append(current)
                        else:
                            empty_matrix.append(image[row][num])
            for multip in range(len(empty_matrix)):
                sum_pix += flat_matrix[multip]*empty_matrix[multip]
            sum_pix = round(sum_pix)
            if sum_pix < 0:
                sum_pix = 0
            if sum_pix > 255:
                sum_pix = 255
            new_image[row1][num1] = sum_pix
    return new_image


def bilinear_interpolation(image, y, x):
    """

    :param image: image
    :param y: cordinate
    :param x: cordinate
    :return: value according to the cordinates
    """
    a = image[math.floor(y)][math.floor(x)]
    b = image[math.ceil(y)][math.floor(x)]
    c = image[math.floor(y)][math.ceil(x)]
    d = image[math.ceil(y)][math.ceil(x)]
    x = x - math.floor(x)
    y = y - math.floor(y)
    singel_value = (a * (1 - x) * (1 - y)) + (b * y * (1 - x)) + (
                c * x * (1 - y)) + (d * x * y)
    singel_value = round(singel_value)
    return singel_value


def resize(image, new_height, new_width):
    """

    :param image: image
    :param new_height: new_height
    :param new_width: new_width
    :return: new resize image
    """
    new_row = (len(image)-1)/(new_height-1)
    new_column = (len(image[0])-1)/(new_width-1)
    new_image = []
    for row in range(new_height):
        new_image.append([])
        for column in range(new_width):
            new_image[row].append(bilinear_interpolation(image, row*new_row, column*new_column))
    return new_image


def rotate_90(image, direction):
    """

    :param image: image
    :param direction: r or l
    :return: new rotate image
    """
    new_image = [] * len(image)
    for i in range(len(image[0])):
        new_image.append([])
    if direction == 'R' or direction == 'r':
        for row in range((len(image)-1), -1, -1):
            for column in range(len(image[0])):
                new_image[column].append(image[row][column])
        return new_image
    else:
        for column in range(len(image[0])):
            for row in range(len(image)):
                new_image[column].append(image[row][column])
        new_image_L = []
        for r in range((len(new_image)-1), -1, -1):
            new_image_L.append(new_image[r])
    return new_image_L


def get_edges(image, blur_size, block_size, c):
    """

    :param image: imge
    :param blur_size: blur param
    :param block_size: param for edges
    :param c: param for threshold
    :return: new edges image
    """
    new_image = copy.deepcopy(image)
    blurred_image = apply_kernel(image, blur_kernel(blur_size))
    r = block_size // 2
    for row1 in range(len(blurred_image)):
        for num1 in range(len(blurred_image[0])):
            current = blurred_image[row1][num1]
            empty_matrix = []
            for row in range(row1 - r, row1 + r + 1):
                for num in range(num1 - r, num1 + r + 1):
                    if (row > (len(blurred_image) - 1) or row < 0
                            or num > len(blurred_image[0]) - 1 or num < 0):
                        empty_matrix.append(current)
                    else:
                        empty_matrix.append(blurred_image[row][num])
            sum_pix = sum(empty_matrix)
            threshold = sum_pix/(len(empty_matrix))
            if blurred_image[row1][num1] < (threshold - c):
                new_image[row1][num1] = 0
            else:
                new_image[row1][num1] = 255
    return new_image


def quantize(image,N):
    """

    :param image: 3d image
    :param N: number of colors
    :return: new quantize image
    """
    new_image = copy.deepcopy(image)
    for row in range(len(new_image)):
        for column in range(len(new_image[0])):
            new_image[row][column] = round((math.floor(image[row][column]*(N/255)))*255/N)
    return new_image


def quantize_colored_image(image, N):
    """

    :param image: 3d image
    :param N: number of colors
    :return: new quantize image
    """
    new_image = copy.deepcopy(image)
    new_separate = separate_channels(new_image)
    for channel in range(len(new_separate)):
        new_separate[channel] = quantize(new_separate[channel], N)
    combine_new_separate = combine_channels(new_separate)
    return combine_new_separate


def add_mask(image1, image2, mask):
    """

    :param image1: 3d image
    :param image2: 3d image
    :param mask: 2d image
    :return: combined 3 images
    """
    new_image = copy.deepcopy(image1)
    if isinstance(image1[0][0], int):
        for row in range(len(new_image)):
            for column in range(len(new_image[0])):
                new_image[row][column] = round((image1[row][column]) * (mask[row][column])
                           + (image2[row][column])* (1 - mask[row][column]))
    elif isinstance(image1[0][0][0], int):
        for i in range(len(new_image)):
            for row in range(len(new_image[0])):
                for column in range(len(new_image[0][0])):
                    new_image[i][row][column] = round((image1[i][row][column]) * (mask[i][row])
                               + (image2[i][row][column])* (1 - mask[i][row]))
    return new_image


def resize_values(image, max_new_image_value):
    """

    :param image: image
    :param max_new_image_value: value for resize
    :return: two values for resize
    """
    rows = len(image)
    columns = len(image[0])
    big = max(rows, columns)
    small = min(rows, columns)
    ratio = big/max_new_image_value
    small = small/ratio
    return round(small),  round(max_new_image_value)


def make_mask(image):
    """

    :param image: image
    :return: image mask
    """
    for row in range(len(image)):
        for column in range(len(image[0])):
            image[row][column] = (image[row][column] / 255)
    return image


def resize_if_image_vivid(image, max_im_size):
    """

    :param image: image
    :param max_im_size:resize param
    :return: new resized image
    """
    new_height, new_width = resize_values(image, max_im_size)
    new_image = copy.deepcopy(image)
    if isinstance(new_image[0][0][0], int):
        new_image = separate_channels(new_image)
        for channel in range(len(new_image)):
            new_image[channel] = resize(new_image[channel], new_height, new_width)
        new_small_image = combine_channels(new_image)
    else:
        new_small_image = resize(new_image, new_height, new_width)
    return new_small_image


def convert_2d_3d(blackahite_image):
    """

    :param blackahite_image: 2d image
    :return: 3d blackahite_image
    """
    for row in range(len(blackahite_image)):
        for column in range(len(blackahite_image[0])):
            new_lst = []
            new_lst.append(blackahite_image[row][column])
            new_lst.append(blackahite_image[row][column])
            new_lst.append(blackahite_image[row][column])
            blackahite_image[row][column] = new_lst
    return blackahite_image


def cartoonify(image, blur_size, th_block_size, th_c, quant_num_shades):
    """

    :param image: image
    :param blur_size: blur param
    :param th_block_size:
    :param th_c:
    :param quant_num_shades:
    :return:
    """
    new_image = copy.deepcopy(image)
    new_image1 = copy.deepcopy(new_image)
    grey_image = RGB2grayscale(new_image1)
    quantize_new_image1 = quantize_colored_image(new_image, quant_num_shades)
    edges_new_image2 = get_edges(grey_image, blur_size, th_block_size, th_c)
    edges_new_image3 = copy.deepcopy(edges_new_image2)
    edges_image_3d = convert_2d_3d(edges_new_image2)
    mask_image = make_mask(edges_new_image3)
    cartoon_image = add_mask(quantize_new_image1, edges_image_3d, mask_image)
    return cartoon_image


def main():
    variabels = sys.argv
    if len(variabels) == 8:
        image_source = variabels[1]
        cartoon_dest = variabels[2]
        max_im_size = int(variabels[3])
        blur_size = int(variabels[4])
        th_block_size = int(variabels[5])
        th_c = float(variabels[6])
        quant_num_shades = int(variabels[7])
        initial_image = ex5_helper.load_image(image_source)
        new_small_image = resize_if_image_vivid(initial_image, max_im_size)
        cartoon_image = cartoonify(new_small_image, blur_size, th_block_size, th_c, quant_num_shades)
        ex5_helper.save_image(cartoon_image, cartoon_dest)
    else:
        print("wrong argument")
        sys.exit()


if __name__ == "__main__":
    main()







