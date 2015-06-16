"""
This Twitterbot takes an image from your local memory. 
Transfroms it in different ways.
Saves the transformed picture on you computer. 
And finally post it on twitter.
"""


"""importing the librarys needed for image processing""" 
from PIL import Image, ImageFilter, ImageColor, ImageOps #Python Image Libray: adds image processing capabilities to your Python interpreter
import numpy as np #nummerical python used for calculating huge arrays and matrices with numeric data 
import colorsys #contains function for converting between different Colormodes as RGB and other 
import random #contains different random number generators 


"""importing the librarys needed for posting the image on twitter""" 
import tweepy 		#needed to acess the twitter API 
import sys 			#sys module offers constants, functions and methodes from the python interpreter
from keys import* 	#specific keys for verify the twitter acount login 


################################################################
# defining several methods how the imagine could be transformed#
################################################################

"""Using Image Module"""
#just flips the image upsidedown 
def flip(img):
    return img.transpose(Image.FLIP_TOP_BOTTOM)

#rotates the image with a specific degree (e.g 90)
def rotate(img):
	return img.transpose(Image.ROTATE_90)


"""Using ImageOps Module""" #Image Operations 
#turning the image into an one chanel (L) grayscale image 
def grayscale(img):
    return ImageOps.grayscale(img)

#substitute different colors to the white and black pixels. It expact a RGB tuple for each of them. (Only works with RGB colormode)
def color_change(img):
    return ImageOps.colorize(img, (255, 0, 0),(0, 0, 255))


"""Using ImageFilter Module"""
#applying gaussian blur to the image. Changing the radius(intensity) of the blur 
def blur(img):
    return img.filter(ImageFilter.GaussianBlur(radius=4))

#applying contour to the image 
def contour(img):
    return img.filter(ImageFilter.CONTOUR)
#applying a edge enhancement to the image 
def edge(img):
    return img.filter(ImageFilter.EDGE_ENHANCE_MORE)


################################################################
# some more advanced image processing                          #
################################################################

# shifting pixels with a specific amount | rows or columns 
def shifting_pixels(img, fn=None, amount=10, horizontal=True):
    
    if fn is None:
        fn = shift_list

    # getting the imagine demention > full image 
    ymax, xmax = img.size 

    # converting the input (image) into an array with numpy 
    a1 = np.asarray(img)
    a2 = np.zeros((xmax, ymax, 3))

    # shifting columns of pixels
    if horizontal is True:

        # iterate over half(xmax / 2) of the rows | any other array of the image could be selected full image would be xmax /1 
        for x in range(xmax / 2):
            #define the amount the pixels should be moved with a random selector in a number array("amount" can be replaced by any number)
            d = random.randint(-amount, amount)
            row = a1[x,:,:] 
            a2[x,:,:] = fn(row, d)

        # iterate over the other half
        for x in range(xmax / 2, xmax):
            a2[x,:,:] = a1[x,:,:]

    # sorting rows of pixels
    else:

        # iterate over half(ymax / 2) of the columns
        for y in range(ymax / 2):
            d = random.randint(-amount, amount)
            col = a1[:,y,:]
            a2[:,y,:] = fn(col, d)

        # iterate over the other half
        for y in range(ymax / 2, ymax):
            a2[:,y,:] = a1[:,y,:]

  
    # turn the numpy array back into an image
    a2 = np.uint8(a2)
    out = Image.fromarray(a2)

    # return the result (image)
    return out


def shift_list(lst, amount):

    # make sure we got lists
    lst = list(lst)

    # combine slices
    lst = lst[amount:] + lst[:amount]
    return lst


#pixel sorting using numpy 
def sort(img, fn=None, horizontal=True, reverse=False):
    
    # get image dimensions > full image |other demensions are possible 
    ymax, xmax = img.size

    #you can apply brightness, redness, yellowness and hue to fn as they are defined below  
    if fn is None:
        fn = brightness
    else: 
        fn = redness

    # lets work with arrays and numpy (changing the image into numpy usable data)
    a1 = np.asarray(img)
    a2 = np.zeros((xmax, ymax, 3))

    # sorting rows(x) of pixels
    if horizontal is True:

        # iterate over all the rows(xmax) or any other amount of the image (e.g half (xmax / 2))
        for x in range(xmax / 1):
            row = a1[x,:,:]
            a2[x,:,:] = sorted(row, key=fn, reverse=reverse)

        for x in range(xmax / 1, xmax):
            a2[x,:,:] = a1[x,:,:]

    else:

        # iterate over all columns(y) or any other amount of the image (e.g half (ymax / 2))
        for y in range(ymax / 1):
            col = a1[:,y,:]
            a2[:,y,:] = sorted(col, key=fn, reverse=reverse)

        # iterate over the other half
        for y in range(ymax / 1, ymax):
            a2[:,y,:] = a1[:,y,:]
  
    # turn the numpy array back into an image
    a2 = np.uint8(a2)
    out = Image.fromarray(a2)

    # return the result (image)
    return out

################################################################
#defining some further image processings which are colled above#
#and will determine the order of colors  					   #
################################################################

def brightness(c):
    """ assign a value to each color """
    r, g, b = c
    return 0.01 * r + 0.587 * g + 0.114 * b

def redness(c):
    """ return the amount of red """
    r, g, b = c
    return r

def yellowness(c):
    """ return the amount of yellow """
    r, g, b = c
    return r * 0.5 + g * 0.5

def hue(c):
    """ return the hue of some color """
    r, g, b = c
    h, s, v = colorsys.rgb_to_hsv(float(r), float(g), float(b))
    return h

################################################################
# trying new stuff                   #
################################################################
# Sorts a given row of pixels
def sort_interval(interval):
    if interval == []:
        return []
    else:
        return(sorted(interval, key = lambda x: x[0] + x[1] + x[2]))


################################################################
# calling the functions we have defined above         		   #
################################################################

if __name__ == "__main__":

    #loading any image from your local memory
    img = Image.open("test1.jpg")

    #applying any of the defined filters to the image
    img = sort(img, fn=None, horizontal=False, reverse=True)
    img = shifting_pixels(img, amount=480, horizontal=True)
    img = shifting_pixels(img, amount=480, horizontal=False)
    #img = blur(img)

    #showing the image on your computer
    img.show()

    #saving the transformed image with a new name on your local memory 
    img.save("new_test.jpg")


################################################################
# posting the new transformed image on twitter         		   #
################################################################

#checking the keys of the specific twitter account 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

#authorization for the twitter API
api = tweepy.API(auth)

#choose the image which should be uploaded 
image = "new_test.jpg"

#this will show up in ur shell 
print("Tweeting at %s" % api.me().name)
print("Posting image: %s" % image)

#choosing the words which should be posted with the image 
if len(sys.argv) == 1:
    api.update_with_media(image, status="Posting an Image")
else:
    api.update_with_media(image, status=" ".join(sys.argv[1:]))

































