import cv2
import numpy as np
import sys
import glob
import os

'''
Make sure the image has the same pixel size as the given dimmensions

References:
    https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
    https://stackoverflow.com/questions/33662693/add-pixels-in-python-opencv
    http://tsaith.github.io/combine-images-into-a-video-with-python-3-and-opencv-3.html
    https://docs.scipy.org/doc/numpy/reference/generated/numpy.concatenate.html
    https://stackoverflow.com/questions/12881926/create-a-new-rgb-opencv-image-using-python#12890573
    https://www.pythoninformer.com/python-libraries/numpy/numpy-and-images/
'''
def resize_img(img_frame, width, height, fill_color = (0, 0, 0)):
    #Get ratios
    img_height, img_width, channels = img_frame.shape
    scalar_difference_height = height / img_height
    scalar_difference_width = width / img_width

    #Resize image so that is is the same as the video aspect ratio in one dim, and less than it (or equal) in another
    scalar = 0
    if (img_height * scalar_difference_width) > height:
        scalar = scalar_difference_height
    else:
        scalar = scalar_difference_width

    new_width = int(img_width * scalar)
    new_height = int(img_height * scalar)
    new_size = (new_width, new_height)
    resized = cv2.resize(img_frame, (new_width, new_height))

    #If both dims are equal, we are done
    if new_size == (width, height):
        return resized

    #If not, we need to add blank (black) pixels. Note that a frame is a numpy array of pixels with values 0 to 255
    if new_width == width: #we need to add pixels to the top and bottom
        difference = height - new_height
        top_diff = difference // 2
        bottom_diff = difference - top_diff

        top = np.zeros((top_diff, width, channels), np.uint8)
        bottom = np.zeros((bottom_diff, width, channels), np.uint8)

        top[:,:] = fill_color
        bottom[:,:] = fill_color

        resized = np.concatenate((top, resized), axis = 0)
        resized = np.concatenate((resized, bottom), axis = 0)
    else: #we need to add pixels to the sides
        difference = width - new_width
        left_diff = difference // 2
        right_diff = difference - left_diff

        left = np.zeros((height, left_diff, channels), np.uint8)
        right = np.zeros((height, right_diff, channels), np.uint8)

        left[:,:] = fill_color
        right[:,:] = fill_color

        resized = np.concatenate((left, resized), axis = 1)
        resized = np.concatenate((resized, right), axis = 1)

    return resized

'''
Batch converts the images at a given file location to given dimensions and writes them out into given folder

Arguments
    1 input folder (containing images only)
    2 output folder (for resized images)
    3 width for resize
    4 height for resize
    5 (optional) fill color (default black). Give in the form rrr-ggg-bbb (no higher than 255-255-255)

References:
    https://docs.opencv.org/2.4/doc/tutorials/introduction/load_save_image/load_save_image.html
'''
def main():
    #Handle incorrect input
    if(len(sys.argv) < 5):
        print('Please provide the input folder, outpug folder, desired width, and desired height')
        print('For example: python batchResize.py in/folder/ out/folder/ 640 480')
        exit()

    #Collect input and handle invalid input
    inDir = sys.argv[1]
    outDir = sys.argv[2]
    fill_color = (0, 0, 0)
    if len(sys.argv) > 5:
        r, g, b = sys.argv[5].split('-')
        fill_color = (int(r), int(g), int(b))
        if fill_color[0] > 255 or fill_color[1] > 255 or fill_color[2] > 255 or fill_color[0] < 0 or fill_color[1] < 0 or fill_color[2] < 0:
            print('Invalid input: r, g, b, all must be on the interval [0, 255]')
            exit()
    try:
        width = int(sys.argv[3])
        height = int(sys.argv[4])
        if width < 1 or height < 1:
            raise ValueError('Width or height was not positive')
    except:
        print('Invalid width or height value')
        print('Please only enter positive integers for width and height')
        print('For example: python batchResize.py in/folder/ out/folder/ 640 480')
        exit()

    #Get image names (base names only)
    os.chdir(inDir)
    image_names = glob.glob('*')
    os.chdir('..')

    #Resize images
    success = 0
    for image_name in image_names:
        try:
            img_frame = resize_img(cv2.imread(os.path.join(inDir, image_name)), width, height, fill_color)
            cv2.imwrite(os.path.join(outDir, image_name), img_frame)
            success += 1
        except Exception as e:
            print('Failed to resize or write image: ' + image_name)
            print(e)
            print()

    print('Succeeded on ' + str(success) + ' / ' + str(len(image_names)) + ' (' + str((success / len(image_names)) * 100) + '%) of images')

main()