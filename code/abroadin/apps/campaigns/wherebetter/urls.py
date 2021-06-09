from django.urls import path

from . import views

urlpatterns = [
    path('apply-redeem-code/<int:user_id>/', views.ApplyRedeemCodeAPIView.as_view(), name='apply-redeem-code'),
    path('invite-by-referral/<int:user_id>/', views.InviteByReferralAPIView.as_view(), name='apply-by-referral'),
    path('participants/', views.ParticipantsAPIView.as_view(), name='participant-list'),
    path('participants/<int:user_id>/', views.ParticipantAPIView.as_view(), name='participant-detail'),

]