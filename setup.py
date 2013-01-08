import sys
from distutils.core import setup

if sys.version_info < (3,0,0):
	print("Python 3.x is required!",file=sys.stderr)
	exit(1)

from biorhythm import APPNAME,APPVERSION,AUTHOR,DESCRIPTION,YEAR,PAGE,EMAIL

setup(
	name = APPNAME,
	version = APPVERSION,
	author = AUTHOR,
	author_email = EMAIL,
	description = DESCRIPTION,
	url = PAGE,
	packages = ['biorhythm'],
	scripts=['biocli.py','qbiobeat.py'],
	data_files=[
		('share/applications',['QBioBeat.desktop']),
	]
)
