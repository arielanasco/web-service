from django.db import models

# Create your models here.
class TestFile(models.Model):
	file_name = models.FileField(upload_to='test_file')
