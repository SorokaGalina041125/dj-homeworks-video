from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        
        main_count = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_main'):
                    main_count += 1
        
        if main_count == 0:
            raise ValidationError('Выберите хотя бы один основной раздел')
        if main_count > 1:
            raise ValidationError('Не может быть больше одного основного раздела')


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1
    ordering = ['-is_main', 'tag__name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at']
    list_filter = ['published_at']
    search_fields = ['title']
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ['article', 'tag', 'is_main']
    list_filter = ['is_main']
    search_fields = ['article__title', 'tag__name']