# Download and Install Anaconda Python 2.7
- Head to Continuum (https://www.continuum.io/downloads) and download and install Anaconda Python 2.7 for your platform (macOS or Linux). Follow the installation instructions offered by the installer.
- To verify the installation succeeded, open a terminal window and run the command ```python```. The output should be as follows:
![Anaconda 2.7](images/anaconda-2-7.png?raw=true)
If the output is not Python 2.7.x | Anaconda x.x.x, then the installation did not succeed and needs to be fixed first before continuing with the next steps.
# Install additional packages
Additional Python packages are required to run the NBD application. These packages can be installed on a UNIX machine using pip, the Python package manager. pip comes bundled with Anaconda and you can confirm this by running the command ```which pip``` on your terminal, which should output ```/anaconda/bin/pip```. 
- The additional packages required are NumPy, GeoPy, and OpenCV and can be installed by running the following commands on the terminal: ```pip install numpy```, ```pip install geopy```, and ```pip install opencv-python```
![Additional Packages](images/additional-packages.png?raw=true)
- Confirm each package is installed by running the command ```pip show package-name``` where package-name is numpy etc. The output is as below:
![NumPy](images/numpy.png?raw=true)