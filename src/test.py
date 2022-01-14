from PIL import Image

import numpy as np
from scipy.cluster.vq import whiten, kmeans
import pandas as pd

from typing import Union, Literal, Tuple, List

def getTextColours(paletteColours: list) -> List[tuple]:
    textColourOptions = [(255, 255, 255), (0, 0, 0)]
    textColours = []

    for colour in paletteColours:
        # Format colour
        uiRGB = [(c / 255) for c in colour]
        r, g, b = uiRGB
        colourCheck = (r * 0.299) + (g * 0.587) + (b * 0.114)

        # Add colour colour
        isBlack = colourCheck > 186
        textColours.append(textColourOptions[isBlack])

    return textColours


paletteColours = [(185, 181, 171), (5, 14, 20), (247, 250, 249), (189, 44, 46), (42, 113, 140)]
textColours = getTextColours(paletteColours)
print(textColours)