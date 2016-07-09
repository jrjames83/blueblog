from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils.text import slugify
from django.views.generic import CreateView
from django.http.response import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, UpdateView
from blog.models import Blog, BlogPost
# Create your views here.


from blog.forms import BlogForm, BlogPostForm



class HomeView(TemplateView):
	template_name = 'home.html'

	#https://docs.djangoproject.com/en/1.9/ref/class-based-views/mixins-simple/
	def get_context_data(self, **kwargs):
		ctx = super(HomeView, self).get_context_data(**kwargs)

		if self.request.user.is_authenticated():
			if Blog.objects.filter(owner=self.request.user).exists():
				ctx['has_blog'] = True
				blog = Blog.objects.get(owner=self.request.user)
				ctx['blog'] = blog
				ctx['blog_posts'] = BlogPost.objects.filter(blog=blog)

		return ctx

class NewBlogView(CreateView):
	form_class = BlogForm
	template_name = 'blog_settings.html'

	def form_valid(self, form):
		blog_obj = form.save(commit=False)
		blog_obj.owner = self.request.user 
		blog_obj.slug = slugify(blog_obj.title)

		blog_obj.save()
		return HttpResponseRedirect(reverse('home'))


	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		user = request.user
		if Blog.objects.filter(owner=user).exists():
			return HttpResponseForbidden("You cannot create more than 1 blog dude")
		else:
			#If the above is not met, dispatch the view to the CreateView
			#methods which will do the get/post type of thing for you
			return super(NewBlogView, self).dispatch(request, *args, **kwargs)


class UpdateBlogView(UpdateView):
	form_class = BlogForm
	template_name = 'blog_settings.html'
	#success_url = '/'
	model = Blog

	#self.kwargs would have anything dynamic
	def get_success_url(self):
		return "/" 

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(UpdateBlogView, self).dispatch(request, *args, **kwargs)



class NewBlogPostView(CreateView):
	form_class = BlogPostForm
	template_name = 'blog_post.html'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(NewBlogPostView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		blog_post_obj = form.save(commit=False)
		blog_post_obj.blog = Blog.objects.get(owner=self.request.user)
		blog_post_obj.slug = slugify(blog_post_obj.title)
		blog_post_obj.is_published = True

		blog_post_obj.save()

		return HttpResponseRedirect(reverse('home'))






