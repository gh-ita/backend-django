from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from injector import inject
from .services.interfaces import ICustomerService

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
        ordered_filters = request.GET.getlist("filters")
        distribution = self.customer_service.get_customer_distribution(ordered_filters)
        return JsonResponse(distribution)
      
#
