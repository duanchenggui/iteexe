# ===========================================================================
# eXe 
# Copyright 2004-2005, University of Auckland
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# ===========================================================================

import sys
import logging
import gettext
from exe.webui import common
from exe.engine.packagestore import g_packageStore
log = logging.getLogger(__name__)
_   = gettext.gettext


# ===========================================================================
class OutlinePane(object):
    """
    OutlinePane is responsible for creating the XHTML for the package outline
    """
    def __init__(self):
        self.package = None

    def process(self, request, package):
        """ 
        Get current package
        """
        log.debug("process")
        self.package = package
        
        if "action" in request.args:
            if request.args["action"][0] == "changeNode":
                nodeId = request.args["object"][0]
                self.package.currentNode = self.package.findNode(nodeId)

            elif request.args["action"][0] == "addChild":
                nodeId = request.args["object"][0]
                parent = self.package.findNode(nodeId)
                self.package.currentNode = parent.createChild("")
                

    def getChildrenTitles(self, node):
        """
        Recursive function for getting children's titles 
        """
        log.debug("getChildrenTitles for node="+node.idStr())

        html  = ""
        title = node.title
        if title == "":
            title = self.package.levelName(len(node.id) - 2);

        if node == self.package.currentNode:
            html += title
        else:
            html += common.submitLink(title, "changeNode", node.idStr())      

        childLevel = self.package.levelName(len(node.id) - 1);
        html += common.submitLink(_(" Add ")+childLevel, 
                                  "addChild", node.idStr(), "action")      

        if len(node.children) > 0:
            html += "<ul>\n"
            for i in range (0, len(node.children)):
                html += "<li>" 
                html += self.getChildrenTitles(node.children[i]) 
                html += "</li>\n"
                
            html += "</ul>\n"
        
        return html

            
    def render(self):
        """
        Returns an XHTML string for viewing this pane
        """
        log.debug("render")
        
        html  = "<div id=\"outline\">\n"
        html += "<ul>\n"
        html += "<li>" 
        if self.package.draft == self.package.currentNode:
            html += self.package.draft.title
        else:
            html += common.submitLink(self.package.draft.title, "changeNode", 
                                      self.package.draft.idStr())      
        html += "</li>\n"
        html += "<li>" 
        html += self.getChildrenTitles(self.package.root)
        html += "</li>\n"
        html += "</ul>\n"
        html += "</div>\n"
        return html
        
        
         


    
# ===========================================================================
