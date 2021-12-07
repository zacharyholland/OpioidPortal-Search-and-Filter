from django.db.models.aggregates import Sum
from django.db.models.fields import CharField
from django.shortcuts import render
from .models import Credential, Prescriber, Drug, PrescriberCredential, Triple, Specialty, State
from django.db.models import Q, Avg, Count, Sum

# Create your views here.
def indexPageView(request) :
    return render(request, 'OpioidData/index.html')

def resourcesPageView(request) :
    return render(request, 'OpioidData/resources.html')

def portalPageView(request) :
    return render(request, 'OpioidData/portalhome.html')

def allPrescriberPageView(request) :
    data = Prescriber.objects.all()
    data1 = Specialty.objects.all()
    data2 = Credential.objects.all()

    context = {
        "prescriber" : data,
        "specialty" : data1,
        "credential" : data2
    }

    return render(request, 'OpioidData/prescribers.html', context)

def allDrugsPageView(request) :
    data = Drug.objects.all()

    context = {
        "drug" : data
    }

    return render(request, 'OpioidData/drugs.html', context)

def singlePrescriberPageView(request, npi) :
    my_dict = {
        "prescriberid" : npi
    }
    
    data = Prescriber.objects.get(npi = npi)
    data2 = Triple.objects.raw(''' SELECT DISTINCT drugname, prescriberid, qty AS id FROM pd_triple WHERE prescriberid = %(prescriberid)s ''', my_dict)
    data3 = PrescriberCredential.objects.filter(npi = npi)
    data4 = Triple.objects.filter(prescriberid = npi).aggregate(totaldrug=Sum('qty'))
    #data5 = Triple.objects.filter(prescriberid = npi).values('drugname')
    #sum = Triple.objects.filter(drugname=data2.drugname).aggregate(sum=Sum('qty'))
    #count = Triple.objects.filter(drugname=data2.drugname).annotate(Count('drugname'))
    #averages = sum/count
    data6 = Triple.objects.filter(prescriberid = npi).raw(''' SELECT drugname, ROUND(AVG(qty),2) AS id FROM pd_triple GROUP BY drugname ''')
    data5 = Triple.objects.raw(''' SELECT prescriberid, drugname, SUM(qty) AS id FROM pd_triple WHERE prescriberid = %(prescriberid)s GROUP BY drugname, prescriberid ''', my_dict)

    context = {
        "record" : data,
        "drugs" : data2,
        "credentials" : data3,
        "average" : data6,
        "sum" : data4,
        "sums" : data5
    }

    return render(request, 'OpioidData/prescriber.html', context)

def trendsPageView(request) :
    return render(request, 'OpioidData/trends.html')

def editPageView(request, npi) :
    data = Prescriber.objects.get(npi = npi)
    data1 = Specialty.objects.all()
    data2 = State.objects.all()

    context = {
        "record" : data,
        "specialty" : data1,
        "state" : data2
    }

    return render(request, 'OpioidData/edit.html', context)

def singleDrugPageView(request, drugname) :
    data = Drug.objects.get(drugname = drugname)

    my_dict = {
   'drugname': drugname
    } 

    data2 = Triple.objects.raw('''SELECT * from pd_triple where drugname = %(drugname)s ORDER BY qty DESC LIMIT 10 ''', my_dict)

    context = {
        "record" : data,
        "triple" : data2
    }

    return render(request, 'OpioidData/drug.html', context)

def updatePageView(request, npi) :
    if request.method == 'POST' :
        npi = request.POST['npi']

        prescriber = Prescriber.objects.get(npi=npi)

        prescriber.Fname = request.POST['Fname']
        prescriber.Lname = request.POST['Lname']
        prescriber.Gender = request.POST['Gender']
        prescriber.State = request.POST['State']
        prescriber.isipioid_prescriber = request.POST['IsOpioid']
        prescriber.specialty = request.POST['Specialty']

        prescriber.save()

    return singlePrescriberPageView(request, npi)

def deletePageView(request, npi) :
    data = Prescriber.objects.get(npi=npi)

    data.delete()

    return allPrescriberPageView(request)

