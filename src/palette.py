from PIL import Image

import numpy as np
from scipy.cluster.vq import whiten, kmeans
import pandas as pd

from typing import Union, Literal, Tuple, List

def resizeImages(orgImages: list, resizeLength: int, resizeHeight: int) -> list:
    ''' Returns a list of resized images (200 X 200 px). '''
    for i in range(len(orgImages)):
        orgImages[i] = orgImages[i].resize((resizeLength, resizeHeight))
    return orgImages

def combineImages(resizedImages: list, resizeLength: int, resizeHeight: int) -> Image:
    combinedImage = Image.new('RGB', (resizeLength * len(resizedImages), resizeHeight),(250,250,250))
    for i in range(len(resizedImages)):
        combinedImage.paste(resizedImages[i], (resizeLength * i, 0))
    return combinedImage

def getCombinedImage(orgImages: list , resizeLength=200, resizeHeight=200) -> Image:
    resizedImages = resizeImages(orgImages, resizeLength, resizeHeight)
    combinedImage = combineImages(resizedImages, resizeLength, resizeHeight)
    # combinedImage.show()
    print("Combined image created")
    return combinedImage

def imageToDf(finalImage: Image) -> pd.DataFrame:

    # Convert to array
    imageArr = np.array(finalImage)

    # Flatten array
    df = pd.DataFrame()
    df['r']=pd.Series(imageArr[:,:,0].flatten())
    df['g']=pd.Series(imageArr[:,:,1].flatten())
    df['b']=pd.Series(imageArr[:,:,2].flatten())

    df.head()
    return df

def whitenDf(flatDf: pd.DataFrame) -> pd.DataFrame:
    flatDf['r_whiten'] = whiten(flatDf['r'])
    flatDf['g_whiten'] = whiten(flatDf['g'])
    flatDf['b_whiten'] = whiten(flatDf['b'])

    flatDf.head()
    return flatDf

def preprocessImage(finalImage: Image) -> pd.DataFrame:
    df = imageToDf(finalImage)
    processedDf = whitenDf(df)
    return processedDf

def getKMeanColoursRGB(df: pd.DataFrame, clusterNo) -> list:
    ''' Determines the K-Mean centers and converts the data to RGB format. '''

    # K-Mean centers
    cluster_centers, distortion = kmeans(df[['r_whiten', 'g_whiten', 'b_whiten']], clusterNo)

    # Convert back to RGB
    r_std, g_std, b_std = df[['r', 'g', 'b']].std()
    colours = [] 
    for c in cluster_centers:
        sr, sg, sb = c
        colours.append((int(sr*r_std), int(sg*g_std), int(sb*b_std)))

    return colours

def getKMeanColoursHex(coloursRGB: list) -> list:
    ''' Converts the K-Mean colours from RGB to Hex format. '''
    coloursHex = []
    for colour in coloursRGB:
        colourHex = '#%02x%02x%02x' % colour
        coloursHex.append(colourHex)
    return coloursHex 

def getPalette(orgImages: list, clusterNo = 5) -> Tuple[list, list]:
    combinedImage = getCombinedImage(orgImages)
    processedDf = preprocessImage(combinedImage)
    RGB = getKMeanColoursRGB(processedDf, clusterNo)
    hex = getKMeanColoursHex(RGB)
    return RGB, hex
  
def getTextColours(paletteColours: list) -> List[tuple]:
    textColourOptions = [(255, 255, 255), (0, 0, 0)]
    textColours = []

    for colour in paletteColours:
        # Format colour
        r, g, b = colour
        colourCheck = (r * 0.299) + (g * 0.587) + (b * 0.114)

        # Add colour colour
        isBlack = colourCheck > 186
        textColours.append(textColourOptions[isBlack])


    return textColours

        


    

