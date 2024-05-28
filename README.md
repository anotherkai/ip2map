# IP Geolocation to Map Image

This Python script generates a map image based on IP geolocation. It fetches the latitude and longitude coordinates of a given IP address using an external API and then generates a map image.

## Running

First, clone the repository using:

`git clone https://github.com/anotherkai/ip2map.git`

Then, install all the required modules from pypi using `pip`:

`pip install -r requirements.txt`

Lastly, if no errors was presented when completing the 2 other steps, we can proceed to running the actual app using:

`python3 ip2map.py [IP_ADDRESS]`

Make sure to replace `[IP_ADDRESS]` with the actual IP address.

Note: Domains do work using the API route provided in the code, however if you wish to change it to another API, this feature may not be available.
