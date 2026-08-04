# Dealership Reviews Capstone

A full-stack dealership review application built with Django and React. It supports user registration and login, dealer browsing and state filtering, dealer details, customer reviews, review submission, a lightweight sentiment endpoint, and Django administration.

## Run locally

1. In `server`, run `python -m pip install -r requirements.txt`, then `python manage.py migrate` and `python manage.py runserver`.
2. In `server/frontend`, run `npm install` and `npm start`.

The Django API runs at `http://127.0.0.1:8000`; the React development application runs at `http://localhost:3000` and proxies API calls to Django.
