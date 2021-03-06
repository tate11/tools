#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) SHS-AV s.r.l. (<http://www.zeroincombenze.org>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
"""
    Zeroincombenze® unit test library for python programs Regression Test Suite
"""

# import pdb
import os
import os.path
import sys
from zerobug import Z0test

__version__ = "1.1.4"

MODULE_ID = 'wok_news'
TEST_FAILED = 1
TEST_SUCCESS = 0


def version():
    return __version__


# Run main if executed as a script
if __name__ == "__main__":
    Z = Z0test
    ctx = Z.parseoptest(sys.argv[1:],
                        version=version())
    UT_LIST = ["__version_V_" + __version__ + os.path.join(Z.pkg_dir,
                                                           "wok_news.py"),]
    sts = Z.main_file(ctx, UT=UT_LIST)
    exit(sts)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
