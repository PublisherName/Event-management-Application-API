from django.contrib import admin
from django.db import models
from django_summernote.widgets import SummernoteWidget  # type: ignore


class SummernoteFieldMixin:
    """
    A mixin class that customizes form fields for models with text fields,
    applying the Summernote widget to enable rich text editing.
    """

    formfield_overrides = {
        models.TextField: {"widget": SummernoteWidget()},
    }

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Customize the form field for specific database fields.
        If the field is a TextField, applies the Summernote widget.
        """
        if isinstance(db_field, models.TextField):
            kwargs["widget"] = SummernoteWidget()
        return super().formfield_for_dbfield(db_field, **kwargs)


class SummernoteModelAdmin(SummernoteFieldMixin, admin.ModelAdmin):
    """
    A custom ModelAdmin that uses the SummernoteFieldMixin to apply Summernote
    widgets in the admin, enabling rich text editing for TextFields.
    """

    pass


class SummernoteInlineMixin(SummernoteFieldMixin):
    """
    A mixin for inline admin form to apply the Summernote widget for text
    fields, providing a rich-text editing experience in inline formsets.
    """

    pass
