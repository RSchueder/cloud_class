from fastai.vision import *
from os import listdir
from PIL import Image as PImage
import os
import shutil
import glob

from flask import url_for, current_app


def predict(model_path, img_path):

  data_path = os.path.join(current_app.root_path, 'static/networks', os.path.split(model_path)[1].replace('.pth',''),'') 
  print(model_path)
  print(data_path)

  print('# classes = %i' % (len(glob.glob(data_path + '*'))))

  data = ImageDataBunch.from_folder(data_path, train = ".", valid_pct = 0.2, ds_tfms = get_transforms(), size = 222, num_workers = 0).normalize(imagenet_stats)

  if '34' in model_path:
    learn = cnn_learner(data, models.resnet34, metrics = error_rate)
  else:
    learn = cnn_learner(data, models.resnet50, metrics = error_rate)

  weight_path = data_path[:-1]

  
  learn.load(weight_path)
  img = open_image(img_path)
  pred_class, _, _ = learn.predict(img)

  return pred_class



