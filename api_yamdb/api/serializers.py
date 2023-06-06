from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, User, Review, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField()

    class Meta:
        fields = '__all__'
        # fields = ('id', 'name', 'description', 'category',
        #     'genre', 'year', 'rating')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
#    author = SlugRelatedField(slug_field='username', read_only=True)

    # title_id = self.context['view'].kwargs.get('title_id')
    # print ('titleid', title_id)
    # rating = serializers.FloatField()
    class Meta:
        fields = '__all__'

        model = Review


class CommentSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(
    #     read_only=True, slug_field='username'
    # )
    # review = serializers.ReadOnlyField(source="post_id")

    class Meta:
        fields = '__all__'
        model = Comment


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
