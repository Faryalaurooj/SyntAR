from PIL import Image
import os
import cv2
import numpy as np

# Useful Constants and Variables
cropping_list = []
DATASET_DIR = './All_images' # Folder 1
saved_folder_path='crops_images'


IMG_EXTENSION = '.tif'

######################
# Folder 1
######################

IMG_NAME = 'algeria_dakain_0p5_0424.tif'



infile = os.path.join(DATASET_DIR, IMG_NAME)
CHOP_SIZE = 400
Image.MAX_IMAGE_PIXELS = None


def click_func(event, x, y, flags, param):
    """
    Click function that fire-up against the user click event
    :param event:
    :param x:
    :param y:
    :param flags:
    :param param:
    :return:
    """
    global cropping_list
    if event == cv2.EVENT_LBUTTONDOWN:
        x1 = x - CHOP_SIZE // 2
        x2 = x + CHOP_SIZE // 2
        y1 = y - CHOP_SIZE // 2
        y2 = y + CHOP_SIZE // 2

        cv2.rectangle(param, (x1, y1), (x2, y2), (0, 255, 0), thickness=3)
        cv2.imshow(IMG_NAME, param)
        cropping_list.append([x1, y1, x2, y2])


def crop_patch(image, cr_item):
    """
    Function to crop the patch from the loaded image
    :param image: Pillow image
    :param cr_item: Box coordinates
    :return:
    """
    width, height = image.size
    box = (cr_item[0], cr_item[1],
           cr_item[0] + CHOP_SIZE if cr_item[0] + CHOP_SIZE < width else width - 1,
           cr_item[1] + CHOP_SIZE if cr_item[1] + CHOP_SIZE < height else height - 1)
    # try:
    fname = 'slice_%s_x%03d_y%03d.png' % (IMG_NAME.replace(IMG_EXTENSION, ''), cr_item[0], cr_item[1])
    new_name = os.path.sep.join([DATASET_DIR, saved_folder_path, fname])
    image.crop(box).save(new_name)


def show_loading():
    """
    Display the loadingIMG_NAMEas a feedback for the user
    :return:
    """
    img_progress = np.ones(shape=(64, 64, 1))
    cv2.putText(img_progress, 'WORKING ON IMAGE, PLEASE WEIGHT',
                (0, 32),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (255, 255, 255,), 1, cv2.LINE_AA, False)
    cv2.imshow('Loading', img_progress)


def main():
    """
    Main function to load the image and process it using the loop
    :return:
    """
    img = cv2.imread(infile)
    height, width, _ = img.shape
    cv2.namedWindow(IMG_NAME, cv2.WINDOW_FREERATIO)
    cv2.setMouseCallback(IMG_NAME, click_func, param=img)

    while True:
        cv2.imshow(IMG_NAME, img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('e'):
            show_loading()
            img_clone = Image.open(infile)
            for crop_item in cropping_list:
                crop_patch(img_clone, crop_item)
            img_clone.close()
            cropping_list.clear()
            break  # or load next image

        elif key == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
