from django.shortcuts import render, redirect
from django.views import *
from django.views.generic.edit import *
from .models import *
from .forms import *
from django.http import Http404
from django.contrib.auth.mixins import *
from django.contrib.auth.models import *
from django.contrib.auth import (authenticate, login, logout)
from django.core.urlresolvers import reverse_lazy
# from django.contrib import messages
# from django.contrib.messages import get_messages

class Login(FormView):

    template_name = 'login.html'
    # form_class in FormView !
    form_class = Login

    def get_success_url(self):
        # find your next url here
        # here method should be GET or POST.
        next_url = self.request.GET.get('next')
        if next_url:
            success_url = next_url
            return success_url  # you can include some query strings as well
        else:
            # success_url = '/accounts/login/'
            success_url = reverse_lazy('login')
            return success_url  # what url you wish to return'

    def form_valid(self, form):
        user_login = form.cleaned_data["login"]
        password = form.cleaned_data["password"]
        user = authenticate(username=user_login, password=password)
        if user is not None:
            login(self.request, user)
        return super(Login, self).form_valid(form)


class Logout(FormView):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('login'))


class MainPage(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def get(self, request):
        message = []
        total_likes = []
        liked_photos_list = []
        # photos = Photo.objects.order_by('-creation_date')\
        #                       .filter(my_user=request.user)
        photos = Photo.objects.order_by('-creation_date').all()
        # get all likes for each photo
        for photo in photos:
            total_likes.append([Like.objects.
                               filter(photo_id=photo.id).count(), photo.id])

        # query set of Likes objects for logged user
        likes = (Like.objects.filter(user_id=request.user.id))
        for like in likes:
            # photo.id -> field in Likes table
            liked_photos_list.append(like.photo.id)
        # like_user_list = Like.objects.filter()

        context = {
            "title": "Main Page",
            "photos": photos,  # all photos list
            "message": message,  # additional message
            "total_likes": total_likes,  # total likes for each photo
            "liked_photos": liked_photos_list,  # photos liked by logged user
        }
        return render(request, "main_page.html", context)

    def post(self, request):
        # if user clicked "like" or "dislike"
        photo_id = request.POST.get('photo_id')
        social_action = int(request.POST.get('social_action'))
        # if user clicked "like" button
        if social_action:
            # creation of new Like object
            photo = Photo.objects.get(pk=photo_id)
            Like.objects.get_or_create(user=request.user, photo=photo)
        # if user clicked "dislike" button
        else:
            like_obj = Like.objects.filter(user=request.user,
                                           photo_id=photo_id)
            like_obj.delete()
        return redirect(reverse_lazy('main-page'))


class AddUser(FormView):
    template_name = 'add_user.html'
    form_class = AddUserForm
    success_url = reverse_lazy('add-user')

    def form_valid(self, form):
        # takes data from the form
        username = form.cleaned_data['username']
        # first_name = form.cleaned_data['first_name']
        # last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        pass1 = form.cleaned_data['password']
        pass2 = form.cleaned_data['password_retype']

        if pass1 != pass2:
            form = AddUserForm
            # (self.request.POST)
            return render(self.request, 'add_user.html',
                          {'message': 'Pass1 and Pass2 do not match!',
                           'form': form})

        try:  # check if login isn't already taken by someone else
            if User.objects.get(username=username):
                return render(self.request, 'add_user.html',
                              {'message': 'Login taken!', 'form': form})

        except ObjectDoesNotExist:
            # if there is no user with such login - creating is possible
            pass
        # User class has it's own method for creating new user
        # ->.create_user
        User.objects.create_user(username=username, email=email,
                                 password=pass1)
        return super(AddUser, self).form_valid(form)


class AddPhoto(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def get(self, request):
        form = AddPhotoForm()
        context = {"form": form}
        return render(request, "add_photo.html", context)

    def post(self, request):
        form = AddPhotoForm(request.POST, request.FILES)

        if form.is_valid():
            server_path = form.cleaned_data['server_path']
            disk_file = form.cleaned_data['disk_file']
            # XOR for input fields
            if not ((server_path and not disk_file) or
                    (not server_path and disk_file)):
                raise forms.ValidationError('Please fill only one '
                                            'of the fields.')

            if server_path:
                # create and save Photo Model!
                new_photo = Photo.objects.create(path=server_path,
                                                 file="Server_path",
                                                 my_user=request.user)
                new_photo.save()
                context = {
                    'message': 'Photo path added!',
                    'form': form,
                }
            if disk_file:
                # save files
                new_photo = Photo.objects.create(path="File_path",
                                                 file=disk_file,
                                                 my_user=request.user)
                new_photo.save()
                context = {
                    'message': 'Photo file added!',
                    'form': form,
                }

        # if form not valid
        else:
            context = {
                'message': 'Form not valid!',
                'form': form,
            }
        return render(request, "add_photo.html", context)


class UserInfo(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def get(self, request):
        logged_user = request.user
        photos = Photo.objects.filter(my_user_id=logged_user.id)
        context = {
            'user': logged_user,
            'photos': photos,
        }
        return render(request, "user_info.html", context)


class UpdateUser(LoginRequiredMixin, View):
    def get(self, request, pk):
        raise Http404("You posted in wrong neighborhood!")

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        return redirect(reverse_lazy('user-info'))


class PhotoInfo(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def get(self, request, photo_id):
        photo = Photo.objects.get(pk=photo_id)
        comments = Comment.objects.filter(photo_id=photo.id)\
                                  .order_by('created')

        context = {
            'photo': photo,
            'comments': comments,
        }
        return render(request, "photo_info.html", context)

    def post(self, request, photo_id):
        comment = request.POST.get('text_field')
        # photo_id = request.POST.get('photo_id')
        photo = Photo.objects.get(pk=photo_id)
        Comment.objects.create(text=comment, user=request.user, photo=photo)
        return redirect(reverse_lazy('photo-info',
                                     kwargs={'photo_id': photo_id}))

