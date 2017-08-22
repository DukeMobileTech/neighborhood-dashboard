# Running the Neighborhood Dashboard from source code in UNIX (Mac OS X, Linux)
# Download and Install Anaconda Python 2.7
- The Neighborhood Dashboard (NBD) application runs on Anaconda Python 2.7. It will not run on the default Python bundled with your OS or on Python 3.
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
# Obtaining API Keys
The NBD uses publicly accessible APIs to collect neighborhood data. Some of these APIs require keys to access them though.
- **Google API Key** - For the NBD to download StreetView images, you need to obtain an API key from Google by following the instructions contained in this site (https://developers.google.com/maps/documentation/javascript/get-api-key).
- **Walkability API Key** - For the NBD to obtain the Walk Scores for a given neighborhood, you need an API key from Walk Score (https://www.walkscore.com/professional/walk-score-apis.php). To automatically get the key, ensure that your email address/domain name are the same i.e. if your email is awesome_address@good_school.edu, then the domain name should be good_school.edu. If they differ, you will need to contact Walk Score.  
# Download the NBD source code from Github
- Download/Clone the NBD source code from Github by running the command ```git clone git@github.com:DukeMobileTech/neighborhood-dashboard.git``` in your terminal. You can install git (or the latest version) by following these instructions (https://www.atlassian.com/git/tutorials/install-git)
- Navigate into the neighborhood-dashboard directory which contains several folders in it. Unzip the ```input.zip``` file (It contains 3 test locations). The input folder is where your input files (location.csv, sso.csv, and urbanicity.csv) go. You can swap out the locations.csv file with your own locations file. The locations file contains comma separated values in the format *family_id, latitude, longitude*.
# config.cfg
- This contains the configuration values needed to run the NBD. An example of this file (named config_example) is found in the folder user-interface. The file should look as below:
```
[files]
location = ../input/locations.csv
sso = ../input/sso.csv
urbanicity = ../input/urbanicity.csv

[settings]
year = 2014
output-directory = ../output/html/data
fake-requests = 1
fake-requests-count = 4
streetview-detection = 1

[api-keys]
gsv = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
walkability = yyyyyyyyyyyyyyyyyyyyyyyyyyyy

[debug]
generate-kml = 1
```
- Create your own config.cfg file or rename the config_example.cfg file to config.cfg and then replace the gsv key value with the Google API Key and the walkability API Key value with the key from Walk Score. 
- To understand the meaning of these configuration values, look at **Part 2** of the PDF manual found in the README section (http://81.7.15.7/~donald/nd/Tutorial_NBDashboard_v5.pdf).
# Running the NBD
- Navigate into the NBD folder and run the command ```python create_nd.py ```. This starts the NBD application. You should see logs of the *pre-processing step and the data download steps*. 
![Data Download](images/data-processing.png?raw=true)
- The time taken by this step is dependent on the number of addresses in the input folder and the number of fake addresses in the config file. If the NBD is launched with 9 fake address look-ups, you can expect to download data of up to 400 real addresses in a 24-hour period. *All the data has to be downloaded before you can view any of it.* 
- In case the NBD crashes mid-way, you can re-start it and it will load up the data it had downloaded before starting the new download from where it crashed.
# Viewing the downloaded data
- *You can unzip the ```output.zip``` file to view the downloaded data for the locations contained in the ```input.zip``` file*
- The downloaded data is written to the output folder specified in the config.cfg file, i.e. ```output/html/data``` in our example.
- Navigate to that folder and open the ```index.html``` file using your browser. 
- The generic data page appears as below. It contains the family id, the family's home/school/etc geographical coordinates, the street address of the geo-code and the walkability score of the street of that address.
![Generic](images/generic.png?raw=true)
- The crime data page appears as below. It contains a pie-chart of the various types of crimes that happened within that neighborhood in the year that was specified in the config.cfg file.
![Crime](images/crime.png?raw=true)
- The points of interest page appears as below. The types of points of interest are hard-coded into the NBD application and are currently unmodifiable in the config.cfg file.
![POI](images/poi.png?raw=true)
- To the top right of the dashboard is a Google Map that is focused on the familyid's geo-code. You can use the buttons below it to toggle whatever feature the button indicates.
- To the bottom right of the dashboard are a set of StreetView images from the family's street.
- *Review Part 5 of the PDF manual found in the README to further understand what is being displayed in the dashboard*
- Within the output folder, there is a **```csv```** folder that contains raw data files whose data is fed to the dashboard. This is probably the data that is of interest to researchers. The files are ```closest_poi_data.csv```, ```police_crime_data.csv```, ```police_stop_and_search_data.csv```, ```urbanicity_data.csv```, and ```walkability_data.csv```.

 
 

