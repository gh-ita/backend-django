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
            raise ValueError("Expected a dictionary as output")
        return result
