from django.urls import path
from .views import predictorPageView, addCredentialPageView, newDrugPageView, addDrugPageView, resourcesPageView, portalPageView, searchPrescribersPageView, searchDrugsPageView, addPageView, deletePageView, updatePageView, editPageView, trendsPageView, allPrescriberPageView, allDrugsPageView, singlePrescriberPageView, singleDrugPageView, indexPageView

urlpatterns = [
    path("predictor/", predictorPageView, name="predictor"),
    path("addcredential/<int:npi>", addCredentialPageView, name="addcredential"),
    path("newdrug/", newDrugPageView, name="newdrug"),
    path("searchprescribers/", searchPrescribersPageView, name="searchprescribers"),
    path("searchdrugs/", searchDrugsPageView, name="searchdrugs"),
    path("add/", addPageView, name="add"),
    path("delete/<int:npi>/", deletePageView, name='delete'),
    path("update/<int:npi>", updatePageView, name="update"),
    path("edit/<int:npi>/", editPageView, name="edit"),
    path("trends/", trendsPageView, name="trends"),
    path("prescribers/", allPrescriberPageView, name="prescribers"),
    path("drugs/", allDrugsPageView, name="drugs"),
    path("adddrug/<int:npi>", addDrugPageView, name="adddrug"),
    path("prescriber/<int:npi>", singlePrescriberPageView, name="prescriber"),
    path("drug/<str:drugname>", singleDrugPageView, name="drug"),
    path("resources/", resourcesPageView, name="resources"),
    path("portal/", portalPageView, name='portal'),
    path("", indexPageView, name="index"),
]