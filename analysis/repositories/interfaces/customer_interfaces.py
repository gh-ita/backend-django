from abc import ABC, abstractmethod

class ICustomerRepository(ABC):
    @abstractmethod
    def get_customer_distribution(self, filters):
        pass
    @abstractmethod
    def total_clients_with_policies(self):
        pass