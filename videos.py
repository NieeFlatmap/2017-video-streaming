import sys
from time import time
from pprint import pprint
from boilerplate import *
from model import *

debug = True

videos, endpoints, caches, requests = read_data(sys.argv[1])

if debug: print('start!')
start_time = time()

#requests.sort(key=lambda it: it.relative_weight(requests), reverse=True)
for i, request in enumerate(requests):
    if debug and i % 10000 == 0:
        print('=', sum)

    video, endpoint = request.video, request.endpoint
    for cache, latency in endpoint.connections_by_latency():
        if cache.can_fit(video) and latency <= endpoint.center_latency:
            cache.videos.append(video)
            break

print_solution(caches)

if debug:
    print('took: {0:.4f} s'.format(time() - start_time))
    print('(score) saved: {} ms'.format(score_solution(requests, caches)))
