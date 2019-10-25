import cv2
import numpy as np

def transform_v1(image, puzzle_image, puzzle_mask):
  return puzzle_image

# Input: Image and padding shape
# Output: Padded image
def add_padding(image, padding_shape):

  try:
    assert (padding_shape[0] >= image.shape[0] and padding_shape[1] >= image.shape[1]), 'Padding size must be equal or bigger than image size.'
  except AssertionError as err:
    print('Error: {}'.format(err))
    exit(1)

  # Create empty image
  padded_image = np.zeros((padding_shape[0], padding_shape[1], image.shape[2]), dtype=np.uint8)

  # Calculate image left corner x position
  left_corner_x = padding_shape[0] - image.shape[0]
  left_corner_x //= 2

  # Calculate image left corner y position
  left_corner_y = padding_shape[1] - image.shape[1]
  left_corner_y //= 2

  # Center image on padded image
  padded_image[left_corner_x:left_corner_x + image.shape[0], left_corner_y:left_corner_y + image.shape[1]] = image

  return padded_image