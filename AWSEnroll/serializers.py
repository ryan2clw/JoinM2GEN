from .models import Project
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.utils.field_mapping import get_nested_relation_kwargs

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('project_set', 'username','id')
        read_only_fields = ('username','id')

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['name', 'id', 'owner']

class ProjectMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['name', 'members', 'owner']
        depth = 2

    def build_nested_field(self, field_name, relation_info, nested_depth):
        """
        Create nested fields for forward and reverse relationships.
        """
        class NestedSerializer(serializers.ModelSerializer):
            class Meta:
                model = relation_info.related_model
                depth = nested_depth - 1
                fields = ['username']

        field_class = NestedSerializer
        field_kwargs = get_nested_relation_kwargs(relation_info)

        return field_class, field_kwargs
