from datetime import datetime
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title,  Review, Comment #User
#TODO заменить далее User на CustomUser
from users.models import CustomUser

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
    rating = serializers.FloatField() #TODO в предыдущем сериалайзере рейтинг вроде не нужен? 
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = '__all__'
        # fields = ('id', 'name', 'description', 'category',
        #     'genre', 'year', 'rating')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
#    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Comment


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(max_length=5, required=True)

    class Meta:
        model = CustomUser
        fields = ['confirmation_code', 'username']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']
