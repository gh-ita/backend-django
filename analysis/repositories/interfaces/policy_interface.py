from abc import ABC, abstractmethod

class IPolicyRepository(ABC):
    @abstractmethod
    def get_coverages_count(self) :
        pass
    @abstractmethod
    def get_coverages_count_filtered(self,filters) :
        pass