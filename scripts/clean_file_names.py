import os
import glob
import shutil as sh
from fastai.vision import *

def find_last(var,ss):
    '''
    returns the index AFTER the index of the last instance of the 
    passed character in the passed string
    '''
    ind = 0
    lstInd = ind
    it = 0
    while ind >= 0:
        ind = var.find(ss,ind + it,len(var))
        it = 1
        if ind < 0:
            return lstInd + 1
        lstInd = ind

thresh = 100

# copy all downloaded images to production folder if file is valid
root = os.getcwd()[:find_last(os.getcwd(),'\\')]
for dd in os.listdir(root + 'data\\raw\\downloads\\'):
    if not os.path.exists(root + 'data\\verified\\' + dd):
        os.mkdir(root + 'data\\verified\\' + dd)
    for full_file in glob.glob(root + 'data\\raw\\downloads\\' + dd + '\\*'):
        file_name = full_file[find_last(full_file,'\\'):]
        old = file_name
        ext = find_last(old,'.')
        file_name = file_name[:ext]
        extension = old[ext-1:]
        
        if len(file_name) > thresh:
            file_name = file_name[0:thresh] + '_clean' + extension
        else:
            file_name = file_name + '_clean' + extension    
        
        print(len(old), len(file_name))

        # copy compatible file to production folder
        # if the file name is too long or corrupted, skip it
        try:
            sh.copy(full_file, root + 'data\\verified\\' + dd + '\\' + file_name)
            os.remove(full_file)
        except(FileNotFoundError):
            print('file name is too long, omitting')
            print(full_file)
            os.remove(full_file)
