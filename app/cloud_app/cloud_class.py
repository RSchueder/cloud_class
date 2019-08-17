from fastai.vision import *
from os import listdir
from PIL import Image as PImage
import os

def find_last(var, ss):
  ind = 0
  lst_ind = ind
  it = 0
  while ind >= 0:
    ind = var.find(ss, ind + it, len(var))
    it = 1
    if ind < 0:
      return lst_ind + 1
    lst_ind = ind

# this is os-dependent, needs to be trained
root = os.getcwd()[:find_last(os.getcwd(),'/')]

# predict

learn = cnn_learner(data, models.resnet34, metrics = error_rate)
learn.load(root + '/models/state-2')
pic = receive_image()
img = open_image()
pred_class,pred_idx,outputs = learn_cln.predict(img)

print(pred_class)
