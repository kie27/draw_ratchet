#!/usr/bin/python
#
# Copyright (C) 2016 Kie Brooks
# Distributed under GPLv3 or later.
# draw_ratchet
# version 0.1
#
#   This file is part of draw_ratchet
#
#   draw_ratchet is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# description :
# draw ratchet gears to arbitrary sizes and precision
#
# I am not an engineer, I am sure this little program could be improved or made much more complex,
# it may contain horrible flaws but it fills my current need and should be easy to improve on.
# Alternatively pay me some money and I might do it for you ;P
#
# This program is used by inkscape.
# It can be found in the menu :  extensions -> render -> ratchet
# see file draw_ratch.inx
# (directory ~/.config/inkscape/extensions/)

import inkex, simplestyle
import math
from lxml import etree

Line_style =   { 'stroke'        : '#000000',
                 'stroke-width'  : '0.5px',
                 'fill'          : 'none' }

### SVG shape helpers
def draw_SVG_circle(parent, r, cx, cy, name, style):
    " structure an SVG circle entity under parent "
    circ_attribs = {'style': str(inkex.Style(style)),
                    'cx': str(cx), 'cy': str(cy), 
                    'r': str(r),
                    inkex.addNS('label','inkscape'): name}
    circle = etree.SubElement(parent, inkex.addNS('circle','svg'), circ_attribs )

###
class Ratchet(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("--centre_hole",      action="store", type=inkex.Boolean,
                                  dest="centre_hole",      default=True, help="Show or not")
        self.arg_parser.add_argument("--teeth",            action="store", type=int,
                                  dest="teeth",            default=12, help="Number of teeth around outside")
        self.arg_parser.add_argument("--centre_hole_diam", action="store", type=float,
                                  dest="centre_hole_diam", default=1, help="Dia of central hole")
        self.arg_parser.add_argument("--diam_in",          action="store", type=float,
                                  dest="diam_in",          default=28, help="Inner diamter of the Ratchet")
        self.arg_parser.add_argument("--diam_out",         action="store", type=float,
                                  dest="diam_out",         default=30, help="Outer diamter of the Ratchet")
        self.arg_parser.add_argument('--vtooth_shape',     action='store', type=str,
                                  dest='vtooth_shape',     default='straight', help="Shape of tooth")
        self.arg_parser.add_argument('--htooth_shape',     action='store', type=str,
                                  dest='htooth_shape',     default='curve', help="Shape of tooth")



    def effect(self):
        # sort out the options
        teeth = self.options.teeth
        diam_in = self.options.diam_in
        diam_out = self.options.diam_out
        vtooth_shape = self.options.vtooth_shape
        htooth_shape = self.options.htooth_shape
        # Create group center of view
        t = 'translate(%s,%s)' % (self.svg.namedview.center[0], self.svg.namedview.center[1])
        grp_attribs = {inkex.addNS('label','inkscape'):'Ratchet', 'transform':t}
        grp = etree.SubElement(self.svg.get_current_layer(), 'g', grp_attribs)
        #
        # Central hole (at origin)
        if self.options.centre_hole:
            draw_SVG_circle(grp, self.options.centre_hole_diam, 0,0, 'Central_hole', Line_style)
        #Polygon drawing
        #    <path d="M50,50 A30,50 0 0,1 100,100"
        #          style="stroke:#660000; fill:none;"/>
        # L - line : x posn, y posn
        # A - arc : radius x, radius y, x-axis rotation, large arc flag, sweep flag
        # Points on the ratchet
        #    b
        #    |\
        #    |  \    |\
        # \  |    \  |  \
        #  \ |      \|    \
        #    a       c      \
        path = "M%s %s " %(diam_in,0)
        for i in range(teeth):
            angle = math.radians(i * 360/ teeth)
            x_a = diam_in * math.cos(angle)
            y_a = diam_in * math.sin(angle)
            x_b = diam_out * math.cos(angle)
            y_b = diam_out * math.sin(angle)
            if vtooth_shape == "straight":
                path += ' L %s %s ' %(x_b, y_b)
            else:
                path += " A %s,%s 0 0 0 %s %s" % (diam_in, diam_in, x_b, y_b)
            #
            angle_next = math.radians((i+1) * 360 / teeth)
            x_c = diam_in * math.cos(angle_next)
            y_c = diam_in * math.sin(angle_next)
            if htooth_shape == "straight":
                path += ' L %s %s ' %(x_c, y_c)
            else: # Arc
                path += " A %s,%s 0 0 1 %s %s" % (diam_in, diam_in, x_c, y_c)
        # close path
        path += 'z'
        # draw it
        line_attribs = {'style' : str(inkex.Style(Line_style)), inkex.addNS('label','inkscape') : 'Cone' }
        line_attribs['d'] = path
        etree.SubElement(grp, inkex.addNS('path','svg'), line_attribs )


effect = Ratchet()
effect.run()	
