import requests

def get_consumption_from_user():
    API_KEY = 'yBAKkSc0W8n-xxpDnQ4brbAZiZ1T45eUlWkC-kNILNU'  # Replace with your actual API key
    url = 'https://api.tibber.com/v1-beta/gql'

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }

    # 1. First, get the home ID
    query_id = """
    {
        viewer {
            homes {
                id
                address {
                    address1
                    city
                }
            }
        }
    }
    """

    try:
        response = requests.post(url, json={'query': query_id}, headers=headers)
        response.raise_for_status()

        data = response.json()
        homes = data.get('data', {}).get('viewer', {}).get('homes', [])

        if not homes:
            print("No homes found.")
            return

        home_id = homes[0].get('id')
        #print(f"Home ID: {home_id}")

        # 2. Now fetch consumption data


        query_consumption = """
        {
            viewer {
                home(id: "%s") {
                    consumption(resolution: HOURLY, last: 100) {
                        nodes {
                            to
                            cost 
                            unitPrice
                            unitPriceVAT
                            consumption
                            consumptionUnit
                        }
                    }
                }
            }
        }
        """ % home_id

        response = requests.post(url, json={'query': query_consumption}, headers=headers)
        response.raise_for_status()

        data = response.json()

        if 'errors' in data:
            print(f"GraphQL Error: {data['errors']}")
            return

        consumption_data = data.get('data', {}).get('viewer', {}).get('home', {}).get('consumption', {})
        nodes = consumption_data.get('nodes', [])

        if not nodes:
            print("No consumption data available.")
            return

        # Print header
        print("Date,Time,Timezone,Consumption_Cost[EUR],Consumption_UnitPrice[EUR/kWh],Consumption_UnitPriceVAT[EUR/kWh],Consumption[kWh]")

        for entry in nodes:
            if entry.get('consumption') is not None:
                timestamp = entry['to']
                date = timestamp[:10]
                time = timestamp[11:16]  # Get only HH:MM:SS
                timezone = timestamp[23:]
                cost = entry['cost']
                unit_price = entry['unitPrice']
                unit_price_vat = entry['unitPriceVAT']
                consumption = entry['consumption']

                print(f"{date},{time},{timezone},{cost:.6f},{unit_price:.6f},{unit_price_vat:.6f},{consumption:.3f}")

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        if err.response.status_code == 400:
            print("Bad Request - likely query syntax error")
            print("Response content:", err.response.text)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    get_consumption_from_user()