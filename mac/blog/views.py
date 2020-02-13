from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Blogpost

# Create your views here.
def index(request):
	all_blogs = Blogpost.objects.order_by('-pub_date')
	return render(request, 'blog/index.html',{'blogs':all_blogs})
def blogpost(request, id):
	prev_id = id -1
	next_id = id +1
	post = Blogpost.objects.filter(post_id = id)[0]
	prev = Blogpost.objects.filter(post_id = id)
	if len(Blogpost.objects.filter(post_id = prev_id)):
		prev_blog = Blogpost.objects.filter(post_id = prev_id)[0]
	else:
		prev_blog = {}
	if len(Blogpost.objects.filter(post_id = next_id)):
		next_blog = Blogpost.objects.filter(post_id = next_id)[0]
	else:
		next_blog = {}	
	print(prev_blog)
	print(next_blog)	
	return render(request, 'blog/blogpost.html',{'post':post,'next_blog':next_blog,'prev_blog':prev_blog})
