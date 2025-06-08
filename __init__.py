import sys
import os

absFilePath = os.path.abspath(__file__)                # Absolute Path of the module
# print(absFilePath)
fileDir = os.path.dirname(os.path.abspath(__file__))   # Directory of the Module
# print(fileDir)
parentDir = os.path.dirname(fileDir)                   # Directory of the Module directory
# print(parentDir)

api = os.path.join(fileDir, 'api')   # Get the directory for framework
print(api)
api = os.path.join(fileDir, 'api')   # Get the directory for framework
api4app = os.path.join(api, 'api4app')   # Get the directory for framework
print(api4app)
framework = os.path.join(parentDir, 'framework')   # Get the directory for framework
print("framework", framework)
utils = os.path.join(framework, 'utils')
print(utils)
nmt = os.path.join(parentDir, 'nmt')   # Get the directory for framework
print("Importing...")

sys.path.append(api)                               # Add path into PYTHONPATH
sys.path.append(api4app)                               # Add path into PYTHONPATH
sys.path.append(framework)                               # Add path into PYTHONPATH
sys.path.append(utils)                               # Add path into PYTHONPATH
sys.path.append(nmt)                               # Add path into PYTHONPATH

