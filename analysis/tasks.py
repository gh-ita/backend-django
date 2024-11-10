from celery import shared_task
from .services.interfaces import *
from injector import inject
from typing import Union, Dict

#Customer distribution task
@shared_task
@inject
def get_customer_distribution_task(filters):
    customer_service = ICustomerService()
    distribution = customer_service.get_customer_distribution(filters)
    return distribution

#Coverage count task
@shared_task
@inject
def get_coverages_count_task():
    """Asynchronous task to fetch coverage counts."""
    policy_service = IPolicyService()  
    try:
        result = policy_service.get_coverages_count()
        return result
    except ValueError as e:
        return {"error": str(e)}

#Filtered coverage count task
@shared_task
@inject
def get_coverages_count_filtered_task(filters: Dict[str, Union[str, int]]):
    """Asynchronous task to fetch coverage counts based on filters."""
    policy_service = IPolicyService()  
    try:
        result = policy_service.get_coverages_count_filtered(filters)
        return result
    except (ValueError, TypeError) as e:
        return {"error": str(e)}

# Total policies by month task 
@shared_task
@inject
def get_total_policies_by_month_task() -> Dict[int, int]:
    """Asynchronous task to fetch the total policies by month."""
    policy_service = IPolicyService()  
    try:
        result = policy_service.get_total_policies_by_month()
        if not isinstance(result, dict):
            raise ValueError("Expected a dictionary for total policies by month")
        return result
    except (ValueError, TypeError) as e:
        return {"error": str(e)}

#Total policies by year 
@shared_task
@inject
def get_total_policies_by_year_task() -> Dict[int, int]:
    """Asynchronous task to fetch the total policies by month."""
    policy_service = IPolicyService()  
    try:
        result = policy_service.get_total_policies_by_year()
        if not isinstance(result, dict):
            raise ValueError("Expected a dictionary for total policies by month")
        return result
    except (ValueError, TypeError) as e:
        return {"error": str(e)}

#Total policies by quarter 

@shared_task
@inject
def get_total_policies_by_quarter_task() -> Dict[int, int]:
    """Asynchronous task to fetch the total policies by month."""
    policy_service = IPolicyService()  
    try:
        result = policy_service.get_total_policies_by_quarter()
        if not isinstance(result, dict):
            raise ValueError("Expected a dictionary for total policies by month")
        return result
    except (ValueError, TypeError) as e:
        return {"error": str(e)}    
    
#Average premium task 
@shared_task
@inject
def average_premium_filtered_task(filters: Dict[str, Union[str, int]]) -> float:
    """Asynchronous task to fetch the total policies by month."""
    policy_service = IPolicyService()  
    try:
        result = policy_service.average_premium_filtered(filters)
        if not isinstance(result, float):
            raise ValueError("Expected a float for average")
        return result
    except (ValueError, TypeError) as e:
        return {"error": str(e)}    
    
#Coverages by premium interval task
@shared_task
@inject
def count_coverages_by_premium_interval_task() -> Dict[str, int]:
    """Asynchronous task to fetch the total policies by month."""
    policy_service = IPolicyService()  
    try:
        result = policy_service.count_coverages_by_premium_interval()
        if not isinstance(result, dict):
            raise ValueError("Expected a dictionnary for coverage count by premium interval")
        return result
    except (ValueError, TypeError) as e:
        return {"error": str(e)}    
    
#Coverage by car type task
@shared_task
@inject
def get_coverage_perc_by_car_type_task(car_type : str) -> Dict[str, int]:
    """Asynchronous task to fetch the total policies by month."""
    policy_service = IPolicyService()  
    try:
        result = policy_service.get_coverage_perc_by_car_type(car_type= car_type)
        if not isinstance(result, dict):
            raise ValueError("Expected a dictionnary for coverage percentage by car type")
        return result
    except (ValueError, TypeError) as e:
        return {"error": str(e)}    

