from django.contrib import admin
from .models import Ticket, Answare


class AnswerAdminInline(admin.TabularInline):
    model = Answare
    fields = ('description', 'user')


@admin.register(Ticket)
class TicketAdminInline(admin.ModelAdmin):
    fields = ('title', 'description', 'user', 'status')
    list_display = ('title', 'description', 'user', 'status')
    inlines = (AnswerAdminInline,)


admin.register(Ticket, TicketAdminInline)
