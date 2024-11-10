from injector import inject, Module, singleton
from .repositories import *
from .repositories.interfaces import *
from .services import *
from .services.interfaces import *

class AppModule(Module):
    def configure(self, binder):
        binder.bind(ICustomerRepository, to=CustomerRepository, scope=singleton)
        binder.bind(IPolicyRepository, to=PolicyRepository, scope=singleton)
        binder.bind(CustomerService, to=CustomerService, scope=singleton)
