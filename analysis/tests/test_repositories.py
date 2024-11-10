from django.test import TestCase
from ..models import *
from ..repositories import *
from unittest.mock import patch
from django.utils import timezone

class CustomerRepositoryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setup initial data
        cls.date = Date.objects.create(date=timezone.now())
        cls.customer1 = Customer.objects.create(customer_id=1, gender="Male", income_group="0- $25K", region="West")
        cls.customer2 = Customer.objects.create(customer_id=2, gender="Female", income_group="0- $25K", region="East")
        cls.customer3 = Customer.objects.create(customer_id=3, gender="Male", income_group="0- $25K", region="West")
        
        
        cls.policy2 = Policy.objects.create(policy_id=2, customer_id=cls.customer1, vehicle_segment="B", premium=300, date_id = cls.date)
        cls.policy3 = Policy.objects.create(policy_id=3, customer_id=cls.customer2, vehicle_segment="A", premium=700, date_id = cls.date)
        cls.policy4 = Policy.objects.create(policy_id=4, customer_id=cls.customer3, vehicle_segment="A", premium=700, date_id = cls.date)
    @patch('django.core.cache.cache.get')
    @patch('django.core.cache.cache.set')
    def test_get_customer_distribution_cache_miss(self, mock_cache_set, mock_cache_get):
        # Simulate cache miss
        mock_cache_get.return_value = None 
        
        repo = CustomerRepository()
        
        ordered_filters = [('vehicle_segment', 'A'),('gender', None)]
        
        distribution = repo.get_customer_distribution(ordered_filters)
        
        self.assertEqual(len(distribution), 2)  
        self.assertEqual(distribution[1]['count'], 1)  
        
        mock_cache_set.assert_called_once()

    @patch('django.core.cache.cache.get')
    def test_get_customer_distribution_cache_hit(self, mock_cache_get):
        # Simulate cache hit by returning a pre-defined cache value
        mock_cache_get.return_value = {'vehicle_segment': 'A', 'count': 3}
        
        repo = CustomerRepository()
        
        ordered_filters = [('vehicle_segment', 'A'), ("gender")]
        distribution = repo.get_customer_distribution(ordered_filters)
        
        # Check that the result is fetched from cache and not from the database
        self.assertEqual(distribution, {'vehicle_segment': 'A', 'count': 3})
        mock_cache_get.assert_called_once()


    def test_total_clients_with_policies(self):
        repo = CustomerRepository()
        date = Date.objects.create(date=timezone.now())
        # Customer 1 has 2 policies
        customer1 = Customer.objects.create(customer_id=3, gender="Male", income_group="0- $25K", region="West")
        Policy.objects.create(policy_id=1, customer_id=customer1, vehicle_segment="A", premium=500, date_id = date)
        Policy.objects.create(policy_id=2, customer_id=customer1, vehicle_segment="A", premium=500, date_id = date)
        # Customer 2 has 1 policy
        customer2 = Customer.objects.create(customer_id=4, gender="F", income_group="0- $25K", region="East")
        Policy.objects.create(policy_id=3, customer_id=customer2, vehicle_segment="A", premium=700, date_id = date)
        
        # Test the total count of customers with more than one policy
        count = repo.total_clients_with_policies()
        
        # Only customer1 should be counted, as customer2 has only 1 policy
        self.assertEqual(count, 1)
