from fastai.vision import *
from os import listdir
from PIL import Image as PImage
import os

root = os.getcwd()[:find_last(os.getcwd(),'\\')]
path_img = root + '\\data\\verified\\'
for cloud_type in listdir(path_img):
  verify_images(path_img + '/' + cloud_type, delete = True, max_size = 1300)

for cind, cloud_type in enumerate(listdir(path_img)):
  fnames = get_image_files(path_img + cloud_type + '/')
  for pic in range(0,4):
    plt.figure(cind)
    plt.subplot(2,2,pic+1)
    plt.title(cloud_type)
    img = PImage.open(fnames[pic])
    plt.imshow(img)
  plt.tight_layout()

np.random.seed(42)
data = ImageDataBunch.from_folder(path_img, train = ".", valid_pct = 0.2,
                                  ds_tfms = get_transforms(), size = 224, num_workers = 0).normalize(imagenet_stats)

learn = cnn_learner(data, models.resnet34, metrics = error_rate)
learn.fit_one_cycle(1)
learn.save('../models/state-1')