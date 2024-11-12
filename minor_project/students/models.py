from django.db import models

class Student(models.Model):
    username = models.IntegerField(primary_key=True,null=False)
# Username as primary key
    phone = models.CharField(max_length=15)
    roll_no = models.CharField(max_length=15, unique=True)
    c_name = models.CharField(max_length=255)  # Candidate name
    gender = models.CharField(max_length=15)
    dob = models.DateField()  # Date of Birth
    
    c_rank = models.IntegerField()
    xii_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=15)
    nationality = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    email = models.EmailField()  # Use EmailField for validation

    def __str__(self):
        return str(self.roll_no)
    class Meta:
        db_table = 'candidate'

class College(models.Model):
    college_id = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=255)
    college_type = models.CharField(max_length=20)
    contact_no = models.CharField(max_length=15)
    location=models.CharField(max_length=255,null=True)  # Using CharField for formatting
    email = models.EmailField() 
    website=models.CharField(max_length=255,null=True) # For validation

    def __str__(self):
        return self.college_name
    class Meta:
        db_table = 'college'


