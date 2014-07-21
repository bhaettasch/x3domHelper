__author__ = 'Benjamin Haettasch <benjamin.haettasch@igd.fraunhofer.de>'

from xml.dom.minidom import parse, parseString


class X3DScene:

    def __init__(self):
        DEFAULT_SCENE = "<X3D><Scene DEF='scene'></Scene></X3D>"
        self.dom = parseString(DEFAULT_SCENE)

    def setDom(self, newDom):
        self.dom = newDom

    def getDom(self):
        return self.dom

    def getSceneNode(self):
        return self.dom.getElementsByTagName('Scene')[0]

    def appendNodeToScene(self, node):
        sceneNode = self.getSceneNode()
        sceneNode.appendChild(node)

    def getExternalShapes(self):
        return self.dom.getElementsByTagName('ExternalShape')

    def write(self, file):
        self.dom.writexml(file, addindent="    ", newl="\n", encoding="UTF-8")

    @staticmethod
    def parseFile(file_or_filename):
        tmpScene = X3DScene()
        tmpScene.setDom(parse(file_or_filename))
        return tmpScene

#Usage example:
if __name__ == "__main__":
    INPUT_FILE = "output/03_0000_0003.x3d"
    scene = X3DScene.parseFile(INPUT_FILE)
    externalShapeNode = scene.getExternalShapes()[0]
    print externalShapeNode
    externalShapeNode.setAttribute('url', 'src233.src')

    newScene = X3DScene()
    sceneNode = newScene.getSceneNode()
    print(sceneNode)

    newScene.appendNodeToScene(externalShapeNode)

    print newScene.getDom().toprettyxml()
