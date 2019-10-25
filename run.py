import cv2
import argparse
import numpy as np 
import os
import modules.puzzle_creation as puzzle_creation
import modules.effects as effects
import modules.transformations as transformations

def main():

  # Define and parse the arguments
  parser = argparse.ArgumentParser()

  parser.add_argument('-b', '--background_path', dest='background_path', type=str, default=None, help='Path to the background image.')
  parser.add_argument('-i', '--input_path', dest='input_path', type=str, default='examples/lena.png', help='Path to the input image.')
  parser.add_argument('-o', '--output_path', dest='output_path', type=str, default='output.png', help='Path to save the output image (directory and name). Make sure that the directory exists.')
  parser.add_argument('-t', '--type', dest='type', type=str, default='normal', help='puzzle size (small, normal or big)')

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
  puzzle_image, puzzle_mask = puzzle_creation.create(original_image, args.type)

  # Initialize background related variables with None
  background_image = None
  background_shape = None

  # Check if background image exists
  if args.background_path is not None:

    # Read background image
    background_image = cv2.imread(args.background_path)

    # Get background shape
    background_shape = background_image.shape

  # Transform image
  puzzle_image, puzzle_mask = transformations.transform_v1(puzzle_image, puzzle_mask, args.type, background_shape)
  
  # Check if background image exists
  if background_image is not None:

    # Add background to image
    puzzle_image, puzzle_mask = effects.add_background(background_image, puzzle_image)
  
  # Apply relief and shadow effects to the image
  # TODO

  # Save the output image and the mask
  cv2.imwrite(args.output_path, puzzle_image)

if __name__ == '__main__':
  main()