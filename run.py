import cv2
import argparse
import numpy as np 
import os
from modules.puzzle_creator import PuzzleCreator
from modules.effects_handler import EffectsHandler
from modules.transformations_handler import TransformationsHandler

def main():

  # Define and parse the arguments
  parser = argparse.ArgumentParser()

  parser.add_argument('-i', '--input_path', dest='input_path', type=str, default='examples/lena.png', help='Path to the input image.')
  parser.add_argument('-o', '--output_path', dest='output_path', type=str, default='output.png', help='Path to save the output image (directory and name). Make sure that the directory exists.')

  args = parser.parse_args()

  # Read the image
  original_image = cv2.imread(args.input_path)

  # Check if image exists
  try:
    assert (original_image is not None), 'Image does not exist.'
  except AssertionError as err:
    print('Error: {}'.format(err))
    exit(1)
  
  # Create the puzzle mask and the puzzle image
  puzzle_image, puzzle_mask = PuzzleCreator.create(original_image)

  # Transform the image and the puzzle mask
  puzzle_image, puzzle_mask = TransformationsHandler.transform(original_image, puzzle_image, puzzle_mask)

  # Apply Effects to the image
  output_image = EffectsHandler.apply(original_image, puzzle_image, puzzle_mask)
  
  # Save the output image and the mask
  cv2.imwrite(args.output_path, output_image)

if __name__ == '__main__':
  main()