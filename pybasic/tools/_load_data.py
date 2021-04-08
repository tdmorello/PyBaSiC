import os
import numpy as np
from PIL import Image
import PIL

def load_data_old(dir, file_ext='.tif', working_size=(128,128), interpolation_method='bilinear'):
    '''
    Load all image from given directory that have the same file extension
    :param dir: Directory of images
    :param file_ext: File extension
    :param working_size: image size that the algorithm will work with
    :param interpolation_method: computation method for resizing the images
    :return: array containing all images, shape: (N,M,L) with (N,M) working size and L number of images
    '''

    all_files = os.listdir(dir)
    image_files = []
    for file in all_files:
        if file.endswith(file_ext):
            image_files.append(os.path.join(dir, file))
    stack = None
    if interpolation_method == 'bilinear':
        resample_method = PIL.Image.BILINEAR
    elif interpolation_method == 'nearest':
        resample_method = PIL.Image.NEAREST
    else:
        raise IOError('unknown interpolation method', interpolation_method)
    print('Loading image sequence...')
    for i, image_file in enumerate(image_files):
        if i % 10 == 0:
            print(i, '/', len(image_files))
        # temp_img = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
        # temp_img = cv2.resize(temp_img,(working_size[0], working_size[1]),
        #                          interpolation = cv2.INTER_LINEAR)
        temp_img = Image.open(image_file)
        temp_img = temp_img.convert('I')
        temp_img = temp_img.resize([working_size[0], working_size[1]], resample=resample_method)
        temp_img = np.asarray(temp_img)

        if stack is None:
            stack = np.expand_dims(temp_img, 2)
        else:
            stack = np.concatenate((stack, np.expand_dims(temp_img, 2)), 2)
    return stack


def load_data(dir, file_ext='.tif'):
    '''
    Load all image from given directory that have the same file extension
    :param dir: Directory of images
    :param file_ext: File extension
    :return: a list of all images (a list of numpy arrays)
    '''

    all_files = os.listdir(dir)
    image_files = []
    images = []
    for file in all_files:
        if file.endswith(file_ext):
            image_files.append(os.path.join(dir, file))
    image_files.sort()
    for i, image_file in enumerate(image_files):
        if i % 10 == 0:
            print(i, '/', len(image_files))
        temp_img = Image.open(image_file)
        temp_img = temp_img.convert('F')
        images.append(np.array(temp_img))

    return images