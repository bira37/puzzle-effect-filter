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

  parser.add_argument('-b', '--background_path', dest='background_path', metavar='', type=str, default=None, help='Path to the background image. Default is white background')
  parser.add_argument('-i', '--input_path', dest='input_path', metavar='', type=str, default='examples/lena.png', help='Path to the input image. Default is \'examples/lena.png\'')
  parser.add_argument('-n', '--n_moving_pieces', dest='n_moving_pieces', metavar='', type=int, default=3, help='Number of pieces that are going to be moved. If the number given is bigger than the number of pieces, the default behaviour is to assume n_moving_pieces = number of pieces in the puzzle. Default number is 3.')
  parser.add_argument('-o', '--output_path', dest='output_path', metavar='', type=str, default='output.png', help='Path to save the output image (directory and name). Make sure that the directory exists. Default is \'output.png\'.')
  parser.add_argument('-t', '--type', dest='type', metavar='', type=str, default='medium', help='Size of the puzzle pieces. The choices are: small for 32x32, medium for 64x64, big for 128x128.')

  args = parser.parse_args()

  # Read the image
  original_image = cv2.imread(args.input_path)

  # Read background image
  background_image = cv2.imread(args.background_path)

  # Declare the piece size (to be changed later)
  piece_size = -1

  # Asserts
  try:
    # Check if image exists
    assert (original_image is not None), 'Image does not exist.'

    # Check if the piece type exists and get the piece size
    assert (args.type in ['big', 'small', 'medium']), 'Type of piece size does not exist.'
    if args.type == 'small':
      piece_size = 32
    elif args.type == 'big':
      piece_size = 128
    else:
      piece_size = 64

    # Check if image size is greater than two times the piece size
    assert ((original_image.shape[0] >= 2*piece_size and original_image.shape[1] >= piece_size) or (original_image.shape[0] >= piece_size and original_image.shape[1] >= 2*piece_size)), 'Input image has smaller dimensions than the puzzle piece. Make sure that the image can fit at least two puzzle pieces.'

    # Check if number of moved pieces is greater or equal than zero
    assert (args.n_moving_pieces >= 0), 'Number of pieces to be moved needs to be greater or equal than zero.'

  except AssertionError as err:
    print('Error: {}'.format(err))
    exit(1)
  
  # Create the puzzle mask and the puzzle image
  puzzle_image, puzzle_mask = puzzle_creation.create(original_image, piece_size)

  # If the user does not give a correct path to the background, create a white background image
  if background_image is None:
    background_image = np.full(puzzle_image.shape, (255, 255, 255), dtype=np.uint8)

  # Assert that the background has dimensions greater or equal than the image
  try:
    assert (background_image.shape[0] >= puzzle_image.shape[0] and background_image.shape[1] >= puzzle_image.shape[1]), 'Background needs to be bigger or equal than the image.'
  except AssertionError as err:
    print('Error: {}'.format(err))
    exit(1)

  # Transform image
  puzzle_image, puzzle_mask, foreground_mask = transformations.transform_v1(puzzle_image, puzzle_mask, piece_size, background_image.shape, args.n_moving_pieces)

  # Add background to image
  puzzle_image = effects.add_background(background_image, puzzle_image, foreground_mask)
  
  # Apply relief and shadow effects to the image
  puzzle_image, puzzle_mask = effects.apply_relief_and_shadow(puzzle_image, puzzle_mask)

  # Save the output image and the mask
  cv2.imwrite(args.output_path, puzzle_image)

if __name__ == '__main__':
  main()