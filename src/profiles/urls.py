from django.urls import path
from .views import (my_profile_view,
                    invites_received_view,
                    invite_profiles_list_view, ProfileListView, ProfileDetailView,
                    send_invitation, remove_from_friends,
                    accept_invatation, reject_invatation
                    )

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name='all-profiles-view'),
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('my-invites/', invites_received_view, name='my-invites-view'),
    path('<slug>/', ProfileDetailView.as_view(), name='profile-detail-view'),
    path('to-invites/', invite_profiles_list_view, name='invite-profiles-view'),
    path('send-invite/', send_invitation, name='send-invite'),
    path('remove-friend/', remove_from_friends, name='remove-friend'),
    path('my-invites/accept/', accept_invatation, name='accept-invite-view'),
    path('my-invites/reject/', reject_invatation, name='reject-invite-view'),

]
