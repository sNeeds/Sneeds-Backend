from django.urls import path

from . import views

urlpatterns = [
    path('applied-redeem-codes/', views.ApplyRedeemCodeAPIView.as_view(), name='applied-redeem-code-list'),
    path('applied-redeem-codes/<int:id>/', views.ApplyRedeemCodeAPIView.as_view(), name='applied-redeem-code-list'),
    path('apply-redeem-code/', views.ApplyRedeemCodeAPIView.as_view(), name='apply-redeem-code'),
    path('invite-info/', views.InviteInfoListAPIView.as_view(), name='invite-info-list'),
    path('invite-info/<int:id>/', views.InviteInfoDetailAPIView.as_view(), name='invite-info-detail'),
    path('invite-by-referral/', views.InviteByReferralAPIView.as_view(), name='invite-by-referral'),
    path('participants/', views.ParticipantsAPIView.as_view(), name='participant-list'),
    path('participants/<int:user_id>/', views.ParticipantAPIView.as_view(), name='participant-detail'),

]