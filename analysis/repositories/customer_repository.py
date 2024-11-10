from .interfaces import ICustomerRepository
from ..models import Customer, Policy
from django.db.models import Count
from django.core.cache import cache

class CustomerRepository(ICustomerRepository):
    def get_customer_distribution(self, ordered_filters):
        cache_key = f"customer_distribution_{ordered_filters}"
        distribution = cache.get(cache_key)
        if distribution is None:
            queryset = Customer.objects.all()
            distribution = {}
            for field, value in ordered_filters:
                if value:  # Apply the filter if a value is provided
                    if field == 'vehicle_segment':
                        queryset = queryset.filter(policies__vehicle_segment=value)
                    else:
                        queryset = queryset.filter(**{field: value})
                #For the filter to which we didn't precise a value, it can be the first as well as the last
                else :
                    if field == 'vehicle_segment' : 
                        distribution = queryset.values('policies__vehicle_segment').annotate(count=Count('id'))
                    else :
                        # count how many records for each value of the field 
                        distribution = queryset.values(field).annotate(count=Count('id'))
            cache.set(cache_key,distribution)
        #return a dict for each value based on the last filter the total count 
        return distribution
    
    def total_clients_with_policies(self):
           """A method that counts the total number of clients with at least two policies"""
           queryset = Customer.objects.annotate(num_policies=Count('policy')).filter(num_policies__gt=1)
           return queryset.count()  