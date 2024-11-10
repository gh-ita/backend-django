from django.test import TestCase
from ..models import *
from ..repositories import *
from unittest.mock import patch
from django.utils import timezone
from django.db.models import Sum, Avg, Count, Max

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

class PolicyRepositoryTest(TestCase):
    
    def setUp(self):
        """Set up data for the tests."""
        self.repo = PolicyRepository()
        self.date1 = Date.objects.create(date=timezone.now())
        
        self.customer1 = Customer.objects.create(customer_id=1, gender="Male", income_group="0- $25K", region="West")
        self.customer2 = Customer.objects.create(customer_id=2, gender="Female", income_group="25K- $50K", region="East")
        
        self.coverage1 = Coverage_type.objects.create(name="bodily_injury_liability")
        self.coverage2 = Coverage_type.objects.create(name="personal_injury_protection")

        Policy.objects.create(policy_id=1, customer_id=self.customer1, vehicle_segment="A", premium=500, date_id=self.date1, bodily_injury_liability=True)
        Policy.objects.create(policy_id=2, customer_id=self.customer1, vehicle_segment="A", premium=300, date_id=self.date1, personal_injury_protection=True)

        # Create Policy instances for customer2 (one policy)
        Policy.objects.create(policy_id=3, customer_id=self.customer2, vehicle_segment="B", premium=700, date_id=self.date1, bodily_injury_liability=True)

    def test_get_coverages_count(self):
        """Test for counting the coverage types."""
        coverages_count = self.repo.get_coverages_count()
        self.assertEqual(len(coverages_count), 2)  # Should return coverage counts for bodily_injury_liability and personal_injury_protection

    def test_get_coverages_count_filtered(self):
        """Test for counting the coverage types with filters."""
        ordered_filters = [("gender", "Male"), ("income_group", None)]
        coverages_count_filtered = self.repo.get_coverages_count_filtered(ordered_filters)
        self.assertTrue(len(coverages_count_filtered) > 0)  

    def test_get_total_policies_by_month(self):
        """Test for counting policies by month."""
        total_policies_by_month = self.repo.get_total_policies_by_month()
        self.assertEqual(len(total_policies_by_month), 1)  # As we have only one date in the test, it should return one month count.

    def test_get_total_policies_by_year(self):
        """Test for counting policies by year."""
        total_policies_by_year = self.repo.get_total_policies_by_year()
        self.assertEqual(len(total_policies_by_year), 1)  # We have policies for one year in the test data

    def test_get_total_policies_by_quarter(self):
        """Test for counting policies by quarter."""
        total_policies_by_quarter = self.repo.get_total_policies_by_quarter()
        self.assertEqual(len(total_policies_by_quarter), 1)  # One quarter in the test data

    def test_average_premium(self):
        """Test for calculating average premium."""
        average_premium = self.repo.average_premium()
        self.assertEqual(average_premium, 500)  # (500 + 300 + 700) / 3 = 500

    def test_average_premium_filtered(self):
        """Test for calculating average premium with filters."""
        ordered_filter = [("vehicle_segment", "A"), ("income_group", "0- $25K")]
        average_premium_filtered = self.repo.average_premium_filtered(ordered_filter)
        self.assertEqual(average_premium_filtered, 400)  # (500 + 300) / 2 = 400

    def test_count_coverages_by_premium(self):
        """Test for counting coverage types based on premium intervals."""
        count_coverages = self.repo.count_coverages_by_premium(200, 600)
        self.assertTrue(len(count_coverages) > 0)  # Should return coverage count percentages for premium between 200 and 600.

    def test_count_coverages_by_premium_interval(self):
        """Test for counting coverage types based on premium intervals."""
        count_coverages_by_premium_interval = self.repo.count_coverages_by_premium_interval()
        self.assertTrue(len(count_coverages_by_premium_interval) > 0)  # Should return coverage count percentages for different premium intervals.

    def test_get_coverage_perc_by_car_type(self):
        """Test for counting coverage percentages per vehicle segment."""
        coverage_percentage = self.repo.get_coverage_perc_by_car_type("A")
        self.assertTrue(len(coverage_percentage) > 0)  # Should return coverage percentages for vehicle segment "A"

    def test_total_premium(self):
        """Test for calculating the total premium."""
        total_premium = self.repo.total_premium()
        self.assertEqual(total_premium, 1500)  # 500 + 300 + 700 = 1500

    def test_total_policy(self):
        """Test for counting the total number of policies."""
        total_policy = self.repo.total_policy()
        self.assertEqual(total_policy, 3)  # We have three policies in the test data
