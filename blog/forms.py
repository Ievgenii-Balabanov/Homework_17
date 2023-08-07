from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Comment, MyUser, UserPost


class RegisterForm(UserCreationForm):
    about = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = MyUser
        fields = ["username", "email", "password1", "password2"]

#
# class UpdateUserPostForm(forms.Form):
#     title = forms.CharField(max_length=100)


class UpdateUserPostForm(forms.ModelForm):
    # body = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = UserPost
        # fields = ["title", "description"]
        fields = ["title", "content", "status"]


class PostCreateForm(forms.ModelForm):
    # body = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = UserPost
        # fields = ["title", "description"]
        fields = ["title", "content", "status"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', "body"]


class ContactAdminForm(forms.Form):
    from_email = forms.EmailField(required=True)
    name = forms.CharField(max_length=50)
    message = forms.CharField(widget=forms.Textarea)


class ContactUsForm(forms.Form):
    from_email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=35)
    last_name = forms.CharField(max_length=40)
    message = forms.Textarea()


class ContactUsForm(forms.ModelForm):
    publication_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    book_type = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': "custom-select"}),
    )
    #
    # class Meta:
    #     model = Book
    #     fields = ('title', 'publication_date', 'author', 'price', 'pages', 'book_type', )
