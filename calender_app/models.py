from djongo import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    # description = models.TextField()
    start_time = models.DateField()
    year = models.CharField(max_length=5, blank=True)
    month = models.CharField(max_length=5, blank=True)
    day = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return f"ID={self.id} Title={self.title}"

    def save(self, *args, **kwargs):
        # print("time=",self.start_time.strftime('%Y'),"year=",self.year)
        if not self.year:
            self.year = self.start_time.strftime('%Y')
        if not self.month:
            self.month = self.start_time.strftime('%m')
        if not self.day:
            self.day = self.start_time.strftime('%d')
        super(Event, self).save(*args, **kwargs)
