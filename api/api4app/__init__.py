import os
import sys

absFilePath = os.path.abspath(__file__)                # Absolute Path of the module
print(absFilePath)
fileDir = os.path.dirname(os.path.abspath(__file__))   # Directory of the Module
# print(fileDir)
parentDir = os.path.dirname(fileDir)                   # Directory of the Module directory
# print(parentDir)
parent = os.path.dirname(parentDir)
settings = os.path.join(parentDir, 'settings')
api = os.path.join(parentDir, 'api')   # Get the directory for framework

api4app = os.path.join(parentDir, 'api4app')
framework = os.path.join(parent, 'framework')   # Get the directory for framework
utils = os.path.join(framework, 'utils')   # Get the directory for framework
nmt = os.path.join(parentDir, 'nmt')   # Get the directory for framework
print("Importing...")

sys.path.append(api)                               # Add path into PYTHONPATH
sys.path.append(api4app)                               # Add path into PYTHONPATH
sys.path.append(framework)                               # Add path into PYTHONPATH
sys.path.append(utils)                               # Add path into PYTHONPATH
sys.path.append(nmt)                               # Add path into PYTHONPATH
sys.path.append(settings)

