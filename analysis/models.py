from django.db import models

# Create your models here.
class Customer(models.Model):
    INCOME_CHOICES = [
        ('0-25K', '0- $25K'),
        ('25-70K', '$25-$70K'),
        ('70K+', '>$70K'),
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    REGION_CHOICES = [
        ('North', 'North'),
        ('South', 'South'),
        ('East', 'East'),
        ('West', 'West'),
    ]
    customer_id = models.IntegerField()
    gender = models.CharField(max_length=6, choices = GENDER_CHOICES)
    income_group = models.CharField(max_length=6, choices = INCOME_CHOICES)
    region = models.CharField(max_length=5, choices = REGION_CHOICES)

class Date(models.Model):
    date_id = models.AutoField(primary_key=True)
    date = models.DateField()
    month = models.IntegerField()
    year = models.IntegerField()
    quarter = models.IntegerField()
    
class Policy(models.Model):
    VEHICLE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]
    policy_id = models.IntegerField()
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='policies')
    date_id = models.ForeignKey(Date, on_delete=models.CASCADE, related_name='policies')
    premium = models.IntegerField()
    vehicle_segment = models.CharField(max_length=1, choices = VEHICLE_CHOICES)
    bodily_injury_liability = models.BooleanField(default=True)
    personal_injury_protection = models.BooleanField(default=True) 
    property_damage_liability = models.BooleanField(default=True)
    collision = models.BooleanField(default=True)
    comprehensive = models.BooleanField(default=True)

class Coverage_type(models.Model):
    COVERAGE_CHOICES = [
        ('bodily_injury_liability', 'Bodily Injury Liability'),
        ('personal_injury_protection', 'Personal Injury Protection'),
        ('property_damage_liability', 'Property Damage Liability'),
        ('collision', 'Collision'),
        ('comprehensive', 'Comprehensive'),
    ]
    coverage_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, choices = COVERAGE_CHOICES)

