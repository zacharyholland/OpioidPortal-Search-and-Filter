from django.db import models
from django.db.models.fields import NOT_PROVIDED, BooleanField
from django.db.models.deletion import DO_NOTHING

# Create your models here.
class Prescriber(models.Model) :
    npi = models.CharField(unique=True, max_length=10)
    Fname = models.CharField(max_length=30)
    Lname = models.CharField(max_length=30)
    Gender = models.CharField(max_length=7)
    State = models.CharField(max_length=2)
    isopioid_prescriber = models.BooleanField(default=False)

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
    credential_code = models.IntegerField
    class Meta:
        db_table = "pd_credential"
        
class PrescriberCredential(models.Model):
    credential_code = models.ForeignKey(Credential, on_delete=DO_NOTHING)
    npi = models.IntegerField(blank=False)
    class Meta:
        db_table = "prescriber_credential"

class Specialtie(models.Model):
    specialty_title = models.CharField(max_length=70)
    specialty_code = models.IntegerField
    class Meta:
        db_table = "pd_specialtie"

class Triple(models.Model):
    prescriberid = models.ForeignKey(Prescriber, to_field="npi", db_column="prescriberid", on_delete=DO_NOTHING)
    drugname = models.ForeignKey(Drug, to_field="drugname", db_column="drugname", on_delete=DO_NOTHING)
    qty = models.IntegerField()

    class Meta :
        db_table = "pd_triple"