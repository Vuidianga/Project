import requests

def get_market_price():
    API_KEY = 'yBAKkSc0W8n-xxpDnQ4brbAZiZ1T45eUlWkC-kNILNU'  # Replace with your actual API key
    url = 'https://api.tibber.com/v1-beta/gql'

    query = """
    {
      viewer {
        homes {
          currentSubscription {
            priceInfo {
              current {
                total
                energy
                tax
                startsAt
              }
              today {
                total
                energy
                tax
                startsAt
              }
              tomorrow {
                total
                energy
                tax
                startsAt
              }
            }
          }
        }
      }
    }
    """

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(url, json={'query': query}, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)

        data = response.json()

        if 'errors' in data:
            print(f"GraphQL Error: {data['errors']}")
            return

        # Extract and print price info
        homes = data.get('data', {}).get('viewer', {}).get('homes', [])

        if not homes:
            print("No homes found in the response.")
            return

        for home in homes:
            subscription = home.get('currentSubscription')
            if not subscription:
                print("No active subscription found.")
                continue

            price_info = subscription.get('priceInfo')
            if not price_info:
                print("No price info available.")
                continue

            #print("\n--- Current Electricity Prices ---")
            #print(f"Current Total Price: {price_info['current']['total']} EUR/kWh")
            #print(f"Today's Prices:")
            print('Date,Time,Timezone, Prices[EUR/kWh]  ')
            for price in price_info['today']:

                print(f"{price['startsAt'][:10]},{price['startsAt'][11:23]},{price['startsAt'][23:]},{price['total']}")



            if price_info['tomorrow']:
                #print("\nTomorrow's Prices:")
                for price in price_info['tomorrow']:
                    print(f"{price['startsAt'][:10]},{price['startsAt'][11:23]},{price['startsAt'][23:]},{price['total']}")

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")

if __name__ == '__main__':
    get_market_price()