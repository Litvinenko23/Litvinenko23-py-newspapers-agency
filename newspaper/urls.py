from django.urls import path

from newspaper.views import (
    index,
    TopicListView,
    NewspaperListView,
    NewspaperDetailView,
    NewspaperCreateView,
    NewspaperUpdateView,
    NewspaperDeleteView,
    # RedactorDeleteView,
    TopicCreateView,
    TopicUpdateView,
    TopicDeleteView,
)


urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("topics/create/",
         TopicCreateView.as_view(),
         name="topic-create",
    ),
    path("topics/<int:pk>/update/",
         TopicUpdateView.as_view(),
         name="topic-update",
    ),
    path("topics/<int:pk>/delete/",
         TopicDeleteView.as_view(),
         name="topic-update",
    ),

    path(
        "newspapers/",
        NewspaperListView.as_view(),
        name="newspaper-list",
    ),
    path(
        "newspapers/<int:pk>/",
        NewspaperDetailView.as_view(),
        name="newspaper-detail",
    ),
    path("newspapers/create/",
         NewspaperCreateView.as_view(),
         name="newspaper-create",
    ),
    path(
        "newspapers/<int:pk>/update/",
        NewspaperUpdateView.as_view(),
        name="newspaper-update",
    ),
    path(
        "newspapers/<int:pk>/delete/",
        NewspaperDeleteView.as_view(),
        name="redactor-delete",
    ),
]

app_name = "newspaper"
