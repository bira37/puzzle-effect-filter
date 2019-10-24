import cv2
import numpy as np

class TransformationsHandler:

  def __init__(self):
    pass

  # Input: The image, image with the puzzle drawn and the puzzle mask
  # Output: The transformed image with the puzzle drawn and the transformed puzzle mask 
  @classmethod
  def transform(cls, image, puzzle_image, puzzle_mask):
    return cls.transform_v1(image, puzzle_image, puzzle_mask)

  # First version of transform method   
  @staticmethod
  def transform_v1(image, puzzle_image, puzzle_mask):
    return puzzle_image