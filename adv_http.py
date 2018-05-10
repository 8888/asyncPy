'''
This is more attempts at async http requests using asyncio and aiohttp

Some requests won't always be sent async
an example is sequential POST requests that depend on the previous
you may POST data, send another POST to update it, send a GET to confirm state after the posts
async will not work as they will not stay in order

You may have batches that can be async, and others that need to be sequential
But the batches may not necessarily depend on each other

So this will create batches of POST requests
within the batch, they must be sequntial
but all of the batches can be sent using async

This will just use dummy POST requests to http://httpbin.org
Since this is demo only, the posts will all use the same endpoint and payload
'''
import asyncio
from timeit import default_timer
from aiohttp import ClientSession

async def fetch(session, url, b, u):
    ''' async POST request for a single URL '''
    start = default_timer()
    resp = await session.post(url, json={'test': 'someData'})
    print('Batch #{} -- URL #{} {:.2f}'.format(b, u, default_timer() - start))
    async with resp:
        return resp

async def create_batch(session, batch, b):
    start = default_timer()
    status = []
    for u, url in enumerate(batch):
        response = await fetch(session, url, b, u)
        status.append(response.status)
    print('** Batch #{} completed: {:.2f}'.format(b, default_timer() - start))
    return status

async def send_batches(batches):
    tasks = []
    async with ClientSession() as session:
        for b, batch in enumerate(batches):
            task = asyncio.ensure_future(create_batch(session, batch, b))
            tasks.append(task)
        futures = await asyncio.gather(*tasks)
        return futures

def async_post(*batches):
    '''
    takes any number of batches
    a batch is a list of urls
    send sequential POST requests to those urls
    all batches are run async
    '''
    start = default_timer()
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(send_batches(batches))
    print('Total time for all batches: {:.2f}'.format(default_timer() - start))
    return results

if __name__ == '__main__':
    # simulating needing multiple requests
    batch_a = ['http://httpbin.org/post'] * 2
    batch_b = ['http://httpbin.org/post'] * 3
    batch_c = ['http://httpbin.org/post'] * 2
    results = async_post(batch_a, batch_b, batch_c)
    print(results)
