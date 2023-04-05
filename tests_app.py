import json

import app


def test_mood_today():
    client = app.mood_today()
    response = client.get('/today-mood')
    assert response is None


def test_mood_week():
    client = app.mood_week()
    response = client.get('/today-week')
    assert response is None


def test_mood_month():
    client = app.mood_month()
    response = client.get('/today-month')
    assert response is None


def test_mood_percentage_today():
    client = app.mood_percentages_today()
    response = client.get('/today_mood_percentages')
    assert response is None


def test_mood_percentage_week():
    client = app.mood_percentages_week()
    response = client.get('/week_mood_percentages')
    assert response is None


def test_mood_percentage_month():
    client = app.mood_percentages_month()
    response = client.get('/month_mood_percentages')
    assert response is None
