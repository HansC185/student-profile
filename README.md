# Student Profile Maker

A multi-page Django website where students create an account, build their own
profile, and share a personal link such as `/u/username/`.

**Target users:** students who want a simple online profile or portfolio.

## Features
- Sign up, log in, log out (Django authentication)
- Edit profile: name, tagline, course, school, bio, profile photo, theme color
- Add and delete skills, projects and gallery photos
- Public profile page for every user at `/u/<username>/`
- Copy-link button, dark mode, photo lightbox, animated skill bars
- Responsive layout (mobile menu)

## Django concepts used
- `base.html` with `{% block %}` and `{% extends %}` on every page
- `{% include %}` for navbar, footer and form fields
- `{% url %}` for every link, `{% load static %}` / `{% static %}` for CSS and JS
- Models with `OneToOneField` and `ForeignKey`, `ModelForm`, `ImageField`
- `@login_required`, `get_object_or_404`, signals, messages framework

## Setup
```bash
git clone https://github.com/<your-username>/student-profile.git
cd student-profile
python -m venv venv
venv\Scripts\activate            # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations profiles
python manage.py migrate
python manage.py runserver
```
Open http://127.0.0.1:8000/

Uploaded photos are stored in `media/`, which is not uploaded to GitHub.

## Acknowledgment
AI tools (Claude) and tutorials were used as learning help for parts of this
project. I reviewed and understand the code.

## Author
Your Name - Course - Section
