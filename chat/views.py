from django.template.context_processors import request

from .forms import SignUpForm, LoginForm
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .models import User, ChatRoom, ChatHistory


class HomeView(TemplateView):
    template_name = 'base.html'

class Signup(TemplateView):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = True
            user.save()
            login(request, user)
            return redirect(reverse_lazy('home'))
        return self.render_to_response({'form': form})

class Login(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            user.backend = 'chat.authenticate.EmailBackend'
            login(request, form.get_user())
            return redirect('list-users')  # error : Reverse for 'list-users' not found. 'list-users' is not a valid view function or pattern name
        print("Form errors:", form.errors)
        return self.render_to_response({'form': form})

    def get(self, request, *args, **kwargs):
        form= LoginForm
        return self.render_to_response({'form': form})


class UsersList(TemplateView):
    template_name = 'users_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_in_user = self.request.user
        context['users'] = User.objects.exclude(id=logged_in_user.id)

        return context

class ChatData(TemplateView):
    template_name = 'chat.html'
    
    def get_context_data(self, **kwargs):
        from django.db.models import Q

        context = super().get_context_data(**kwargs)
        
        sender = self.request.user
        receiver = self.kwargs.get('id')
        room = "channel_" + str(sender.id) + "-" + str(receiver)
        room_1 = "channel_" + str(receiver) + "-" + str(sender.id)

        try:
            chat_room = ChatRoom.objects.get(Q(room_name= room) |
                                             Q(room_name=room_1))
            context['room_id'] = chat_room.id
            context['receiver'] = receiver
            context['users'] = User.objects.exclude(id=sender.id)
            context['chat_user'] = User.objects.get(id=receiver).first_name
            history = ChatHistory.objects.filter(room=chat_room).order_by('created_on')
            if history:
                context['history'] = history
            else:
                context['history'] = None
            return context
        except ChatRoom.DoesNotExist:
            chat_room = ChatRoom.objects.create(room_name= room, created_by= sender)
            
            context['room_id'] = chat_room.id
            context['history'] = None
            context['receiver'] = receiver
            context['users'] = User.objects.exclude(id=sender.id)
            context['chat_user'] = User.objects.get(id=receiver).first_name
            return context

