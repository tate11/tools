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
"""
     Back-up database files from Production Machine to Development Machine
     Make 2 server quite identical, ready to use
     May be used to create a mirror server of Zeroincombenze®
"""


# import pdb
import os
import os.path
import sys
from os0 import os0
import glob
from sys import platform as _platform
from datetime import date, timedelta
import re
# from zarlib import ZAR as zar
from zar.zar.zarlib import ZAR as zar


__version__ = "2.1.24.3"


def version():
    return __version__


class Backup_Mirror:

    def init_bck(self, lpath=None):
        self.ftp_fd = open(self.ftp_cfn, "w")
        self.ls_fd = open(self.flist, "w")

        self.ftp_rootdir = ""                                   # No root dir
        self.ftp_dir = ""                                       # No subdir
        if lpath:
            self.chdir(lpath)

    def __init__(self, ctx):
        dbg_mode = ctx['dbg_mode']
        os0.set_debug_mode(dbg_mode)
        # Production machine
        self.prodhost = ctx["production_host"]
        # Development machine
        self.devhost = ctx["development_host"]
        # PC for test & debug
        self.PChost = "PC0004"
        # Postgresql directory
        self.pgdir = ctx["pg_dir"]
        # Mysql directory
        self.mysqldir = ctx["mysql_dir"]
        # Temporary ftp command script
        self.ftp_cfn = ctx["ftp_script"]
        self.flist = ctx["list_file"]
        os0.set_tlog_file(ctx["tracelog"])

        # Log begin execution
        os0.wlog("Backup database files", __version__)
        # Simulate backup
        self.simulate = True
        if self.hostname == self.prodhost:
            os0.wlog("Running on production machine")
            # Backup onto prod machine
            self.bck_host = "shsdev14"
            self.simulate = False                               # Real backup
        elif self.hostname == self.devhost:
            os0.wlog("This command cannot run on development machine")
            # Backup onto dev machine !?
            self.bck_host = "shsprd14"
