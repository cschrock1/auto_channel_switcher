import cv2
import numpy as np

def extract_scorebug(frame, region):
    """Extract the scoreboard region from the frame."""
    x, y, w, h = region
    return frame[y:y+h, x:x+w]

def scorebug_present(frame, region, threshold):
    """
    Determine whether the scoreboard is present.
    Commercials brighten the scorebug area; games usually darken it.
    """
    crop = extract_scorebug(frame, region)
    brightness = np.mean(crop)
    return brightness < threshold
