from datetime import datetime

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id', )
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError('Неверный год произведения')
        return value


class TitleInfoSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = '__all__'
        model = Title


# class FollowSerializer(serializers.ModelSerializer):
#    user = SlugRelatedField(
#        read_only=True,
#        slug_field='username',
#        default=serializers.CurrentUserDefault()
#    )
#    following = SlugRelatedField(
#        queryset=User.objects.all(),
#        slug_field='username', read_only=False,
#    )

#    class Meta:
#        fields = '__all__'
#        model = Follow
#        validators = [
#            UniqueTogetherValidator(
#                queryset=Follow.objects.all(),
#                fields=['user', 'following']
#            )
#        ]

#    def validate_following(self, data):
#        if data == self.context.get('request').user:
#            raise serializers.ValidationError(
#                'Попытка подписаться на самого себя'
#            )
#        return data


# class PostSerializer(serializers.ModelSerializer):
#    author = SlugRelatedField(slug_field='username', read_only=True)

#    class Meta:
#        fields = '__all__'
#        model = Post