#            raise Exception("Command aborted due development machine")
        elif self.hostname == self.PChost:
            os0.wlog("Running on PC just for test")
            # Backup onto dev machine (just for test)
            self.bck_host = "95.110.187.135"
        else:
            os0.wlog("Unknown machine - Command aborted")
            raise Exception("Command aborted due unknown machine")

        # May be (.gz or .bz2)
        self.tar_ext = ".gz"
        # May be (z or j)
        self.tar_opt = "z"
        # May be (null or .sql)
        self.pre_ext = ".sql"
        # May be (null or .sql)
        self.sql_ext = ".sql"

        self.psql_uu = "postgres"                               # Postgres UID
        self.mysql_uu = "mysql"                                 # Mysql UID

        self.init_bck()

    def gen_db_list(self, dbtype, user, sqlcmd):
        # pdb.set_trace()
        dblist = []
        os0.wlog(" Creating", dbtype, "db list")

        if dbtype == "psql":
            cmd = sqlcmd + " -U" + user + " -l"
            cmdlog = cmd
        elif dbtype == "mysql":
            cmd = sqlcmd + " -u " + user + \
                " --password=SHS13mgr -e \"show databases;\" mysql"
            cmdlog = sqlcmd + " -u " + user + " -e \"show databases;\" mysql"
        else:
            cmd = ""
            cmdlog = cmd
        os0.trace_debug(">", cmdlog)
        os0.muteshell(cmd, simulate=self.simulate, keepout=True)
        stdinp_fd = open(os0.setlfilename(os0.bgout_fn), 'r')
        line = stdinp_fd.readline()
        while line != "":
            i = line.rfind('\n')
            if i >= 0:
                if dbtype == "psql":
                    if line[0:1] == ' ' and line[1:2] != ' ':
                        x = line.split('|')
                        dbname = x[0].strip()
                        if re.match("z[ei].*|demo", dbname):
                            dblist.append(dbname)
                            if os0.debug_mode:
                                os0.wlog("> dblist.append({0})".format(dbname))
                elif dbtype == "mysql":
                    dbname = line.strip()
                    if re.match("w.*|mg.*|assioma.*", dbname):
                        dblist.append(dbname)
                        if os0.debug_mode:
                            os0.wlog("> dblist.append({0})".format(dbname))
            line = stdinp_fd.readline()
        stdinp_fd.close()

        if not os0.debug_mode and not self.simulate and os0.bgout_fn != "":
            # Delete files list
            os.remove(os0.setlfilename(os0.bgout_fn, 'r'))

        return dblist

    def bck_db(self, dbtype, dblist, user, sqlcmd):
        # pdb.set_trace()
        # save_ftp_rootdir = self.ftp_rootdir
        p = "backups"
        # Make full dir path (root + sub)
        lpath = self.ftp_rootdir + '/' + p
        self.chdir(lpath)                                       # Set directory

        for f in dblist:
            tar_ext = self.tar_ext
            tar_opt = self.tar_opt
            fzip_fn = f + tar_ext
            if not os.path.isfile(fzip_fn):
                if self.tar_ext == ".gz":
                    tar_ext = ".bz2"
                    tar_opt = "j"
                    fzip_fn = f + tar_ext
                    if not os.path.isfile(fzip_fn):
                        tar_ext = self.tar_ext
                        tar_opt = self.tar_opt
                        # No compressed file found
                        fzip_fn = ""
                elif self.tar_ext == ".bz2":
                    tar_ext = ".gz"
                    tar_opt = "z"
                    fzip_fn = f + tar_ext
                    if not os.path.isfile(fzip_fn):
                        tar_ext = self.tar_ext
                        tar_opt = self.tar_opt
                        # No compressed file found
                        fzip_fn = ""

            # Compressed file found
            if fzip_fn != "":
                cmd = "tar -x" + tar_opt + "f " + fzip_fn
                os0.trace_debug(">", cmd)
                os0.muteshell(cmd, simulate=self.simulate)
                if not self.simulate:
                    os.remove(fzip_fn)

            dts = date.today().strftime("%Y%m%d")
            fsql = f + "-" + dts + self.sql_ext
            if dbtype == "psql":
                cmd = sqlcmd + " -U" + user + " -F p -f " + fsql + " " + f
                cmdlog = cmd
            elif dbtype == "mysql":
                cmd = sqlcmd + " -u " + user + \
                    " --password=SHS13mgr " + f + " -r " + fsql
                cmdlog = sqlcmd + " -u " + user + " " + f + " -r " + fsql
            else:
                cmd = ""
                cmdlog = cmd
            os0.trace_debug(">", cmdlog)
            os0.muteshell(cmd, simulate=self.simulate)

            if os.path.isfile(fsql):
                os0.wlog(" ", fsql)
                self.add_2_ftp(fsql)
            else:
                os0.wlog("  file", fsql, "not found!!!")

            self.purge_db(dbtype, f)

    def purge_db(self, dbtype, f):
        if self.sql_ext != self.pre_ext:
            self.change_file_ext(f)

        dtc = date.today() - timedelta(90)
        os0.wlog("  removing file older than", dtc.strftime("%Y-%m-%d"))
        fzip_fn = f + self.tar_ext
        force_change_ext = False
        for i in range(180, 90, -1):
            dtc = date.today() - timedelta(i)
            dts = dtc.strftime("%Y%m%d")
            fsql = f + "-" + dts + self.sql_ext
            if not os.path.isfile(fsql) and self.sql_ext != self.pre_ext:
                ftmp = f + "-" + dts + self.pre_ext
                if os.path.isfile(ftmp):
                    try:
                        os0.wlog("> mv", ftmp, fsql)
                        if not self.simulate:
                            # Rename old ext -> nex ext
                            os.rename(ftmp, fsql)
                        # Force change sql file extension
                        force_change_ext = True
                    except:
                        pass

            if dtc.day != 1:
                if not self.remove_sql_file(fsql) \
                        and self.sql_ext != self.pre_ext:
                    fsql = f + "-" + dts + self.pre_ext
                    self.remove_sql_file(fsql)

        if force_change_ext:
            self.change_file_ext(f)

        fsql = f + "-????????" + self.sql_ext
        if dbtype == "psql":
            cmd = "chown " + self.psql_uu + ":" + self.psql_uu + " " + fsql
        elif dbtype == "mysql":
            cmd = "chown " + self.mysql_uu + ":" + self.mysql_uu + " " + fsql
        os0.trace_debug("> ", cmd)
        os0.muteshell(cmd, simulate=self.simulate)

        cmd = "tar -c" + self.tar_opt + "f " + fzip_fn + " " + fsql
        os0.trace_debug("> ", cmd)
        os0.muteshell(cmd, simulate=self.simulate)

        if dbtype == "psql":
            cmd = "chown " + self.psql_uu + ":" + self.psql_uu + " " + fzip_fn
        elif dbtype == "mysql":
            cmd = "chown " + self.mysql_uu + \
                ":" + self.mysql_uu + " " + fzip_fn
        os0.trace_debug("> ", cmd)
        os0.muteshell(cmd, simulate=self.simulate)

        os0.wlog("  removing archived files")
        fsql = f + "-????????" + self.sql_ext
        dts = date.today().strftime("%Y%m%d")
        fsql_nodel = f + "-" + dts + self.sql_ext
        f_ids = glob.glob(fsql)
        for fsql in f_ids:
            if fsql != fsql_nodel:
                self.remove_sql_file(fsql)

    def change_file_ext(self, f):
        os0.wlog("  changing extension files")
        fsql = f + "-????????" + self.pre_ext
        f_ids = glob.glob(fsql)
        for f in f_ids:
            l = len(f) - len(self.pre_ext)
            fsql = f[0:l] + self.sql_ext
            if not os.path.isfile(fsql):
                ftmp = f
                if os.path.isfile(ftmp):
                    try:
                        os0.wlog("> mv", ftmp, fsql)
                        if not self.simulate:
                            # Rename old ext -> nex ext
                            os.rename(ftmp, fsql)
                    except:
                        pass

    def remove_sql_file(self, fsql):
        try:
            fzip_fd = open(fsql, "r")
            fzip_fd.close()
            os0.trace_debug("> rm", fsql)
            if not self.simulate:
                os.remove(fsql)
            sts = True
        except:
            sts = False
        return sts

    def exec_bck(self):
        # Close files list
        self.ls_fd.close()
        self.set_chdir("/root")
        # Copy files list too
        self.ftp_fd.write(
            "put {0} {0}.tmp\n".format(os.path.basename(self.flist)))
        self.ftp_fd.close()
        self.ftp_fd = None
        fn = os.path.basename(self.ftp_cfn)
        if _platform == "win32":
            cmd = "ftp"
            p1 = "-s:" + fn
            p2 = self.bck_host
        else:
            cmd = "sftp"
            p1 = "-b" + fn
            p2 = "root@" + self.bck_host
        cmd = cmd + " " + p1 + " " + p2
        os0.muteshell(cmd, simulate=self.simulate, tlog=True)
        if not self.simulate:
            # os.remove(self.ftp_cfn)
            # os.remove(self.flist)                               # Delete
            # files list
            cmd = "ssh {0} \"cat {1}.tmp>>{1}; rm {1}.tmp\"".format(
                self.bck_host, self.flist)
            os0.muteshell(cmd, keepout=os0.debug_mode, tlog=True)
            cmd = "ssh root@" + self.bck_host + " \"at -f ./restdb now\""
            os0.muteshell(cmd, keepout=os0.debug_mode, tlog=True)

    def chdir(self, path):
        # Change root dir
        lpath = os0.setlfilename(path)
        os0.wlog(" [{0}]".format(lpath))
        self.set_chdir(lpath)
        self.ftp_rootdir = lpath
        self.ftp_dir = ""
        return lpath

    def set_chdir(self, path):
        # Exec chdir and store into ftp script
        os.chdir(path)
        if self.ftp_fd:
            self.ftp_fd.write("lcd {0}\n".format(path))
            self.ftp_fd.write("cd {0}\n".format(path))

    def add_2_ftp(self, fl):
        # Add filename to ftp file list
        # Extract subdir if supplied
        p = os.path.dirname(fl)
        fn = os.path.basename(fl)                               # Just filename
        # No dir supplied
        if p == "":
            # If prior subdir ..
            if self.ftp_dir != "":
                # .. return to root dir
                self.set_chdir(self.ftp_rootdir)
                # Forget prior subdir
                self.ftp_dir = ""
            fqn = self.ftp_rootdir + '/' + fl
        elif p[0:1] == '/' or p[0:1] == '.':
            fqn = p + '/' + fn
            fqn = self.ftp_rootdir + '/' + fn
            # Set local directory
            self.set_lchdir(p)
            self.ftp_dir = p
        else:
            fqn = self.ftp_rootdir + '/' + p + '/' + fl
            if p != self.ftp_dir:                             # Change subdir
                # Make full dir path (root + sub)
                lpath = self.ftp_rootdir + '/' + p
                self.set_chdir(lpath)                       # Set directory
                self.ftp_dir = p                            # Remember subdir
        self.ls_fd.write("{0}\n".format(fqn))
        # self.ftp_fd.write("put {0} {0}.new\n".format(fn))
        self.ftp_fd.write("put {0}\n".format(fn))


