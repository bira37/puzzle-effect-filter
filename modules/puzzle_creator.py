import cv2
import numpy as np

class PuzzleCreator:

  def __init__(self):
    pass

  # Input: The image
  # Output: The image with a puzzle drawn and the puzzle puzzle_mask
  @classmethod
  def create(cls, image):
    return cls.create_v1(image)

  # First version of create method
  @staticmethod
  def create_v1(image):

    puzzle_image = image.copy()

    puzzle_mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)

    # Draw a bounding box on the puzzle mask
    cv2.rectangle(puzzle_mask, (0,0), (puzzle_mask.shape[1]-1, puzzle_mask.shape[0]-1), 255, thickness=1)
    # Loop through each square piece
    for i in range(0, puzzle_mask.shape[1], 64):
      for j in range(0, puzzle_mask.shape[0], 64):

        # Check if it is not the top border before drawing
        if i != 0:
          # Draw the piece lines
          cv2.line(puzzle_mask, (j,i), (min(j+22, puzzle_mask.shape[0]), i), 255, thickness=1)
          cv2.line(puzzle_mask, (min(j+42, puzzle_mask.shape[0]),i), (min(j+64, puzzle_mask.shape[0]), i), 255, thickness=1)

          # Select the piece hole direction
          if np.random.randint(1,3) == 1:
            # Draw upwards
            cv2.ellipse(puzzle_mask, (j+32, i-16), (10, 4), 0, 180, 360, 255, thickness=1)
            cv2.ellipse(puzzle_mask, (j+42, i-8), (4, 8), 0, 90, 270, 255, thickness=1)
            cv2.ellipse(puzzle_mask, (j+22, i-8), (4, 8), 0, 270, 360, 255, thickness=1)
            cv2.ellipse(puzzle_mask, (j+22, i-8), (4, 8), 0, 0, 90, 255, thickness=1)
          else:
            # Draw downwards
            cv2.ellipse(puzzle_mask, (j+32, i+16), (10, 4), 0, 0, 180, 255, thickness=1)
            cv2.ellipse(puzzle_mask, (j+42, i+8), (4, 8), 0, 90, 270, 255, thickness=1)
            cv2.ellipse(puzzle_mask, (j+22, i+8), (4, 8), 0, 270, 360, 255, thickness=1)
            cv2.ellipse(puzzle_mask, (j+22, i+8), (4, 8), 0, 0, 90, 255, thickness=1)
        
        # Check if it is not the left border before drawing
        if j != 0:
          # Draw the piece lines
          cv2.line(puzzle_mask, (j,i), (j, min(i+24, puzzle_mask.shape[1])), 255, thickness=1)
          cv2.line(puzzle_mask, (j,min(i+40, puzzle_mask.shape[1])), (j, min(i+64, puzzle_mask.shape[1])), 255,thickness=1)

          # Select the piece hole direction
          if np.random.randint(1,3) == 1:
            # Draw to the left
            cv2.ellipse(puzzle_mask, (j-16, i+32), (4, 10), 0, 90, 270, 255, thickness=1)
            cv2.ellipse(puzzle_mask, (j-8, i+22), (8, 4), 0, 0, 180, 255, thickness=1)
            cv2.ellipse(puzzle_mask, (j-8, i+42), (8, 4), 0, 180, 360, 255, thickness=1)
          else:
            # Draw to the right
            cv2.ellipse(puzzle_mask, (j+16, i+32), (4, 10), 0, 270, 360, 255, thickness=1)
            cv2.ellipse(puzzle_mask, (j+16, i+32), (4, 10), 0, 0, 90, 255, thickness=1)
            cv2.ellipse(puzzle_mask, (j+8, i+22), (8, 4), 0, 0, 180, 255, thickness=1)
            cv2.ellipse(puzzle_mask, (j+8, i+42), (8, 4), 0, 180, 360, 255, thickness=1)
    
    # Draw the puzzle on the image
    puzzle_image = cv2.bitwise_or(puzzle_image, np.dstack([puzzle_mask]*3))

    # Return the puzzle image and mask
    return puzzle_image, puzzle_mask