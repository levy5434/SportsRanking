from django.contrib import admin
from api.models import Team, League, Match, Matchday, MyLeague, Prediction

admin.site.register(Team)
admin.site.register(League)
admin.site.register(Match)
admin.site.register(Matchday)
admin.site.register(MyLeague)
admin.site.register(Prediction)
