import os
from X3DScene import X3DScene

"""
@author Benjamin Haettasch
@version 0.1

Convert all obj files in the current directory to one x3d file while storing the shape coordinates in individual src
files
"""


#Get a list of all obj files in the current directory
BASEDIR = '.'
objs = [file for file in os.listdir(BASEDIR) if file.endswith(".obj")]

#Create a empty scene to contain the final output
newScene = X3DScene()

convertedCount = 0

#Loop over all obj files...
for obj in objs:
    simplename = obj[:-4]
    #...and try to convert them into individual x3d files
    temporaryX3DFile = 'output/'+simplename+'.x3d'
    returnVal = os.system('aopt -i ' + obj + ' -Y "" -x "'+temporaryX3DFile+'"')

    #Iff this was successful...
    if returnVal == 0:
        #...move and rename the src file
        #Assume only on src file first:
        #srcfiles = [file for file in os.listdir(BASEDIR) if file.endswith(".src")]
        srcFileName = simplename+'.src'
        os.rename('src0.src', 'output/'+srcFileName)

        #...parse the generated x3d file
        scene = X3DScene.parseFile(temporaryX3DFile)
        externalShapeNode = scene.getExternalShapes()[0]

        #...change url field to new name of src file
        externalShapeNode.setAttribute('url', srcFileName)
        externalShapeNode.setAttribute('id', "node_"+simplename)

        #...and add the node to the new complete scene
        newScene.appendNodeToScene(externalShapeNode)

        #Afterwards, the original x3d file can be deleted
        os.remove(temporaryX3DFile)
        convertedCount += 1


#Write complete scene to file
outFile = open('output/out.x3d', 'w')
newScene.write(outFile)

#Show some log info
print("\n\nConversion finished.")
print("===============================================")
print("Found OBJ files: %d" % len(objs))
print("Successfully converted: %d" % convertedCount)