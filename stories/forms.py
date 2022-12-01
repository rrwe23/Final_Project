from .models import Stories, StoryComment
from django import forms

class StoriesForm(forms.ModelForm):
    class Meta:
        model = Stories
        fields = ["title","name", "breed", "content", "image"]
        labels = {
            "title": "제목",
            "name": "반려동물 이름",
            "breed": "견종",
            "content": "내용",
            "image": "사진",
        }

class Stories_CommentForm(forms.ModelForm):
    class Meta:
        model = StoryComment
        fields = ["content",]
        labels = {
            "content": "댓글입력",
        }
        widgets = {
            "content": forms.Textarea(attrs={"rows": 1, "cols": 10}),
        }