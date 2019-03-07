from django.contrib import admin

# Register your models here.
from .models import Instrument, Afirmation, Option

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1

class AfirmationAdmin(admin.StackedInline):
    model = Afirmation
    extra = 1
    list_display = ('text')
    

class InstrumentAmdin(admin.ModelAdmin):
    fields = ['name','status']
    inlines = [AfirmationAdmin]
    list_display = ('name', 'status')

admin.site.register(Instrument, InstrumentAmdin)
admin.site.register(Option)
