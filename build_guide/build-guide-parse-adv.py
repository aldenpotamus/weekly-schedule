import os
import sys
import re
import random
from PIL import Image, ImageFilter, ImageOps

javascript = '''
if(imgPixel.red > imgPixel.blue && imgPixel.red > imgPixel.green) {
    imgDNA += 'R'
} else if((imgPixel.red > imgPixel.blue && imgPixel.red < imgPixel.green) || (imgPixel.red < imgPixel.blue && imgPixel.red > imgPixel.green)) {
    imgDNA += 'r'
} else {
    imgDNA += 'X'
}

if(imgPixel.blue > imgPixel.red && imgPixel.blue > imgPixel.green) {
    imgDNA += 'B'
} else if((imgPixel.blue > imgPixel.red && imgPixel.blue < imgPixel.green) || (imgPixel.blue < imgPixel.red && imgPixel.blue > imgPixel.green)) {
    imgDNA += 'b'
} else {
    imgDNA += 'X'
}

if(imgPixel.green > imgPixel.red && imgPixel.green > imgPixel.blue) {
    imgDNA += 'G'
} else if((imgPixel.green > imgPixel.red && imgPixel.green < imgPixel.blue) || (imgPixel.green < imgPixel.red && imgPixel.green > imgPixel.blue)) {
    imgDNA += 'g'
} else {
    imgDNA += 'X'
}

if(imgPixel.red == imgPixel.blue == imgPixel.green <= 30) {
    imgDNA += '*'
} else if(imgPixel.red == imgPixel.blue == imgPixel.green) {
    imgDNA += '='
} else {
    imgDNA += '-'
}
'''

import json
f = open('./build-seed-pixels.json')
brutePixels = json.load(f)

def getPixel(img, pixel):
    return img.getdata()[img.width*pixel[1]+pixel[0]]

def extractDNA(img, seedPixels):
    imgDNA = ''
    for pixelToGet in seedPixels:
        pixelToGet = (int(pixelToGet[0]/2), int(pixelToGet[1]/2))
        imgPixel = getPixel(img, pixelToGet)[0:3]
        
        if imgPixel[0] > imgPixel[1] and imgPixel[0] > imgPixel[2]:
            imgDNA += 'R'
        elif (imgPixel[0] > imgPixel[1] and imgPixel[0] < imgPixel[2]) or (imgPixel[0] < imgPixel[1] and imgPixel[0] > imgPixel[2]):
            imgDNA += 'r'
        else:
            imgDNA += 'X'
        
        if imgPixel[1] > imgPixel[0] and imgPixel[1] > imgPixel[2]:
            imgDNA += 'B'
        elif (imgPixel[1] > imgPixel[0] and imgPixel[1] < imgPixel[2]) or (imgPixel[1] < imgPixel[0] and imgPixel[1] > imgPixel[2]):
            imgDNA += 'b'
        else:
            imgDNA += 'X'
        
        if imgPixel[2] > imgPixel[0] and imgPixel[2] > imgPixel[1]:
            imgDNA += 'G'
        elif (imgPixel[2] > imgPixel[0] and imgPixel[2] < imgPixel[1]) or (imgPixel[2] < imgPixel[0] and imgPixel[2] > imgPixel[1]):
            imgDNA += 'g'
        else:
            imgDNA += 'X'
        
        if imgPixel[0] == imgPixel[1] == imgPixel[2] <= 30:
            imgDNA += '*'
        elif imgPixel[0] == imgPixel[1] == imgPixel[2]:
            imgDNA += '='
        else:
            imgDNA += '-'

    return imgDNA

def testSeed(imgs, seedPixels):
    prints = {}
    for img in images:
        dna = extractDNA(img, seedPixels)

        if dna not in prints:
            prints[dna] = re.sub('.png$', '', re.sub(r'^.*\\', '', img.filename))
        else:
            print(f"FAIL ON {img.filename} and {prints[dna]}")
            return None 

    return prints

images = []
for filename in os.listdir("./perks"):
    image = Image.open(os.path.join("./perks", filename))
    images.append(image)

result = testSeed(images, brutePixels)

print(result)