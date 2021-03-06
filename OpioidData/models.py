from django.db import models
from django.db.models.fields import NOT_PROVIDED, BooleanField
from django.db.models.deletion import DO_NOTHING

# Create your models here.
class Specialty(models.Model):
    specialty_type = models.CharField(unique=True, max_length=70)

    def __str__(self) :
       return (self.specialty_type)
       
    class Meta:
        db_table = "specialty"

class Prescriber(models.Model) :
    npi = models.CharField(unique=True, max_length=10)
    Fname = models.CharField(max_length=30)
    Lname = models.CharField(max_length=30)
    Gender = models.CharField(max_length=7, blank=True)
    State = models.CharField(max_length=2, blank=True)
    isopioid_prescriber = models.CharField(max_length=7, blank=True)
    specialty = models.CharField(max_length=30, blank=True)
    
    class Meta:
        db_table = "pd_prescriber"

    @property
    def full_name(self):
            return '%s %s' % (self.Fname, self.Lname)

    def __str__(self):
        return (self.full_name)

class Drug(models.Model) :
    drugname = models.CharField(unique=True, max_length=100)
    isopioid = models.BooleanField(default=False)

    class Meta:
        db_table = "pd_drugs"

    def __str__(self) :
        return (self.drugname)

class Credential(models.Model):
    credential = models.CharField(max_length=15)
    credential_code = models.IntegerField(unique=True, default=10000000000)
    
    class Meta:
        db_table = "pd_credential"
    
    def __str__(self) :
        return (self.credential)
        
class PrescriberCredential(models.Model):
    credential = models.ForeignKey(Credential, to_field="credential_code", on_delete=DO_NOTHING, default=110)
    npi = models.ForeignKey(Prescriber, to_field="npi", on_delete=DO_NOTHING)
    
    class Meta:
        db_table = "prescriber_credential"
    
    def __str__(self) :
       return (self.credential)

class Triple(models.Model):
    prescriberid = models.ForeignKey(Prescriber, to_field="npi", db_column="prescriberid", on_delete=DO_NOTHING)
    drugname = models.ForeignKey(Drug, to_field="drugname", db_column="drugname", on_delete=DO_NOTHING)
    qty = models.IntegerField()

    class Meta :
        db_table = "pd_triple"

class State(models.Model) :
    state = models.CharField(max_length=5)
    class Meta :
        db_table = "state"
    
    def __str__(self) :
        return (self.state)