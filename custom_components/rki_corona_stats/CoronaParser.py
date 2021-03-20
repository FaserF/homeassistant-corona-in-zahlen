import sys
import requests


class CoronaParser:
    """
    Corona class to get the actual COVID data
    """
    @staticmethod
    def get_value(district):
        """
        Returns the COVID data for a matching given district.

        :param district: The district of where to fetch the COVID data
        :return: COVID data or None if no data was found
        """
        url = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/' \
              f'query?where=county%20%3D%20%27{district.upper()}%27&outFields=GEN,cases7_per_100k,county,cases,deaths&outSR=4326&f' \
              '=json'

        request = requests.get(url)
        if request.status_code == 200:
            print("District: " + district)
            try:
                return {
                        "cases7_per_100k": request.json()['features'][0]['attributes']['cases7_per_100k'],
                        "deaths": request.json()['features'][0]['attributes']['deaths'],
                        "cases": request.json()['features'][0]['attributes']['cases']
                        }
            except (KeyError, IndexError):
                return None
        else:
            print("Error getting COVID data.", file=sys.stderr)
            return None
