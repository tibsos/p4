from ipware import get_client_ip
import geocoder

def get_ip_country_city(request):
    ip, is_routable = get_client_ip(request)
    country = None
    city = None
    
    if ip:
        try:
            # Get geolocation information based on IP
            geo = geocoder.ip(ip)
            country = geo.country
            city = geo.city
        except Exception as e:
            # Handle exceptions
            pass

    return ip, country, city