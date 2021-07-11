from django.contrib import admin
from .models import Ticket, QuestionAndAnswer


class AnswerAdminInline(admin.TabularInline):
    model = QuestionAndAnswer
    fields = ('description', 'user','question')


@admin.register(Ticket)
class TicketAdminInline(admin.ModelAdmin):
    fields = ('title', 'user', 'status')
    list_display = ('title', 'user', 'status')
    inlines = (AnswerAdminInline,)


admin.register(Ticket, TicketAdminInline)
