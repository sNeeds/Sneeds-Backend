from sNeeds.apps.estimation.analyze.models import Chart, ChartItemData
from random import randint

gpa = 11.0
chart, created = Chart.objects.get_or_create(title=Chart.ChartTitle.GRADE_POINT_AVERAGE)

while gpa < 20:
    t = randint(5, 10)
    obj, created = ChartItemData.objects.get_or_create(chart=chart, label=str(gpa),
                                                       defaults={'count': t})

    gpa += 0.25



