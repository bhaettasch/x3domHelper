import os
from X3DScene import X3DScene
import re

"""
@author Benjamin Haettasch
@version 0.1

Convert all x3dv files in the current directory to one x3d file while storing the shape coordinates in individual src
files
"""


#Get a list of all obj files in the current directory
BASEDIR = '.'
x3dvs = [file for file in os.listdir(BASEDIR) if file.endswith(".x3dv")]

#Create a empty scene to contain the final output
newScene = X3DScene()

convertedCount = 0
createdSRCCount = 0

#Loop over all obj files...
for x3dv in x3dvs:
    simplename = x3dv[:-5]
    #...and try to convert them into individual x3d files
    temporaryX3DFile = 'out_lod2/'+simplename+'.x3d'
    returnVal = os.system('aopt -i ' + x3dv + ' -F Scene:"cacheopt(true)" -Y "sharedSRCs(true)" -x "'+temporaryX3DFile+'"')

    #Iff this was successful...
    if returnVal == 0:

        #Assume only on src file first:
        #srcfiles = [file for file in os.listdir(BASEDIR) if file.endswith(".src")]

        #...parse the generated x3d file
        scene = X3DScene.parseFile(temporaryX3DFile)
        externalShapeNodes = scene.getExternalShapes()
        if len(externalShapeNodes) == 1:
            externalShapeNode = scene.getExternalShapes()[0]

            #...move and rename the src file
            srcFileName = simplename+'.src'
            os.rename('src0.src', 'out_lod2/'+srcFileName)

            #...change url field to new name of src file
            externalShapeNode.setAttribute('url', srcFileName)
            externalShapeNode.setAttribute('id', "node_"+simplename)
            externalShapeNode.setAttribute('DEF', "node_"+simplename)

            #...and add the node to the new complete scene
            newScene.appendNodeToScene(externalShapeNode)

            createdSRCCount += 1

        else:
            for i, externalShapeNode in enumerate(externalShapeNodes):
                #Get name of the src
                originalSrcUrl = externalShapeNode.getAttribute('url')
                matchedSRC = re.search(r"(src\d+.src)", originalSrcUrl)
                originalSrc = matchedSRC.group(0)

                #...move and rename the src file
                srcFileName = simplename+'_'+str(i)+'.src'
                os.rename(originalSrc, 'out_lod2/'+srcFileName)

                #...change url field to new name of src file
                externalShapeNode.setAttribute('url', srcFileName)
                externalShapeNode.setAttribute('id', "node_"+simplename)

                #...and add the node to the new complete scene
                newScene.appendNodeToScene(externalShapeNode)

                createdSRCCount += 1

        #Afterwards, the original x3d file can be deleted
        os.remove(temporaryX3DFile)
        convertedCount += 1


#Write complete scene to file
outFile = open('out_lod2/out.x3d', 'w')
newScene.write(outFile)

#Show some log info
print("\n\nConversion finished.")
print("===============================================")
print("Found X3DV files: %d" % len(x3dvs))
print("Successfully converted files: %d" % convertedCount)
print("Created SRCs: %d" % createdSRCCount)