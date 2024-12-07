from django.contrib.admin import SimpleListFilter

from events.models.category import Category


class ActiveCategoryFilter(SimpleListFilter):
    title = "Active Category"
    parameter_name = "category"

    def lookups(self, request, model_admin):  # noqa: PLR6301
        active_categories = Category.objects.filter(is_active=True).order_by("name")
        return [(category.id, category.name) for category in active_categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__id=self.value())
        return queryset
