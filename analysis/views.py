from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from injector import inject
from .services.interfaces import *
from .tasks import *
from celery.result import AsyncResult

# Create your views here.
def index(request):
  return HttpResponse("Hello Geeks")

#Customer distribution view
class CustomerDistributionView(View):
    @inject
    def __init__(self, customer_service: ICustomerService, *args, **kwargs):
        self.customer_service = customer_service
        super().__init__(*args, **kwargs)

    def get(self, request):
        filter_params = request.GET.getlist("filters")
        
        filters = {}
        for param in filter_params:
            if "=" in param:
                key, value = param.split("=")
                filters[key] = value
                
        task = get_customer_distribution_task.apply_async(args=[filters])
        return JsonResponse({
            "task_id": task.id,
            "status": "Task started. Check task status later."
        })
        
#Coverage count view without filters 
class CoverageCountView(View):
  @inject 
  def  __init__(self, policy_service = IPolicyService, *args, **kwargs ):
    self.policy_service = policy_service
    super().__init__(*args, **kwargs)
    
  def get(self):
    task = get_coverages_count_task.apply_async()  
    return JsonResponse({
            "task_id": task.id,
            "status": "Task started. Check task status later."
        })
#Coverage count view filtered
class CoverageCountFilteredView(View):
  @inject 
  def  __init__(self, policy_service = IPolicyService, *args, **kwargs ):
    self.policy_service = policy_service
    super().__init__(*args, **kwargs)
     
  def get(self, request):
    filter_params = request.GET.getlist("filters")
    filters = {}
    for param in filter_params:
      if "=" in param:
        key, value = param.split("=")
        filters[key] = value
        
    task = get_coverages_count_filtered_task.apply_async(args=[filters])
    return JsonResponse({
            "task_id": task.id,
            "status": "Task started. Check task status later."
        })

#Total Policies per month view 
class PoliciesByMonthView(View):
  @inject 
  def  __init__(self, policy_service = IPolicyService, *args, **kwargs ):
    self.policy_service = policy_service
    super().__init__(*args, **kwargs)
    
  def get(self):
    task = get_total_policies_by_month_task.apply_async()
    return JsonResponse({
            "task_id": task.id,
            "status": "Task started. Check task status later."
        })
  
#Total Policies per year view
class PoliciesByYearView(View):
  @inject 
  def  __init__(self, policy_service = IPolicyService, *args, **kwargs ):
    self.policy_service = policy_service
    super().__init__(*args, **kwargs)
     
  def get(self):
    task = get_total_policies_by_year_task.apply_async()
    return JsonResponse({
            "task_id": task.id,
            "status": "Task started. Check task status later."
        })

#Total Policies per quarter view 
class PoliciesByQuarterView(View):
  @inject 
  def  __init__(self, policy_service = IPolicyService, *args, **kwargs ):
    self.policy_service = policy_service
    super().__init__(*args, **kwargs)
     
  def get(self):
    task = get_total_policies_by_quarter_task.apply_async()
    return JsonResponse({
            "task_id": task.id,
            "status": "Task started. Check task status later."
        })

#Average premium view 
class AvgPremiumView(View):
  @inject 
  def  __init__(self, policy_service = IPolicyService, *args, **kwargs ):
    self.policy_service = policy_service
    super().__init__(*args, **kwargs)
     
  def get(self, request):
    filter_params = request.GET.getlist("filters")
    filters = {}
    for param in filter_params:
      if "=" in param:
        key, value = param.split("=")
        filters[key] = value
        
    task = average_premium_filtered_task.apply_async(args=[filters])
    return JsonResponse({
            "task_id": task.id,
            "status": "Task started. Check task status later."
        })
  
#Coverages by premium interval view 
class CoverageByPremiumView(View):
  @inject 
  def  __init__(self, policy_service = IPolicyService, *args, **kwargs ):
    self.policy_service = policy_service
    super().__init__(*args, **kwargs)
     
  def get(self,):
    task = count_coverages_by_premium_interval_task.apply_async()
    return JsonResponse({
            "task_id": task.id,
            "status": "Task started. Check task status later."
        })

#Coverage by car type view 
class CoverageByCarTypeView(View):
  @inject 
  def  __init__(self, policy_service = IPolicyService, *args, **kwargs ):
    self.policy_service = policy_service
    super().__init__(*args, **kwargs)
     
  def get(self, request):
    car_type = request.GET.get('car_type') 
    if not car_type:
      return JsonResponse({"error": "car_type parameter is required"}, status=400)
    task = get_coverage_perc_by_car_type_task.apply_async(args=[car_type])
    return JsonResponse({
            "task_id": task.id,
            "status": "Task started. Check task status later."
        })
