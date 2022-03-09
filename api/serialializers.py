from dataclasses import field
from rest_framework import serializers
from .models import users


def userValidator(user_name,token):
    usr = users.objects.filter(user_name=user_name).exists()
    if usr:
      dictionary = users.objects.filter(user_name=user_name).values()[0]
      if usr and dictionary["tocken"] == token:
       return({"msg":"Authenticated",'status':True})
      else:
        return({"msg":"Not Authenticated Token",'status':False})
    return({"msg":"Not Authenticated user",'status':False})
