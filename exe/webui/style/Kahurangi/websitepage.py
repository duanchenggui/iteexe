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
"""
This class transforms an eXe node into a page on a self-contained website
"""

import logging
import re
from cgi                      import escape
from exe.webui.blockfactory   import g_blockFactory
from exe.engine.error         import Error
from exe.engine.path          import Path
from exe.export               import websitepage

log = logging.getLogger(__name__)


# ===========================================================================
class WebsitePage(websitepage.WebsitePage):
    """
    This class transforms an eXe node into a page on a self-contained website
    """
    def leftNavigationBar(self, pages):
        """
        Generate the left navigation string for this page
        """
        depth    = 1
        nodePath = [None] + list(self.node.ancestors()) + [self.node]

        html = "<ul id=\"navlist\">\n"

        for page in pages:
            while depth < page.depth:
                html += "<ul id=\"navlist\">\n"
                depth += 1
            while depth > page.depth:
                html += "</ul>\n"
                depth -= 1

            if page.node == self.node:
                html += "<li class=\"active "
                html += "depth%d " % page.depth 
                if page.node.children:
                    html += "withChild\">"
                else:
                    html += "withoutChild\">"
                html += escape(page.node.title)
                html += "</li>\n"
            else:
                html += "<li class=\""
                html += "depth%d " % page.depth 
                if page.node.children:
                    html += "withChild\">"
                else:
                    html += "withoutChild\">"
                html += "<a href=\""+page.name+".html\">"
                html += escape(page.node.title)
                html += "</a></li>\n"

        while depth > 1:
            html += "</ul>\n"
            depth -= 1
        html += "</ul>\n"
        return html
        
        
