from torchvision import transforms
from tqdm import tqdm_notebook
import torch
import numpy as np


def transorm_photo(photo):
    resnet_transforms = transforms.Compose([
        transforms.Resize(256),  # размер каждой картинки будет приведен к 256*256
        transforms.CenterCrop(224),  # у картинки будет вырезан центральный кусок размера 224*224
        transforms.ToTensor(),  # картинка из питоновского массива переводится в формат torch.Tensor
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # значения пикселей картинки нормализуются
    ])
    return resnet_transforms(photo)


def get_answer(model, images):
    dct = {1: 'armchair', 2: 'bed', 3: 'chair', 0:'dresser', 4: 'sofa', 5:'swivelchair', 6:'table', 7:'wardrobe'}
    model_output = model(images.reshape((1, 3, 224, 224)))
    return dct[np.argmax(model_output.data.cpu().numpy())]
