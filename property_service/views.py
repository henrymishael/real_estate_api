from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Property
from .serializers import PropertySerializer
from django.contrib.postgres.search import SearchVector, SearchQuery

# Create your views here.


class ManagePropertyView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user

            if not user.is_agent:
                return Response(
                    {
                        "error": "User does not have necessary permissions for adding a Property"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            slug = request.query_params.get("slug")

            if not slug:
                property = Property.objects.order_by("-date_created").filter(
                    agent=user.email
                )
                property = PropertySerializer(property, many=True)

                return Response(
                    {"properties": property.data}, status=status.HTTP_200_OK
                )

            if not Property.objects.filter(agent=user.email, slug=slug).exists():
                return Response(
                    {"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND
                )

            property = Property.objects.get(agent=user.email, slug=slug)
            property = PropertySerializer(property)

            return Response({"property": property.data}, status=status.HTTP_200_OK)
        except:
            return Response(
                {
                    "error": "Something went wrong with retrieving property and property details"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve_values(self, data):
        title = data["title"]
        slug = data["slug"]
        address = data["address"]
        city = data["city"]
        state = data["state"]
        zipcode = data["zipcode"]
        description = data["description"]

        price = data["price"]
        try:
            price = int(price)
        except:
            return -1

        sale_type = data["sale_type"]

        if sale_type == "FOR_RENT":
            sale_type = "For Rent"
        else:
            sale_type = "For Sale"

        property_type = data["property_type"]

        if property_type == "HOUSE":
            property_type = "House"
        elif property_type == "APARTMENT":
            property_type = "Apartment"
        else:
            property_type = "Land"

        bedrooms = data["bedrooms"]
        bathrooms = data["bathrooms"]
        main_photo = data["main_photo"]
        photo_1 = data["photo_1"]
        photo_2 = data["photo_2"]
        photo_3 = data["photo_3"]
        is_published = data["is_published"]

        if is_published == "True":
            is_published = True
        else:
            is_published = False

        data = {
            "title": title,
            "slug": slug,
            "address": address,
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "description": description,
            "price": price,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "sale_type": sale_type,
            "property_type": property_type,
            "main_photo": main_photo,
            "photo_1": photo_1,
            "photo_2": photo_2,
            "photo_3": photo_3,
            "is_published": is_published,
        }

        return data

    def post(self, request):
        try:
            user = request.user

            if not user.is_agent:
                return Response(
                    {
                        "error": "User does not have necessary permissions for getting this data"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            data = request.data
            data = self.retrieve_values(data)

            if data == -1:
                return Response(
                    {"error": "Price must be an integer"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            title = data["title"]
            slug = data["slug"]
            address = data["address"]
            city = data["city"]
            state = data["state"]
            zipcode = data["zipcode"]
            description = data["description"]
            price = data["price"]
            bedrooms = data["bedrooms"]
            bathrooms = data["bathrooms"]
            sale_type = data["sale_type"]
            property_type = data["property_type"]
            main_photo = data["main_photo"]
            photo_1 = data["photo_1"]
            photo_2 = data["photo_2"]
            photo_3 = data["photo_3"]
            is_published = data["is_published"]

            if Property.objects.filter(slug=slug).exists():
                return Response(
                    {"error": "Property with this key exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Property.objects.create(
                agent=user.email,
                title=title,
                slug=slug,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
                description=description,
                price=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                sale_type=sale_type,
                property_type=property_type,
                main_photo=main_photo,
                photo_1=photo_1,
                photo_2=photo_2,
                photo_3=photo_3,
                is_published=is_published,
            )

            return Response(
                {"success": "Property created successfully"},
                status=status.HTTP_201_CREATED,
            )

        except:
            return Response(
                {"error": "Something went wrong with creating a property"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request):
        try:
            user = request.user

            if not user.is_agent:
                return Response(
                    {
                        "error": "User does not have necessary permissions for updating this data"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            data = request.data

            data = self.retrieve_values(data)

            if data == -1:
                return Response(
                    {"error": "Price must be an integer"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            title = data["title"]
            slug = data["slug"]
            address = data["address"]
            city = data["city"]
            state = data["state"]
            zipcode = data["zipcode"]
            description = data["description"]
            price = data["price"]
            bedrooms = data["bedrooms"]
            bathrooms = data["bathrooms"]
            sale_type = data["sale_type"]
            property_type = data["property_type"]
            main_photo = data["main_photo"]
            photo_1 = data["photo_1"]
            photo_2 = data["photo_2"]
            photo_3 = data["photo_3"]
            is_published = data["is_published"]

            if not Property.objects.filter(agent=user.email, slug=slug).exists():
                return Response(
                    {"error": "property does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            Property.objects.filter(agent=user.email, slug=slug).update(
                agent=user.email,
                title=title,
                slug=slug,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
                description=description,
                price=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                sale_type=sale_type,
                property_type=property_type,
                main_photo=main_photo,
                photo_1=photo_1,
                photo_2=photo_2,
                photo_3=photo_3,
                is_published=is_published,
            )

            return Response(
                {"success": "Property updated successfully"}, status=status.HTTP_200_OK
            )

        except:
            return Response(
                {"error": "Something went wrong when processing update"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request):
        try:
            user = request.user

            if not user.is_agent:
                return Response(
                    {
                        "error": "User does not have necessary permissions for updating this data"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            data = request.data

            slug = data["slug"]
            is_published = data["is_published"]
            if is_published == "True":
                is_published = True
            else:
                is_published = False

            if not Property.objects.filter(agent=user.email, slug=slug).exists():
                return Response(
                    {"error": "No such property exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            Property.objects.filter(agent=user.email, slug=slug).update(
                is_published=is_published
            )

            return Response(
                {"success": "Published property updated Successfully!"},
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                {"error": "Something went wrong when updateing this property"}
            )

    def delete(self, request):
        try:
            user = request.user

            if not user.is_agent:
                return Response(
                    {
                        "error": "User does not have necessary permissions for deleting this data"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            data = request.data

            try:
                slug = data["slug"]
            except:
                return Response(
                    {"error": "Slug was not provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not Property.objects.filter(agent=user.email, slug=slug).exists():
                return Response(
                    {"error": "Property you are trying to delete does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            Property.objects.filter(agent=user.email, slug=slug).delete()
            if not Property.objects.filter(agent=user.email, slug=slug).exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"error": "Failed to delete property"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except:
            return Response(
                {"error": "Something went wrong when deleting this property"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PropertyDetailView(APIView):
    def get(self, request, format=None):
        try:
            slug = request.query_params.get("slug")

            if not slug:
                return Response(
                    {"error": "Must provide slug"}, status=status.HTTP_400_BAD_REQUEST
                )

            if not Property.objects.filter(slug=slug, is_published=True).exists():
                return Response(
                    {"error": "Published property with this slug does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            property = Property.objects.get(slug=slug, is_published=True)
            property = PropertySerializer(property)

            return Response({"property": property.data}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"error": "Error retrieving property"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PropertyListView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        try:
            if not Property.objects.filter(is_published=True).exists():
                return Response(
                    {"error": "No published properties in this database"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            property = Property.objects.order_by("-date_created").filter(
                is_published=True
            )
            property = PropertySerializer(property, many=True)

            return Response({"properties": property.data}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"error": "Something went wrong with retrieving Property Lists"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SearchPropertyView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        try:
            search = request.query_params.get("search")

            properties = Property.objects.annotate(
                search=SearchVector(
                    "title", "description", "address", "property_type", "price"
                )
            ).filter(search=SearchQuery(search))

            # OR
            # filter(
            # title__search=search,
            # description__search=search,
            # is_published=True,
            # location_search=search)'''

            print("properties:")
            print(properties)
            for property in properties:
                print(property.title)
            return Response({"success": "Data Received"}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"error": "something went wrong when searching for properties"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
