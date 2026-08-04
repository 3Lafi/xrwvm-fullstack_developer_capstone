"""Views for the local dealership demo API."""
import json
from pathlib import Path

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

DATA_DIR = Path(__file__).resolve().parent.parent / 'database' / 'data'


def _load_data(filename, key):
    with open(DATA_DIR / filename, encoding='utf-8') as file:
        return json.load(file)[key]


DEALERS = _load_data('dealerships.json', 'dealerships')
REVIEWS = _load_data('reviews.json', 'reviews')
CARS = _load_data('car_records.json', 'cars')


@csrf_exempt
def login_user(request):
    data = json.loads(request.body or '{}')
    username, password = data.get('userName', ''), data.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'userName': username, 'status': 'Authenticated'})
    return JsonResponse({'userName': username, 'status': 'Unauthenticated'}, status=401)


def logout_request(request):
    logout(request)
    return JsonResponse({'status': 200, 'message': 'Logged out'})


@csrf_exempt
def registration(request):
    if request.method != 'POST':
        return JsonResponse({'status': 405, 'message': 'POST required'}, status=405)
    data = json.loads(request.body or '{}')
    username, password = data.get('userName', '').strip(), data.get('password', '')
    if not username or not password:
        return JsonResponse({'status': 400, 'message': 'Username and password are required'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': 409, 'message': 'Username already exists'}, status=409)
    user = User.objects.create_user(username=username, password=password,
                                    first_name=data.get('firstName', ''),
                                    last_name=data.get('lastName', ''), email=data.get('email', ''))
    login(request, user)
    return JsonResponse({'status': 200, 'userName': user.username, 'firstName': user.first_name, 'lastName': user.last_name})


def get_dealerships(request, state=None):
    dealers = DEALERS if not state or state == 'All' else [item for item in DEALERS if item['state'].lower() == state.lower()]
    return JsonResponse({'status': 200, 'dealers': dealers})


def get_dealer_details(request, dealer_id):
    dealer = [item for item in DEALERS if item['id'] == dealer_id]
    return JsonResponse({'status': 200 if dealer else 404, 'dealer': dealer}, status=200 if dealer else 404)


def _sentiment(text):
    words = set(text.lower().replace('.', '').replace(',', '').split())
    if words & {'fantastic', 'great', 'excellent', 'good', 'love', 'friendly', 'helpful'}:
        return 'positive'
    if words & {'bad', 'poor', 'terrible', 'awful', 'hate', 'slow'}:
        return 'negative'
    return 'neutral'


def get_dealer_reviews(request, dealer_id):
    reviews = [dict(item, sentiment=_sentiment(item['review'])) for item in REVIEWS if item['dealership'] == dealer_id]
    return JsonResponse({'status': 200, 'reviews': reviews})


@csrf_exempt
def add_review(request):
    if request.method != 'POST':
        return JsonResponse({'status': 405, 'message': 'POST required'}, status=405)
    data = json.loads(request.body or '{}')
    required = ('name', 'dealership', 'review', 'car_make', 'car_model', 'car_year')
    if any(not data.get(field) for field in required):
        return JsonResponse({'status': 400, 'message': 'Missing review details'}, status=400)
    review = dict(data, id=max((item['id'] for item in REVIEWS), default=0) + 1)
    review['sentiment'] = _sentiment(review['review'])
    REVIEWS.append(review)
    return JsonResponse({'status': 200, 'review': review})


def get_cars(request):
    cars = [{'CarMake': item['make'], 'CarModel': item['model'], 'CarYear': item['year'], 'CarType': item['bodyType']} for item in CARS]
    return JsonResponse({'status': 200, 'CarModels': cars})


def analyze_review(request, text):
    return JsonResponse({'status': 200, 'sentiment': _sentiment(text)})
