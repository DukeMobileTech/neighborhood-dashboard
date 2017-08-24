# Running the Neighborhood Dashboard from source code in UNIX (Mac OS X, Linux)
# Download and Install Anaconda Python 2.7
- The Neighborhood Dashboard (NBD) application runs on Anaconda Python 2.7. It is highly recommended to install Anaconda Python as opposed to using the traditional Python bundled with your Operating System. Anaconda comes bundled with most of the scientific Python packages you might need, has porting for other big data packages implemented in other languages, as well as offering a flexible way of creating Python environments.
- To install Anaconda Python 2.7 and the extra required packages, follow these [instructions](installing-python-and-required-packages.md).
# Obtaining API Keys
- Read the [utilized APIs](APIs.md) documentation and obtain the 2 necessary API keys.  
# Download the NBD source code from Github
- Clone the NBD source code from Github by running the command ```git clone git@github.com:DukeMobileTech/neighborhood-dashboard.git``` in your terminal. You can install git (or the latest version) by following these instructions (https://www.atlassian.com/git/tutorials/install-git). Another way of downloading the source code is to click on the **Clone or download** link on this [Github repository](https://github.com/DukeMobileTech/neighborhood-dashboard) and then click on the **Download Zip** button.
- Navigate into the downloaded neighborhood-dashboard folder. Unzip the ```input.zip``` file (It contains 3 test locations). The input folder is where your input files (location.csv, sso.csv, and urbanicity.csv) go. You can swap out the locations.csv file with your own locations file when doing a download with your own data. The locations file contains comma separated values in the format *identifier, latitude, longitude*.
# config.cfg
- This contains the configuration values needed to run the NBD. An example of this file (named config_example) is found in the sub-folder user-interface. The file should look as below:
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
- Navigate into the user-interface sub-folder. If you created an nbd environment when installing the extra packages, ensure you're in that environment.
![nbd environment](images/nbd.png?raw=true)  
- Run the command ```python create_nd.py ```. This starts the NBD application. 
- Data pre-processing logs
![Data Pre-processing](images/pre-processing.png?raw=true)
- Real & Fake OSM logs
![OSM Locations](images/OSM-locations.png?raw=true)
- Crime Data logs
![Crime Data Download](images/crime-data.png?raw=true)
- StreetView Images logs
![StreetView Images Download](images/street-view-images.png?raw=true)
- Walkability logs
![Walkability Score Download](images/walk-score.png?raw=true)
- The time taken by this step is dependent on the number of addresses in the input folder and the number of fake addresses in the config file. If the NBD is launched with 9 fake address look-ups, you can expect to download data of up to 400 real addresses in a 24-hour period. *All the data has to be downloaded before you can view any of it.* 
- In case the NBD crashes mid-way, you can re-start it and it will load up the data it had downloaded before starting the new download from where it crashed.
# Viewing the downloaded data
- *You can unzip the ```output.zip``` file to view the downloaded data for the locations contained in the ```input.zip``` file*
- The downloaded data is written to the output folder specified in the config.cfg file, i.e. ```output/html/data``` in our example.
- Navigate to that folder and open the ```index.html``` file using your browser. 
- The generic data page appears as below. It contains the identifier, the identifier's home/school/etc x,y geographical coordinates, the street address of the geo-code and the walkability score of the street of that address.
![Generic](images/generic.png?raw=true)
- The crime data page appears as below. It contains a pie-chart of the various types of crimes that happened within that neighborhood in the year that was specified in the config.cfg file.
![Crime](images/crime.png?raw=true)
- The points of interest page appears as below. The types of points of interest are hard-coded into the NBD application and are currently unmodifiable in the config.cfg file.
![POI](images/poi.png?raw=true)
- To the top right of the dashboard is a Google Map that is focused on the identifier's geographical location. You can use the buttons below it to toggle whatever feature the button indicates.
- To the bottom right of the dashboard are a set of Street View Images from the identifier's street.
![Images](images/google-sv-images.png?raw=true)
- Within the output folder, there is a **```streetviewimages```** folder that contains sub-folders whose names correspond to the unique identifiers. Within each sub-folder are the images that were downloaded from the street reverse-coded from the identifier's latitude and longitude point. 
  - The JPEG images ending with *.jpg* are the original images got from Google's StreetView API. 
    - These images have names with the following format: ```identifier_pointCount_headingCount.jpg``` where:
      - *identifier* is the unique identifier
      - *pointCount* (takes the values 0, 1, 2, 3, 4) are the points demarcating the equal segments within the street with 0 as the starting point and 4 as the ending point.
      - *headingCount* (takes the values 0 and 1) and represents the direction the image is taken from. If the segment in question starts at point 0 and ends at point 1, 0 represents the direction from point 0 to point 1 and 1 represents the direction from point 1 to point 0. The direction value represented by 0 and 1 ranges from 0 to 360 degrees (compass direction) and is the value passed to the *heading* parameter in the query sent to the Google StreetView API.
    - Each of these images has a *field of view (fov) of 120 degrees* and a *pitch of 5*.
    - You can read more about Google Street View [heading, fov, and pitch](https://developers.google.com/maps/documentation/streetview/intro).
  - The PNG images ending with *detection.png* have a similar naming format with the JPEG images from GSV API. These images are the result of passing the GSV JPEG images through a couple of functions of the [OpenCV](http://docs.opencv.org/3.2.0/index.html) library. The GSV images are read by the opencv library, converted from BGR to GRAY color space, resized using different factors, and finally saved back in PNG format. This processing helps in determining the different features in the image i.e. potentially identify any street signs in the image and such. **These are the images displayed in the Street View Images section of the Dashboard**
  - The JPEG images with names ending with *number_ss.jpg* are the images of the detected street signs from passing the GSV JPEG image through the opencv library. The detected street sign images have the same naming format as the GSV images with the exception of the ending. The *digit* in the name indicates the count of the feature i.e if two features were detected, the first takes the digit 0 while the second takes the digit 1.
- *Review Part 5 of the PDF manual found in the README to further understand what is being displayed in the dashboard*
- Within the output folder, there is a **```csv```** folder that contains raw data files whose data is fed to the dashboard. This is probably the data that is of interest to researchers. The files are ```closest_poi_data.csv```, ```police_crime_data.csv```, ```police_stop_and_search_data.csv```, ```urbanicity_data.csv```, and ```walkability_data.csv```.
 
 

