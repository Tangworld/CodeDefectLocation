#! /usr/bin/python

import os, sys

import subprocess
from subprocess import Popen, PIPE

import re

GIT="git"
ANT="ant"

FNULL = open(os.devnull, 'w')

class git:

    def __init__(self, directory):
        self.directory = directory


    def check_out(self, version):            
        cmd = [GIT, '-C', self.directory, 'checkout', '-f', version]
        subprocess.check_call(cmd, stdout=FNULL, stderr=subprocess.STDOUT)


    def get_log(self, start, end):
        cmd = [GIT, '-C', self.directory, 'log', '--after='+start, '--before='+end]#, '--pretty=format:%H']
        p = Popen(cmd, stdout=PIPE)

        (log, stderr) = p.communicate()

        return log

    def get_logs(self, start, end):
        cmd = [GIT, '-C', self.directory, 'log', '--after='+start, '--before='+end, '--pretty=format:%H %s']
        p = Popen(cmd, stdout=PIPE)

        (log, stderr) = p.communicate()
        return log
    def get_name_only(self, commitId):
        cmd = [GIT, '-C', self.directory, 'diff', '--name-only', commitId]
        p = Popen(cmd, stdout=PIPE)

        (name, stderr) = p.communicate()

        return name
    
    def check_version(self, version, older=None):
        pass
	
	def git_reset(self,commitId):
        cmd = [GIT, '-C', self.directory, '--hard', 'commit', commitId]
		p = Popen(cmd, stdout=PIPE)
		
		(out, stderr) = p.communicate()
		
		return out
		
	def git_pull(self):
		cmd = [GIT, '-C', self.directory, 'pull']
		p = Popen(cmd, stdout=PIPE)
		
		(out, stderr) = p.communicate()
		
		return out

	def check_all(self, log=None):
        log = log if log else self.get_log()

        max_log_count = os.getenv("MAX_LOG_COUNT")
        max_log_count = int(max_log_count) if max_log_count else None

        logs = log.splitlines()[0:max_log_count]

        for index, l in enumerate(logs):
            try:
                print("%s\t%s" % (l, 'passed' if self.check_version(l, logs[index + 1]) else 'failed'))
            except IndexError:
                pass


'''

class derby(project):

    def __init__(self, directory):
        super(derby, self).__init__(directory)

        # Thus, we have no need to change working directory by using `-f`
        self.ant_file = os.path.join(directory, 'build.xml')


    def check_version(self, version, older):
        name = self.show_name_only(version, older)

        if self.has_no_derby_engine(name):
            return False

        return self.build_project_at(version)


    def has_no_derby_engine(self, name):
        for line in name.splitlines():
            if line.startswith('java/engine') and line.endswith('.java'):
                return False
        return True


    def build_project_at(self, log):
        # checkout first anyway
        self.check_out(log)

        cmd = [ANT, '-f', self.ant_file, 'clean', 'buildsource']
        retcode = subprocess.call(cmd, stdout=FNULL, stderr=subprocess.STDOUT)

        return retcode == 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: repo_directory [log]")
        exit(1)

    # argv[1] = /a/b/c/derby
    # result in derby
    globals()[os.path.basename(sys.argv[1])](sys.argv[1]).check_all()
'''