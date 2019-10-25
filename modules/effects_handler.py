import cv2
import numpy as np

class EffectsHandler:

  def __init__(self):
    pass

  # Input: The image, transformed image with the puzzle and the puzzle mask
  # Output: The final result image
  @classmethod
  def apply(cls, image, puzzle_image, puzzle_mask):
    return cls.apply_v1(image, puzzle_image, puzzle_mask)
  
  # First version of apply method
  @staticmethod
  def apply_v1(image, puzzle_image, puzzle_mask):
    return puzzle_image, puzzle_mask

  #Input: The background image and the foreground image (both must have the same shape)
  #Output: The original image with a background
  @staticmethod
  def add_background(background, foreground):

    # Check if images have the same shape
    try:
      assert (background.shape == foreground.shape), 'Images must have same size and same number of channels.'
    except AssertionError as err:
      print('Error: {}'.format(err))
      exit(1)

    # Check if images have the same data type
    try:
      assert (background.dtype == foreground.dtype), 'Images must have same data type.'
    except AssertionError as err:
      print('Error: {}'.format(err))
      exit(1)

    # create alpha blending mask
    _, alpha_mask = cv2.threshold(foreground, 0, 1, cv2.THRESH_BINARY)

    # apply mask to foreground image
    foreground = cv2.multiply(alpha_mask, foreground)

    # apply negative mask to background image
    background = cv2.multiply(1 - alpha_mask, background)

    # add background and foreground images
    blended = cv2.add(background, foreground)

    # return blended image
    return blended
