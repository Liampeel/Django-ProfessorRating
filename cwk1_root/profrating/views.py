import json

from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Empty, Sum
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from decimal import *

from json import loads, dumps
from .serializers import ModuleInstanceSerializer, ModuleSerializer, ProfessorSerializer, RatingSerializer
from .models import ModuleInstance, Module, Professor, Rating


class ModuleInstanceViewSet(viewsets.ModelViewSet):
    queryset = ModuleInstance.objects.all().order_by('module')
    serializer_class = ModuleInstanceSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all().order_by('module_code')
    serializer_class = ModuleSerializer


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


@csrf_exempt
@require_http_methods(["GET"])
def GetProfessors(request):
    profs = Professor.objects.all()
    data = ProfessorSerializer(profs, many=True).data
    return JsonResponse(data, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def GetRating(request):
    rating = Rating.objects.all()

    data = RatingSerializer(rating, many=True).data
    obj = loads(dumps(data))

    print(obj)
    return JsonResponse(data, safe=False)


@csrf_exempt
def moduleAvgRating(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.body is not None:
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                professorID = body['professor']
                module_code = body['module']
                rating = Rating.objects.all()

                data = RatingSerializer(rating, many=True).data
                obj = loads(dumps(data))

                moduleName = Module.objects.get(module_code=module_code)
                professorName = Professor.objects.get(professor_id=professorID)



                count = 0
                total = 0
                jsonFinish = []
                for i in obj:
                    professor = (i['professor'])
                    rating = (i['rating'])

                    if str(professor) == str(professorID):
                        if str(module_code) == str((i['module'])):
                            print(i)
                            count += 1
                            total += rating

                RatingValue = total / count
                decimalRating = Decimal(str(RatingValue)).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
                print(decimalRating)

                response = "The Rating of Professor "
                String = ""
                for j in range(int(decimalRating)):
                    String += "*"

                response += (str(professorName))
                modResponse = " In Module " + (str(moduleName))
                response += modResponse
                decimalResponse = " is "
                decimalResponse += (str(String))
                response += decimalResponse
                jsonFinish.append(response)
                return JsonResponse(jsonFinish, safe=False)
            return HttpResponse('error Invalid request' , status=400)
        return HttpResponse('error wrong request mothod', status=400)

    return HttpResponse('Not logged in', status=400)


@csrf_exempt
@require_http_methods(["GET"])
def overallAvgRating(request):
    if request.user.is_authenticated:
        professor = Professor.objects.all()
        data = ProfessorSerializer(professor, many=True).data
        profobj = loads(dumps(data))

        profes = []
        for i in profobj:
            profes.append(i['professor_id'])

        jsonFinish = []

        for i in profes:
            jsonarray = []
            count = 0
            filter = Rating.objects.filter(professor=i).aggregate(Sum('rating'))['rating__sum']
            filter2 = Rating.objects.filter(professor=i).values('rating')

            jsonarray.append(filter2)
            rateobj = loads(dumps(filter))

            data = list(filter2.values())
            for j in data:
                count += 1

            RatingValue = rateobj / count
            decimalRating = Decimal(str(RatingValue)).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
            print(decimalRating)
            response = "The Rating of Professor "
            String = ""
            for j in range(int(decimalRating)):
                String += "*"

            response += (str(i))
            decimalResponse = " is "
            decimalResponse += (str(String))
            response += decimalResponse
            jsonFinish.append(response)
            print(response)
        return JsonResponse(jsonFinish, safe=False)

    return HttpResponse('Not logged in', status=400)


@csrf_exempt
def postRating(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.body is not None:
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                professorName = body['professor']
                module_input = body['module']
                yearInput = body['year']
                semester = body['semester']
                ratingValue = body['rating']

                module = Module.objects.get(module_code=module_input)
                profquery = Professor.objects.get(professor_id=professorName)

                instance = ModuleInstance.objects.filter(module_id=module_input, year=yearInput, semester=semester,
                                                         professor=profquery)
                if instance.exists():
                    modQuery = module
                    yearQuery = yearInput
                    semesterQuery = semester
                    professorQuery = profquery

                    RatingData = Rating(rating=ratingValue, professor=professorQuery, module=modQuery, year=yearQuery,
                                        semester=semesterQuery)
                    RatingData.save()

                    return HttpResponse("Posted Rating")
                return HttpResponse("Not valid post", status=400)
            return HttpResponse('Not valid post', status=400)
        return HttpResponse('error wrong request mothod', status=400)
    return HttpResponse('Not logged in', status=400)


@csrf_exempt
@require_http_methods(["GET"])
def GetModule(request):
    if request.user.is_authenticated:
        module = Module.objects.all()
        data = ModuleSerializer(module, many=True).data
        return JsonResponse(data, safe=False)

    return HttpResponse("invalid login" , status=400)


@csrf_exempt
@require_http_methods(["GET"])
def GetModuleInstance(request):
    if request.user.is_authenticated:
        moduleinstance = ModuleInstance.objects.all()
        data = ModuleInstanceSerializer(moduleinstance, many=True).data
        return JsonResponse(data, safe=False)

    return HttpResponse("invalid login", status=400)


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        if request.body is not None:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            username = body['username']
            email = body['email']
            password = body['password']

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return HttpResponse('The account: ' + username + ' has been successfully created', status=200)
        else:
            return HttpResponse('Invalid request', status=400)


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        if request.body is not None:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            username = body['username']
            password = body['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponse("Successfully logged in")
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")

            return HttpResponse("Invalid login details given")
    return HttpResponse("Invalid login details given")


@csrf_exempt
def logout_request(request):
    logout(request)
    print(request, "Logged out successfully!")
    return HttpResponse("Logged out successfully")
