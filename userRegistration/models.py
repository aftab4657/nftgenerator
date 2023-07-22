
# from django.db import models
from djongo import models

# Create your models here.
class Task(models.Model):
    message= models.TextField()
    status = models.CharField(max_length=100)
    folder_name = models.CharField(max_length=100, default='')
    cid_metadata = models.TextField(max_length=255, default='')
    cid_nfts = models.TextField(max_length=255, default='')

    def __str__(self):
        return self.status
    

# class TaskUpdated(models.Model):
#     message= models.TextField()
#     status = models.CharField(max_length=100)
#     folder_name = models.CharField(max_length=100, default='')
#     cid_metadata = models.TextField(max_length=255, default='')
#     db_id = models.TextField(primary_key=True, max_length=255, default="")
#     cid_nfts = models.TextField(max_length=255, default='')

#     def __str__(self):
#         return self.statusupdated