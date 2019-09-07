from fastai.vision import *
from os import listdir
from PIL import Image as PImage
import os
import shutil
from flask import url_for, current_app


def predict(model_path, pic):
  learn = cnn_learner(data, models.resnet50, metrics = error_rate)
  learn.load(model_path)
  img = open_image(pic)
  pred_class, pred_idx, outputs = learn.predict(img)

  return pred_class

cloud_types = {'stratiform'       : ['cirrostratus', 'altostratus', 'stratus', 'nimbostratus'],
               'cirriform'        : ['cirrus'],
               'stratocumuliform' : ['cirrocumulus', 'altocumulus', 'stratocumulus'],
               'cumuliform'       : ['cumulus'],
               'cumulonimbiform'  : ['cumulonimbus']}

