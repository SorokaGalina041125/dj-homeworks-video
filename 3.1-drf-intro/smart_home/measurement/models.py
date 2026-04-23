from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)      

    def __str__(self):
        return self.name


class Measurement(models.Model):
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)     
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    photo = models.ImageField(upload_to='measurements/', blank=True, null=True)

    def __str__(self):
        return f"{self.sensor.name}: {self.temperature}°C at {self.created_at}"