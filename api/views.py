from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
import docker
import collections
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.template.loader import get_template
from django.template import Context, Template
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serialializers import userValidator
from .models import users
from datetime import datetime


client = docker.from_env()
# client = docker.DockerClient(base_url='tcp://35.244.27.235:2375')
now = datetime.now()


@api_view(['GET'])
def apiOverview(request):
    api_urls={
        "/api/":{
          "methotd":"GET",
          "Input":"",
          "Output":"Api Details"  
        },
        "/getimages/":{
          "methotd":"POST",
          "Input":{"user_name":"","token":""},
          "Output":{"error":"True/False","msg":"","data":{
              "name":"image_name"
              }
          }  
        },
        "/startimages/":{
          "methotd":"POST",
          "Input":{"user_name":"",
                   "token":"","image":""},
           "Output":{"error":"True/False",
                     "msg":"","data":{
                              
                                     }
          }  
        },
        "/getcontainers/":{
          "methotd":"POST",
          "Input":{"user_name":"",
                   "token":""},
           "Output":{"error":"True/False",
                     "msg":"","data":{
                                     "id":"container_id",
                                     "state":"container_state",
                                     "image":"image_name",
                                     "name":"container_name"
                                  

                                     }
                    }  
        },
        "/startcontainer/":{
          "methotd":"POST",
          "Input":{"user_name":"",
                   "token":"","image":"",
                   "container_id":"container_id"},
           "Output":{"error":"True/False",
                     "msg":"","data":{
                              
                                     }}
          },
          "/stopcontainer/":{
          "methotd":"POST",
          "Input":{"user_name":"",
                   "token":"","image":"",
                   "container_id":"container_id"},
           "Output":{"error":"True/False",
                     "msg":"","data":{
                              
                                     }}
          } ,
          "/deletecontainer/":{
          "methotd":"POST",
          "Input":{"user_name":"",
                   "token":"","image":"",
                   "container_id":"container_id"},
           "Output":{"error":"True/False",
                     "msg":"","data":{
                              
                                     }}
          }   ,
          "/deletecontainers/":{
          "methotd":"POST",
          "Input":{"user_name":"",
                   "token":"","image":"",
                   },
           "Output":{"error":"True/False",
                     "msg":"","data":{
                              
                                     }}
          }  
        
    }
    
    return Response(api_urls)

@api_view(['POST'])
def getImages(request):
    auth=userValidator(request.data.get('user_name'),request.data.get('token'))
    if auth.get('status'):
        images =[]
        for image in client.images.list():
            dict = collections.OrderedDict()
            dict['name']= str(image).split("'")[1]
            images.append(dict)
            list= json.dumps(images)
        decoded_json = json.loads(list) 
        return Response({"error":False,"msg":auth.get('msg'),"data":decoded_json})
    else:
        # return Response({"msg":"Not Authenticated"})
        
        return Response({"error":True,"msg":auth.get('msg'),"data":"[]"})




@api_view(['POST'])
def startImage(request):
    auth=userValidator(request.data.get('user_name'),request.data.get('token'))
    image=request.data.get('image')
    if image!="":
        user_name=request.data.get('user_name')
        current_time = now.strftime("%H%M%S")
        if auth.get('status'):
            image=request.data.get('image')
            name=user_name +current_time 
            res=client.containers.run(image,detach=True,name=name)
            
            return Response({"error":False,"msg":auth.get('msg'),"data":""})
        else:
            
            return Response({"error":True,"msg":auth.get('msg'),"data":"[]"})
    else:
        return Response({"error":True,"msg":"Please Provide a valid","data":"[]"})

@api_view(['POST'])
def getContainers(request):
    auth=userValidator(request.data.get('user_name'),request.data.get('token'))
    user_name=request.data.get('user_name')
    containers =[]
    if auth.get('status'):
        for container in client.containers.list(all=True):
            container_details = client.containers.get(container.id)
            container_name=container_details.name
            name=container_name[:-6]
            
            if name==user_name:
                dict = collections.OrderedDict()
                dict['id']= container.id
                dict['state'] = container_details.attrs['State']['Status']
                dict['image'] = container_details.attrs['Config']['Image']
                dict['name']=name
                containers.append(dict)
            list= json.dumps(containers)
            decoded_json = json.loads(list) 
        return Response({"error":False,"msg":auth.get('msg'),"data":decoded_json})
    else:
        return Response({"error":True,"msg":auth.get('msg'),"data":"[]"})
        
@api_view(['POST'])
def startContainer(request):
    auth=userValidator(request.data.get('user_name'),request.data.get('token'))
    user_name=request.data.get('user_name')
    container_id=request.data.get('container_id')
    if container_id!="":
        if auth.get('status'):
            container=client.containers.get(container_id)
            container.start()
            return Response({"error":False,"msg":auth.get('msg'),"data":"[]"})
        else:
            return Response({"error":True,"msg":auth.get('msg'),"data":"[]"})
    else:
        return Response({"error":True,"msg":"Please Provide a valid Container id","data":"[]"})

@api_view(['POST'])
def stopContainer(request):
    auth=userValidator(request.data.get('user_name'),request.data.get('token'))
    user_name=request.data.get('user_name')
    container_id=request.data.get('container_id')
    if container_id!="":
        if auth.get('status'):
            
            container=client.containers.get(container_id)
            container.stop()
            return Response({"error":False,"msg":auth.get('msg'),"data":"[]"})
        else:
            return Response({"error":True,"msg":auth.get('msg'),"data":"[]"})
    else:
        return Response({"error":True,"msg":"Please Provide a valid Container id","data":"[]"})



@api_view(['POST'])
def deleteContainer(request):
    auth=userValidator(request.data.get('user_name'),request.data.get('token'))
    user_name=request.data.get('user_name')
    container_id=request.data.get('container_id')
    if container_id!="":
        if auth.get('status'):
            
            container=client.containers.get(container_id)
            container.stop()
            container.remove()
            return Response({"error":False,"msg":auth.get('msg'),"data":"[]"})
        else:
            return Response({"error":True,"msg":auth.get('msg'),"data":"[]"})
    else:
        return Response({"error":True,"msg":"Please Provide a valid Container id","data":"[]"})

@api_view(['POST'])
def deleteContainers(request):
    auth=userValidator(request.data.get('user_name'),request.data.get('token'))
    user_name=request.data.get('user_name')
    
    if auth.get('status'):
        for container in client.containers.list(all=True):
            container_details = client.containers.get(container.id)
            container_name=container_details.name
            name=container_name[:-6]
            
            if name==user_name:
                
                container_details.stop()
                container_details.remove()

                
             
        return Response({"error":False,"msg":auth.get('msg'),"data":""})
    else:
        return Response({"error":True,"msg":auth.get('msg'),"data":"[]"})
    



    
  



