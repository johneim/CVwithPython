# Implement an unsharp masking operation
# (http://en.wikipedia.org/wiki/Unsharp_masking) by blurring an image and then
# subtracting the blurred version from the original. This gives a sharpening
# effect to the image. Try this on both color and grayscale images.

import argparse
from PIL import Image
from numpy import array, zeros, uint8
from pylab import imshow, show, gray, figure, contour, axis
from scipy.ndimage import filters


parser = argparse.ArgumentParser(description='Apply unsharp filter.')
parser.add_argument('sigma', metavar='sigma', type=int, default=1,
                   nargs='?', help='Sigma for gaussian blue')
parser.add_argument('scale', metavar='scale', type=float, default=0.1,
                   nargs='?', help='scale for gaussian subtraction')
parser.add_argument('--bw', dest='blackwhite', action='store_true',
                   help='use a black and white image.')

args = parser.parse_args()

raw_image = Image.open('data/empire.jpg')
if args.blackwhite:
  raw_image = raw_image.convert('L')
im = array(raw_image)

if args.blackwhite:
  im2 = filters.gaussian_filter(im, args.sigma)
else:
  im2 = zeros(im.shape)
  for i in range(3):
    im2[:,:,i] = filters.gaussian_filter(im[:,:,i],args.sigma)
    im2 = uint8(im2)

if args.blackwhite:
  scaled_blurred_image = args.scale*im2
  sharpened_image = im - scaled_blurred_image
else:
  scaled_blurred_image = args.scale*im2.astype('float')
  sharpened_image = im.astype('float') - scaled_blurred_image
  sharpened_image = sharpened_image.astype('uint8')


figure()

if args.blackwhite:
  gray()

imshow(sharpened_image)
axis('equal')
axis('off')

show()

