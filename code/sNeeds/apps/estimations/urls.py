from django.urls import path

from . import views

app_name = "estimations"

urlpatterns = [
       path('form-comments-detail/<uuid:form_id>/', views.FormCommentsDetail.as_view()),
       path('form-comments-list/', views.FormCommentsList.as_view()),

    path('import-top-universities/', views.ListUsers.as_view(), ),
]
