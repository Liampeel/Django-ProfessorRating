from rest_framework import serializers
from .models import Professor, ModuleInstance, Module, Rating


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['module_code', 'module_name']


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['professor_id', 'name']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['professor', 'module', 'year', 'semester', 'rating']


class ModuleInstanceSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer(many=True)
    module = ModuleSerializer(many=False)

    class Meta:
        model = ModuleInstance
        fields = ['module', 'year', 'semester', 'professor']
