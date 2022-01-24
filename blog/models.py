from django import forms, template
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (FieldPanel, MultiFieldPanel)
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

class BlogIndexPage(Page):
    
    def get_context(self, request):
        context = super(BlogIndexPage, self).get_context(request)
        all_articles = BlogArticle.objects.live().public().order_by('-first_published_at')
        paginator = Paginator(all_articles, 4)

        page = request.GET.get("page")
        
        try:
            # If the page exists and the ?page=x is an int
            articles = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            articles = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            articles = paginator.page(paginator.num_pages)

        context['articles'] = articles
        return context




class BlogArticle(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Imagen del articulo.'
    )
    body = RichTextField(blank=True)
    categories = ParentalManyToManyField("blog.BlogCategory")

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('body', classname="full"),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading = "Categories"
        )
    ]

class BlogCategory(models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel("name")
    ]

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

register_snippet(BlogCategory)
