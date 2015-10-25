# -*- coding: utf-8 -*-
import subprocess
cmd = "nosetests --with-coverage --cover-package=PhysicalQuantities --cover-html"

p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print(line)
retval = p.wait()