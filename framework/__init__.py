import sys
import os

absFilePath = os.path.abspath(__file__)                # Absolute Path of the module
fileDir = os.path.dirname(os.path.abspath(__file__))   # Directory of the Module
parentDir = os.path.dirname(fileDir)                   # Directory of the Module directory

api = os.path.join(parentDir, 'api')   # Get the directory for framework
api4app = os.path.join(api, 'api4app')
framework = os.path.join(parentDir, 'framework')   # Get the directory for framework
print("framework:   ", framework)
utils = os.path.join(framework, 'utils')   # Get the directory for framework
nmt = os.path.join(parentDir, 'nmt')   # Get the directory for framework
settings = os.path.join(parentDir, 'settings')
print("Importing...")

sys.path.append(api)                               # Add path into PYTHONPATH
sys.path.append(api4app)                               # Add path into PYTHONPATH
sys.path.append(framework)                               # Add path into PYTHONPATH
sys.path.append(utils)                               # Add path into PYTHONPATH
sys.path.append(nmt)                               # Add path into PYTHONPATH
sys.path.append(settings)


# Add the root directory (where "framework" lives) to the path
# sys.path.append('..')
