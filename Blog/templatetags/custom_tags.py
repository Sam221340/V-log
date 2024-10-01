import calendar
import datetime

from django import template
from django.template.loader import render_to_string

from Blog.models import Post

register = template.Library()

# @register.inclusion_tag('archive.html')
# def show_archive():
#     post = Post.objects.all().values('created_at__month').distinct()
#     list1 = []
#     for i in post:
#         print(i['created_at__month'])
#         a = Post.objects.filter(created_at__month=i['created_at__month']).count()
#         print(a)
#         list1.append({'month':i['created_at__month'],'count':a})
#
#
#     return {'post': list1}

@register.inclusion_tag('archive.html')
def show_archive():
    posts_by_month = []
    for i in Post.objects.all().values('created_at__month', 'created_at__year').distinct():
        month_number = i['created_at__month']
        year = i['created_at__year']
        month_name = calendar.month_name[month_number]


        # Add month_number to the dictionary
        posts_by_month.append({'month': month_number, 'month_name': month_name, 'year': year, 'post_count': Post.objects.filter(created_at__month=month_number, created_at__year=year).count()})

    return {'posts_by_month': posts_by_month}
