from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

# from ckeditor_uploader.widgets import CKEditorUploadingWidget


from .models import *


# class PostAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorUploadingWidget())

#     class Meta:
#         model = Post
#         fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    # form = PostAdminForm
    prepopulated_fields = {'slug': ('title',)}
    fields = (('title', 'slug'), ('category', 'sort_id', 'tags'), 'content', 'photo',  ('published_at', 'bonusactions'))
    list_display = ('id', 'slug', 'title', 'category', 'published_at', 'bonusactions', 'get_photo', 'views')
    list_display_links = ('title', 'category',)
    list_editable = ('published_at', 'bonusactions',)
    list_filter = ('category', 'tags')
    search_fields = ('title', 'content', 'created_at')
    readonly_fields = ('views', 'created_at')
    save_on_top = True
    save_as = True
    # fieldsets = (
    #     ('Просмотры', {
    #         'classes': ("collapse",),
    #         'fields': (('views',))
    #
    #     }),
    # )

    # показываем фотку в админке
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(F'<img src="{obj.photo.url}" width="75">')
        return '-'
    get_photo.short_description = 'Фото'


class PostsCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title')
    list_display_links = ('title',)
    save_on_top = True
    save_as = True


class MenuCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title')
    list_display_links = ('title',)
    save_on_top = True
    save_as = True


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title')
    list_display_links = ('title',)
    save_on_top = True
    save_as = True


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True
    save_as = True
    fields = (('title', 'slug', 'sort_id'), ('category', 'tags'), ('composition', 'price'), 'photo', 'published',)
    list_display = ('id', 'slug', 'title', 'category', 'published', 'sort_id', 'get_photo', 'updated_at', 'created_at',)
    list_display_links = ('id', 'title', 'category')
    list_editable = ('published', 'sort_id',)
    search_fields = ('title', 'composition', )

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(F'<img src="{obj.photo.url}" width="75">')
        return '-'
    get_photo.short_description = 'Фото'


admin.site.site_title = 'Терминал Craft'
admin.site.site_header = 'Терминал Craft'

admin.site.register(Post, PostAdmin)
admin.site.register(PostsCategory, PostsCategoryAdmin)
admin.site.register(MenuCategory, MenuCategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Product, ProductAdmin)
# admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
# admin.site.register(Comment)
