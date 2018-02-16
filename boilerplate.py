from model import *

def read_data(path):
    with open(path) as f:
        lines = [list(map(int, it.rstrip().split())) for it in f.readlines()]
        video_count, endpoint_count, request_count, \
                cache_count, cache_storage = lines.pop(0)

        videos = {}
        for video_id, video_size in enumerate(lines.pop(0)):
            videos[video_id] = Video(video_id, video_size)

        endpoints = {}
        for endpoint_id in range(endpoint_count):
            endpoints[endpoint_id] = Endpoint(endpoint_id)

        caches = {}
        for cache_id in range(cache_count):
            caches[cache_id] = Cache(cache_id, cache_storage)

        for endpoint_id in range(endpoint_count):
            center_latency, cache_count = lines.pop(0)
            endpoint = endpoints[endpoint_id]
            endpoint.center_latency = center_latency

            for i in range(cache_count):
                cache_id, cache_latency = lines.pop(0)
                cache = caches[cache_id]
                endpoint.connections.append(Connection(cache, cache_latency))
                cache.connections.append(Connection(endpoint, cache_latency))

        requests = []
        for request_id in range(request_count):
            video_id, endpoint_id, request_count = lines.pop(0)
            video, endpoint = videos[video_id], endpoints[endpoint_id]
            request = Request(request_id, video, endpoint, request_count)
            requests.append(request)

        return videos.values(), endpoints.values(), caches.values(), requests

def print_solution(caches):
    used_caches = [it for it in caches if it.videos]
    print(len(used_caches))
    for cache in used_caches:
        print(' '.join(map(str, cache.video_ids())))

def score_solution(requests, caches):
    time_saved = 0
    for request in requests:
        endpoint = request.endpoint
        connection = endpoint.best_connection(request.video)
        saved = endpoint.center_latency - connection.latency if connection else 0
        time_saved += request.request_count * saved
    total_requests = sum(it.request_count for it in requests)
    return round(time_saved * 1000 / total_requests)

