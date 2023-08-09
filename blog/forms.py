from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Comment, MyUser, UserPost


class RegisterForm(UserCreationForm):
    about = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = MyUser
        fields = ["username", "email", "password1", "password2"]


class UpdateUserPostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ["title", "content", "status"]


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ["title", "content", "status"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "body"]


class ContactAdminForm(forms.Form):
    from_email = forms.EmailField(required=True)
    name = forms.CharField(max_length=50)
    message = forms.CharField(widget=forms.Textarea)


class ContactUsForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_from_email(self):
        data = self.cleaned_data["from_email"]

        if data.strip().endswith("mail.ru"):
            # raise ValidationError(_("We can't send email on mail.ru emails"))
            raise ValidationError(_("Incorrect! Choose another domain name instead of 'mail.ru'"))
        return data

    def clean(self):
        email = self.cleaned_data["from_email"]
        subject = self.cleaned_data["subject"]

        if email.endswith("gmail.com") and "spam" in subject.lower():
            self.add_error(None, "Can't send spam emails")
