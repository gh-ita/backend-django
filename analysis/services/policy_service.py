from ..repositories.interfaces import IPolicyRepository
from .interfaces import IPolicyService
from injector import inject
from typing import Dict, Union

class PolicyService(IPolicyService):
    @inject
    def __init__(self, policy_repository: IPolicyRepository):
        self.policy_repository = policy_repository
        
    def get_coverages_count(self) -> Dict[str, int]:
        result = self.policy_repository.get_coverages_count()
        if not isinstance(result, dict):
            raise ValueError("Expected a dictionary as output")
        return result
    
    def get_coverages_count_filtered(self, filters: Dict[str, Union[str, int]]) -> Dict[str, int]:
        if not isinstance(filters, dict):
            raise TypeError("Filters should be a dictionary")
        result = self.policy_repository.get_coverages_count_filtered(filters)
        if not isinstance(result, dict):
            raise ValueError("Expected a dictionary as output")
        return result
    
    def get_total_policies_by_month(self) -> Dict[int, int]:
        """A method that queries the repository to count the total policies purchased based on months"""
        result = self.policy_repository.get_total_policies_by_month()
        if not isinstance(result, dict):
            raise ValueError("Expected a dictionnary for total policies by month")
        
    def get_total_policies_by_year(self) -> Dict[int, int]:
        """A method that queries the repository to count the total policies purchased based on years"""
        result = self.policy_repository.get_total_policies_by_year()
        if not isinstance(result, dict):
            raise ValueError("Expected a dictionnary for total policies by year")
    
    def get_total_policies_by_quarter(self) -> Dict[int, int]:
        """A method that queries the repository to count the total policies purchased based on quarters"""
        result = self.policy_repository.get_total_policies_by_quarter()
        if not isinstance(result, dict):
            raise ValueError("Expected a dictionnary for total policies by quarter")
        
    def average_premium_filtered(self, ordered_filter: Dict[str, Union[str, int]]) -> float:
        if not isinstance(ordered_filter, dict):
            raise TypeError("Ordered_filter should be a dictionary")
        result = self.policy_repository.average_premium_filtered(ordered_filter)
        if not isinstance(result, (float, int)):
            raise ValueError("Expected a numerical value for the average premium")
        return result
        
    
    def count_coverages_by_premium_interval(self) -> Dict[str, int]:
        """A method that queries the repository to count the total each coverage based on premium intervals"""
        result = self.policy_repository.count_coverages_by_premium_interval()
        if not isinstance(result, dict):
            raise ValueError("Expected a dictionnary for coverage count by premium interval")
    
    def get_coverage_perc_by_car_type(self, car_type : str) -> Dict[str, int]:
        """A method that queries the repository to count the total of each coverage per vehicle segment
        input : one character or None"""
        if not isinstance(car_type, str) :
            raise TypeError("car_type should be a character")
        result = self.policy_repository.get_coverage_perc_by_car_type(car_type)
        if not isinstance(result, dict):
            raise ValueError("Expected a dictionnary for coverage percentage by car type")
        
    def total_premium(self) -> float:
        result = self.total_premium()
        if not isinstance(result, float):
            raise ValueError("Expected a float for the total of premiums")
        return result
    def total_policy(self) -> float:
        result = self.total_policy()
        if not isinstance(result, float):
            raise ValueError("Expected a float for the total of policies")
        return result