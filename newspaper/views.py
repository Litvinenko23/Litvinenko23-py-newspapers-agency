from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from newspaper.models import Redactor, Newspaper, Topic


@login_required
def index(request):
    """View function for the home page of the site."""

    num_redactors = Redactor.objects.count()
    num_newspapers = Newspaper.objects.count()
    num_topics = Topic.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_redactors": num_redactors,
        "num_newspapers": num_newspapers,
        "num_topics": num_topics,
        "num_visits": num_visits + 1,
    }

    return render(request, "newspaper/index.html", context=context)


class TopicListView(generic.ListView):
    model = Topic
    template_name = "newspaper/topic_list.html"
    context_object_name = "topic_list"
    queryset = Topic.objects.order_by("name")
    paginate_by = 5


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.select_related("topic")
    paginate_by = 5


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper

