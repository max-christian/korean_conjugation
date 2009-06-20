#!/usr/bin/env python
import glob

print ','.join(x[4:-3] for x in glob.glob('src/*py'))
