# Experimentation with Python's asyncio module
Quick scripts to test, learn, display, and compare async functionality in python.

# HTTP
Async HTTP requests are being made using [aiohttp](https://aiohttp.readthedocs.io/en/stable/) with [asyncio](https://docs.python.org/3/library/asyncio.html). There is a simple helloworld style intro straight from [the aiohttp docs](https://aiohttp.readthedocs.io/en/stable/) in hello_world<span></span>.py. 
## Sync vs Async comparison
There is a quick comparison of the elapsed time using [requests](http://docs.python-requests.org/en/master/) for sync http calls and aiohttp for async http calls in sync_vs_async<span></span>.py. The output is below:
```shell
$ python sync_vs_async.py
**** SYNC ****
https://www.betterin30days.com/ 0.21
http://leecostello.me/ 0.04
https://github.com/betterin30days 0.36
http://httpbin.org/delay/1 1.04
http://httpbin.org/delay/1 1.06
http://httpbin.org/delay/1 1.04
Total time: 3.75
[200, 200, 200, 200, 200, 200]
**** ASYNC ****
http://leecostello.me/ 0.04
https://www.betterin30days.com/ 0.09
https://github.com/betterin30days 0.48
http://httpbin.org/delay/1 1.04
http://httpbin.org/delay/1 1.05
http://httpbin.org/delay/1 1.09
Total time: 1.10
[200, 200, 200, 200, 200, 200]
```
The total time of the sync calls are cumulative. The total time of the async calls is always slightly longer than whichever individual call takes the longest.
## Async batches of sequential requests
Some requests can't be sent async as they depend on a specific order. This example sends multiple POST requests to mimic posting data that must be in a set order. While this batch of POST requests must be sequential, there could be multiple batches being processed asynchronously. Multiple batches of sequential mock POST requests are being sent in asynchronous batches in adv_http<span></span>.py. For demo purposes, the url endpoints and the payloads are all the same, but in the real world this can differ in any way. The mock end put being used is from [httpbin.org](http://httpbin.org/). The output is below:
```shell
$ python adv_http.py
Batch #2 -- URL #0 0.07
Batch #1 -- URL #0 0.10
Batch #2 -- URL #1 0.03
** Batch #2 completed: 0.10
Batch #1 -- URL #1 0.02
Batch #1 -- URL #2 0.02
** Batch #1 completed: 0.15
Batch #0 -- URL #0 0.15
Batch #0 -- URL #1 0.02
** Batch #0 completed: 0.17
Total time for all batches: 0.18
[[200, 200], [200, 200, 200], [200, 200]]
```
The order that the batches are sent is not important, but notice that the URLs from each batch are in order. The total time for all of the batches is always slightly longer than whichever individual batch takes the longest.
