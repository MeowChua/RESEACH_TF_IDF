import cv2
import numpy as np

def sobel_edge_detection(image_path, blur_ksize=7, sobel_ksize=1, skipping_threshold=30):

    img = cv2.imread(image_path)
 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gaussian = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
 
    sobelx64f = cv2.Sobel(img_gaussian, cv2.CV_64F, 1, 0, ksize=sobel_ksize)
    abs_sobel64f = np.absolute(sobelx64f)
    img_sobelx = np.uint8(abs_sobel64f)

    sobely64f = cv2.Sobel(img_gaussian, cv2.CV_64F, 1, 0, ksize=sobel_ksize)
    abs_sobel64f = np.absolute(sobely64f)
    img_sobely = np.uint8(abs_sobel64f)

    img_sobel = (img_sobelx + img_sobely)/2
   
    for i in range(img_sobel.shape[0]):
        for j in range(img_sobel.shape[1]):
            if img_sobel[i][j] < skipping_threshold:
                img_sobel[i][j] = 0
            else:
                img_sobel[i][j] = 255
    return img_sobel

img = cv2.imread("test.jpg")


# image_original = cv2.imread('test.jpg', cv2.IMREAD_COLOR)
# # remove noise
# image_gray = cv2.cvtColor(image_original, cv2.COLOR_BGR2GRAY)
# # Reduce noise in image
# img = cv2.GaussianBlur(image_gray, (3, 3), 0)
# # Filter the image using filter2D, which has inputs: (grayscale image, bit-depth, kernel)
# filtered_image = cv2.Laplacian(img, ksize=3, ddepth=cv2.CV_16S)
# # converting back to uint8
# filtered_image = cv2.convertScaleAbs(filtered_image)

# cv2.imshow('original', image_original)
# cv2.imshow('proceesed', filtered_image)
# k = cv2.waitKey(0)
# if k == 27:         # wait for ESC key to exit
#     cv2.destroyAllWindows()