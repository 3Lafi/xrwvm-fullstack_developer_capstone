from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('register', views.registration, name='register'),
    path('get_dealers', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='reviews'),
    path('add_review', views.add_review, name='add_review'),
    path('get_cars', views.get_cars, name='get_cars'),
    path('analyze/<str:text>', views.analyze_review, name='analyze_review'),
    path('fetchDealers', views.get_dealerships),
    path('fetchDealers/<str:state>', views.get_dealerships),
    path('fetchDealer/<int:dealer_id>', views.get_dealer_details),
    path('fetchReviews/dealer/<int:dealer_id>', views.get_dealer_reviews),
    path('fetchCarMakes', views.get_cars),
    path('analyzeReview/<str:text>', views.analyze_review),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
