from django.db.models.fields import CharField
from django.shortcuts import render
from .models import Credential, Prescriber, Drug, PrescriberCredential, Triple, Specialty
from django.db.models import Q, Avg

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
    data = Prescriber.objects.get(npi = npi)
    data2 = Triple.objects.filter(prescriberid = npi)
    data3 = PrescriberCredential.objects.filter(npi = npi)
    #data5 = Triple.objects.filter(prescriberid = npi).values('drugname')

    data6 = Triple.objects.aggregate(average_quantity=Avg('qty'))

    #Triple.objects.raw(''' SELECT id, drugname, AVG(qty) AS "avgqty" FROM pd_triple GROUP BY id, drugname ''')
    
    #for Triple.drugname in data2 :
     #   average = []
      #  average[iCount] = Triple.objects.filter(drugname = Triple.drugname).aggregate(average_quantity=Avg('qty'))
       # iCount = iCount + 1

    context = {
        "record" : data,
        "drugs" : data2,
        "credentials" : data3,
        "average" : data6
    }

    return render(request, 'OpioidData/prescriber.html', context)

def trendsPageView(request) :
    return render(request, 'OpioidData/trends.html')

def editPageView(request, npi) :
    data = Prescriber.objects.get(npi = npi)
    data1 = Specialty.objects.all()

    context = {
        "record" : data,
        "specialty" : data1,
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

def updatePageView(request) :
    if request.method == 'POST' :
        npi = request.POST['npi']

        prescriber = Prescriber.objects.get(npi=npi)

        prescriber.Fname = request.POST['Fname']
        prescriber.Lname = request.POST['Lname']
        prescriber.Gender = request.POST['Gender']
        prescriber.State = request.POST['State']

        prescriber.save()

    return allPrescriberPageView(request)

def deletePageView(request, npi) :
    data = Prescriber.objects.get(npi=npi)

    data.delete()

    return allPrescriberPageView(request)

def addPageView(request) :
    if request.method == 'POST' :
        prescriber = Prescriber()
        Prescriber_Credential = PrescriberCredential()

        prescriber.npi = request.POST['npi']
        prescriber.Fname = request.POST['Fname']
        prescriber.Lname = request.POST['Lname']
        prescriber.Gender = request.POST['Gender']
        prescriber.State = request.POST['State']
        prescriber.specialty = request.POST['Specialty']
        prescriber.isopioid_prescriber = request.POST['IsOpioid']

        #Prescriber_Credential.npi = request.POST['npi']
        #Prescriber_Credential.credential = request.POST['credentials']

        prescriber.save()
        #Prescriber_Credential.save()

        return allPrescriberPageView(request)
    else :
        data1 = Specialty.objects.all()
        data2 = Credential.objects.all()

        context = {
            "specialty" : data1,
            "credential" : data2
        }

        return render(request, "OpioidData/add.html", context)

def searchDrugsPageView(request) :
    if request.method == "POST" :
        searched = request.POST['searched']
        #opioid = request.POST['opioid']
        drugs = Drug.objects.filter(drugname__icontains=searched)#.filter(isopioid__icontains=opioid)
        return render(request, "OpioidData/drugsearch.html", {'searched' : searched, 'drugs' : drugs})
    else :
        return render(request, "OpioidData/drugsearch.html", {})

def searchPrescribersNamePageView(request) :
    if request.method == "POST" :
        prenpi = str(request.POST['NPIed'])
        npi = "%" + prenpi + "%"
        prename = str(request.POST['name'])
        name = "%" + prename + "%"
        
        my_dict = {
        'npi': npi,
        'name': name
        #'state': request.POST['state'],
        #'specialty': request.POST['specialty']
        } 

        prescribers = Prescriber.objects.raw(''' SELECT * FROM pd_prescribers WHERE npi LIKE '%(npi)s' AND Fname LIKE '%(name)s' ''', my_dict)

        context = {
            'prescribers' : prescribers
        }
        
        return render(request, "OpioidData/searchprescribers.html", context)
    else :
        return render(request, "OpioidData/searchprescribers.html", {})

def searchPrescribersNPIPageView(request) :
    if request.method == "POST" :
        NPIed = request.POST['NPIed']
        prescribers = Prescriber.objects.filter(npi__icontains=NPIed)
        return render(request, "OpioidData/searchprescribersnpi.html", {'NPIed':NPIed, 'prescribers' : prescribers})
    else :
        return render(request, "OpioidData/searchprescribersnpi.html", {})

def opioidDrugsPageView(request) :
    data = Drug.objects.filter(isopioid__icontains=True)

    context = {
        "drug" : data
    }

    return render(request, 'OpioidData/opioiddrugs.html', context)

def notOpioidDrugsPageView(request) :
    data = Drug.objects.filter(isopioid__icontains=False)

    context = {
        "drug" : data
    }

    return render(request, 'OpioidData/notopioiddrugs.html', context)

def malePrescribersPageView(request) :
    data = Prescriber.objects.filter(Gender__icontains='M')

    context = {
        "prescriber" : data
    }

    return render(request, 'OpioidData/male.html', context)

def femalePrescribersPageView(request) :
    data = Prescriber.objects.filter(Gender__icontains='F')

    context = {
        "prescriber" : data
    }

    return render(request, 'OpioidData/female.html', context)

def searchPrescribersPageView(request) :
    if request.method == "POST" :

        my_dict = {
        #'npi': request.POST['npi'],
        'name': request.POST['named'],
        #'state': request.POST['state'],
        #'specialty': request.POST['specialty']
        } 

        prescribers = Prescriber.objects.raw(''' SELECT * FROM pd_prescriber WHERE "Fname" = %(name)s ''', my_dict)

        context = {
            'prescribers' : prescribers
        }
        
        return render(request, "OpioidData/searchprescribers.html", context)
    else :
        return render(request, "OpioidData/searchprescribers.html", {})

def addDrugPageView(request, npi) :
    if request.method == 'POST' :

        triple = Triple()

        triple.prescriberid = npi
        triple.drugname = request.POST['drugname']
        triple.qty = request.POST['qty']
        
        triple.save()

        return singlePrescriberPageView(request)
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

        return allDrugsPageView(request)
    else :
        return render(request, "OpioidData/newdrug.html")

def addCredentialPageView(request, npi) :
    if request.method == 'POST' :
        prescriber_credential = PrescriberCredential()

        prescriber_credential.npi = npi
        prescriber_credential.credential = request.POST['credential']

        prescriber_credential.save()
    
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
