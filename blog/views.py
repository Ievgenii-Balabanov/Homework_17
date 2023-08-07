from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages import get_messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator

from django.views import generic

from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import cache_page

from blog.forms import RegisterForm, ContactAdminForm, ContactUsForm

from blog.models import MyUser, UserPost, Comment
from core.settings import NOREPLY_EMAIL
from . import tasks
from .tasks import send_email, send_email_to_admin, contact_email
from .forms import CommentForm


def index(request):
    return render(request, "index.html")


class RegisterFormView(generic.FormView):
    template_name = "registration/registration.html"
    form_class = RegisterForm
    success_url = reverse_lazy("blog:index")

    def form_valid(self, form):
        user = form.save()

        user = authenticate(self.request, username=user.username, password=form.cleaned_data.get("password1"))
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UserProfile(LoginRequiredMixin, generic.DetailView):
    model = MyUser
    template_name = "registration/user_profile.html"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class PublicUserProfileDetailView(generic.DetailView):
    model = MyUser
    template_name = "blog/public_user_profile.html"


class AllUserProfileListView(generic.ListView):
    model = MyUser
    template_name = "blog/all_user_profiles.html"
    paginate_by = 2
    queryset = MyUser.objects.all()


class UpdateProfileView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = MyUser
    template_name = "registration/update_profile.html"
    fields = ["first_name", "last_name", "email"]
    success_url = reverse_lazy("profile")
    success_message = "Your profile was successfully updated!"

    def get_object(self, queryset=None):
        user = self.request.user
        return user

    def get_success_url(self):
        return reverse_lazy("blog:public_profile", kwargs={"pk": self.object.pk})


class WritePostView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = UserPost
    # fields = ["title", "description", "body"]
    fields = ["title", "summary", "content", "status", "image"]
    success_url = reverse_lazy("blog:post_detail")
    success_message = "Your post has been created and awaits approval!"

    def form_valid(self, formset):
        instance = formset.save(commit=False)
        instance.author = self.request.user
        send_email.apply_async(
            kwargs={
                "subject": "New Post Notification",
                "message": "New Post is created",
                "from_email": "test@test.com",
                },
        )
        send_email_to_admin.apply_async(
            kwargs={
                "subject": "New Post Admin Notification",
                "message": loader.render_to_string(
                    "blog/admin_html_post_message.html", {"message": "message"},
                ),
                "from_email": "test@test.com",
            },
        )
        return super().form_valid(formset)

    def get_success_url(self):
        return reverse_lazy("blog:post_detail", kwargs={'pk': self.object.pk})


class UserPostUpdateView(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, generic.UpdateView):
    model = UserPost
    fields = ["title", "content", "status"]
    template_name = "blog/update_userpost_form.html"
    permission_required = "blog.can_update_post"
    success_url = reverse_lazy("blog:post_detail")
    success_message = "Your post has been successfully updated!"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        obj = queryset.get()
        return obj

    def form_valid(self, formset):
        instance = formset.save(commit=False)
        instance.author = self.request.user
        if instance:
            send_email.apply_async(
                kwargs={
                    "subject": "Update Post Notification",
                    "message": "Your post was successfully updated!",
                    "from_email": "test@test.com",
                    },
            )
            return super().form_valid(formset)

    def get_success_url(self):
        # return reverse_lazy("blog:post_detail", kwargs={'pk': self.object.pk})
        return reverse_lazy("blog:post_detail", kwargs={'pk': self.kwargs.get("pk")})


@method_decorator(cache_page(15), "get")
class AllPostsListView(generic.ListView):
    model = UserPost
    template_name = "blog/all_user_posts_list.html"
    paginate_by = 5
    queryset = UserPost.objects.filter(status=1)


class PostedPostByUserListView(LoginRequiredMixin, generic.ListView):
    model = UserPost
    template_name = "blog/userpost_list.html"
    paginate_by = 8
    # queryset = UserPost.objects.filter(status=1)

    def get_queryset(self):
        return UserPost.objects.filter(author=self.request.user)


class UserPostDetailView(generic.DetailView):
    model = UserPost
    template_name = "blog/post_detail.html"
    context_object_name = "userpost"
    # queryset = UserPost.objects.all()
    queryset = UserPost.objects.select_related("author")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["form"] = CommentForm()
    #     return context
    #
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm(initial={"name": self.request.user.username})
        comments_list = self.object.comments.all()
        paginator = Paginator(comments_list, 4)
        page = self.request.GET.get("page")
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        context["comments"] = comments
        return context


def add_comment(request, pk):
    post = get_object_or_404(UserPost, pk=pk)
    comments = Comment.objects.filter(pk=pk)
    new_comment = None
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            send_email.apply_async(
                kwargs={
                    "subject": "New Comment User Notification",
                    "message": loader.render_to_string(
                        "blog/user_html_message.html", {"post": post}, request
                    ),
                    "from_email": "test@test.com",
                },
            )
            send_email_to_admin.apply_async(
                kwargs={
                    "subject": "New Comment Admin Notification",
                    "message": loader.render_to_string(
                        # "blog/admin_html_comment_message.html", {"message": "message"}, request
                        "blog/admin_html_comment_message.html", {"post": post}, request
                    ),
                    "from_email": "test@test.com",
                },
            )
            messages.success(
                request, "Your comment is successfully created and awaiting moderation")
            new_comment.save()
            return redirect(reverse("blog:post_detail", kwargs={'pk': pk}))

    else:
        form = CommentForm()
        return render(request, 'blog/comments_form.html', {'post': post, 'comments': comments,
                                                           'new_comment': new_comment, 'form': form,
                                                           'messages': get_messages(request)})


def contact_admin(request):
    if request.POST:
        form = ContactAdminForm(request.POST)
        if form.is_valid():
            send_email.apply_async(
                kwargs={
                    "subject": "Reminder",
                    "message": loader.render_to_string(
                        "blog/contact_admin_message.html", {"message": form.cleaned_data["message"]}, request
                    ),
                    "from_email": form.cleaned_data["from_email"],
                },
            )
            return redirect(reverse("blog:index"))
    else:
        form = ContactAdminForm()
    return render(request, "blog/contact_admin.html", context={"form": form})


# def contact_us(request, form, template):
#     data = {}
#     if request.POST:
#         if form.is_valid:
#             form.save()
#             data["form_is_valid"] = True
#             data["html_contact_us"] = render_to_string("blog/contact_admin_message.html",
#                                                        {"message": form.cleaned_data["message"]}, request)
#             send_email.apply_async(
#                 kwargs={
#                     "subject": "Reminder",
#                     "message": loader.render_to_string(
#                         "blog/contact_admin_message.html", {"message": form.cleaned_data["message"]}, request
#                     ),
#                     "from_email": form.cleaned_data["from_email"],
#                 },
#             )
#             data['form_is_valid'] = True
#             data['html_book_list'] = render_to_string('blog/includes/contact_us_form.html', {"form": form})
#         else:
#             data['form_is_valid'] = False
#
#     context = {"form": form}
#     data["html"] = render_to_string(template, context, request=request)
#     return JsonResponse(data)


def contact_us(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            contact_email.apply_async(
                form.cleaned_data.get("subject"),
                form.cleaned_data.get("message"),
                form.cleaned_data["from_email"],
            )
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def contact(request):
    if request.POST:
        form = ContactUsForm(request.POST)
    else:
        form = ContactUsForm()
    return contact_us(request, form, "blog/includes/contact_us_form.html")
