'''
Created on 14.04.2014

@author: bhaettasch
@description: Create a html formatted and alphabetically sorted link list for all entered node names
'''

import os
from os.path import join

#Path to documentation repo
BASEPATH = "U:/x3dom/doc/out/author"
#Part of the path that has to be deleted to get relative paths
BASEREMOVE = "U:/x3dom/doc/out/"
#Part to add to the path
PATHADD = "../../../"

var = raw_input("Please enter the names of the Nodes: ")

nodes = var.split()
nodes.sort()

print ""

#Search matching nodes in the whole documentation
for node in nodes:
    for root, dirs, files in os.walk(BASEPATH):
        for name in files:
            if name == ("%s.html" % node):
                path = join(root, name).replace(BASEREMOVE, "").replace("\\", "/")
                print '<li><a href="%s%s">%s</a></li>\n' % (PATHADD, path, node)

