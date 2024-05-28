import sys
import ipaddress
import requests
import socket
import io
from PIL import Image
import math

# Function to convert latitude and longitude to tile numbers
def deg2num(lat, lon, zoom):
    """
    Converts latitude and longitude coordinates to tile numbers at a given zoom level.

    Args:
        lat (float): Latitude.
        lon (float): Longitude.
        zoom (int): Zoom level.

    Returns:
        Tuple[int, int]: Tile numbers (x, y).
    """
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return x, y

# Function to fetch IP information from an API
def get_ip_info(ip):
    """
    Fetches IP information from an API.

    Args:
        ip (str): IP address.

    Returns:
        dict: IP information.
    """
    api_url = f"https://ipinfo.littlekai.co.uk/lookup?ip={ip}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("Error fetching IP information:", e)
        return None

# Function to generate map image based on IP geolocation
def ip_to_map(ip_or_domain):
    """
    Generates a map image based on IP geolocation.

    Args:
        ip_or_domain (str): IP address or domain name.

    Raises:
        ValueError: If IP information cannot be retrieved or location data is unavailable.
    """
    if not ip_or_domain:
        raise ValueError('IP address or domain name is required')

    ip_info = get_ip_info(ip_or_domain)
    if not ip_info:
        raise ValueError('Failed to retrieve IP information from the API')

    if 'latitude' not in ip_info or 'longitude' not in ip_info:
        raise ValueError('Location data not available for this IP')

    bogon = ip_info.get('is_bogon', False)
    latitude = ip_info['latitude']
    longitude = ip_info['longitude']
    city = ip_info.get('city', 'Unknown')
    country = ip_info.get('country', 'Unknown')
    hostname = ip_info.get('hostname', 'Unknown')
    zoom = 17

    if bogon or ip_or_domain == 'localhost':
        raise ValueError('IP must be a valid public IPv4/IPv6. Bogon IPs will not work.')

    x, y = deg2num(latitude, longitude, zoom)

    tile_size = 256
    tiles = []

    for dy in range(-1, 1):
        row = []
        for dx in range(-1, 1):
            tile_x = x + dx
            tile_y = y + dy
            tile_url = f"https://mt0.google.com/vt/lyrs=s&x={tile_x}&y={tile_y}&z={zoom}"
            response = requests.get(tile_url)
            if response.status_code == 200:
                tile_image = Image.open(io.BytesIO(response.content))
                row.append(tile_image)
            else:
                raise ValueError('Failed to retrieve tile image from server')
        tiles.append(row)

    combined_image = Image.new('RGB', (tile_size * 2, tile_size * 2))
    for i, row in enumerate(tiles):
        for j, tile in enumerate(row):
            combined_image.paste(tile, (j * tile_size, i * tile_size))

    file_path = f'ip_map_{ip_or_domain}.png'
    combined_image.save(file_path, format='PNG')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ip_geolocation_to_map.py [IP_ADDRESS]")
        sys.exit(1)

    ip_to_map(sys.argv[1])
