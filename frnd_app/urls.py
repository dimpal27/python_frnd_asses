from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import SignupView, LoginView, SearchUserView, SendFriendRequestView,AcceptFriendRequestView,RejectFriendRequestView,ListFriendsView, ListPendingRequestsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('list_user/', SearchUserView.as_view(), name='user-search'),
    path('send_friend_request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('accept_friend_request/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('reject_friend_request/', RejectFriendRequestView.as_view(), name='reject-friend-request'),
    path('list_friends/', ListFriendsView.as_view(), name='list-friends'),
    path('list_pending_requests/', ListPendingRequestsView.as_view(), name='list-pending-requests'),
]