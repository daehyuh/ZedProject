import cv2
import numpy as np
from PIL import Image


def maxis255(data):
    max_data, min_data = np.max(data), np.min(data)
    data = (data - min_data)/(max_data - min_data) * 255
    return data


def maxis0(data):
    max_data, min_data = np.max(data), np.min(data)
    data = round((data - max_data)/(min_data - max_data) * 255,4)
    return data


data = np.load('saved_imgs/20220524_153326528163/distance_0008.npz')
print(data['x'])
data = data['x']
print(np.max(data))
data = maxis255(data)
print(np.max(data))

pil_image=Image.fromarray(data)
pil_image.show()
