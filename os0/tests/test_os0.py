#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) SHS-AV s.r.l. (<http://www.zeroincombenze.it>)
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
# For software version see main


"""
     Test module os0
     This module provide OS indipendent interface
     Can manage: linux, Windows and OpenVMS

     Execution test results:
     Date        Author      Linux           Windows        OpenVMS
     2015-01-27  antoniov    python V2.6.6   python V2.7.6  python V2.7.9
                             CentOS V6.5     Windows 7      OpenVMS-IA64 V8.4

"""

# import pdb
import os
import os.path
from os0 import os0
from sys import platform as _platform


class Test:
    # Execute code tests os.path library at low level
    # The purpose is not test os.path module but OpenVMS version on module.
    # Local OpenVMS filesystem has some structure like Windows
    # (Windows inherited filesystem from old PDP/VMS)
    # This program is tested on Linux, Windows and OpenVMS platform
    # in order to verify results (see above header)

    def test_path_splitdrive(self, txtid, fsrc, dtgt, ftgt):
        os0.wlog1("Test ", txtid,
                  ": os.path.splitdrive", dtgt,
                  "->", ftgt)
        d, p = os.path.splitdrive(fsrc)
        if d != dtgt or p != ftgt:
            os0.wlog("Test {0} failed!!!".format(txtid))
            os0.wlog("Expected values {0}, {1}!".format(dtgt, ftgt))
            raise Exception("Test failed!!!")

    def test_path_linux(self):
        self.test_path_splitdrive("0.10",
                                  "myFile.ext",
                                  "", "myFile.ext")
        self.test_path_splitdrive("0.11",
                                  "/usr1/lib/myFile.ext",
                                  "", "/usr1/lib/myFile.ext")
        self.test_path_splitdrive("0.13",
                                  "//machine/usr1/lib/myFile.ext",
                                  "", "//machine/usr1/lib/myFile.ext")

#
    def test_path_vms(self):
        self.test_path_splitdrive("0.10",
                                  "myFile.ext",
                                  "", "myFile.ext")
        self.test_path_splitdrive("0.11",
                                  "[usr1.lib]myFile.ext",
                                  "", "[usr1.lib]myFile.ext")
        self.test_path_splitdrive("0.12",
                                  "/usr1/lib/myFile.ext",
                                  "", "/usr1/lib/myFile.ext")
        self.test_path_splitdrive("0.13",
                                  "machine::[usr1.lib]myFile.ext",
                                  "", "machine::[usr1.lib]myFile.ext")
        self.test_path_splitdrive("0.14",
                                  "//machine/usr1/lib/myFile.ext",
                                  "", "//machine/usr1/lib/myFile.ext")
        self.test_path_splitdrive("0.15",
                                  "sys$sysdevice:[usr1.lib]myFile.ext",
                                  "sys$sysdevice:", "[usr1.lib]myFile.ext")

#
    def test_path_win(self):
        self.test_path_splitdrive("0.10", "myFile.ext",
                                  "", "myFile.ext")
        self.test_path_splitdrive("0.11", "\\usr1\\lib\\myFile.ext",
                                  "", "\\usr1\\lib\\myFile.ext")
        self.test_path_splitdrive("0.12", "/usr1/lib/myFile.ext",
                                  "", "/usr1/lib/myFile.ext")
        self.test_path_splitdrive("0.13",
                                  "\\\\machine\\usr1\\lib\\myFile.ext",
                                  "", "\\\\machine\\usr1\\lib\\myFile.ext")
        self.test_path_splitdrive("0.14", "//machine/usr1/lib/myFile.ext",
                                  "", "//machine/usr1/lib/myFile.ext")
        self.test_path_splitdrive("0.15", "c:\\usr1\\lib\\myFile.ext",
                                  "c:", "\\usr1\\lib\\myFile.ext")

#
    def check_4_lfile(self, fsrc, ftgt):
        f = os0.setlfilename(fsrc, os0.LFN_FLAT)
        if f != ftgt:
            return False
        else:
            return True

#
    def check_4_lfile_exe(self, fsrc, ftgt):
        f = os0.setlfilename(fsrc, os0.LFN_EXE)
        if f != ftgt:
            return False
        else:
            return True

#
    def check_4_lfile_cmd(self, fsrc, ftgt):
        f = os0.setlfilename(fsrc, os0.LFN_CMD)
        if f != ftgt:
            return False
        else:
            return True

