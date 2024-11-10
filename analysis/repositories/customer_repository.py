from .interfaces import ICustomerRepository
from ..models import Customer, Policy
from django.db.models import Count

class CustomerRepository(ICustomerRepository):
    def get_customer_distribution(self, ordered_filters):
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

        #return a dict for each value based on the last filter the total count 
        return distribution