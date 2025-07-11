from django.db import models
from datetime import date
# Create your models here.

class FoodPromotionManager(models.Manager): #prefilter to only return promotions that are still valid (contains a date that hasnt passed)
    def is_valid(self):
        today = date.today().isoformat()
        valid_promotions = []
        for promo in super().get_queryset(): #superquery get all promos
            if promo.active_dates[-1] >= today: #since dates are sorted, last date will be last active date, see if expired
                valid_promotions.append(promo) 
            #else:? dlete?
        return valid_promotions # !!! on each get, run something that deletes old expired promotions as well to declutter, or have CRON to do it?

class FoodPromotion(models.Model):
    telegram_message_id = models.CharField(max_length=255, unique=True)

    restaurant_name = models.CharField(max_length=255)
    deal_type = models.CharField(max_length=255)
    active_dates = models.JSONField(default=list)
    location = models.CharField(max_length=255) #use textsearchquery in googlemaps and shove this in
    image = models.ImageField(upload_to='telefoodpromos_photos/', null=True, blank=True) 
    
    full_message_text = models.TextField(null=True, blank=True) #for reference
    created_at = models.DateTimeField(auto_now_add=True)
    more_info_url = models.URLField(blank=True, null=True)

    objects = FoodPromotionManager() #'override' objects for the model

    def __str__(self):
        return f"{self.restaurant_name} - {self.deal_type}"
