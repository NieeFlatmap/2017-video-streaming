from collections import namedtuple

Connection = namedtuple('Connection', 'target, latency')

class Struct:
    pass

class Video(Struct):
    def __init__(self, id, size):
        self.id, self.size = id, size

    def __repr__(self):
        return '<Video {}: {}MB>'.format(self.id, self.size)

class Cache(Struct):
    def __init__(self, id, storage):
        self.id, self.storage = id, storage
        self.connections = []
        self.videos = []

    def __repr__(self):
        return '<Cache {}: vids {}, free {}MB>'.format(\
            self.id, self.video_ids(), self.free_storage())

    def video_ids(self):
        return [it.id for it in self.videos]

    def taken_storage(self):
        return sum(it.size for it in self.videos)

    def free_storage(self):
        return self.storage - self.taken_storage()

    def can_fit(self, video):
        return self.free_storage() >= video.size

    def connections_by_latency(self):
        return sorted(self.connections, key=lambda it: it.latency)

class Endpoint(Struct):
    def __init__(self, id):
        self.id = id
        self.center_latency = None
        self.connections = []

    def connections_by_latency(self):
        return sorted(self.connections, key=lambda it: it.latency)

    def best_connection(self, video):
        connections = [it for it in self.connections if \
            video.id in it.target.video_ids()]
        return min(connections, key=lambda it: it.latency, default=None)

class Request(Struct):
    def __init__(self, id, video, endpoint, request_count):
        self.id, self.video, self.endpoint, self.request_count = \
            id, video, endpoint, request_count

    def __repr__(self):
        return '<Request {}: video {} * {} to {}>'.format(\
            self.id, self.video.id, self.request_count, self.endpoint.id)

    @property
    def size(self):
        return self.video.size

    def relative_weight(self, all_requests):
        same_video_requests = sum(1 for it in all_requests if \
                it.video == self.video)
        return same_video_requests

