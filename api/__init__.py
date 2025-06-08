import sys
import os

absFilePath = os.path.abspath(__file__)                # Absolute Path of the module
fileDir = os.path.dirname(os.path.abspath(__file__))   # Directory of the Module
parentDir = os.path.dirname(fileDir)                   # Directory of the Module directory
api = os.path.join(parentDir, 'api')   # Get the directory for framework
api4app = os.path.join(parentDir, 'api/api4app')
framework = os.path.join(parentDir, 'framework')   # Get the directory for framework
utils = os.path.join(framework, 'utils')
nmt = os.path.join(parentDir, 'nmt')   # Get the directory for framework

sys.path.append(api)                               # Add path into PYTHONPATH
sys.path.append(api4app)                               # Add path into PYTHONPATH
sys.path.append(framework)                               # Add path into PYTHONPATH
sys.path.append(utils)
sys.path.append(nmt)                               # Add path into PYTHONPATH

