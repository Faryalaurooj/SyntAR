
import glob
import os
import pathlib
import shutil

source = 'Harmonized_samples/'

path = pathlib.Path(source)

files = list(path.rglob('*'))
files = [str(i) for i in files]

dest = 'harmonizationFilesTesting/'

count = 1
for file in files:
	if file.endswith('.png'):
		#print ((file))
		shutil.copy( file, dest + file.split('/')[-2]+ '.png')
		count = count + 1
	
