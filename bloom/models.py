from django.db import models
from django.contrib.auth.models import User

class Gardens(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gardens')
    name = models.CharField(max_length=100)
    private = models.BooleanField()

class Plant(models.Model):
    id = models.AutoField(primary_key=True)
    common_name = models.CharField(max_length=50, null=True)
    scientific_name = models.CharField(max_length=100, unique=True)
    year = models.IntegerField(null=True)                                                  # The first publication year of a valid name of this species                             
    family = models.CharField(max_length=100, null=True) 
    genus = models.CharField(max_length=100, null=True)  
    genus_id = models.IntegerField(null=True)  

    edible = models.BooleanField(blank=True, null=True)
    vegetable = models.BooleanField(blank=True, null=True)

    growth_rate = models.CharField(max_length=50, blank=True, null=True)
    max_height = models.IntegerField(blank=True, null=True) 
    avg_height = models.IntegerField(blank=True, null=True) 
    growth_months = models.JSONField(blank=True, null=True)                   # Most active growing months (all year for perennial plants)
    row_spacing = models.JSONField(blank=True, null=True)                     # Minimum line spacing between rows centimeiters
    spread = models.JSONField(blank=True, null=True)                          # Average spreading of the plant in centimeiters

    toxicity = models.CharField(max_length=5, null=True)

    soil_moisture = models.IntegerField(blank=True, null=True)                           #  From 0 (clay) to 10 (rock)
    soil_texture = models.IntegerField(blank=True, null=True)                            #  From 0 (xerophile) to 10 (subaquatic)
    
    soil_nutriments = models.IntegerField(blank=True, null=True)                         #  From 0 (oligotrophic) to 10 (hypereutrophic)
    soil_salinity = models.IntegerField(blank=True, null=True)                           #  From 0 (untolerant) to 10 (hyperhaline)

    ph_max = models.IntegerField(blank=True, null=True)                                  # Of top 30 cm of soil 
    ph_min = models.IntegerField(blank=True, null=True) 

    sunlight = models.IntegerField(blank=True, null=True)                                #  From 0 (no light, <= 10 lux) to 10 (very intensive insolation, >= 100 000 lux)
    max_temp = models.IntegerField(blank=True, null=True)                                # The maximum tolerable temperature for the species. In celsius or fahrenheit degrees
    min_temp = models.IntegerField(blank=True, null=True)                                # The minimum tolerable temperature for the species. In celsius or fahrenheit degrees

    days_to_harvest = models.IntegerField(blank=True, null=True)                         # The average numbers of days required to from planting to harvest
    atmospheric_humidity = models.IntegerField(blank=True, null=True)                    # Required relative moisture in the air, on a scale from 0 (<=10%) to 10 (>= 90%)

    min_root_depth = models.JSONField(blank=True, null=True)                         # Minimum depth of soil required for the species, in centimeters. Plants that do not have roots such as rootless aquatic plants have 0
    bloom_months = models.JSONField(blank=True, null=True)    
    fruit_months = models.JSONField(blank=True, null=True)       

class PersonalPlant(models.Model):

    id = models.AutoField(primary_key=True)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='plants')
    name = models.CharField(max_length=100, blank=True, null=True)
    sensor_id = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personal_plants')
    garden = models.ForeignKey(Gardens, on_delete=models.CASCADE, related_name='personal_plants')
    status = models.CharField(max_length=20, choices=[('Happy', 'Happy'), ('Thirsty', 'Thirsty'), ('Wet', 'Wet')], null=True)
    auto_watering = models.BooleanField(default=False) 
    last_watered = models.DateTimeField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

class WateringHistory(models.Model):
    personal_plant = models.ForeignKey(PersonalPlant, on_delete=models.CASCADE, related_name='watering_history')
    date_watered = models.DateTimeField(auto_now_add=True) 
    
class StatusHistory(models.Model):
    personal_plant = models.ForeignKey(PersonalPlant, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=50)
    date_changed = models.DateTimeField(auto_now_add=True)
    