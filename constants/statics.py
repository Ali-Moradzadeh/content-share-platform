from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class SimpleViewSet(viewsets.ViewSet):
    list_filtering = {}
    list_serializer_class = None
    retrieve_serializer_class = None
    create_serializer_class = None
    update_serializer_class = None
    full_update_serializer_class = None
    partial_update_serializer_class = None
    
    
    def _get_model(self):
        return self.serializer_class.Meta.model
    
    def _get_model_manager(self):
        return self._get_model()._meta.default_manager
    
    def get_queryset(self):
        intersections = set(self.list_filtering.keys()) & set(self.request.query_params.keys())
        intersection_dict = {}
        for i in intersections:
            intersection_dict[self.list_filtering[i]] = self.request.query_params[i] 
        return self.queryset.filter(**intersection_dict)
        
    def list(self, request):
        srz_cls = self.list_serializer_class or self.serializer_class
        srz = srz_cls(instance=self.get_queryset(), many=True)
        return Response(srz.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        instance = get_object_or_404(self._get_model(), pk=pk)
        srz_cls = self.retrieve_serializer_class or self.serializer_class
        srz = srz_cls(instance=instance)
        return Response(srz.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        srz_cls = self.create_serializer_class or self.serializer_class
        srz = srz_cls(data=request.data)
        if srz.is_valid():
            srz.save()
            return Response(srz.data, status=status.HTTP_201_CREATED)
        return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk):
        instance = self._get_model_manager().get(pk=pk)
        srz_cls = self.partial_update_serializer_class or self.serializer_class
        srz = srz_cls(instance=instance, data=request.data, partial=True)
        if srz.is_valid():
            srz.save()
            return Response(srz.data, status=status.HTTP_200_OK)
        return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request, pk):
        instance = get_object_or_404(self._get_model(), pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


SPECIAL_CHARACTERS = ('?', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+')

INITIAL_USERS = [
    {
        "username": "ali",
        "email": "ali@gmail.com",
        "password": "Ali1111?",
        "phone_number": "09000000000",
        "is_staff": True,
        "is_superuser": True,
    },
    {
        "username": "zari",
        "email": "zahra@gmail.com",
        "password": "Zahra1111?",
        "phone_number": "09111111111",
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "amir",
        "email": "amir@gmail.com",
        "password": "Amir1111?",
        "phone_number": "09222222222",
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "sina",
        "email": "sina@gmail.com",
        "password": "Sina1111?",
        "phone_number": "09333333333",
        "is_staff": False,
        "is_superuser": False,
    },
]
