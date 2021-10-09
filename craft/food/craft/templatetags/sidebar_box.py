from django import template
from django.db.models import F, Count
from craft.models import Post, PostsCategory, Tag


register = template.Library()


@register.inclusion_tag('craft/post_cat_tpl.html')
def get_post_cat():
    category = PostsCategory.objects.annotate(cnt=Count('posts', filter=F('posts__published_at')))
    return {'category': category}


@register.inclusion_tag('craft/last_post_tpl.html')
def get_last_post(cnt=3):
    posts = Post.objects.order_by('-created_at')[:cnt]
    return {'posts': posts}


@register.inclusion_tag('craft/tags_cloud_tpl.html')
def get_tag_cloud():
    tags = Tag.objects.all()
    return {'tags': tags}

