import os
import sys
import glob
import shutil
import numpy as np
from fastai.vision import *
from os import listdir
from PIL import Image as PImage
import json
import pylab
import matplotlib.pyplot as plt 

cloud_types = {'stratiform'       : ['cirrostratus', 'altostratus', 'stratus', 'nimbostratus'],
               'cirriform'        : ['cirrus'],
               'stratocumuliform' : ['cirrocumulus', 'altocumulus', 'stratocumulus'],
               'cumuliform'       : ['cumulus'],
               'cumulonimbiform'  : ['cumulonimbus']}


root = os.getcwd()
data_path = os.path.join(root, 'data','verified')
model_path = os.path.join(root, 'models')

def make_merged_db(cloud_types):

    if os.path.exists(os.path.join(data_path,'merged')):
        shutil.rmtree(os.path.join(data_path,'merged'))

    if not os.path.exists(os.path.join(data_path,'merged')):
        os.mkdir(os.path.join(data_path,'merged'))

    for cloud_type in cloud_types.keys():
        if not os.path.exists(os.path.join(data_path,'merged', cloud_type)):
            os.mkdir(os.path.join(data_path,'merged', cloud_type))
        for sub_type in cloud_types[cloud_type]:
            print(sub_type)
        for pic in glob.glob(os.path.join(data_path, sub_type + ' clouds', '*')):
            shutil.copy(pic, os.path.join(data_path,'merged', cloud_type))

class Model():

    def __init__(self, params):
        self.name = params['name']
        self.data_path = params['data_path']
        self.out_path = params['out_path']

        self.size = params['size']
        self.cycles = params['cycles']
        self.epochs = params['epochs']
        self.transfer_type = params['transfer_type']


    def make_bunch(self):
        print('creating data bunch')
        np.random.seed(42)
        self.data = ImageDataBunch.from_folder(self.data_path, train = ".", valid_pct = 0.2, ds_tfms = get_transforms(), size = self.size, num_workers = 0).normalize(imagenet_stats)
        
        print('data bunch created, status:')
        print('classes, train, valid')
        print(self.data.classes, self.data.c, len(self.data.train_ds), len(self.data.valid_ds))


    def load(self, path):
        print('loading model')
        if '34' in self.transfer_type:
            learn_cnn = cnn_learner(data_cleaned, models.resnet34, metrics = error_rate)
        elif '50' in self.transfer_type:
            learn_cnn = cnn_learner(data_cleaned, models.resnet50, metrics = error_rate)
        else:
            raise ModuleNotFoundError

        self.model = learn_cnn.load(path)
        print('model loaded')
        

    def train(self):
        print('beginning training')
        print('will train %i cycles of %i epochs each' % (self.cycles, self.epochs))

        if '34' in self.transfer_type:
            self.model = cnn_learner(self.data, models.resnet34, metrics = error_rate)
        elif '50' in self.transfer_type:
            self.model = cnn_learner(self.data, models.resnet50, metrics = error_rate)
        else:
            raise ModuleNotFoundError
        
        self.model.unfreeze()
        self.model.fit_one_cycle(1, max_lr = slice(1e-4, 1e-3))
        
        for ii in range(0, self.cycles):
            self.model.fit_one_cycle(self.epochs, max_lr = slice(1e-4, 1e-3))
            self.model.save(self.out_path + self.name + '_cycle%i' % (ii+1))

        print('training finished')

    def evaluate(self):
        self.model.export()
        self.model.recorder.plot_losses()
        self.interp = ClassificationInterpretation.from_learner(self.model)
        self.interp.plot_confusion_matrix()
        pylab.save(self.interp, self.out_path + self.name + '.png')
        # pred_class, pred_idx, outputs = learn_cnn.predict(img)


#make_merged_db(cloud_types)

j_file = sys.argv[1]

with open(os.path.join(model_path, j_file + '.json'), 'r') as par_file:
    params = json.load(par_file)

model = Model(params)
model.make_bunch()
model.train()
#model.evaluate()