#
    def check_4_lfile_dir(self, fsrc, ftgt):
        f = os0.setlfilename(fsrc, os0.LFN_DIR)
        if f != ftgt:
            return False
        else:
            return True

    def test_fn(self, txtid, fsrc, ftgt):
        os0.wlog("Test {0} setlfilename({1})->{2}".format(txtid, fsrc, ftgt))
        if not self.check_4_lfile(fsrc, ftgt):
            os0.wlog("Test {0} failed!!!".format(txtid))
            os0.wlog("Expected value {0}!".format(ftgt))
            raise Exception("Test failed!!!")

#
    def test_fn_linux(self):
        os0.wlog("- Specific test for Linux platform")

        self.test_fn("1.01", "myFile", "myFile")

        os0.wlog("Test 1.02 setlfilename(myFile, exe)")
        if not self.check_4_lfile_exe("myFile", "myFile"):
            os0.wlog("Test 1.02 failed")
            raise Exception("Test 1.02 failed: !!!")
        os0.wlog("Test 1.03 setlfilename(myFile, cmd)")
        if not self.check_4_lfile_cmd("myFile", "myFile"):
            os0.wlog("Test 1.03 failed")
            raise Exception("Test 1.03 failed: !!!")
        os0.wlog("Test 1.04 setlfilename(myFile, dir)")
        if not self.check_4_lfile_dir("myFile", "myFile"):
            os0.wlog("Test 1.04 failed")
            raise Exception("Test 1.04 failed: !!!")

        self.test_fn("1.05", "myFile.py", "myFile.py")
        self.test_fn("1.06", "/root/myFile.py", "/root/myFile.py")
        self.test_fn("1.07", "/usr1/lib/myFile.py", "/usr1/lib/myFile.py")
        self.test_fn("1.08", "lib/myFile.py", "lib/myFile.py")
        self.test_fn("1.09", "./myFile.py", "./myFile.py")
        self.test_fn("1.10", "../myFile.py", "../myFile.py")
        self.test_fn("1.11", "../lib/myFile.py", "../lib/myFile.py")
        self.test_fn("1.12", "../../myFile.py", "../../myFile.py")
        self.test_fn("1.13", "/myFile.py", "/myFile.py")

        self.test_fn("1.20", "/usr1/lib/python.2.7/myFile.py",
                     "/usr1/lib/python.2.7/myFile.py")
        self.test_fn("1.21", "not.myFile.py", "not.myFile.py")
        self.test_fn("1.22", "/usr1/lib/python.2.7/not.myFile.py",
                     "/usr1/lib/python.2.7/not.myFile.py")

        self.test_fn("1.30", "/dev/null", "/dev/null")

#
    def test_fn_vms(self):
        os0.wlog("- Specific test for OpenVMS platform")

        self.test_fn("1.01", "myFile", "myFile")

        os0.wlog("Test 1.02 setlfilename(myFile, exe)")
        if not self.check_4_lfile_exe("myFile", "myFile.exe"):
            os0.wlog("Test 1.02 failed")
            raise Exception("Test 1.02 failed: !!!")
        os0.wlog("Test 1.03 setlfilename(myFile, cmd)")
        if not self.check_4_lfile_cmd("myFile", "myFile.com"):
            os0.wlog("Test 1.03 failed")
            raise Exception("Test 1.03 failed: !!!")
        os0.wlog("Test 1.04 setlfilename(myFile, dir)")
        if not self.check_4_lfile_dir("myFile", "myFile.DIR"):
            os0.wlog("Test 1.04 failed")
            raise Exception("Test 1.04 failed: !!!")

        self.test_fn("1.05", "myFile.py", "myFile.py")
        self.test_fn("1.06", "/root/myFile.py", "[root]myFile.py")
        self.test_fn("1.07", "/usr1/lib/myFile.py", "[usr1.lib]myFile.py")
        self.test_fn("1.08", "lib/myFile.py", "[.lib]myFile.py")
        self.test_fn("1.09", "./myFile.py", "[]myFile.py")
        self.test_fn("1.10", "../myFile.py", "[-]myFile.py")
        self.test_fn("1.11", "../lib/myFile.py", "[-.lib]myFile.py")
        self.test_fn("1.12", "../../myFile.py", "[-.-]myFile.py")
        self.test_fn("1.13", "/myFile.py", "[000000]myFile.py")

        self.test_fn("1.20", "/usr1/lib/python.2.7/myFile.py",
                     "[usr1.lib.python^.2^.7]myFile.py")
        self.test_fn("1.21", "not.myFile.py", "not^.myFile.py")
        self.test_fn("1.22", "/usr1/lib/python.2.7/not.myFile.py",
                     "[usr1.lib.python^.2^.7]not^.myFile.py")

        self.test_fn("1.30", "/dev/null", "NL0:")

        self.test_fn("1.90", "/sys$sysdevice/myfile",
                     "sys$sysdevice:[000000]myfile")
        self.test_fn("1.91", "/sys$sysdevice/usr1/myfile",
                     "sys$sysdevice:[usr1]myfile")

