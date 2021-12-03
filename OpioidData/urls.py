from django.urls import path
from .views import searchPrescribersPageView, searchPrescribersNPIPageView, searchPrescribersNamePageView, femalePrescribersPageView, malePrescribersPageView, notOpioidDrugsPageView, opioidDrugsPageView, searchDrugsPageView, addPageView, deletePageView, updatePageView, editPageView, trendsPageView, allPrescriberPageView, allDrugsPageView, singlePrescriberPageView, singleDrugPageView, indexPageView

urlpatterns = [
    path("searchprescribers/", searchPrescribersPageView, name="searchprescribers"),
    path("searchprescribersnpi/", searchPrescribersNPIPageView, name="searchprescribersnpi"),
    path("searchprescribersname/", searchPrescribersNamePageView, name="searchprescribersname"),
    path("female/", femalePrescribersPageView, name="female"),
    path("male/", malePrescribersPageView, name="male"),
    path("notopioiddrugs/", notOpioidDrugsPageView, name="notopioiddrugs"),
    path("opioiddrugs/", opioidDrugsPageView, name="opioiddrugs"),
    path("searchdrugs/", searchDrugsPageView, name="searchdrugs"),
    path("add/", addPageView, name="add"),
    path("delete/<int:npi>/", deletePageView, name='delete'),
    path("update/", updatePageView, name="update"),
    path("edit/<int:npi>/", editPageView, name="edit"),
    path("trends/", trendsPageView, name="trends"),
    path("prescribers/", allPrescriberPageView, name="prescribers"),
    path("drugs/", allDrugsPageView, name="drugs"),
    path("prescriber/<int:npi>", singlePrescriberPageView, name="prescriber"),
    path("drug/<str:drugname>", singleDrugPageView, name="drug"),
    path("", indexPageView, name="index"),
]