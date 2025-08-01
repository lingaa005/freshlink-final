from django.urls import path
from .views import (VendorGroupChatListCreateAPIView,VendorProducerListAPIView,ProducerDetailAPIView
,ProducerOwnReviewsAPIView,SubmitRatingView
)
from .views import LoginView, LogoutView, ChatMessageCreateView, ChatMessageListView,SentMessagesView,AllUserMessagesView,VendorSignupView, ProducerSignupView

urlpatterns = [
    path('vendor-chat/', VendorGroupChatListCreateAPIView.as_view(), name='vendor-chat'),
    path('producers/', VendorProducerListAPIView.as_view(), name='vendor-producer-list'),
    path('producers/<int:producer_id>/', ProducerDetailAPIView.as_view(), name='producer-detail'),
    path('producers/reviews/', ProducerOwnReviewsAPIView.as_view(), name='producer-own-reviews'),
    path('rate-producers/', SubmitRatingView.as_view(), name='vendor-rate-producer'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('messages/', ChatMessageCreateView.as_view(), name='send-message'),
    path('messages/<int:user_id>/', ChatMessageListView.as_view(), name='get-conversation'),
    path('messages/sent/', SentMessagesView.as_view(), name='sent-messages'),
    path('all/', AllUserMessagesView.as_view(), name='all-messages'),
    path('signup/vendor/', VendorSignupView.as_view(), name='vendor-signup'),
    path('signup/producer/', ProducerSignupView.as_view(), name='producer-signup'),


]
