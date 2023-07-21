from PIL import Image
import os
import json
class Nft:
    metadata = ''
    number = 0
    layers = ''
    dnaPaths = ''
    folder_path = ''
    attributes_count = 0
    filteredAttributes = []
    def __init__(self, number, name, attributes, filteredAttributes,jsonTemplate, dnaPath, layers, attributes_count, folder_path, dir_path):
        self.metadata = jsonTemplate
        self.dnaPaths = dnaPath
        self.dir_path = dir_path
        self.layers = layers
        self.name = name
        self.attributes = attributes
        self.filteredAttributes = filteredAttributes
        self.number = number
        self.folder_path = folder_path
        self.attributes_count = attributes_count
    def CreateImage(self):
        baseLayer = Image.open(self.dir_path + '/input/assets/' + self.layers[0] + '/' + self.dnaPaths[0])
        baseLayer = baseLayer.convert('RGBA')
        for i in range(1, len(self.layers)):
            frontLayer = Image.open(self.dir_path + '/input/assets/' + self.layers[i] + '/' + self.dnaPaths[i])
            frontLayer = frontLayer.convert('RGBA')

            # for fixing different dimensions i added this custom code
            baseLayer = baseLayer.resize((1600,1600),Image.ANTIALIAS)
            frontLayer = frontLayer.resize((1600,1600),Image.ANTIALIAS)

            baseLayer = Image.alpha_composite(baseLayer, frontLayer)
        baseLayer = baseLayer.resize((1600,1600),Image.ANTIALIAS)
        baseLayer.save(self.dir_path + '/output/nfts/' + self.folder_path + '/' + str(self.number) + '.png', quality = 100)

    def CreateMetadata(self):
        with open(self.dir_path + '/output/nfts/' + self.folder_path + '/' + str(self.number) + '.json', 'w') as jsonFile:
            # The following two lines make this project compatible with new features in CMv2 (Candy Machine version 2)
            # The JSON metadata new requirement is named image files.  Code will work only with png files.
            # Change Date: 01/19/2022 - ck256-2000
            self.metadata['image'] = str(self.number) + '.png'
            self.metadata['properties']['files'][0] = {"uri" : str(self.number) + ".png", "type":"image/png"}
            json.dump(self.metadata, jsonFile, indent = 4)




