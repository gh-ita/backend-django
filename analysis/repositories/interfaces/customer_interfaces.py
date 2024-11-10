from abc import ABC, abstractmethod

class ICustomerRepository(ABC):
    @abstractmethod
    def get_customer_distribution(self, filters):
        pass