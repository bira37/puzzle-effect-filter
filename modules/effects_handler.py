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
    return puzzle_image