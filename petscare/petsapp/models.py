from django.db import models
from django.utils import timezone

# Create your models here.
class login(models.Model):
    Username = models.CharField(max_length=50)
    Password=models.CharField(max_length=50)
    Status=models.IntegerField()

    def __str__(self):
        return self.Username
class user(models.Model):
    Name=models.CharField(max_length=50)
    Address=models.CharField(max_length=50)
    Phone = models.IntegerField()
    Email = models.EmailField()
    Username = models.CharField(max_length=50)
    def __str__(self):
        return self.Name
class caretaker(models.Model):
    Name = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    Location=models.CharField(max_length=50)
    Photo=models.FileField()
    Phone = models.IntegerField()
    Email = models.EmailField()
    Licence=models.FileField()
    Username = models.CharField(max_length=50)
    Action=models.CharField(max_length=50)

    def __str__(self):
        return self.Name
class details(models.Model):
    Username = models.CharField(max_length=50)
    Name=models.CharField(max_length=50)
    Service=models.CharField(max_length=100)
    Description=models.CharField(max_length=100)
    Amount=models.IntegerField()
    def __str__(self):
        return self.Service
class booking(models.Model):
    Pet_owner=models.CharField(max_length=50)
    Pet_type=models.CharField(max_length=50)
    No_pets=models.IntegerField()
    Breed=models.CharField(max_length=50)
    Service=models.CharField(max_length=50)
    Date_of_service=models.DateField()
    Phone=models.IntegerField()
    Email=models.EmailField()
    Name=models.CharField(max_length=50)
    Username=models.CharField(max_length=50)
    Action=models.CharField(max_length=50)
    Pstatus=models.CharField(max_length=50)
    def __str__(self):
        return self.Name
class feedback(models.Model):
    Pet_owner=models.CharField(max_length=50)
    Pet_caretaker=models.CharField(max_length=50)
    Msg_type=models.CharField(max_length=50)
    Message=models.CharField(max_length=100)
    Username = models.CharField(max_length=50)
    def __str__(self):
        return self.Pet_owner
class p_details(models.Model):
    Pet_owner = models.CharField(max_length=50)
    Name = models.CharField(max_length=50)
    Date=models.DateField(default=timezone.now)
    Email = models.EmailField()
    # Service = models.CharField(max_length=50)
    Amount = models.IntegerField()
    def __str__(self):
        return self.Name
class adpay(models.Model):
    Username=models.CharField(max_length=50)
    Name=models.CharField(max_length=50)
    Amount=models.IntegerField()
    Date=models.DateField(default=timezone.now)
    def __str__(self):
        return self.Name
class PasswordReset(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    token=models.CharField(max_length=4)

class complaint(models.Model):
    Username = models.CharField(max_length=50)
    Name = models.CharField(max_length=50)
    Ct=models.CharField(max_length=50)
    Email = models.EmailField()
    Phone = models.IntegerField()
    Complaint=models.CharField(max_length=500)
    def __str__(self):
        return self.Name


