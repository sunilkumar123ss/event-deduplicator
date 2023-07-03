"""Bounded, first-seen TTL deduplication with explicit backpressure."""
import argparse
from collections import OrderedDict
import json
import math

class Deduplicator:

    def __init__(self, ttl=10, capacity=100):
        if type(ttl) not in (int, float) or not math.isfinite(ttl) or ttl <= 0:
            raise ValueError('TTL must be positive')
        if type(capacity) is not int or capacity < 1:
            raise ValueError('Capacity must be positive')
        self.ttl = ttl
        self.capacity = capacity
        self.entries = OrderedDict()
        self.now = 0

    def accept(self, event_id, now):
        if not isinstance(event_id, str) or not event_id:
            raise ValueError('Event ID must be nonempty')
        if type(now) not in (int, float) or not math.isfinite(now) or now < self.now or (not math.isfinite(now + self.ttl)):
            raise ValueError('Finite monotonic time required')
        self.now = now
        while self.entries and next(iter(self.entries.values())) <= now:
            self.entries.popitem(last=False)
        if event_id in self.entries:
            return False
        if len(self.entries) >= self.capacity:
            raise OverflowError('Deduplication window is full')
        self.entries[event_id] = now + self.ttl
        return True
