from abc import ABC, abstractmethod

class ICustomerService(ABC):
    @abstractmethod
    def get_customer_distribution(self, ordered_filters):
        pass
