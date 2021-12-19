from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm

from .models import Message, Room, Topic, User
from .form import RoomForm, UserForm, UserEditForm, UserSettingsForm, RegistrationForm

# Create your views here.


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist', fail_silently=True)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request, 'Please sign up or try again!', fail_silently=True)
    context = {'page': page}
    return render(request, "base/login.html", context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    # page = 'register'
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request, "An error occured during registration!", fail_silently=True)
    context = {'form': form}
    return render(request, "base/signup.html", context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q) | Q(host__username__icontains=q))
    topics = Topic.objects.all()[:8]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__name__icontains=q))
    message_count = room_messages.count()
    topics_count = topics.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,
               'room_messages': room_messages, 'message_count': message_count, 'topics_count': topics_count}
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    comments = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('post')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    participants_count = participants.count()
    context = {'room': room, 'comments': comments,
               'participants': participants, 'participants_count': participants_count}
    return render(request, "base/room.html", context)


def user_profile(request, pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    message_count = room_messages.count()
    context = {'user': user, 'rooms': rooms,
               'message_count': message_count, 'topics': topics, 'room_messages': room_messages}
    return render(request, 'base/profile.html', context)


@login_required(login_url='/login')
def room_create(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        """ 
        #My older(usual) way of doing forms
        form = RoomForm(request.POST)
        if form.is_valid:
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home') 
        """
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, "base/create_room.html", context)


@login_required(login_url='/login')
def room_update(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You're not allowed here!!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST, instance=room)

        """ 
            # old fomart
            if form.is_valid:
                form.save()
        """

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/create_room.html', context)


# @login_required(login_url='/login')
def room_delete(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You're not allowed here!!")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='/login')
def message_delete(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You're not allowed here!!")

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})
# settings.html


@login_required(login_url='/login')
def settings(request):
    user = request.user
    form = UserSettingsForm(instance=user)
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    context = {'form': form}
    return render(request, 'base/settings.html', context)


@login_required(login_url='/login')
def edit_user(request):
    form = UserEditForm(instance=request.user)
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    context = {'form': form}
    return render(request, 'base/edit_user.html', context)

# Just adding a few more views to make it mobile responsive
# Topica and activities component


def m_topic(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(Q(name__icontains=q))
    context = {'topics': topics}
    return render(request, 'base/m_topics.html', context)


def m_activities(request):
    room_messages = Message.objects.all()
    message_count = room_messages.count()

    context = {'room_messages': room_messages, 'message_count': message_count}
    return render(request, 'base/m_activities.html', context)

# Error messages

def error_404(request, exception):

        return render(request,'404.html')

# def error_500(request,  exception):
#     data = {}
#     return render(request,'500.html', data)
        
# def error_403(request, exception):
#     data = {}

#     return render(request,'403.html')

# def error_400(request,  exception):
#     data = {}
#     return render(request,'400.html', data) 