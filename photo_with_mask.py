import cv2
import numpy as np
from PIL import Image


def get_color(photo):
    im = np.array(photo)
    WHITE_COLOR = np.array([255, 255, 255])
    dct_of_colors = dict()
    dct_for_count_colors = dict()
    with open('color_borders.txt') as file:
        reader = file.read().splitlines()

    for i in reader:
        color, hsv = i.split('-')
        hsv_min_max = hsv.split(':')
        h1 = hsv_min_max[0].split(',')[0]
        s1 = hsv_min_max[0].split(',')[1]
        v1 = hsv_min_max[0].split(',')[2]
        h2 = hsv_min_max[1].split(',')[0]
        s2 = hsv_min_max[1].split(',')[1]
        v2 = hsv_min_max[1].split(',')[2]
        dct_of_colors[color] = {'hsv_min': list(map(int, [h1, s1, v1])), 'hsv_max': list(map(int, [h2, s2, v2]))}
        dct_for_count_colors[color] = 0

    for key, value in dct_of_colors.items():
        lower_range = np.array(dct_of_colors[key]['hsv_min'])
        upper_range = np.array(dct_of_colors[key]['hsv_max'])
        hsv_img = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv_img, lower_range, upper_range)
        for pixels in mask:
            for pix in pixels:
                if all(pix == WHITE_COLOR):
                    dct_for_count_colors[key] += 1
    return max(dct_for_count_colors.keys(), key=lambda x: dct_for_count_colors[x])
