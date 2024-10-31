#!/usr/bin/env python3
""" FIFO caching """

from collections import OrderedDict
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ allows storing with a FIFO removal mechanism when """
    def __init__(self):
        """ Initializes the cache """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """ Adds an item """
        if key is None or item is None:
            return
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            f_key, _ = self.cache_data.popitem(False)
            print("DISCARD:", f_key)

    def get(self, key):
        """ Retrieves an item """
        return self.cache_data.get(key, None)
