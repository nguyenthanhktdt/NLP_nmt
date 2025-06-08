import sys
import os

absFilePath = os.path.abspath(__file__)                # Absolute Path of the module
#print(absFilePath)
fileDir = os.path.dirname(os.path.abspath(__file__))   # Directory of the Module
#print(fileDir)
parentDir = os.path.dirname(fileDir)                   # Directory of the Module directory
#print(parentDir)

infer = os.path.join(parentDir, 'infer')   # Get the directory for framework
preprocessing = os.path.join(parentDir, 'preprocessing')   # Get the directory for framework
train = os.path.join(parentDir, 'train')   # Get the directory for framework
utils = os.path.join(parentDir, 'utils')   # Get the directory for framework
sys.path.append(infer)                               # Add path into PYTHONPATH
sys.path.append(preprocessing)                               # Add path into PYTHONPATH
sys.path.append(train)                               # Add path into PYTHONPATH
sys.path.append(utils)                               # Add path into PYTHONPATH
