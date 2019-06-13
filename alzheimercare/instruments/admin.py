from django.contrib import admin

# Register your models here.
from .models import Instrument, Afirmation, Option, InstrumentAnswer, Answers, InstrumentRank

class OptionAdmin(admin.ModelAdmin):
    model = Option
    extra = 1
    list_display = ('option', 'value')

class AfirmationAdmin(admin.StackedInline):
    model = Afirmation
    extra = 1
    list_display = ('text')

class InstrumentAmdin(admin.ModelAdmin):
    fields = ['name','status','is_complex']
    inlines = [AfirmationAdmin]
    list_display = ('name', 'status')

admin.site.register(Instrument, InstrumentAmdin)
admin.site.register(Option, OptionAdmin)
admin.site.register(InstrumentAnswer)
admin.site.register(Answers)
admin.site.register(InstrumentRank)