#
    def test_fn_win(self):
        os0.wlog("- Specific test for Windows platform")

        os0.wlog("Test 1.01 setlfilename(myFile)")
        if not self.check_4_lfile("myFile", "myFile"):
            os0.wlog("Test 1.01 failed")
            raise Exception("Test 1.01 failed: !!!")
        os0.wlog("Test 1.02 setlfilename(myFile, exe)")
        if not self.check_4_lfile_exe("myFile", "myFile.exe"):
            os0.wlog("Test 1.02 failed")
            raise Exception("Test 1.02 failed: !!!")
        os0.wlog("Test 1.03 setlfilename(myFile, cmd)")
        if not self.check_4_lfile_cmd("myFile", "myFile.bat"):
            os0.wlog("Test 1.03 failed")
            raise Exception("Test 1.03 failed: !!!")
        os0.wlog("Test 1.04 setlfilename(myFile, dir)")
        if not self.check_4_lfile_dir("myFile", "myFile"):
            os0.wlog("Test 1.04 failed")
            raise Exception("Test 1.04 failed: !!!")

#
        self.test_fn("1.05", "myFile.py", "myFile.py")
        self.test_fn("1.06", "/root/myFile.py", "\\root\\myFile.py")
        self.test_fn("1.07", "/usr1/lib/myFile.py", "\\usr1\\lib\\myFile.py")
        self.test_fn("1.08", "lib/myFile.py", "lib\\myFile.py")
        self.test_fn("1.09", "./myFile.py", ".\\myFile.py")
        self.test_fn("1.10", "../myFile.py", "..\\myFile.py")
        self.test_fn("1.11", "../lib/myFile.py", "..\\lib\\myFile.py")
        self.test_fn("1.12", "../../myFile.py", "..\\..\\myFile.py")
        self.test_fn("1.13", "/myFile.py", "\\myFile.py")

        self.test_fn("1.20", "/usr1/lib/python.2.7/myFile.py",
                     "\\usr1\\lib\\python.2.7\\myFile.py")
        self.test_fn("1.21", "not.myFile.py", "not.myFile.py")
        self.test_fn("1.22", "/usr1/lib/python.2.7/not.myFile.py",
                     "\\usr1\\lib\\python.2.7\\not.myFile.py")

        self.test_fn("1.30", "/dev/null", "nul")

        self.test_fn("1.90", "/c/myfile", "c:\\myfile")
        self.test_fn("1.91", "/c/usr1/myfile", "c:\\usr1\\myfile")

#
    def check_4_tkn_in_stdout(self, token):
        # Now search for this program name in output;
        # if found muteshell worked right!
        found_chunk = False
        try:
            stdout_fd = open(os0.setlfilename(os0.bgout_fn, 'r'))
            f = stdout_fd.read()
            if f.find(token) >= 0:
                found_chunk = True
            stdout_fd.close()
        except:
            pass
        if not found_chunk:
            os0.wlog("Test failed: muteshell did not work!!!")
            raise Exception("Test failed: muteshell did not work!!!")


#
class main:
    #
    # Run main if executed as a script
    if __name__ == "__main__":
        # Need debug mode to avoid security fault in Linux
        os0.set_debug_mode(True)
        title = "os0 regression test. Version: V0.2.10"
        if os0.version != "0.2.10":
            raise Exception("Test not executable: invalid os0 version")
        if 'DEV_ENVIRONMENT' in os.environ:
            LOCAL_ECHO = False
        else:
            LOCAL_ECHO = True
        # Remove test log file if executed previous crashed test
        tlog_fn = "os0_test.log"
        os0.set_tlog_file(tlog_fn)
        tlog_pathname = os0.tlog_fn
        os0.set_tlog_file('', echo=True)
        if os.path.isfile(tlog_pathname):
            os.remove(tlog_pathname)
        os0.wlog(title)
        os0.wlog("Test 0.xx: Level", 0, "tests")
