import asyncio
from timeit import default_timer

from aiohttp import ClientSession
import requests

async def fetch(session, url):
    '''
    async GET request for a single URL
    since this is async, we need to await that it completes
    '''
    start = default_timer() # timer for demo display only
    resp = await session.get(url)
    print('{} {:.2f}'.format(url, default_timer() - start))
    # using async with so the response object is released after
    async with resp:
        # the full Response object is returned
        return resp

async def fetch_multiple(urls):
    '''
    receives a list of arrays
    creates a list of Futures to fetch each url
    '''
    tasks = [] # list of Task objects, subclass of Future
    async with ClientSession() as session:
        for url in urls:
            # create Task (Future) for each url
            task = asyncio.ensure_future(fetch(session, url))
            # append to list
            tasks.append(task)
        # gather all of the futures into a returnable Future object
        # *tasks unpacks the list and pass each into gather
        futures = await asyncio.gather(*tasks)
        return futures

def async_get(urls):
    '''
    async approach using aiohttp
    takes a list of urls
    uses the asyncio event loop to send a GET request to each url
    '''
    print('**** ASYNC ****')
    start = default_timer()

    # create the basic event loop
    loop = asyncio.get_event_loop()

    # run the event loop on multiple Futures
    # these are created by fetch_multiple()
    results = loop.run_until_complete(fetch_multiple(urls))

    # the result is a list of results
    # these are returned from each function wrapped in a Future
    # in this example result comes from the return of fetch()
    status_codes = [result.status for result in results]
    
    print('Total time: {:.2f}'.format(default_timer() - start))
    return status_codes

def sync_get(urls):
    '''
    standard sync approach using requests
    takes a list of urls
    sends a GET request to each url
    '''
    print('**** SYNC ****')
    start = default_timer()
    status_codes = [] # some type of resulting data to return
    for url in urls:
        start_url = default_timer()
        r = requests.get(url)
        status_codes.append(r.status_code)
        print('{} {:.2f}'.format(url, default_timer() - start_url))
    print('Total time: {:.2f}'.format(default_timer() - start))
    return status_codes

if __name__ == '__main__':
    urls = [
        'https://www.betterin30days.com/',
        'http://leecostello.me/',
        'https://github.com/betterin30days',
        'http://httpbin.org/delay/1',
        'http://httpbin.org/delay/1',
        'http://httpbin.org/delay/1'
    ]
    sync_result = sync_get(urls)
    print(sync_result)
    async_result = async_get(urls)
    print(async_result)
