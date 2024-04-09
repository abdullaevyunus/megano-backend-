from rest_framework import serializers
from .models import Product, Review, Image, Tag, Specification, Category, Subcategory, Sales, Order, OrderProduct, \
    Profile, Payment, Basket
from django.contrib.auth.models import User


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('src', 'alt')


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ('name', 'value')


class SubcategorySerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Subcategory
        fields = ('id', 'title', 'image')


class CategorySerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'subcategories')
from .models import Product, Review


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    specifications = SpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class SalesSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Sales
        fields = ('id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images')


class OrderProductPOSTSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = '__all__'

    def get_reviews(self, obj):
        return obj.reviews.count


class OrderProductGETSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = (
            'id', 'category', 'price', 'count', 'date', 'title', 'description', 'freeDelivery', 'images', 'tags',
            'reviews',
            'rating',)

    def get_reviews(self, obj):
        return obj.reviews.count()


class OrderGETSerializer(serializers.ModelSerializer):
    products = OrderProductGETSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'createdAt', 'fullName', 'email', 'phone', 'deliveryType', 'paymentType', 'totalCost', 'status', 'city', 'address', 'products', )


class OrderPOSTSerializer(serializers.ModelSerializer):
    products = OrderProductGETSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
        'id', 'createdAt', 'fullName', 'email', 'phone', 'deliveryType', 'paymentType', 'totalCost', 'status', 'city',
        'address', 'products',)




class ProfileSerializer(serializers.ModelSerializer):
    avatar = ImageSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['fullName', 'email', 'phone', 'avatar']


class ChangePasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(max_length=100)
    newPassword = serializers.CharField(max_length=100)


class ChangeAvatarSerializer(serializers.ModelSerializer):
    avatar = ImageSerializer()

    class Meta:
        model = Profile
        fields = ['avatar']


class UserRegistrationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, source='first_name')
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('name', '')
        )
        return user


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(write_only=True, required=True)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('order', 'number', 'name', 'month', 'year', 'code')


class BasketPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ['id', 'count']


class BasketGetSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        return obj.reviews.count()

    class Meta:
        model = Product
        fields = (
            'id', 'category', 'price', 'count', 'date', 'title', 'description', 'freeDelivery', 'images', 'tags',
            'reviews',
            'rating')