#
# Simple initial tests
        os0.wlog("Test 0.01: Check for empty tracelog")
        os0.set_tlog_file(tlog_fn, new=True, echo=LOCAL_ECHO)
        fzero = False
        try:
            tlog_fd = open(os0.tlog_fn, 'r')
            fexts = True
            tlog_fd.seek(0, os.SEEK_END)
            if tlog_fd.tell() == 0:
                fzero = True
            tlog_fd.close()
        except:
            fexts = False
        if not fexts:
            raise Exception("Test failed: tracelog file not found!!!")
        elif not fzero:
            raise Exception("Test failed: tracelog file not empty!!!")

        os0.wlog("- Device null is {0}".format(os0.bginp_fn))
        os0.trace_debug("- Inititializing ...")
        os0.set_debug_mode(False)
        os0.trace_debug("TEST FAILED!!!!")
        os0.set_debug_mode(True)
        os0.trace_debug("- Inititializing (2) ...")
        os0.wlog(title)
        os0.wlog("- os0 version:", os0.version)
        os0.wlog("- platform:", _platform)

        os0.wlog("Test 0.02: Check for tracelog size")
        os0.set_tlog_file("os0_test.log", echo=LOCAL_ECHO)
        fzero = False
        try:
            tlog_fd = open(os0.tlog_fn, 'r')
            fexts = True
            tlog_fd.seek(0, os.SEEK_END)
            if tlog_fd.tell() == 0:
                fzero = True
            tlog_fd.close()
        except:
            fexts = False
        if not fexts:
            raise Exception("Test failed: tracelog file not found!!!")
        elif fzero:
            raise Exception("Test failed: tracelog file is empty!!!")

        os0.wlog("Test 0.03: Check for unicode support")
        wchar_string = u"- Unicode string àèìòù"
        os0.wlog(wchar_string)
        x = unichr(0x3b1) + unichr(0x3b2) + unichr(0x3b3)
        os0.wlog("- Greek letters", x)

        os0.wlog1("Test 0.04: str2bool(true)")
        res = os0.str2bool('true', None)
        if not res:
            raise Exception("Test failed: str2bool")
        os0.wlog1("Test 0.05: str2bool(0)")
        res = os0.str2bool('0', None)
        if res:
            raise Exception("Test failed: str2bool")
        os0.wlog1("Test 0.06: str2bool(0)")
        res = os0.str2bool(False, None)
        if res:
            raise Exception("Test failed: str2bool")
        os0.wlog1("Test 0.07: str2bool(0)")
        res = os0.str2bool('invalid', False)
        if res:
            raise Exception("Test failed: str2bool")

        os0.wlog1("Test 0.08: nakedname(myfile)")
        res = os0.nakedname('myfile')
        if res != 'myfile':
            raise Exception("Test failed: nakedname")
        os0.wlog1("Test 0.09: nakedname(myfile.py)")
        res = os0.nakedname('myfile.py')
        if res != 'myfile':
            raise Exception("Test failed: nakedname")
#
# Level 0 tests
        T = Test()
        if _platform == "win32":
            T.test_path_win()
        elif _platform == "OpenVMS":
            T.test_path_vms()
        else:
            T.test_path_linux()

#
# Level I tests
        os0.wlog("\nTest 1.00: Level I tests")

        if _platform == "win32":
            T.test_fn_win()
        elif _platform == "OpenVMS":
            T.test_fn_vms()
        else:
            T.test_fn_linux()


#
# Level II tests
        os0.wlog("\nTest 2.00: Level II tests")

        if os.path.dirname(__file__) == "":
            if __file__ == "__main__.py":
                cmd = "dir " + os0.setlfilename("../")
            else:
                cmd = "dir " + os0.setlfilename("./")
        else:
            cmd = "dir " + os0.setlfilename(os.path.dirname(__file__))
        os0.wlog("Test 2.01: exec->{0}".format(cmd))
        try:
            os.remove(os0.setlfilename(os0.bgout_fn))
        except:
            pass
        os0.muteshell(cmd, keepout=True)
# Now search for this program name in output; if found muteshell worked right!
        T.check_4_tkn_in_stdout(os.path.basename(__file__))
        if not os.path.isfile(os0.bgout_fn):
            raise Exception("Test failed: output file")

        os0.wlog("Test 2.02: Simulate command")
        if _platform == "win32":
            cmd = "del"
        elif _platform == "OpenVMS":
            cmd = "delete"
        else:
            cmd = "rm"
        cmd = cmd + " " + (os0.setlfilename(os0.bgout_fn))
        os0.muteshell(cmd, simulate=True, tlog=True)
        T.check_4_tkn_in_stdout(cmd)
        if not os.path.isfile(os0.bgout_fn):
            raise Exception("Test failed: output file")

        os0.wlog("Test 2.03: Execute command")
        cmd = "dir"
        os0.muteshell(cmd)
        if os.path.isfile(os0.bgout_fn):
            raise Exception("Test failed: output file")

#
#
        os0.wlog("Test successfully ended. See {0} file".
                 format(os0.setlfilename(os0.tlog_fn)))