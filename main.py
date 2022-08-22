import requests
import sys
import time

urls = {
  'orange': 'http://api.nbp.pl/api/exchangerates/rates/a/eur/last/100/?format=json'
}



def main(arguments):
    start = time.time()
    response = requests.get(urls['orange'])
    end = time.time()
    print("Time")
    print(end - start)
    if 'application/json' in response.headers.get('Content-Type'):
      print("Yes")
    try:
        response_content = response.json()
    except ValueError:
        print("This is not JSON type file")

    print(response.status_code)

    for element in response_content['rates']:
      print(element['mid'])

if __name__ == "__main__":
    main(sys.argv)