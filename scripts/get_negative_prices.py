import requests

def get_market_price():
    API_KEY = 'yBAKkSc0W8n-xxpDnQ4brbAZiZ1T45eUlWkC-kNILNU'  # Your API key
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
        response.raise_for_status()

        data = response.json()

        if 'errors' in data:
            print(f"GraphQL Error: {data['errors']}")
            return

        homes = data.get('data', {}).get('viewer', {}).get('homes', [])

        if not homes:
            print("No homes found in the response.")
            return

        negative_prices = []

        for home in homes:
            subscription = home.get('currentSubscription')
            if not subscription:
                print("No active subscription found.")
                continue

            price_info = subscription.get('priceInfo')
            if not price_info:
                print("No price info available.")
                continue

            #print("\n--- Negative Prices Today ---")
            for price in price_info['today']:
                if price['energy'] < 0:
                    negative_prices.append({
                        'date': price['startsAt'][:10],
                        'time': price['startsAt'][11:16],
                        'timezone': price['startsAt'][23:],
                        'price': price['energy']

                    })

            if price_info['tomorrow']:
                #print("\n--- Negative Prices Tomorrow ---")
                for price in price_info['tomorrow']:
                    if price['energy'] < 0:
                        negative_prices.append({
                            'date': price['startsAt'][:10],
                            'time': price['startsAt'][11:16],
                            'timezone': price['startsAt'][23:],
                            'price': price['energy']
                        })

        if negative_prices:
            print('Date,Time,Timezone,Negative_prices[EUR/kWh]')
            for item in negative_prices:
                print(f"{item['date']},{item['time']},{item['timezone']},{item['price']}")

        else:
            print("\n No negative prices found in the forecast.")

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")

if __name__ == '__main__':
    get_market_price()
