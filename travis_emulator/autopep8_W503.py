#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) SHS-AV s.r.l. (<http://ww.zeroincombenze.it>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
"""recover W503
"""

# import os
import sys


def move_tk_line_up(tk, n, lines):
    if n > 0:
        i = lines[n].find(tk)
        l = len(tk)
        newln = lines[n][0:i] + lines[n][i+l+1:]
        if newln.strip() == "":
            lines[n] = ""
        else:
            lines[n] = newln
        n -= 1
        lines[n] = lines[n] + " " + tk


def exec_W503(filepy):
    fd = open(filepy, 'r')
    source = fd.read()
    fd.close()
    lines = source.split('\n')
    for n in range(len(lines)):
        ln = lines[n].strip()
        if ln == "or":
            tk = "or"
            move_tk_line_up(tk, n, lines)
        elif ln == "and":
            tk = "and"
            move_tk_line_up(tk, n, lines)
        if ln[0:3] == "or ":
            tk = "or"
            move_tk_line_up(tk, n, lines)
        elif ln[0:4] == "and ":
            tk = "and"
            move_tk_line_up(tk, n, lines)
    fd = open(filepy, 'w')
    for n in range(len(lines)):
        ln = lines[n] + "\n"
        fd.write(ln)
    fd.close()
    return 0


if __name__ == "__main__":
    filepy = sys.argv[1]
    sts = exec_W503(filepy)
    sys.exit(sts)
