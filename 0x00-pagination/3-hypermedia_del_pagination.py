#!/usr/bin/env python3
""" Deletion-resilient hypermedia pagination """

import csv
import math
from typing import Dict, List


class Server:
    """ Server class to paginate """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """ Cached dataset """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                read = csv.reader(f)
                dset = [row for row in read]
            self.__dataset = dset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """ Retrieves a page """
        if self.__indexed_dataset is None:
            dset = self.dataset()
            truncated_dataset = dset[:1000]
            self.__indexed_dataset = {
                i: dset[i] for i in range(len(dset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """ Retrieves info about a page """
        focus = []
        dset = self.indexed_dataset()
        index = 0 if index is None else index
        ks = sorted(dset.keys())
        assert index >= 0 and index <= ks[-1]
        [focus.append(i)
         for i in ks if i >= index and len(focus) <= page_size]
        data = [dset[v] for v in focus[:-1]]
        next_index = focus[-1] if len(focus) - page_size == 1 else None
        return {'index': index, 'data': data,
                'page_size': len(data), 'next_index': next_index}
