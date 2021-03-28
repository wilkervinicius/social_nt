from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.


def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None,
                            request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        form.save()
        confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/myprofile.html', context)


def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invatations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False

    if len(results) == 0:
        is_empty = True
    context = {
        'qs': results,
        'is_empty': is_empty,
    }
    return render(request, 'profiles/my_invites.html', context)


def accept_invatation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        relationship = get_object_or_404(
            Relationship, sender=sender, receiver=receiver)
        if relationship.status == 'send':
            relationship.status = 'accepted'
            relationship.save()
        return redirect('profiles:my-profile-view')


def reject_invatation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        relationship = get_object_or_404(
            Relationship, sender=sender, receiver=receiver)

        relationship.delete()

        return redirect('profiles:my-invites-view')


"""
Substituida pela classe abaino
def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {
        'qs': qs
    }

    return render(request, 'profiles/profiles_list.html', context)
"""


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    def get_object(self, slug=None, **kwargs):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        relationship_sender = Relationship.objects.filter(receiver=profile)
        relationship_receiver = Relationship.objects.filter(sender=profile)

        rel_sender = []
        rel_receiver = []
        for item in relationship_sender:
            rel_sender.append(item.sender.user)
        for item in relationship_receiver:
            rel_receiver.append(item.receiver.user)

        context['rel_sender'] = rel_sender
        context['rel_receiver'] = rel_receiver
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object(
        ).get_all_authors_posts()) > 0 else False
        return context


class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profiles_list.html'
    # context_object_name = 'qs'   a classe retorna para template o object_list

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        relationship_sender = Relationship.objects.filter(receiver=profile)
        relationship_receiver = Relationship.objects.filter(sender=profile)

        rel_sender = []
        rel_receiver = []
        for item in relationship_sender:
            rel_sender.append(item.sender.user)
        for item in relationship_receiver:
            rel_receiver.append(item.receiver.user)

        context['rel_sender'] = rel_sender
        context['rel_receiver'] = rel_receiver
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invites(user)

    context = {
        'qs': qs,
    }

    return render(request, 'profiles/to_invite_list.html', context)


def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relationship = Relationship.objects.create(
            sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile:my-profile-view')


def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relationship = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (
                Q(receiver=receiver) & Q(sender=sender))
        )
        relationship.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile:my-profile-view')
