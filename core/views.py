from django.shortcuts import render
from django.views.generic import TemplateView
from products.models import Product

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Show the latest added products first so new admin uploads appear on the homepage immediately
        context['featured_products'] = Product.objects.filter(available=True).order_by('-created')[:8]
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'

class ContactView(TemplateView):
    template_name = 'core/contact.html'