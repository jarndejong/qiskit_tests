# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 15:13:38 2018

@author: Jarnd
"""
import pickle
import os

from datetime import datetime
timestamp = datetime.now().strftime("%m_%d-%H_%M_%S")
directory = 'Measured data/'
filepath = directory+timestamp+"--tomodata.txt"

os.makedirs(os.path.dirname(filepath), exist_ok=True)

fo = open(filepath, "wb")



pickle.dump(tomo_data, fo)

fi = open(filepath,"rb")
tomo_data_data_load = pickle.load(fi)
