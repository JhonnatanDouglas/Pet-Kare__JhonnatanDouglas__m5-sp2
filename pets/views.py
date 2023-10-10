from rest_framework.views import Request, Response, APIView, status
from rest_framework.pagination import PageNumberPagination
from .models import Pet
from .serializers import PetSerializer
from groups.models import Group
from traits.models import Trait
from django.shortcuts import get_object_or_404


class PetView(APIView, PageNumberPagination):
    def get(self, req: Request) -> Response:
        trait = req.query_params.get("trait", None)

        if trait:
            all_pets = Pet.objects.filter(traits__name=trait)
        else:
            all_pets = Pet.objects.all()

        result = self.paginate_queryset(all_pets, req)
        pet_serializer = PetSerializer(result, many=True)

        return self.get_paginated_response(pet_serializer.data)

    def post(self, req: Request) -> Response:
        pet_serializer = PetSerializer(data=req.data)

        pet_serializer.is_valid(raise_exception=True)

        group_data = pet_serializer.validated_data.pop("group")
        traits_data_list = pet_serializer.validated_data.pop("traits")

        this_pet_created = Pet.objects.create(**pet_serializer.validated_data)

        try:
            group = Group.objects.get(
                scientific_name__iexact=group_data["scientific_name"]
            )
        except Group.DoesNotExist:
            group = Group.objects.create(**group_data)

        this_pet_created.group = group
        this_pet_created.save()

        for trait_data in traits_data_list:
            try:
                trait = Trait.objects.get(name__iexact=trait_data["name"])
            except Trait.DoesNotExist:
                trait = Trait.objects.create(**trait_data)
            this_pet_created.traits.add(trait)

        pet_serializer = PetSerializer(this_pet_created)

        return Response(pet_serializer.data, status.HTTP_201_CREATED)


class PetDetailView(APIView):
    def get(self, req: Request, pet_id: int) -> Response:
        founded_pet = get_object_or_404(Pet, pk=pet_id)
        serializer = PetSerializer(founded_pet)
        return Response(serializer.data)

    def patch(self, req: Request, pet_id: int) -> Response:
        founded_pet = get_object_or_404(Pet, pk=pet_id)
        serializer = PetSerializer(data=req.data, partial=True)

        serializer.is_valid(raise_exception=True)

        founded_pet.name = serializer.validated_data.get("name", founded_pet.name)
        founded_pet.age = serializer.validated_data.get("age", founded_pet.age)
        founded_pet.weight = serializer.validated_data.get("weight", founded_pet.weight)
        founded_pet.sex = serializer.validated_data.get("sex", founded_pet.sex)

        group_data = serializer.validated_data.get("group")
        traits_data = serializer.validated_data.get("traits")

        if group_data:
            try:
                group = Group.objects.get(
                    scientific_name__iexact=group_data["scientific_name"]
                )
            except Group.DoesNotExist:
                group = Group.objects.create(**group_data)
            founded_pet.group = group

        if traits_data:
            founded_pet.traits.clear()
            for trait_data in traits_data:
                try:
                    trait = Trait.objects.get(name__iexact=trait_data["name"])
                except Trait.DoesNotExist:
                    trait = Trait.objects.create(**trait_data)
                founded_pet.traits.add(trait)

        founded_pet.save()

        serializer = PetSerializer(founded_pet)
        return Response(serializer.data)

    def delete(self, req: Request, pet_id: int) -> Response:
        founded_pet = get_object_or_404(Pet, pk=pet_id)
        founded_pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
