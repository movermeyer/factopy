from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, \
    PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from factopy.models import BackendModel, Worker, Machine, Cluster, TagManager, \
    Stream, MaterialStatus, Material, Process, ProcessOrder, ComplexProcess, \
    Filter, Collect, Adapt
from django.forms import ModelForm


class BackendModelChildAdmin(PolymorphicChildModelAdmin):
    base_model = BackendModel


class BackendModelAdmin(PolymorphicParentModelAdmin):
    base_model = BackendModel
    list_filter = (PolymorphicChildModelFilter,)
    child_models = (
        (Worker, BackendModelChildAdmin),
        (Machine, BackendModelChildAdmin),
        (Cluster, BackendModelChildAdmin),
    )


class TagManagerAdmin(admin.ModelAdmin):
    list_display = ['tag_string']


class StreamAdmin(admin.ModelAdmin):
    list_display = ['unprocessed_count', 'created', 'modified']


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


class ProcessInlineForm(ModelForm, object):
    class Meta(object):
            model = ProcessOrder
            fields = ['position', 'process']


class ProcessOrderInline(admin.TabularInline):
    form = ProcessInlineForm
    model = ProcessOrder
    fk_name = 'complex_process'
    extra = 0  # how many rows to show
    ordering = ["position", "process__name"]


class ComplexProcessChildAdmin(ProcessChildAdmin):
    list_display = ['name', 'description']
    inlines = [ProcessOrderInline]
    search_fields = ['name', 'description', ]


class ProcessAdmin(PolymorphicParentModelAdmin):
    base_model = Process
    list_filter = (PolymorphicChildModelFilter,)
    child_models = (
        (ComplexProcess, ComplexProcessChildAdmin),
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
