from django.http import Http404
from django.shortcuts import render

from .page_registry import LANDING_PAGES


def landing_detail(request, slug):
    page_config = LANDING_PAGES.get(slug)
    if not page_config:
        raise Http404("Landing page not found.")

    context = {
        "page": {
            **page_config,
            "slug": slug,
        }
    }
    return render(request, page_config["template_name"], context)

