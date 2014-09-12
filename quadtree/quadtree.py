from PIL import Image
import math
import os
import re
import shutil

"""
:author Benjamin Haettasch
:email Benjamin.Haettasch@igd.faunhofer.de
:company Fraunhofer Institut fuer Graphische Datenverarbeitung, Darmstadt, Deutschland
:version 0.1
"""


class Quadtree():
    """
    A class to create a quadtree out of images with a button up approach
    The implementation is robust and can deal with missing tiles or tilecounts that cannot be divided by 4
    It assumes either a flat input strategy
    or the files to lay in folders with the same name as the filename if using the prepareInputFiles function
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    levelCount = 0
    xStart = 0
    xEnd = 0
    yStart = 0
    yEnd = 0
    xRange = 0
    yRange = 0

    @staticmethod
    def merge(im1, im2, im3, im4, outPath, size, mode, resize=False):
        """
        Merge four image quadratic patches to one image

        :param im1: First image to merge
        :param im2: Second image to merge
        :param im3: Third image to merge
        :param im4: Fourth image to merge
        :param outPath: Name and path of the newly created file
        :param size: Size of the input patch
        :param mode: Color mode of the target image
        :param resize: Whether to resize the image to the size of one patch
        """
        out = Image.new(mode, (size*2, size*2), (0, 0, 0))
        out.paste(im1, (0, size))
        out.paste(im2, (0, 0))
        out.paste(im3, (size, size))
        out.paste(im4, (size, 0))
        if resize:
            out = out.resize((size, size))
        out.save(outPath, 'JPEG')

    @staticmethod
    def openImage(filename, targetSize=4096, targetMode='RGB'):
        """
        Open an image with the given name and path
        If it is not possible to open an image, return a white image with the given size and color mode

        :param filename: Path and name of the image
        :param targetSize: Size the placeholder image should have
        :param targetMode: Color mode the placeholder image should have
        :return: the image or a placeholder if the filename was not valid
        """
        try:
            im = Image.open(filename)
        except IOError:
            im = Image.new(targetMode, (targetSize, targetSize), (255, 255, 255))
        return im

    def setRange(self, xStart, xEnd, yStart, yEnd):
        """
        Set coordinate ranges of the input tiles.
        This allows to build the tree out of only a part of data where the area does not have to start at 0
        It also calculates width and depth of the tree

        :param xStart: start coordinate in x direction
        :param xEnd: end coordinate in x direction
        :param yStart: start coordinate in y direction
        :param yEnd: end coordinate in y direction
        """
        self.xStart = xStart
        self.xEnd = xEnd
        self.yStart = yStart
        self.yEnd = yEnd
        self.xRange = xEnd - xStart + 1
        self.yRange = yEnd - yStart + 1
        self.levelCount = int(math.ceil(math.log(max(self.xRange, self.yRange), 2))) + 1

    def prepareInputFiles(self, path, targetPath, search, replace):
        """
        Prepare input files by copying to a flat folder structure and renaming them to the given format

        :param path: input path
        :param targetPath: path where the tree is build
        :param search: regular expression to extract the coordinates from the filename
        :param replace: new name of the file
        """
        folders = os.listdir(path)
        try:
            os.makedirs(targetPath)
        except OSError:
            print "Output path already exists - no need to create newly"

        for folder in folders:
            if path + "/" + folder == targetPath:
                continue
            newName = re.sub(search, replace, folder)
            shutil.copyfile(path+'/'+folder+'/'+folder+'.jpg', targetPath+'/'+newName)

    @staticmethod
    def buildFileName(prefix, path, level, x, y):
        """
        Construct the name of a file with given level and coordinates

        :param prefix: prefix to add to file name
        :param path: path where the file is/will be stored
        :param level: level of the tree the file belongs to
        :param x: start coordinate in x direction the file represents
        :param y: start coordinate in y direction the file represents
        :return: a matching name to either open or save the image
        """
        #return "%s/%s_%d_%d_%d.jpg" % (path, prefix, level, x, y)
        return path + '/' + prefix + '_' + str(level) + '_' + str(x) + '_' + str(y) + '.jpg'

    def build(self, prefix, path, size, mode):
        """
        Build a quadtree with the given params and based upon the range already set

        :param prefix: prefix each file name should have
        :param path: path where the tree should be build
        :param size: size each tile will have (quadratic, in pixels)
        :param mode: color mode each output image should use
        """
        offset = 2
        for level in reversed(range(1, self.levelCount)):
            print level
            indexOffset = offset / 2

            for x in range(self.xStart, self.xEnd + 1, offset):
                print x
                for y in range(self.yStart, self.yEnd + 1, offset):

                    im1 = Quadtree.openImage(Quadtree.buildFileName(prefix, path, level+1, x, y))
                    im2 = Quadtree.openImage(Quadtree.buildFileName(prefix, path, level+1, x, y + indexOffset))
                    im3 = Quadtree.openImage(Quadtree.buildFileName(prefix, path, level+1, x + indexOffset, y))
                    im4 = Quadtree.openImage(Quadtree.buildFileName(prefix, path, level+1, x + indexOffset, y + indexOffset))

                    Quadtree.merge(im1, im2, im3, im4, Quadtree.buildFileName(prefix, path, level, x, y), size, mode, True)
            offset *= 2
