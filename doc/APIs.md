# Utilized public APIs
The NBD uses publicly accessible APIs to collect neighborhood data. Some of these APIs require keys to access them though.
- **Google API Key** - For the NBD to download StreetView images, you need to obtain an API key from Google by following the instructions contained in this site (https://developers.google.com/maps/documentation/javascript/get-api-key).
- **Walkability API Key** - For the NBD to obtain the Walk Scores for a given neighborhood, you need an API key from Walk Score (https://www.walkscore.com/professional/walk-score-apis.php). To automatically get the key, ensure that your email address/domain name are the same i.e. if your email is awesome_address@good_school.edu, then the domain name should be good_school.edu. If they differ, you will need to contact Walk Score.
- The other APIs (listed below) used by the NBD do not require any special keys to access or use them.
  - **[UK Police Data API](https://data.police.uk/docs/):** Read their about page to figure out if the locations and time periods you are interested in are covered by the API. Generally most of the data obtainable from the API is from 2014 onwards. Some locations though might have some crime data from 2011.
  - **[Overpass API](http://overpass-api.de/index.html)** This API provides Open Street Map (OSM) location data.
# Future APIs
- **[The Community Crime Map](https://communitycrimemap.com/)** and the **[Crime Mapping](https://www.crimemapping.com/)** APIs will be incorporated to the NBD to provide crime data for various US locations.