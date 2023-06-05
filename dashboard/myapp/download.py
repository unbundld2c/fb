import csv
from django.http import HttpResponse
import json

def download_csv(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data = json.loads(data)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'

        writer = csv.writer(response)
        writer.writerow(data[0].keys())  # Write header row

        for row in data:
            writer.writerow(row.values())

        return response
    else:
        return HttpResponse(status=400)
