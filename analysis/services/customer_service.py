from ..repositories.interfaces import ICustomerRepository
from injector import inject
from .interfaces import ICustomerService
from typing import Dict, Union

class CustomerService(ICustomerService):
    @inject
    def __init__(self, customer_repository: ICustomerRepository):
        self.customer_repository = customer_repository

    def get_customer_distribution(self, ordered_filters : Dict[str, Union[str, int]])-> Dict[str, int]:
        """Get customer distribution based on the filters."""
        if not isinstance(ordered_filters, dict):
            raise TypeError("Filters should be a dictionary")
        result = self.customer_repository.get_customer_distribution(ordered_filters)
        if not isinstance(result, dict):
            raise ValueError("Expected a dictionary as output in get customer distribution method")
        return result
    
    def total_clients_with_policies(self) -> float:
        """Get the total number of customers with more than one policy"""
        result = self.customer_repository.total_clients_with_policies()
        if not isinstance(result, float):
            raise ValueError("Expected a float as output in total clients with policies method")
        return result