def addPageView(request) :
    if request.method == 'POST' :
        prescriber = Prescriber()

        prescriber.npi = request.POST['npi']
        prescriber.Fname = request.POST['Fname']
        prescriber.Lname = request.POST['Lname']
        prescriber.Gender = request.POST['Gender']
        prescriber.State = request.POST['State']
        prescriber.specialty = request.POST['Specialty']
        prescriber.isopioid_prescriber = request.POST['IsOpioid']

        prescriber.save()

        prescriber_credential = PrescriberCredential()

        prescriber_credential.npi = Prescriber.objects.get(npi = request.POST['npi'])
        prescriber_credential.credential = Credential.objects.get(credential_code = request.POST['credential'])

        prescriber_credential.save()

        #Prescriber_Credential.npi = request.POST['npi']
        #Prescriber_Credential.credential = request.POST['credentials']

        
        #Prescriber_Credential.save()

        return allPrescriberPageView(request)
    else :
        data1 = Specialty.objects.all()
        data2 = Credential.objects.all()
        data3 = State.objects.all()

        context = {
            "specialty" : data1,
            "credential" : data2,
            "states" : data3
        }

        return render(request, "OpioidData/add.html", context)

def searchDrugsPageView(request) :
    if request.method == "POST" :
        drugname = request.POST['drugname']
        isopioid = request.POST['isopioid']

        drugs = Drug.objects.filter(drugname__icontains=drugname).filter(isopioid__icontains=isopioid)

        context = {
            'drugs' : drugs
        }

        return render(request, "OpioidData/drugsearch.html", context)
    else :
        return render(request, "OpioidData/drugsearch.html", {})

def searchPrescribersPageView(request) :
    if request.method == "POST" :

        npi = request.POST['npi']
        name = request.POST['name']
        gender = request.POST['gender']
        opioid = request.POST['isopioid']
        state = request.POST['state']
        specialty = request.POST['specialty']

        prescribers = Prescriber.objects.filter(npi__icontains=npi).filter(Q(Fname__icontains=name) | Q(Lname__icontains=name)).filter(Gender__icontains=gender).filter(isopioid_prescriber__icontains=opioid).filter(specialty__icontains=specialty).filter(State__icontains=state)

        context = {
            'prescribers' : prescribers
        }
        
        return render(request, "OpioidData/searchprescribers.html", context)
    else :
        return render(request, "OpioidData/searchprescribers.html", {})

def addDrugPageView(request, npi) :
    if request.method == 'POST' :

        triple = Triple()

        triple.prescriberid = Prescriber.objects.get(npi = npi)
        triple.drugname = Drug.objects.get(drugname = request.POST['drugname'])
        triple.qty = request.POST['qty']
        
        triple.save()
        
        return singlePrescriberPageView(request, npi)
    else :
        prescriber = Prescriber.objects.get(npi = npi)
        data1 = Drug.objects.all()

        context = {
            "record" : prescriber,
            "drugs" : data1
        }

        return render(request, "OpioidData/adddrug.html", context)

def newDrugPageView(request) :
    if request.method == 'POST' :
        drug = Drug()

        drug.drugname = request.POST['drugname']
        drug.isopioid = request.POST['isopioid']

        drug.save()

        return allPrescriberPageView(request)
    else :
        return render(request, "OpioidData/newdrug.html")


def addCredentialPageView(request, npi) :
    if request.method == 'POST' :
        prescriber_credential = PrescriberCredential()

        prescriber_credential.npi = Prescriber.objects.get(npi = npi)
        prescriber_credential.credential = Credential.objects.get(credential_code = request.POST['credential'])

        prescriber_credential.save()

        data = Prescriber.objects.all()
        data1 = Specialty.objects.all()
        data2 = Credential.objects.all()

        context = {
            "prescriber" : data,
            "specialty" : data1,
            "credential" : data2
        }

        return singlePrescriberPageView(request, npi)
    
    else :
        record = Prescriber.objects.get(npi=npi)
        data1 = PrescriberCredential.objects.filter(npi=npi)
        data2 = Credential.objects.all()

        context = {
            "record" : record,
            "credentials" : data1,
            "credential_options" : data2
        }

        return render(request, "OpioidData/addcredential.html", context)

def predictorPageView(request) :
    return render(request, "OpioidData/predictor.html")