import cv2
import numpy as np

# Input
def transform_v1(puzzle_image, puzzle_mask, piece_type, background_shape=None):

  # Get piece size based on type
  type_to_size = {'big':128, 'normal':64, 'small':32}
  piece_size = type_to_size[piece_type]

  # Create visited matrix
  # Initially the puzzle borders are setted as visited
  vis = puzzle_mask >= 1

  # Create offset lists
  dx = [-1,  0, 0, 1]
  dy = [ 0, -1, 1, 0]

  # Create variables for rows and cols
  rows = puzzle_image.shape[0]
  cols = puzzle_image.shape[1]

  # Iterate over centers of all pieces
  for i in range(piece_size // 2, rows, piece_size):
    for j in range(piece_size // 2, cols, piece_size):

      # Randomly pick pieces to transform
      if vis[i, j] == False and np.random.randint(1,20) == 1:
        # Do a BFS to visit each pixel of the piece with center at (i, j)
        q = []
        q.append((i, j))
        while q:
          x, y = q.pop(0)

          # Turn each pixel from the piece with center at (i, j) black
          puzzle_image[x, y] = 0

          # Iterate over adjacents
          for k in range(0, 4):
            if 0 <= x + dx[k] < rows and 0 <= y + dy[k] < cols and vis[x + dx[k], y + dy[k]] == False:
              vis[x + dx[k], y + dy[k]] = True
              q.append((x + dx[k], y + dy[k]))

  if background_shape is not None:
    puzzle_image = add_padding(puzzle_image, background_shape)
    puzzle_mask = add_padding(puzzle_mask, background_shape)

  return puzzle_image, puzzle_mask

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