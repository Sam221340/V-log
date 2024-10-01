from django import forms
from Blog.models import Category, Tag

category_choices = Category.objects.all().values_list('id','name')



class PostBlogForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    description = forms.CharField(label="Description",widget=forms.Textarea)
    category = forms.CharField(label="Category",widget=forms.Select(choices=category_choices))
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    # active = forms.BooleanField(required=False)
    image = forms.ImageField()
    author_image = forms.ImageField(label="Your photo")
    author = forms.CharField(label="User",widget=forms.HiddenInput,required=False)

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

