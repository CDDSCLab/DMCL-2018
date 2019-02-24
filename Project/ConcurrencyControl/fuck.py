#-*- coding:utf8 -*-
import re

import os
 
def file_name(file_dir): 
    L=[] 
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.md':
                L.append(os.path.join(root, file))

    return L

def find_md(file_dir):
	L=[] 
	for file in os.listdir('.'):
		if os.path.splitext(file)[1] == '.md':
			L.append(file)
	return L

for each in find_md('.'):
	res = ''
	with open(each) as f:
		try:
			res = re.search(r'\d+-\d+-\d+',f.read()).group()+'-'
		except Exception as e:
			continue
	os.rename(each,res+each)

