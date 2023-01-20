import time
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Room, Message, Note, Tag, User
from .forms import RoomForm, NoteForm, MyUserCreationForm, UserForm
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exit")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password does not exit!")
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
    return render(request, 'base/login_register.html', {'form':form})


# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(name__icontains=q) |
        Q(host__name__icontains=q)
    )
    context={'rooms':rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk) #passes in the id to get the correct room
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST': #If a value is passed in...
        Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    context={'user':user}
    return render(request, 'base/profile.html', context)    

@login_required(login_url='login')
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)
    context = {'form': form}  

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/profile_form.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm() 

    if request.method == 'POST':  #If user submitted data
        form = RoomForm(request.POST) #All POST data entered into Room Form.
        if form.is_valid(): #ensures the RoomForm has correct values
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            room.participants.add(request.user)
            return redirect('home') 
    context={'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def leaveRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.participants.remove(request.user)
        if not room.participants.first():
            room.delete()
        else:
            room.host = room.participants.first()
            room.save()
        return redirect('home')
    
    context = {'room':room}

    return render(request, 'base/leave_room.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def addMember(request, pk):
    room = Room.objects.get(id=pk)
    users = User.objects.all()

    if request.method == 'POST':
        username = request.POST.get('member').lower()
        try:
            user = User.objects.get(username=username)
            room.participants.add(user)
            return redirect('room', pk=room.id)
        except:
            messages.error(request, 'The user you entered does not exist')
        
    context={'room':room,"users":users}
    return render(request, 'base/add_member_form.html', context)

@login_required(login_url='login')
def removeMember(request,pk, rk):
    room = Room.objects.get(id=rk)
    participant = User.objects.get(id=pk)

    if request.method == 'POST':
        room.participants.remove(participant)
        return redirect('room',rk)
    
    context = {'room':room, 'participant':participant}
    return render(request, 'base/remove_user.html', context)


@login_required(login_url='login')
def notePage(request):   
    notes = Note.objects.all()
    context = {'notes':notes}
    return render(request, 'base/note_component.html', context)


@login_required(login_url='login')
def createNote(request):
    form = NoteForm()
    tags = Tag.objects.all()
    if request.method == 'POST':
        tag_name=request.POST.get('tag')
        tag, created = Tag.objects.get_or_create(name=tag_name)
        
        Note.objects.create(
            user=request.user,
            tag=tag,
            title=request.POST.get('title'),
            body=request.POST.get('body')
        )

        return redirect('note-page')
    context={'form':form, 'tags':tags}
    return render(request, 'base/note_form.html', context)

@login_required(login_url='login')
def updateNote(request, pk):
    note = Note.objects.get(id=pk)
    form = NoteForm(instance=note)
    tags = Tag.objects.all()

    if request.user != note.user and request.user not in note.recipients.all():
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        tag_name=request.POST.get('tag')
        tag, created = Tag.objects.get_or_create(name=tag_name) #get the tag or create it for a model if DNE.
        note.title = request.POST.get('title')
        note.tag = tag
        note.body = request.POST.get('body')
        note.save()
        return redirect('note-page')
    context = {'form':form, 'tags':tags, 'note':note}
    return render(request, 'base/note_form.html', context)

@login_required(login_url='login')
def deleteNote(request,pk):
    note = Note.objects.get(id=pk)
    if request.user != note.user:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST':
        note.delete()
        return redirect('note-page')
    
    return render(request, 'base/delete.html', {'obj':note})

#Uses same html form as addMember
@login_required(login_url='login')
def shareNote(request,pk):
    note = Note.objects.get(id=pk)
    users = User.objects.all()

    if request.method == 'POST':
        username = request.POST.get('member').lower()
        try:
            user = User.objects.get(username=username)
            note.recipients.add(user)
            return redirect('note-page')
        except:
            messages.error(request, 'The user you entered does not exist')
        
    context={'note':note,"users":users}
    return render(request, 'base/add_member_form.html', context)
