from .interfaces import IPolicyRepository
from ..models import Policy, Coverage_type, Date
from django.db.models import Count, Avg, Max, Sum
from django.core.cache import cache


class PolicyRepository(IPolicyRepository):
    def get_coverages_count(self):
        """A method for the pie chart of coverage types without filters"""

        coverages = Coverage_type.objects.all()
        coverage_count = {}

        for coverage in coverages:
            field_name = coverage.name
            count = Policy.objects.filter(**{field_name: True}).count()
            if count != 0 :
                coverage_count[field_name] = count
        sorted_coverage_count = sorted(
            coverage_count.items(), key=lambda x: x[1])
        return sorted_coverage_count

    def get_coverages_count_filtered(self, ordered_filters):
        """A method for the pie chart of coverage types with filters which are gender, income group, vehicle segment, region"""
        cache_key = f"coverages_count_filtered_{ordered_filters}"
        sorted_coverage_count = cache.get(cache_key)
        if sorted_coverage_count is None:
            coverages = Coverage_type.objects.all()
            coverage_count = {}

            *filters, (last_field, _) = ordered_filters

            for coverage in coverages:
                # Start with policies by coverage type
                queryset = Policy.objects.filter(**{coverage.name: True})
                # If there ’s only one filter, use it directly for aggregation
                if len(ordered_filters) == 1:
                    if last_field == "vehicle_segment":
                        coverage_count[coverage] = queryset.values(
                            'vehicle_segment').annotate(count=Count('id'))
                    else:
                        coverage_count[coverage] = queryset.values(
                            f'customer__{last_field}').annotate(
                            count=Count('id'))
                    continue
                # Apply all filters except the last one
                for field, value in filters:
                    if value:
                        if field == "vehicle_segment":
                            queryset = queryset.filter(vehicle_segment=value)
                        else:
                            queryset = queryset.filter(
                                **{f'customer_id__{field}': value})
                if last_field == "vehicle_segment":
                    coverage_count[coverage.name] = queryset.values(
                        'vehicle_segment').annotate(count=Count('id'))
                else:
                    coverage_count[coverage.name] = queryset.values(
                        f'customer_id__{last_field}').annotate(
                        count=Count('id'))

                sorted_coverage_count = sorted(
            coverage_count.items(), 
            key=lambda x: sum(item['count'] for item in x[1]), 
            reverse=True
        )
                cache.set(cache_key, sorted_coverage_count, timeout=300)
            return sorted_coverage_count

    def get_total_policies_by_month(self):
        """A method to count the total policies purchased based on months"""
        total_policies_by_month = {}
        months = Date.objects.values("month").distinct()
        for month in months:
            total_policies_by_month[month["month"]] = Policy.objects.filter(
                date_id__month = month["month"]).count()
        return total_policies_by_month

    def get_total_policies_by_year(self):
        """A method to count the total policies purchased based on year"""
        total_policies_by_year = {}
        years = Date.objects.values("year").distinct()
        for year in years:
            total_policies_by_year[year["year"]] = Policy.objects.filter(
                date_id__year = year["year"]).count()
        return total_policies_by_year

    def get_total_policies_by_quarter(self):
        """A method to count the total policies purchased based on quarter"""
        total_policies_by_quarter = {}
        quarters = Date.objects.values("quarter").distinct()
        for quarter in quarters:
            total_policies_by_quarter[quarter["quarter"]] = Policy.objects.filter(
                date_id__quarter = quarter["quarter"]).count()
        return total_policies_by_quarter

    def average_premium(self):
        """A method that calculates the average premium"""
        average = Policy.objects.aggregate(Avg('premium'))
        return average['premium__avg']

    def average_premium_filtered(self, ordered_filter):
        """A method that calculates the average premium based on the specific filters, gender, vehicle segment, region, income_group"""
        cache_key = f"average_premium_filtered_{ordered_filter}"
        average = cache.get(cache_key)
        if average is None:
            queryset = Policy.objects.values("premium", "vehicle_segment")

            for field, value in ordered_filter:
                if value:  # Apply the filter if a value is provided
                    if field == 'vehicle_segment':
                        queryset = queryset.filter(vehicle_segment=value)
                    else:
                        queryset = queryset.filter(**{f'customer_id__{field}': value})
                else:  # The filter without value (either first or last)
                    if field == 'vehicle_segment':
                        queryset = queryset.values('vehicle_segment')
                    else:
                        queryset = queryset.values(f'customer__{field}')

            # Calculate the average premium
            # After applying all filters, we use `aggregate` to compute the average
            # premium
            average = queryset.aggregate(Avg('premium'))
            # Return the average premium value or None if no records match the
            # filters
            cache.set(cache_key, average['premium__avg'], timeout=3600) 
        return average['premium__avg']

    def count_coverages_by_premium(self, max, min):
        """A method that counts the total of each coverage"""
        coverages = Coverage_type.objects.values("name")
        queryset = Policy.objects.filter(premium__gte=min, premium__lte=max)
        coverage_count_by_premium = {}

        for coverage in coverages:
            coverage_field = coverage["name"]
            count = queryset.filter(**{coverage_field: True}).count()
            percentage = count / queryset.count() * 100 if queryset.count() > 0 else 0
            coverage_count_by_premium[coverage_field] = percentage
        return coverage_count_by_premium

    def count_coverages_by_premium_interval(self):
        """A method that counts the total each coverage based on premium intervals"""
        cache_key = "coverage_count_by_premium_interval"
        coverage_counts_by_interval = cache.get(cache_key)
        if coverage_counts_by_interval is None:
            max_premium = Policy.objects.aggregate(Max('premium'))['premium__max']
            firstd = 0
            secondd = max_premium / 3
            thirdd = max_premium / 3 * 2
            fourthd = max_premium
            coverage_counts_by_interval = {}
            coverage_counts_by_interval[f'{firstd}-{secondd}'] = self.count_coverages_by_premium(
                firstd, secondd)
            coverage_counts_by_interval[f'{secondd}-{thirdd}'] = self.count_coverages_by_premium(
                secondd, thirdd)
            coverage_counts_by_interval[f'{thirdd}-{fourthd}'] = self.count_coverages_by_premium(
                thirdd, fourthd)
            cache.set(cache_key, coverage_counts_by_interval, timeout=3600)
        return coverage_counts_by_interval

    def get_coverage_perc_by_car_type(self, car_type):
        """A method that counts the total of each coverage per vehicle segment"""
        cache_key = f"coverage_perc_by_car_type_{car_type}"
        coverage_percentage = cache.get(cache_key)
        if coverage_percentage is None:
            coverages = Coverage_type.objects.values("name")
            coverage_percentage = {}
            if car_type is None:
                for coverage in coverages:
                    coverage_field = coverage["name"]
                    count = Policy.objects.filter(**{coverage_field: True}).count()
                    coverage_percentage[coverage_field] = count
            else:
                for coverage in coverages:
                    coverage_field = coverage["name"]
                    # Count policies that match the car type and have the coverage
                    # field set to True
                    count = Policy.objects.filter(
                        vehicle_segment=car_type, **{coverage_field: True}).count()
                    coverage_percentage[coverage_field] = count
            cache.set(cache_key, coverage_percentage, timeout=3600)
        return coverage_percentage
        
    def total_premium(self):
        """A method that counts the total amount of premiums"""
        queryset = Policy.objects.aggregate(total_premium=Sum('premium'))
        return queryset.get('total_premium', 0)
    
    def total_policy(self):
        """A method that counts the total amount of policies"""
        queryset = Policy.objects.aggregate(total_policies = Count('policy_id'))
        return queryset.get("total_policies",0)
    
    
