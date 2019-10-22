import cv2
import numpy as np

class PuzzleCreator:

  def __init__(self):
    pass

  # Input: The image
  # Output: The image with a puzzle drawn and the puzzle puzzle_mask
  @classmethod
  def create(cls, image):
    return cls.create_v2(image)

  # First version of create method
  @staticmethod
  def create_v1(image):

    puzzle_image = image.copy()

    puzzle_mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)

    # Draw a bounding box on the puzzle mask
    cv2.rectangle(puzzle_mask, (0,0), (puzzle_mask.shape[1]-1, puzzle_mask.shape[0]-1), 255, thickness=2)
    # Loop through each square piece
    for i in range(0, puzzle_mask.shape[0], 64):
      for j in range(0, puzzle_mask.shape[1], 64):

        # Check if it is not the top border before drawing
        if i != 0:
          # Draw the piece lines
          cv2.line(puzzle_mask, (j,i), (min(j+22, puzzle_mask.shape[0]), i), 255, thickness=2)
          cv2.line(puzzle_mask, (min(j+42, puzzle_mask.shape[0]),i), (min(j+64, puzzle_mask.shape[0]), i), 255, thickness=2)

          # Select the piece hole direction
          if np.random.randint(1,3) == 1:
            # Draw upwards
            cv2.ellipse(puzzle_mask, (j+32, i-16), (10, 4), 0, 180, 360, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+42, i-8), (4, 8), 0, 90, 270, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+22, i-8), (4, 8), 0, 270, 360, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+22, i-8), (4, 8), 0, 0, 90, 255, thickness=2)
          else:
            # Draw downwards
            cv2.ellipse(puzzle_mask, (j+32, i+16), (10, 4), 0, 0, 180, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+42, i+8), (4, 8), 0, 90, 270, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+22, i+8), (4, 8), 0, 270, 360, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+22, i+8), (4, 8), 0, 0, 90, 255, thickness=2)
        
        # Check if it is not the left border before drawing
        if j != 0:
          # Draw the piece lines
          cv2.line(puzzle_mask, (j,i), (j, min(i+24, puzzle_mask.shape[1])), 255, thickness=2)
          cv2.line(puzzle_mask, (j,min(i+40, puzzle_mask.shape[1])), (j, min(i+64, puzzle_mask.shape[1])), 255,thickness=2)

          # Select the piece hole direction
          if np.random.randint(1,3) == 1:
            # Draw to the left
            cv2.ellipse(puzzle_mask, (j-16, i+32), (4, 10), 0, 90, 270, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j-8, i+22), (8, 4), 0, 0, 180, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j-8, i+42), (8, 4), 0, 180, 360, 255, thickness=2)
          else:
            # Draw to the right
            cv2.ellipse(puzzle_mask, (j+16, i+32), (4, 10), 0, 270, 360, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+16, i+32), (4, 10), 0, 0, 90, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+8, i+22), (8, 4), 0, 0, 180, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+8, i+42), (8, 4), 0, 180, 360, 255, thickness=2)
    
    # Draw the puzzle on the image
    puzzle_image = cv2.bitwise_or(puzzle_image, np.dstack([puzzle_mask]*3))

    # Return the puzzle image and mask
    return puzzle_image, puzzle_mask

  # Second version of create method
  @staticmethod
  def create_v2(image):
    puzzle_image = image.copy()

    puzzle_mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)

    # Draw a bounding box on the puzzle mask
    cv2.rectangle(puzzle_mask, (0,0), (puzzle_mask.shape[1]-1, puzzle_mask.shape[0]-1), 255, thickness=2)
    # Loop through each square piece
    for i in range(0, puzzle_mask.shape[0], 64):
      for j in range(0, puzzle_mask.shape[1], 64):
        
        # Check if it is not the upper border before drawing
        if i != 0:
          if (j//64)%2:
            cv2.ellipse(puzzle_mask, (j+32, i+3), (32, 3), 0, 180 - 70, 180, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+32, i+3), (32, 3), 0, 0, 70, 255, thickness=2)
          else:
            cv2.ellipse(puzzle_mask, (j+32, i+3), (32, 3), 0, 180, 180 + 70, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+32, i+3), (32, 3), 0, 360 - 70, 360, 255, thickness=2)

          # Select the piece hole direction
          if np.random.randint(1,3) == 1:
            # Add an offset from the curve if required
            offset = 0
            if (j//64)%2:
              offset = 6
            
            # Draw upwards
            cv2.ellipse(puzzle_mask, (j+32, i-12 + offset), (10, 4), 0, 180, 360, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+42, i-6 + offset), (4, 6), 0, 90, 270, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+22, i-6 + offset), (4, 6), 0, 270, 360, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+22, i-6 + offset), (4, 6), 0, 0, 90, 255, thickness=2)
          else:
            # Add an offset from the curve if required
            offset = 0
            if (j//64)%2:
              offset = 6
            
            # Draw downwards
            cv2.ellipse(puzzle_mask, (j+32, i+12 + offset), (10, 4), 0, 0, 180, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+42, i+6 + offset), (4, 6), 0, 90, 270, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+22, i+6 + offset), (4, 6), 0, 270, 360, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+22, i+6 + offset), (4, 6), 0, 0, 90, 255, thickness=2)

        # Check if it is not the left border before drawing
        if j != 0:
          if (i//64)%2:
            cv2.ellipse(puzzle_mask, (j+3, i+32), (3, 32), 0, 270, 270 + 70, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+3, i+32), (3, 32), 0, 90 - 70, 90, 255, thickness=2)
          else:
            cv2.ellipse(puzzle_mask, (j+3, i+32), (3, 32), 0, 90, 90 + 70, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+3, i+32), (3, 32), 0, 270 - 70, 270, 255, thickness=2)
          
          # Select the piece hole direction
          if np.random.randint(1,3) == 1:
            # Add an offset from the curve if needed
            offset = 0
            if (i//64)%2:
              offset = 6

            # Draw to the left
            cv2.ellipse(puzzle_mask, (j-12 + offset, i+32), (4, 10), 0, 90, 270, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j-6 + offset, i+22), (6, 4), 0, 0, 180, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j-6 + offset, i+42), (6, 4), 0, 180, 360, 255, thickness=2)
          else:
            # Add an offset from the curve if needed
            offset = 0
            if (i//64)%2:
              offset = 6

            # Draw to the right
            cv2.ellipse(puzzle_mask, (j+12 + offset, i+32), (4, 10), 0, 270, 360, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+12 + offset, i+32), (4, 10), 0, 0, 90, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+6 + offset, i+22), (6, 4), 0, 0, 180, 255, thickness=2)
            cv2.ellipse(puzzle_mask, (j+6 + offset, i+42), (6, 4), 0, 180, 360, 255, thickness=2)

    # Draw the puzzle on the image
    puzzle_image = cv2.bitwise_or(puzzle_image, np.dstack([puzzle_mask]*3))

    # Return the puzzle image and mask
    return puzzle_image, puzzle_mask