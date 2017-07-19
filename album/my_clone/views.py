from django.shortcuts import render, redirect
from django.views import *
from django.views.generic.edit import *
from .models import *
from .forms import *
from django.contrib.auth.mixins import *
from django.contrib.auth.models import *
from django.contrib.auth import (authenticate, login, logout)
#
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
            success_url = '/login/'
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
        return redirect('/login')


class MainPage(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        message = []
        total_likes = []
        liked_photos_list = []
        # photos = Photo.objects.order_by('-creation_date')\
        #                       .filter(my_user=request.user)

        photos = Photo.objects.order_by('-creation_date').all()

        # if user clicked "like"
        photo_id = request.GET.get('photo_id')
        if photo_id:
            # creation of new Like object
            photo = Photo.objects.get(pk=photo_id)
            new_like, created = Like.objects.get_or_create(user=request.user,
                                                            photo=photo)
            if not created:
                message.append(["Already liked!", photo_id])
            else:
                # if created -> OK
                pass

        # get all likes for each photo
        for photo in photos:
            total_likes.append([Like.objects.
                               filter(photo_id=photo.id).count(), photo.id])

        # query set of Likes objects for logged user
        likes = (Like.objects.filter(user_id=request.user.id))
        for like in likes:
            # photo.id -> field in Likes table
            liked_photos_list.append(like.photo.id)

        # wez liste wszystkich zdjec ktore lubi zalogowany user,
        # sprawdzaaj kazde zdjecie - jezeli user je lubi, dopisz do
        # wiadomosci id zdjecia oraz wiadomosc "lubisz to"
        # like_user_list = Like.objects.filter()

        context = {
            "title": "Main Page",
            "photos": photos,  # all photos list
            "message": message,  # additional message
            "total_likes": total_likes,  # total likes for each photo
            "liked_photos": liked_photos_list,  # photos liked by logged user
        }
        return render(request, "main_page.html", context)


class AddUser(FormView):
    template_name = 'add_user.html'
    form_class = AddUserForm
    success_url = '/add_user/'

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
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        form = AddPhotoForm()
        context = {"form": form}
        return render(request, "add_photo.html", context)

    def post(self, request):
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            server_path = form.cleaned_data['server_path']
            # disk_file = form.cleaned_data['disk_file']
            # if not ((server_path and not disk_file) or
            #         (not server_path and disk_file)):
                # raise forms.ValidationError('Please fill one of the fields.')
                # context = {
                #     'message': 'Please fill only one of the fields.',
                #     'form': form,
                # }

            context = {
                'message': 'Photo added!',
                'form': form,
            }
            # create and save Photo Model!
            new_photo = Photo.objects.create(path=server_path,
                                             my_user=request.user)
            new_photo.save()
        else:
            context = {
                'message': 'Form not valid!',
                'form': form,
            }

        return render(request, "add_photo.html", context)


class UserInfo(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        logged_user = request.user
        photos = Photo.objects.filter(my_user_id=logged_user.id)
        context = {
            'user': logged_user,
            'photos': photos,
        }
        return render(request, "user_info.html", context)


class UpdateUser(UpdateView):
    model = User
    template_name = "user_update_form.html"
    fields = ['first_name', 'last_name', "email"]
    success_url = '/user_info'
    

class PhotoInfo(LoginRequiredMixin, View):
    login_url = '/login/'
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
        return redirect('/photo_info/' + photo_id)





