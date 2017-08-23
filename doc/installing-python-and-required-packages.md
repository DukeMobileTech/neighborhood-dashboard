# Download and Install Anaconda Python 2.7
- Head to Continuum (https://www.continuum.io/downloads) and download and install Anaconda Python 2.7 for your platform (macOS or Linux). Follow the installation instructions offered by the installer until the end.
- To verify the installation succeeded, open a terminal window and run the command ```python```. The output should be as follows:
![Anaconda 2.7](images/anaconda-2-7.png?raw=true)
- If the output is not Python 2.7.x | Anaconda x.x.x, then the installation did not succeed and needs to be fixed first before continuing with the next steps. Google around and hopefully you don't get into a rabbit hole!
- Additional Python packages (scipy, numpy, geopy, opencv, scikit-learn, scikit-image) are required to run the NBD application. These packages can be installed on a UNIX machine using pip or conda. 
- If you use Python for different programs that might require different versions of the same package and therefore need to keep different Python environments, skip to the step that installs using conda or the step that installs using an environment file. Otherwise proceed with the step that uses pip.
# Installing additional packages using pip
Pip, a package management system, comes bundled with Anaconda. You can confirm this by running the command ```which pip``` on your terminal, which should output ```/anaconda/bin/pip```. 
- The additional packages can be installed by running the following commands on the terminal: ```pip install numpy geopy opencv-python scikit-learn scikit-image```
![Additional Packages](images/additional-packages.png?raw=true)
- Confirm each package is installed by running the command ```pip show package-name``` where package-name is numpy etc. The output is as below:
![NumPy](images/numpy.png?raw=true)
# Installing additional packages using conda
- Conda is both a package management as well as an environment management system that comes bundled with Anaconda. You can confirm it is installed by running the command ```conda --version``` which should display a version number such as ```conda 4.3.14```. If you get an error message, fix that first before proceeding.
- Create a new Python environment named nbd by running the following command ```conda create --name nbd```. If you run into any errors try updating conda by running the command ```conda update conda```. 
- During the install process, if any of the package install commands asks for permission to proceed ```proceed ([y]/n)?```, enter ```y``` to proceed.
- Creating the environment gives the below output:
![Conda Create Environment](images/conda-create.png?raw=true)
- Switch to the environment you just created using the command ```source activate nbd```.
- Add the ```conda-forge``` channel to your channels using the command ```conda config --add channels conda-forge```.
- Install the additional packages using the command ```conda install scipy numpy geopy opencv scikit-learn scikit-image```. This will most likely ask to install other packages that they depend on. Enter ```y``` if it asks to proceed at any point.
# Installing additional packages using an environment.yml file
- You can also create a Python environment using conda with a YAML file e.g. [environment.yml](environment.yml). Copy and paste the contents of that file into a similarly named file in your current path and execute the command ```conda env create -f environment.yml```.
![Conda environment.yml](images/conda-environment.png?raw=true)
- Switch to the environment using the command ```source activate nbd```.
# More Resources
- [Getting started with Conda](https://conda.io/docs/user-guide/getting-started.html)
- [Conda vs Pip vs VirtualEnv](http://stuarteberg.github.io/conda-docs/_downloads/conda-pip-virtualenv-translator.html)
- [Conda Myths and Misconceptions](https://jakevdp.github.io/blog/2016/08/25/conda-myths-and-misconceptions/) 