def main():
    """Tool main"""
    sts = 0
    # pdb.set_trace()
    ctx = zar.parse_args(sys.argv[1:], version=version())
    if ctx['xtall']:
        sts = zar.install(ctx)
        sys.exit(sts)
    BM = Backup_Mirror(ctx)
#
# Backup postgres database
    if BM.pgdir:
        BM.chdir(BM.pgdir)
        dblist = BM.gen_db_list("psql", "openerp", "psql")
        if ctx['db_name'] != "":
            if ctx['db_name'] in dblist:
                dblist = []
                dblist.append(ctx['db_name'])
            else:
                dblist = []
        for db in dblist:
            BM.init_bck(BM.chdir(BM.pgdir))
            BM.bck_db("psql", [db], "openerp", "pg_dump")
            BM.exec_bck()
#
# Backup mysql database
    if BM.mysqldir:
        BM.init_bck(BM.chdir(BM.mysqldir))
        # BM.chdir("/var/lib/mysql")
        dblist = BM.gen_db_list("mysql", "root", "mysql")
        if ctx['db_name'] != "":
            if ctx['db_name'] in dblist:
                dblist = []
                dblist.append(ctx['db_name'])
            else:
                dblist = []
        BM.bck_db("mysql", dblist,  "root", "mysqldump")
        BM.exec_bck()

    os0.wlog("Backup DB ended.")
    return sts

if __name__ == "__main__":
    # if running detached
    sts = main()
    sys.exit(sts)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: