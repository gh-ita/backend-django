from abc import ABC, abstractmethod

class IPolicyRepository(ABC):
    @abstractmethod
    def get_coverages_count(self) :
        pass
    @abstractmethod
    def get_coverages_count_filtered(self,filters) :
        pass
    @abstractmethod
    def get_total_policies_by_month(self):
        pass
    @abstractmethod
    def get_total_policies_by_year(self):
        pass
    @abstractmethod
    def get_total_policies_by_quarter(self):
        pass
    @abstractmethod
    def average_premium_filtered(self, ordered_filter):
        pass
    @abstractmethod
    def count_coverages_by_premium_interval(self):
        pass
    @abstractmethod
    def get_coverage_perc_by_car_type(self, car_type):
        pass
    @abstractmethod
    def total_premium(self):
        pass
    @abstractmethod
    def total_policy(self):
        pass
    
    
        