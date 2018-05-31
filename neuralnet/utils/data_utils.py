#!/home/akhanal1/Spring2018/pl-env/bin/python3.5
# Torch imports
import os
import sys
sys.path.append('/home/akhanal1/Spring2018/ature')
os.chdir('/home/akhanal1/Spring2018/ature')
import numpy as np
import PIL.Image as IMG
from commons.IMAGE import Image


# Flip data 4-ways and then crop to fixed 564 * 564
def get_class_weights(y):
    """
    :param y: labels
    :return: correct weights of each classes for balanced training
    """
    cls, count = np.unique(y, return_counts=True)
    counter = dict(zip(cls, count))
    majority = max(counter.values())
    return {cls: round(majority / count) for cls, count in counter.items()}


def flip_4ways(Dirs, get_mask_file, get_ground_truth_file):
    file_names = os.listdir(Dirs['images']).copy()
    for ID, img_file in enumerate(file_names):
        img_obj = Image()

        img_obj.load_file(data_dir=Dirs['images'], file_name=img_file)
        img_obj.working_arr = img_obj.image_arr

        img_obj.load_mask(mask_dir=Dirs['mask'], fget_mask=get_mask_file, erode=True)
        img_obj.load_ground_truth(gt_dir=Dirs['truth'], fget_ground_truth=get_ground_truth_file)

        working_arr = img_obj.working_arr.copy()
        ground_truth = img_obj.ground_truth.copy()
        mask = img_obj.mask.copy()

        img_obj.working_arr = np.flip(working_arr.copy(), 0)
        img_obj.ground_truth = np.flip(ground_truth.copy(), 0)
        img_obj.mask = np.flip(mask.copy(), 0)

        IMG.fromarray(img_obj.working_arr).save(Dirs['images'] + sep + 'a' + img_obj.file_name)
        IMG.fromarray(img_obj.ground_truth).save(Dirs['truth'] + sep + 'a' + get_ground_truth_file(img_obj.file_name))
        IMG.fromarray(img_obj.mask).save(Dirs['mask'] + sep + 'a' + get_mask_file(img_obj.file_name))

        img_obj.working_arr = np.flip(working_arr.copy(), 1)
        img_obj.ground_truth = np.flip(ground_truth.copy(), 1)
        img_obj.mask = np.flip(mask.copy(), 1)

        IMG.fromarray(img_obj.working_arr).save(Dirs['images'] + sep + 'b' + img_obj.file_name)
        IMG.fromarray(img_obj.ground_truth).save(Dirs['truth'] + sep + 'b' + get_ground_truth_file(img_obj.file_name))
        IMG.fromarray(img_obj.mask).save(Dirs['mask'] + sep + 'b' + get_mask_file(img_obj.file_name))

        img_obj.working_arr = np.flip(img_obj.working_arr.copy(), 0)
        img_obj.ground_truth = np.flip(img_obj.ground_truth.copy(), 0)
        img_obj.mask = np.flip(img_obj.mask.copy(), 0)

        IMG.fromarray(img_obj.working_arr).save(Dirs['images'] + sep + 'c' + img_obj.file_name)
        IMG.fromarray(img_obj.ground_truth).save(Dirs['truth'] + sep + 'c' + get_ground_truth_file(img_obj.file_name))
        IMG.fromarray(img_obj.mask).save(Dirs['mask'] + sep + 'c' + get_mask_file(img_obj.file_name))

        print('Done ' + img_obj.file_name)


def resize_DRIVE_572by572(Dirs, get_mask_file, get_ground_truth_file):
    file_names = os.listdir(Dirs['images']).copy()
    for ID, img_file in enumerate(file_names):
        img_obj = Image()

        img_obj.load_file(data_dir=Dirs['images'], file_name=img_file)
        img_obj.working_arr = img_obj.image_arr

        img_obj.load_mask(mask_dir=Dirs['mask'], fget_mask=get_mask_file, erode=True)
        img_obj.load_ground_truth(gt_dir=Dirs['truth'], fget_ground_truth=get_ground_truth_file)
        img_obj.working_arr = np.pad(img_obj.working_arr, [(0, 0), (4, 3), (0, 0)], 'constant')
        img_obj.ground_truth = np.pad(img_obj.ground_truth, [(0, 0), (4, 3)], 'constant')
        img_obj.mask = np.pad(img_obj.mask, [(0, 0), (4, 3)], 'constant')

        IMG.fromarray(img_obj.working_arr[7:579, :, :]).save(Dirs['images'] + sep + img_obj.file_name)
        IMG.fromarray(img_obj.ground_truth[7:579, :]).save(
            Dirs['truth'] + sep + get_ground_truth_file(img_obj.file_name))
        IMG.fromarray(img_obj.mask[7:579, :]).save(Dirs['mask'] + sep + get_mask_file(img_obj.file_name))

        print('Done ' + img_obj.file_name)


if __name__ == '__main__':
    os.chdir('/home/akhanal1/Spring2018/ature')

    sep = os.sep
    Dirs = {}
    Dirs['data'] = 'data' + sep + 'DRIVE' + sep + 'training'
    Dirs['images'] = Dirs['data'] + sep + 'images'
    Dirs['mask'] = Dirs['data'] + sep + 'mask'
    Dirs['truth'] = Dirs['data'] + sep + '1st_manual'


    def get_mask_file(file_name):
        return file_name.split('_')[0] + '_training_mask.gif'


    def get_ground_truth_file(file_name):
        return file_name.split('_')[0] + '_manual1.gif'


    flip_4ways(Dirs, get_mask_file, get_ground_truth_file)
    resize_DRIVE_572by572(Dirs, get_mask_file, get_ground_truth_file)
