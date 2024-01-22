# Jordan King
# CSCI 101 Section D
# Create Project


import cv2
import numpy


def main():
    #read in image and display it
    image = cv2.imread('colorfulpic.jpeg')
    cv2.imshow('image', image)

    #get mouse clicks
    mouse_click = []
    cv2.setMouseCallback('image', get_color, mouse_click)
    cv2.waitKey(0)

    #convert the rgb image to an hsv image
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    x = mouse_click[0][0]
    y = mouse_click[0][1]

    total_hue = 0
    total_sat = 0
    total_val = 0

    #obtain average hsv values based on pixels surrounding the location of the user-click
    for row in range(5):
        for column in range(5):
            index_x = x - 2 + row
            index_y = y - 2 + column

            total_hue = total_hue + hsv_image[index_y, index_x, 0]
            total_sat = total_sat + hsv_image[index_y, index_x, 1]
            total_val = total_val + hsv_image[index_y, index_x, 2]

    average_hue = total_hue/25
    average_sat = total_sat/25
    average_val = total_val/25

    print(average_hue)
    print(average_sat)
    print(average_val)


    hue_range = 10
    sat_range = 70
    val_range = 50

    #create high and low thresholds for the hsv values
    lows = [average_hue - hue_range, (average_sat - sat_range), (average_val - val_range)]
    highs = [(average_hue + hue_range), (average_sat + sat_range), (average_val + val_range)]

    #create structuring element for morphology
    nugget = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    #create binary image from hsv image
    binary = get_binary_image(lows, highs, hsv_image)

    #morphology--to smooth things out
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, nugget)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, nugget)

    cv2.imshow('binary', binary)

    #for all rows and columns and the hue value at each pixel, where the binary image is black, make the saturation
    #zero (grayscale)
    hsv_image[:, :, 1] = numpy.where(binary == 0, 0, hsv_image[:, :, 1])

    #convert the hsv image back to rgb
    output = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    cv2.imshow("original", image)
    cv2.imshow("output", output)
    cv2.waitKey(0)

#function to get binary images based on user-chosen color--creates an image that is white at every instance of
#the color clicked, and black everywhere else
def get_binary_image(lows, highs, hsv_image):
    #separate the hsv image into its three channels: hue, saturation, and value
    hue, sat, val = cv2.split(hsv_image)

    #create binary images using the hue, sat, val images and the high and low thresholds
    #first arg is image, second arg is threshold, third arg is value to set pixels that exceed the threshold to, sets all others to 0
    _, hue_low = cv2.threshold(hue, lows[0], 255, cv2.THRESH_BINARY)
    _, hue_high = cv2.threshold(hue, highs[0], 255, cv2.THRESH_BINARY_INV)
    _, sat_low = cv2.threshold(sat, lows[1], 255, cv2.THRESH_BINARY)
    _, sat_high = cv2.threshold(sat, highs[1], 255, cv2.THRESH_BINARY_INV)
    _, val_low = cv2.threshold(val, lows[2], 255, cv2.THRESH_BINARY)
    _, val_high = cv2.threshold(val, highs[2], 255, cv2.THRESH_BINARY_INV)

    #combine them all into one binary image and return that (true when both pixels are 255)
    binary = cv2.bitwise_and(hue_low, hue_high)
    binary = cv2.bitwise_and(binary, sat_low, sat_high)
    binary = cv2.bitwise_and(binary, val_low, val_high)

    return binary

#mouse callback function
def get_color(event, x, y, flags, mouse_clicks):
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_clicks.append([x, y])
        return


if __name__ == '__main__':
    main()
