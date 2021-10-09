from django import template
from blog.models import Tag, Post

register = template.Library()


# выводим группу популярных постов в шаблоне single
@register.inclusion_tag('blog/popular_posts_tpl.html')
def get_popular(cnt=3):
    posts = Post.objects.order_by('-views')[:cnt]
    return {'posts': posts}


# выводим группу тегов в шаблоне single
@register.inclusion_tag('blog/tags_tpl.html')
def get_tags():
    tags = Tag.objects.all()
    return {'tags': tags}