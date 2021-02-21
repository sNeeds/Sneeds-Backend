import unicodecsv
from abroadin.base.django.contrib.admin.utils import lookup_field, lookup_field_support_nested
from django.http import HttpResponse


def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True, file_name=None, multi_row_field=None):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """

    def export_as_csv(modeladmin, request, queryset, *args, **kwargs):
        opts = modeladmin.model._meta

        if not fields:
            field_names = [field.name for field in opts.fields]
        else:
            field_names = fields

        response = HttpResponse(content_type='text/csv')
        res_file_name = file_name if file_name else str(opts).replace('.', '_')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % res_file_name

        writer = unicodecsv.writer(response, encoding='utf-8')
        if header:
            writer.writerow(field_names)
        for obj in queryset:
            row = dict()
            for field in field_names:
                _, _, value = lookup_field_support_nested(field, obj, modeladmin)
                row[field] = value

            if multi_row_field is not None:
                multi_row_field_value = row.pop(multi_row_field)
                base_row_values = list(row.values())
                if multi_row_field_value:
                    for t in multi_row_field_value:
                        writer.writerow(base_row_values + [t])
                else:
                    writer.writerow(base_row_values + [])
            else:
                writer.writerow(list(row.values()))

        return response

    export_as_csv.short_description = description

    return export_as_csv
