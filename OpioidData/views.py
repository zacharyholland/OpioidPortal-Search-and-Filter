from django.shortcuts import render
from .models import Prescriber, Drug, PrescriberCredential, Triple
from django.db.models import Q

# Create your views here.
def indexPageView(request) :
    return render(request, 'OpioidData/index.html')

def allPrescriberPageView(request) :
    data = Prescriber.objects.all()

    context = {
        "prescriber" : data
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

    context = {
        "record" : data,
        "drugs" : data2,
        "credentials" : data3
    }

    return render(request, 'OpioidData/prescriber.html', context)

def trendsPageView(request) :
    return render(request, 'OpioidData/trends.html')

def editPageView(request, npi) :
    data = Prescriber.objects.get(npi = npi)

    context = {
        "record" : data
    }

    return render(request, 'OpioidData/edit.html', context)

def singleDrugPageView(request, drugname) :
    data = Drug.objects.get(drugname = drugname)
    data2 = Triple.objects.filter(drugname = drugname)
    #data2 = Triple.objects.raw(f'SELECT * FROM pd_triple WHERE drugname = {drugname} ORDER BY qty DESC LIMIT 10;')
    #data2 = Triple.objects.raw(f'SELECT * FROM pd_triple WHERE drugname = {drugname} ORDER BY qty DESC LIMIT 10;')
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

        prescriber.npi = request.POST['npi']
        prescriber.Fname = request.POST['Fname']
        prescriber.Lname = request.POST['Lname']
        prescriber.Gender = request.POST['Gender']
        prescriber.State = request.POST['State']

        prescriber.save()

        return allPrescriberPageView(request)
    else :
        return render(request, "OpioidData/add.html")

def searchDrugsPageView(request) :
    if request.method == "POST" :
        searched = request.POST['searched']
        drugs = Drug.objects.filter(drugname__icontains=searched)
        return render(request, "OpioidData/drugsearch.html", {'searched':searched, 'drugs' : drugs})
    else :
        return render(request, "OpioidData/drugsearch.html", {})

def searchPrescribersNamePageView(request) :
    if request.method == "POST" :
        named = request.POST['named']
        prescribers = Prescriber.objects.filter(Fname__icontains=named)
        return render(request, "OpioidData/searchprescribersname.html", {'named':named, 'prescribers' : prescribers})
    else :
        return render(request, "OpioidData/searchprescribersname.html", {})

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
        named = request.POST['named']
        NPIed = request.POST['NPIed']
        gender = request.POST['gender']
        state = request.POST['state']

        prescribers = Prescriber.objects.filter(Q(Fname__icontains=named) | Q(Lname__icontains=named)).filter(npi__icontains=NPIed).filter(Gender__icontains=gender).filter(State__icontains=state)
        return render(request, "OpioidData/searchprescribers.html", {'named':named, 'NPIed':NPIed, 'gender':gender, 'state':state, 'prescribers' : prescribers})
    else :
        return render(request, "OpioidData/searchprescribers.html", {})