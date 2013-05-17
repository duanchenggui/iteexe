# ===========================================================================
# eXe 
# Copyright 2004-2006, University of Auckland
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
"""
ReflectionBlock can render and process ReflectionIdevices as XHTML
"""

import logging
from exe.webui.block               import Block
from exe.webui                     import common
from exe.webui.element      import TextAreaElement

log = logging.getLogger(__name__)


# ===========================================================================
class NotaBlock(Block):
    """
    ReflectionBlock can render and process ReflectionIdevices as XHTML
    """
    def __init__(self, parent, idevice):
        """
        Initialize a new Block object
        """
        Block.__init__(self, parent, idevice)
        self.commentInstruc   = idevice.commentInstruc

        # to compensate for the strange unpickling timing when objects are 
        # loaded from an elp, ensure that proper idevices are set:

        if idevice.commentTextArea.idevice is None: 
            idevice.commentTextArea.idevice = idevice


        self.commentElement    = TextAreaElement(idevice.commentTextArea)

        self.previewing        = False # In view or preview render

        if not hasattr(self.idevice,'undo'): 
            self.idevice.undo = True


    def process(self, request):
        """
        Process the request arguments from the web server
        """
        Block.process(self, request)

        is_cancel = common.requestHasCancel(request)

        if not is_cancel:
            self.commentElement.process(request)
            if "title"+self.id in request.args:
                self.idevice.title = request.args["title"+self.id][0]
        

    def renderEdit(self, style):
        """
        Returns an XHTML string with the form element for editing this block
        """
        html  = "<div class=\"iDevice\"><br/>\n"
        html += common.textInput("title"+self.id, self.idevice.title)
        html += self.commentElement.renderEdit()
        html += "<br/>" + self.renderEditButtons()
        html += "</div>\n"
        return html

    def renderPreview(self, style):
        """ 
        Remembers if we're previewing or not, 
        then implicitly calls self.renderViewContent (via Block.renderPreview) 
        """ 

        self.previewing = True
        return self.renderNote()

    def renderView(self, style): 
        """ 
        Remembers if we're previewing or not, 
        then implicitly calls self.renderViewContent (via Block.renderPreview) 
        """ 
        self.previewing = False
        return self.renderNote()
        


    
    
    def renderNote(self):
        """
        Returns an XHTML string for this block
        """
        html = u'<div class="classnote">\n'
        if  self.commentElement.field.content:
            html += '<div class="notetitleex" onclick="toggleFeedback(\'%s\')">' % self.id 
        else:
            html += '<div class="notetitle">'
        html +='%s</div>' % self.idevice.title
        if  self.commentElement.field.content:
            """
            html += u'<input type="button" class="notebtn" onclick="toggleFeedback(\'%s\')"' % self.id
            html += u'value="%s" />\n' % _(u"Show/Hide")
            """
            html += '<div id="fb%s" class="notearea">' % self.id        
            
            if self.previewing: 
                html += self.commentElement.renderPreview()            
            else:
                html += self.commentElement.renderView()

            html += "</div>\n"
        if self.previewing:
            html+=Block.renderViewButtons(self)
        html += "</div>\n"

        
        return html
    

from exe.engine.notaidevice  import NotaIdevice
from exe.webui.blockfactory        import g_blockFactory
g_blockFactory.registerBlockType(NotaBlock, NotaIdevice)  

# ===========================================================================