from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import PhotoForm, ProfileForm, ProjectForm, SignUpForm, SkillForm
from .models import Photo, Profile, Project, Skill

MODELS = {'skill': Skill, 'project': Project, 'photo': Photo}
FORMS = {'skill': SkillForm, 'project': ProjectForm, 'photo': PhotoForm}


def get_profile(user):
    """Return the user's profile, creating it if an old account has none."""
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


def home(request):
    profiles = Profile.objects.select_related('user').order_by('-id')[:12]
    return render(request, 'home.html', {'profiles': profiles})


def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created. Fill in your profile below.')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def dashboard(request):
    profile = get_profile(request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile saved.')
            return redirect('dashboard')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = ProfileForm(instance=profile)
    share_url = request.build_absolute_uri(
        reverse('public_profile', args=[request.user.username])
    )
    return render(request, 'dashboard.html', {
        'form': form, 'profile': profile, 'share_url': share_url,
    })


@login_required
def manage(request):
    profile = get_profile(request.user)
    forms = {key: form_class() for key, form_class in FORMS.items()}
    if request.method == 'POST':
        kind = request.POST.get('kind')
        if kind not in FORMS:
            raise Http404
        form = FORMS[kind](request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.profile = profile
            item.save()
            messages.success(request, f'{kind.title()} added.')
            return redirect('manage')
        forms[kind] = form
        messages.error(request, f'Could not add the {kind}. Check the form.')
    return render(request, 'manage.html', {
        'profile': profile,
        'forms': forms,
        'skills': profile.skills.all(),
        'projects': profile.projects.all(),
        'photos': profile.photos.all(),
    })


@login_required
def delete_item(request, kind, pk):
    model = MODELS.get(kind)
    if model is None:
        raise Http404
    # profile=... makes sure people can only delete their own items
    item = get_object_or_404(model, pk=pk, profile=get_profile(request.user))
    if request.method == 'POST':
        if kind == 'photo':
            item.image.delete(save=False)
        item.delete()
        messages.success(request, f'{kind.title()} deleted.')
    return redirect('manage')


def public_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    return render(request, 'profile.html', {
        'profile': profile,
        'is_owner': request.user.is_authenticated and request.user == profile.user,
        'share_url': request.build_absolute_uri(request.path),
    })
