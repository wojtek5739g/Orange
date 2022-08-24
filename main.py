import requests, sys, time, json, csv, os

class ResponsePathNotFound(FileNotFoundError):
    pass

class ResponsePermissionError(PermissionError):
    pass

class ResponsePathIsDirectory(IsADirectoryError):
    pass

class Response:
    def __init__(self, time, isjson, isjsonvalid, httpcode):
        self._time = time
        self._isjson = isjson
        self._isjsonvalid = isjsonvalid
        self._httpcode = httpcode

    def time(self):
        return self._time

    def isjson(self):
        return self._isjson

    def isjsonvalid(self):
        return self._isjsonvalid

    def httpcode(self):
        return self._httpcode

urls = {
  'orange': 'http://api.nbp.pl/api/exchangerates/rates/a/eur/last/100/?format=json'
}

def write_to_log(file_handle, response, writer):
    writer.writerow({
        'Time': response.time(),
        'Is_Json': response.isjson(),
        'Has_Proper_Syntax': response.isjsonvalid(),
        'HTTP_status_code': response.httpcode()
    })

def check(response, file_handle, writer):
    start = time.time()
    end = time.time()
    t = end - start
    print(f'Time: {t}')
    if response.headers.get('Content-Type').startswith('application/json'):
        print("This is a JSON type file")
        isjson = 'yes'
    else:
        print('This is not a JSON type file')
        isjson = 'no'
    try:
        response_content = response.json()
        print("Has a proper JSON syntax")
        isjsonvalid = 'yes'
    except ValueError:
        print("Doesn't have a proper JSON syntax")
        isjsonvalid = 'no'

    httpcode = response.status_code
    print(f'HTTP status code: {httpcode}')
    print("--------------------")

    resp = Response(t, isjson, isjsonvalid, httpcode)

    write_to_log(file_handle, resp, writer)

def main(arguments):
    X = int(input("Enter the number of checks: "))
    Y = int(input("Enter the number of seconds at which the checks are to run: "))

    response = requests.get(urls['orange'])
    response_content = response.json()

    try:
        with open('log.txt', 'a') as file_handle:
            fieldnames = ['Time', 'Is_Json', 'Has_Proper_Syntax', 'HTTP_status_code']
            writer = csv.DictWriter(file_handle, fieldnames, lineterminator='\n')
            if os.stat('log.txt').st_size == 0:
                writer.writeheader()
            for i in range(0, X):
                check(response, file_handle, writer)
                time.sleep(Y)
    except FileNotFoundError:
        raise ResponsePathNotFound("Could not open response database")
    except PermissionError:
        msg = "You do not have permission to open the database"
        raise ResponsePermissionError(msg)
    except IsADirectoryError:
        raise ResponsePathIsDirectory("Can only work on files")

    print("On those days prices of EUR were not between 4.5 and 4.7 PLN: ")
    for record in response_content['rates']:
        if not 4.5 <= record['mid'] <= 4.7:
            print(record['effectiveDate'])

if __name__ == "__main__":
    main(sys.argv)