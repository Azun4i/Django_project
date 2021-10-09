from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
# from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *

#этот класс добавляется во время установки CKEditor
# class PostAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorUploadingWidget())

#     class Meta:
#         model = Post
#         fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    # form = PostAdminForm
    prepopulated_fields = {"slug": ("title",)}
    save_on_top = True
    fields = ('title', 'slug', 'category', 'tags', 'content', 'photo', 'get_photo', 'views', 'author',)
    list_display = ('id', 'title', 'slug', 'author', 'created_at', 'get_photo', 'views', 'category')
    list_display_links = ('id', 'title',)
    list_filter = ('created_at', 'tags', 'views', 'category')
    search_fields = ('title', 'content',)
    readonly_fields = ('views', 'created_at', 'get_photo',)

    # Функция нужна для отображения фото в админке
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'
    print(get_photo)
    get_photo.short_description = 'Фото'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title')


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)



admin.site.site_title = 'Терминал'
admin.site.site_header = 'Терминал'
