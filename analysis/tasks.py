from celery import shared_task
from .services.interfaces import *
from injector import inject
from typing import Union, Dict
from channels.layers import get_channel_layer

#Customer distribution task
@shared_task
@inject
def get_customer_distribution_task(filters):
    customer_service = ICustomerService()
    try :
        distribution = customer_service.get_customer_distribution(filters)
        channel_layer = get_channel_layer()
        group_name = "task_task_notifications"
        channel_layer.group_send(
            group_name,
            {
                'type': 'send_task_result',  # This matches the method in the consumer
                'result': distribution  # The result data you want to send
            }
        )
        return distribution
    except ValueError as e:
        return {"error": str(e)}
    

#Coverage count task
@shared_task
@inject
def get_coverages_count_task():
    """Asynchronous task to fetch coverage counts."""
    policy_service = IPolicyService()  
    try:
        result = policy_service.get_coverages_count()
        channel_layer = get_channel_layer()
        group_name = "task_task_notifications"
        channel_layer.group_send(
            group_name,
            {
                'type': 'send_task_result',  # This matches the method in the consumer
                'result': result  # The result data you want to send
            }
        )
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
        channel_layer = get_channel_layer()
        group_name = "task_task_notifications"
        channel_layer.group_send(
            group_name,
            {
                'type': 'send_task_result',  # This matches the method in the consumer
                'result': result  # The result data you want to send
            }
        )
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
        channel_layer = get_channel_layer()
        group_name = "task_task_notifications"
        channel_layer.group_send(
            group_name,
            {
                'type': 'send_task_result',  # This matches the method in the consumer
                'result': result  # The result data you want to send
            }
        )
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
        channel_layer = get_channel_layer()
        group_name = "task_task_notifications"
        channel_layer.group_send(
            group_name,
            {
                'type': 'send_task_result',  # This matches the method in the consumer
                'result': result  # The result data you want to send
            }
        )
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
        channel_layer = get_channel_layer()
        group_name = "task_task_notifications"
        channel_layer.group_send(
            group_name,
            {
                'type': 'send_task_result',  # This matches the method in the consumer
                'result': result  # The result data you want to send
            }
        )
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
        channel_layer = get_channel_layer()
        group_name = "task_task_notifications"
        channel_layer.group_send(
            group_name,
            {
                'type': 'send_task_result',  # This matches the method in the consumer
                'result': result  # The result data you want to send
            }
        )
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
        channel_layer = get_channel_layer()
        group_name = "task_task_notifications"
        channel_layer.group_send(
            group_name,
            {
                'type': 'send_task_result',  # This matches the method in the consumer
                'result': result  # The result data you want to send
            }
        )
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
        channel_layer = get_channel_layer()
        group_name = "task_task_notifications"
        channel_layer.group_send(
            group_name,
            {
                'type': 'send_task_result',  # This matches the method in the consumer
                'result': result  # The result data you want to send
            }
        )
        return result
    except (ValueError, TypeError) as e:
        return {"error": str(e)} 
    
#Total of premiums task
@shared_task
@inject
def total_premium() -> float:
    policy_service = IPolicyService()
    try:
        result = policy_service.total_premium()
        if not isinstance(result, float):
            raise ValueError("Expected a float for total of premiums")
        channel_layer = get_channel_layer()
        group_name = "task_task_notifications"
        channel_layer.group_send(
            group_name,
            {
                'type': 'send_task_result',  # This matches the method in the consumer
                'result': result  # The result data you want to send
            }
        )
        return result
    except (ValueError, TypeError) as e:
        return {"error": str(e)} 
        
#Total of policies task
@shared_task
@inject
def total_policy() -> float:
    policy_service = IPolicyService()
    try:
        result = policy_service.total_policy()
        if not isinstance(result, float):
            raise ValueError("Expected a float for total of policies")
        channel_layer = get_channel_layer()
        group_name = "task_task_notifications"
        channel_layer.group_send(
            group_name,
            {
                'type': 'send_task_result',  # This matches the method in the consumer
                'result': result  # The result data you want to send
            }
        )
        return result
    except (ValueError, TypeError) as e:
        return {"error": str(e)} 
#Total of customers with more than one policy task  
@shared_task
@inject
def total_clients_with_policies() -> float:
    customer_service = ICustomerService()
    try:
        result = customer_service.total_clients_with_policies()
        if not isinstance(result, float):
            raise ValueError("Expected a float for total of customers with more than one policy")
        channel_layer = get_channel_layer()
        group_name = "task_task_notifications"
        channel_layer.group_send(
            group_name,
            {
                'type': 'send_task_result',  # This matches the method in the consumer
                'result': result  # The result data you want to send
            }
        )
        return result
    except (ValueError, TypeError) as e:
        return {"error": str(e)} 

