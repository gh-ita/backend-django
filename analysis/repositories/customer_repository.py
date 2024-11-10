from .interfaces import ICustomerRepository
from ..models import Customer, Policy
from django.db.models import Count

class CustomerRepository(ICustomerRepository):
    def get_customer_distribution(self, ordered_filters):
        queryset  = Customer.objects.none()

        for field, value in ordered_filters :
            if field == 'vehicle_segment' : 
                queryset = queryset.filter(policies__vehicle_segment = value)
            else : 
                queryset = queryset.filter(**{field: value})
        total_count = queryset.count()

        return total_count