from django.shortcuts import render, get_object_or_404, redirect
from .models import Stories, StoryComment, Image
from .forms import StoriesForm, Stories_CommentForm, ImageForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    stories = Stories.objects.order_by("-created_at")
    image = Image.objects.order_by("-pk")
    page = request.GET.get('page', '1')
    paginator = Paginator(stories, 10)
    page_obj = paginator.get_page(page)
    context = {
        "stories": page_obj,
        "story": stories,
        "image":image
    }
    return render(request, "stories/index.html", context)

@login_required
def create(request):
    if request.method == "POST":
        form = StoriesForm(request.POST, request.FILES)
        image_form = ImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        if form.is_valid() and image_form.is_valid():
            stories = form.save(commit=False)
            stories.user = request.user 
            if len(images):
                for image in images:
                    image_instance = Image(articles=stories, image=image)
                    stories.save()
                    image_instance.save()
            else:
                stories.save()
            return redirect("stories:index")
    else:
        form = StoriesForm()
    context = {
        "form": form
    }
    return render(request, "stories/create.html", context)

def detail(request, pk):
    stories = get_object_or_404(Stories, pk=pk)
    comment_form = Stories_CommentForm()
    comments = stories.storycomment_set.order_by('-created_at')
    context = {
        "stories": stories,
        "comment_form": comment_form,
        "comments": comments,
    }
    stories.hits +=1
    stories.save()
    return render(request, "stories/detail.html", context)

@login_required
def update(request, pk):
    stories = get_object_or_404(Stories, pk=pk)
    if request.user == stories.user:
        if request.method == "POST":
            stories_form = StoriesForm(request.POST, request.FILES, instance=stories)
            if stories_form.is_valid():
                stories_form.save()
                return redirect("stories:detail", stories.pk)
        else:
            stories_form = StoriesForm(instance=stories)
        context = {
            "stories_form": stories_form,
        }
        return render(request, "stories/update.html", context)

@login_required
def delete(request, pk):
    Stories.objects.get(pk=pk).delete()
    return redirect("stories:index")

@login_required
def comment_create(request, stories_pk):
    stories = get_object_or_404(Stories, pk=stories_pk)
    comment_form = Stories_CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.stories = stories
        comment.user = request.user
        comment.save()
        return redirect('stories:detail', stories_pk)

@login_required
def comment_delete(request, stories_pk, storycomment_pk):
    comment = StoryComment.objects.get(pk=storycomment_pk)
    if comment.user == request.user:
        comment.delete()
    return redirect('stories:detail', stories_pk)
    
@login_required
def likes(request, stories_pk):
    stories=get_object_or_404(Stories, pk=stories_pk)
    if stories.like.filter(pk=request.user.pk).exists():
        stories.like.remove(request.user)
        is_liked = False
    else:
        stories.like.add(request.user)
        is_liked = True
    context = {
        "is_liked": is_liked,
    }
    return JsonResponse(context)

@login_required
def comment_likes(request, storycomment_pk):
    comment = get_object_or_404(StoryComment, pk=storycomment_pk)
    if comment.like.filter(pk=request.user.pk).exists():
        comment.like.remove(request.user)
    else:
        comment.like.add(request.user)
    return redirect('stories:detail', comment.stories.pk)
