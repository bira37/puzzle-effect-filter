import cv2
import numpy as np
import queue

# Input
def transform_v1(puzzle_image, puzzle_mask, piece_size, background_shape, n_moving_pieces):

  # Create visited matrix
  vis = np.zeros(puzzle_mask.shape)

  # Create offset lists
  dx = [-1,  0, 0, 1]
  dy = [ 0, -1, 1, 0]

  # Create variables for rows and cols
  rows = puzzle_image.shape[0]
  cols = puzzle_image.shape[1]

  # Create foreground_mask, where 1 is foreground and 0 background
  foreground_mask = np.full(puzzle_mask.shape, 1, dtype=np.uint8)

  # Initialize variables
  puzzle_i = 0
  puzzle_j = 0

  # Check if background and original shapes are different
  if background_shape != puzzle_image.shape:
    puzzle_image, puzzle_i, puzzle_j = add_padding(puzzle_image, background_shape)
    puzzle_mask, _, _ = add_padding(puzzle_mask, background_shape)
    foreground_mask, _, _ = add_padding(foreground_mask, background_shape)

  # create array with pieces indices
  indices = np.indices((rows // piece_size, cols // piece_size)).transpose((1, 2, 0))
  indices = indices.reshape(((rows // piece_size * cols // piece_size), 2))
  indices = np.random.permutation(indices)
  
  # if n_moving_pieces is bigger than the number of pieces
  # n_moving_pices = number of pieces
  n_moving_pieces = np.minimum(len(indices), n_moving_pieces)

  # iterate over pieces indices 
  for ind in range(0, n_moving_pieces):
    
    # get image coordinate from index
    i, j = index_to_coordinate(indices[ind], piece_size)
    
    # add image offset to coordinates
    i += puzzle_i
    j += puzzle_j

    # Do a BFS to visit each pixel of the piece with center at (i, j)
    q = queue.Queue(maxsize = 0)
    q.put((i, j))
    vis[i - puzzle_i, j - puzzle_j] = True

    while not q.empty():
      x, y = q.get()

      # Turn each pixel from the piece with center at (i, j) black
      puzzle_image[x, y] = 0
      foreground_mask[x, y] = 0

      # If it's a border, delete its neighbors and mark them as visited 
      if puzzle_mask[x,y] == 255:
        puzzle_mask[x,y] = 0
        foreground_mask[x, y] = 0
        vx = [0, 1, 0, -1, 1, -1, 1, -1]
        vy = [1, 0, -1, 0, 1, 1, -1, -1]
        for k in range(0, 8):
          if puzzle_i <= x + vx[k] < rows + puzzle_i and puzzle_j <= y + vy[k] < cols + puzzle_j and vis[x + vx[k] - puzzle_i, y + vy[k] - puzzle_j] == False:
            vis[x + vx[k] - puzzle_i, y + vy[k] - puzzle_j] = True
            puzzle_mask[x + vx[k], y + vy[k]] = 0
            puzzle_image[x + vx[k], y + vy[k]] = 0
            foreground_mask[x + vx[k], y + vy[k]] = 0
        continue

      # Iterate over adjacents
      for k in range(0, 4):
        if puzzle_i <= x + dx[k] < rows + puzzle_i and 0 <= y + dy[k] < cols + puzzle_j and vis[x + dx[k] - puzzle_i, y + dy[k] - puzzle_j] == False:
          vis[x + dx[k] - puzzle_i, y + dy[k] - puzzle_j] = True
          q.put((x + dx[k], y + dy[k]))

  # Filter similar to erosion to fix some borders imperfections when pieces are deleted
  for iter in range(2):
    kernel = np.ones((9,9), dtype=np.int16)
    kernel[4,4] = 0
    filtered_mask = puzzle_mask.astype(np.int16)
    filtered_mask = cv2.filter2D(filtered_mask, -1, kernel)

    # Apply corrections on foreground_mask
    correction_mask = np.zeros(filtered_mask.shape, dtype = np.uint8)
    correction_mask[filtered_mask <= 255*5] = 255
    correction_mask = cv2.bitwise_or(correction_mask, correction_mask, mask = puzzle_mask)
    foreground_mask[correction_mask == 255] = 0

    # Apply corrections on puzzle_mask
    puzzle_mask[filtered_mask <= 255*5] = 0

  # Delete borders from foreground
  foreground_mask[puzzle_mask == 255] = 0  
  foreground_mask = np.dstack([foreground_mask]*3)
  return puzzle_image, puzzle_mask, foreground_mask

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

  return padded_image, left_corner_x, left_corner_y

def index_to_coordinate(index, piece_size):
  i, j = index
  i_coord = i * piece_size + piece_size // 2
  j_coord = j * piece_size + piece_size // 2
  return i_coord, j_coord 