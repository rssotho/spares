from django.utils import timezone

from product_management.models import(
    Category,
    CategoryProfile
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
        total_items: int = None,
        product_name: str = None,

    ) -> None:

        # Category
        self.user_id = user_id
        self.file_url = file_url
        self.category_id = category_id
        self.description = description
        self.category_name = category_name
        self.category_profile_id = category_profile_id

        # Product
        self.total_items = total_items
        self.product_name = product_name

    def create_category(self) -> Category:

        category:Category = Category.objects.create(
            date_created = timezone.now(),
            date_modified = timezone.now(),
            description = self.description,
            category_name = self.category_name,
        )

        if not category:

            raise ValueError('Failed to create category, please try again')

        return category

    def get_category(self) -> Category:

        category: Category = Category.objects.filter(
            id = self.category_id
        ).first()

        if not category:

            raise ValueError('The provided category does not exist')

        return category

    def get_user(self) -> User:

        user: User = User.objects.filter(
            id = self.user_id
        ).first()

        if not user:

            raise ValueError('User does not exist')

        return user

    def create_category_profile(self) -> CategoryProfile:

        user_id = self.get_user()
        category_id = self.get_category()

        category_profile: CategoryProfile = CategoryProfile.objects.create(
            file_url = self.file_url,
            category_id = category_id,
            user_id = user_id
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

        category_profile: CategoryProfile = CategoryProfile.objects.filter(
            id = self.category_profile_id
        ).first()

        if not category_profile:

            raise ValueError('Category does not exist')

        return category_profile

    def edit_category_profile(self) -> CategoryProfile:

        category_profile = self.get_category_profile()

        category_profile.file_url = self.file_url
        category_profile.date_modified = timezone.now()





























