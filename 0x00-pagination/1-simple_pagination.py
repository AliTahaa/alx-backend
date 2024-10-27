#!/usr/bin/env python3
""" Simple pagination. """

import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """ Retrieves the index range """

    return ((page - 1) * page_size, ((page - 1) * page_size) + page_size)


class Server:
    """ Server class to paginate a database """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """ Cached dataset """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                read = csv.reader(f)
                dset = [row for row in read]
            self.__dataset = dset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ Retrieves a page """
        assert type(page) == int and type(page_size) == int
        assert page > 0 and page_size > 0
        s, e = index_range(page, page_size)
        data = self.dataset()
        if s > len(data):
            return []
        return data[s:e]
