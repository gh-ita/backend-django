from abc import ABC, abstractmethod

class ICustomerService(ABC):
    @abstractmethod
    def get_customer_distribution(self, ordered_filters):
        pass
    @abstractmethod
    def total_clients_with_policies(self):
        pass