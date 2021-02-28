from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Category, Comment, Genre, Review, Title, User


class CreateUserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.CharField(
        required=False,
        default=None,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        fields = ('email', 'username')
        model = User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'first_name', 'last_name',
                  'username', 'bio', 'email', 'role')
        model = User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class ReadTitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title


class WriteTitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="slug",
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field="slug",
        queryset=Genre.objects.all(),
    )

    def create(self, validated_data):
        title = Title.objects.create(
            name=validated_data.get("name"),
            year=validated_data.get("year"),
            description=validated_data.get("description"),
            category=validated_data.get("category"),
        )
        title.genre.set(validated_data.get("genre"))

        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.year = validated_data.get("year", instance.year)
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.category = validated_data.get("category", instance.category)
        if validated_data.get("genre"):
            instance.genre.set(validated_data.get("genre"))
        instance.save()

        return instance

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="username")

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review

    def validate(self, attrs):
        is_exist = Review.objects.filter(
            author=self.context["request"].user,
            title=self.context["view"].kwargs.get("title_id"),
        ).exists()
        if is_exist and self.context["request"].method == "POST":
            raise serializers.ValidationError("Отзыв у автора уже существует")
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="username")

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment
