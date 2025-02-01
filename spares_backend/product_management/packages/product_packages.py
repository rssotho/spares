from django.utils import timezone

from product_management.models import(
    Product,
    Category,
    ProductProfile,
    CategoryProfile,
)
from system_management.models import User


class ProductManagenentPackages:

    def __init__(
        self,

        # Category
        file_url: str = None,
        user_id: User = None,
        description: str = None,
        category_name: str = None,
        category_id: Category = None,
        category_profile_id: CategoryProfile = None,

        # Product
        price: float = None,
        product_id: int = None,
        total_items: int = None,
        product_name: str = None,
        product_profile_id: int = None,

    ) -> None:

        # Category
        self.user_id = user_id
        self.file_url = file_url
        self.category_id = category_id
        self.description = description
        self.category_name = category_name
        self.category_profile_id = category_profile_id

        # Product
        self.price = price
        self.product_id = product_id
        self.total_items = total_items
        self.product_name = product_name
        self.product_profile_id = product_profile_id

    def get_user(self) -> User:

        user: User = User.objects.get(
            id = self.user_id
        )

        if not user:

            raise ValueError('User does not exist')

        return user

    def create_category(self) -> Category:

        user = self.get_user()

        category:Category = Category.objects.create(
            user_id = user.id,
            date_created = timezone.now(),
            date_modified = timezone.now(),
            description = self.description,
            category_name = self.category_name,
        )

        if not category:

            raise ValueError('Failed to create category, please try again')

        return category

    def get_category(self) -> Category:

        category: Category = Category.objects.get(
            id = self.category_id
        )

        if not category:

            raise ValueError('The provided category does not exist')

        return category

    def create_category_profile(self) -> CategoryProfile:

        category_id = self.get_category()

        category_profile: CategoryProfile = CategoryProfile.objects.create(
            file_url = self.file_url,
            category_id = category_id.id,
            date_created = timezone.now(),
            date_modified = timezone.now(),
        )

        if not category_profile:

            raise ValueError('Failed to create the upload category profile')

        return category_profile

    def edit_category(self) -> Category:

        category = self.get_category()

        category.category_name = self.category_name
        category.description = self.description
        category.date_modified = timezone.now()

        category.save()

        return category

    def get_category_profile(self) -> CategoryProfile:

        category_profile: CategoryProfile = CategoryProfile.objects.get(
            id = self.category_profile_id
        )

        if not category_profile:

            raise ValueError('Category does not exist')

        return category_profile

    def edit_category_profile(self) -> CategoryProfile:

        category_profile = self.get_category_profile()

        category_profile.file_url = self.file_url
        category_profile.date_modified = timezone.now()

        category_profile.save()

        return category_profile

    def create_product(self) -> Product:

        user = self.get_user()
        category = self.get_category()

        product: Product = Product.objects.create(
            user_id = user.id,
            price = self.price,
            category = category,
            date_created = timezone.now(),
            date_modified = timezone.now(),
            description = self.description,
            total_items = self.total_items,
            product_name = self.product_name,
        )

        if not product:

            raise ValueError('Failed to create product, please try again')

        return product

    def get_products(self) -> Product:

        products = Product.objects.get(
            id = self.product_id
        )

        if not products:

            raise ValueError('No products found')

        return products

    def edit_product(self) -> Product:

        product = self.get_products()

        product.price = self.price
        product.product_name = self.product_name
        product.description = self.description
        product.total_items = self.total_items
        product.date_modified = timezone.now()

        product.save()

        return product

    def view_categories(self) -> Category:

        category: Category = Category.objects.all()

        return category

    def view_products(self) -> Product:

        products: Product = Product.objects.all()

        return products

    def create_product_profile(self) -> ProductProfile:

        product: Product = self.get_products()

        product_profile: ProductProfile = ProductProfile.objects.create(
            product_id = product.id,
            file_url = self.file_url,
            date_created = timezone.now(),
            date_modified = timezone.now(),
        )

        if not product_profile:

            raise ValueError('Failed to create the upload product profile')

        return product_profile

    def get_product_profile(self) -> ProductProfile:

        product_profile: ProductProfile = ProductProfile.objects.get(
            id = self.product_profile_id
        )

        if not product_profile:

            raise ValueError('Product does not exist')

        return product_profile
















