from abc import ABCMeta, abstractmethod
from typing import List, Tuple


class BaseSearchQueryGenerator(metaclass=ABCMeta):
    @abstractmethod
    def generate_search_query(self):
        pass


class SimpleSearchQueryGenerator(BaseSearchQueryGenerator):
    def __init__(self, search_terms: List[str], locations: List[str]):
        self.search_terms = search_terms
        self.locations = locations

    def generate_search_query(self) -> Tuple[str, str]:
        for search_term in self.search_terms:
            for location in self.locations:
                yield search_term, location