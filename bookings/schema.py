import graphene
import datetime
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import Service, Booking
from users.models import ExtendUser

class BookingType(DjangoObjectType):
    class Meta:
        model = Booking
        fields = ('id', 'quantity', 'price', 'user', 'service', 'status', 'created_at', 'updated_at')

class ServiceType(DjangoObjectType):
    class Meta:
        model = Service
        fields = ('id', 'name', 'price', 'created_at', 'updated_at')


class ServiceQuery(graphene.ObjectType):
    all_services = graphene.List(ServiceType)

    def resolve_all_services(root, info):
        return Service.objects.all()


class BookingQuery(graphene.ObjectType):    
    all_bookings = graphene.List(BookingType)

    def resolve_all_bookings(root, info, **kwargs):
        return Booking.objects.all()

class CreateBookingMutation(graphene.Mutation):
    class Arguments:
        quantity = graphene.Int(required=True)
        user = graphene.Int(required=True)
        service = graphene.Int(required=True)

    booking = graphene.Field(BookingType)
    @classmethod
    @login_required
    def mutate(cls, root, info, quantity, user, service):
        if info.context.user is not None:
            service = Service.objects.filter(id=service).first()
            user = ExtendUser.objects.filter(id=user).first()
            price = quantity*service.price
            booking = Booking(
                quantity=quantity,
                price=price,
                user=user,
                service=service,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            )
            booking.save()
            return CreateBookingMutation(booking=booking)


class UpdateBookingStatusMutation(graphene.Mutation):
    class Arguments:
        bookingid = graphene.Int(required=True)
        new_status = graphene.String(required=True)

    booking = graphene.Field(BookingType)
    @classmethod
    @login_required
    def mutate(cls, root, info, bookingid, new_status):
        existing = Booking.objects.get(id=bookingid)
        existing.status = new_status
        existing.save()
        booking = Booking.objects.get(id=bookingid)
        return UpdateBookingStatusMutation(booking=booking)

class Mutation(graphene.ObjectType):
    create_booking = CreateBookingMutation.Field() 
    update_status = UpdateBookingStatusMutation.Field()

bookingschema = graphene.Schema(query=BookingQuery, mutation=Mutation)
serviceschema = graphene.Schema(query=ServiceQuery)