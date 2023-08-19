from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

User = get_user_model()

# Create your views here.


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            data = request.data

            name = data["name"]
            email = data["email"]
            email = email.lower()
            password = data["password"]
            re_password = data["re_password"]
            is_agent = data["is_agent"]

            if is_agent == "True":
                is_agent = True
            else:
                is_agent = False

            if password == re_password:
                if len(password) >= 8:
                    if not User.objects.filter(email=email).exists():
                        if not is_agent:
                            User.objects.create_user(
                                name=name, email=email, password=password
                            )

                            return Response(
                                {"success": "User created Successfully"},
                                status=status.HTTP_201_CREATED,
                            )
                        else:
                            User.objects.create_agent(
                                name=name, email=email, password=password
                            )

                            return Response(
                                {"success": "Agent created successfully"},
                                status=status.HTTP_201_CREATED,
                            )

                    else:
                        return Response(
                            {"error": "User with this email already exists"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                else:
                    return Response(
                        {"error": "Password must be at least 8 characters in length"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        except:
            return Response(
                {
                    "error": "Something went wrong when registering an account",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RetrieveUserView(APIView):
    # permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)

            return Response(
                {
                    "user": user.data,
                },
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                {"error": "Something went wrong when retrieving user details"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AgentListView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        try:
            if not User.objects.filter(is_agent=True).exists():
                return Response(
                    {"error": "No agents in this database"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            agents = User.objects.filter(is_agent=True)
            agent = UserSerializer(agents, many=True)

            return Response({"Agents": agent.data}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"error": "Something went wrong with retrieving Agent Lists"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
