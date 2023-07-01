from django.urls import path
from graphene_django.views import GraphQLView
from bookings.schema import bookingschema, serviceschema

urlpatterns = [
    path("book/", GraphQLView.as_view(graphiql=True, schema=bookingschema)),
    path("", GraphQLView.as_view(graphiql=True, schema=serviceschema))
]
