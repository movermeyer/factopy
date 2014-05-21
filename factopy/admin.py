from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, \
    PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from factopy.models import BackendModel, Node, TagManager, Stream, \
    MaterialStatus, Material, Process, Filter, Collect, Adapt


class BackendModelChildAdmin(PolymorphicChildModelAdmin):
    base_model = BackendModel


class BackendModelAdmin(PolymorphicParentModelAdmin):
    base_model = BackendModel
    list_filter = (PolymorphicChildModelFilter,)
    child_models = (
        (Node, BackendModelChildAdmin),
    )


class TagManagerAdmin(admin.ModelAdmin):
    list_display = ['tag_string']


class StreamAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'unprocessed_count', 'created', 'modified']


class MaterialChildAdmin(PolymorphicChildModelAdmin):
    base_model = Material


class MaterialAdmin(PolymorphicParentModelAdmin):
    base_model = Material
    list_filter = (PolymorphicChildModelFilter,)
    child_models = (
        (Material, MaterialChildAdmin),
    )


class MaterialStatusAdmin(admin.ModelAdmin):
    list_display = ['stream', 'material']


class ProcessChildAdmin(PolymorphicChildModelAdmin):
    base_model = Process


class ProcessAdmin(PolymorphicParentModelAdmin):
    base_model = Process
    list_filter = (PolymorphicChildModelFilter,)
    child_models = (
        (Filter, ProcessChildAdmin),
        (Collect, ProcessChildAdmin),
        (Adapt, ProcessChildAdmin),
    )


admin.site.register(BackendModel, BackendModelAdmin)
admin.site.register(TagManager, TagManagerAdmin)
admin.site.register(Stream, StreamAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(MaterialStatus, MaterialStatusAdmin)
admin.site.register(Process, ProcessAdmin)
