from django.urls import path
#now import the views.py file into this code
from . import views
from .views import *

urlpatterns=[
  path('',views.index), 
  path('policies-by-quarter/', PoliciesByQuarterView.as_view(), name='policies_by_quarter_api'),
  path('policies-by-year/', PoliciesByYearView.as_view(), name='policies_by_year_api'),
  path('policies-by-month/', PoliciesByMonthView.as_view(), name='policies_by_month_api'),
  path('customer-distribution', CustomerDistributionView.as_view(), name = 'customer_distribution_api'), 
  path('coverage-count', CoverageCountView.as_view(), name = 'coverage_count_api'),
  path('coverage-count-filtered', CoverageCountFilteredView, name = 'coverage_count_filtered_api'),
  path('avg-premium', AvgPremiumView.as_view(), name = 'avg_premium_api'),
  path('coverage-by-premium', CoverageByPremiumView.as_view(), name = 'coverage_by_premium_api'), 
  path('coverage-by-car-type', CoverageByCarTypeView.as_view(), name = 'coverage_by_cartype_api'),
  path('total-premium', TotalPremiumView.as_view(), name = 'total_premium_api'),
  path('total-policy', TotalPolicyView.as_view(), name = 'total_policy_api'),
  path('total-customers', TotalCustomers.as_view(), name = 'total_customers_api')
]