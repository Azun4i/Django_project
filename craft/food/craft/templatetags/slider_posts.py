from django import template
from craft.models import Post


register = template.Library()


@register.inclusion_tag('craft/slider_post.html')
def get_slider_post(cnt=3):
    posts = Post.objects.filter(bonusactions=True)[:cnt]
    return {'posts': posts}



