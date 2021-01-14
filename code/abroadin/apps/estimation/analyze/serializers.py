from django.db.models import F, Sum
from rest_framework import serializers

import abroadin.apps.estimation.form.models as form_models
import abroadin.apps.data.applydata.models as ad_models
from abroadin.apps.estimation.analyze.models import ChartItemData


def get_unchanged_chart_items(qs):
    data = dict()
    for obj in qs:
        item = data[obj.label] = data.get(obj.label, {})
        item['count'] = item.get('count', 0) + obj.count
        item['percent'] = item.get('percent', 0) + obj.percent
    return data


def get_converted_chart_items(qs, label_convert_function, data_number=None):
    data = dict()
    for obj in qs:
        view_label = label_convert_function(obj.label)
        item = data[view_label] = data.get(view_label, {})
        item['count'] = item.get('count', 0) + obj.count
        item['percent'] = item.get('percent', 0) + obj.percent
        # item['percent'] = item.get('percent', 0.0) + obj.count / data_number
    return data


def get_store_to_view_labels(store_labels, label_convert_function=None):
    if label_convert_function is None:
        return store_labels

    view_labels = []
    if store_labels is not None:
        for label in store_labels:
            view_labels.append(label_convert_function(label))
    return view_labels


def get_user_status(user_positions, items_qs, compare_func, store_to_view_convert_func=None):
    if user_positions is None or len(user_positions) == 0:
        return None

    data = dict()
    worse_cases_count = 0
    worse_cases_percent = 0.0

    user_best_position_label = user_positions[0]
    for position in user_positions:
        user_best_position_label = compare_func(user_best_position_label, position)

    for obj in items_qs:
        if compare_func(user_best_position_label, obj.label) == user_best_position_label and \
                user_best_position_label != obj.label:
            worse_cases_count += obj.count
            worse_cases_percent += obj.percent
    if store_to_view_convert_func is None:
        data['user_best_position_label'] = user_best_position_label
    else:
        data['user_best_position_label'] = store_to_view_convert_func(user_best_position_label)
    data['worse_cases_count'] = worse_cases_count
    data['worse_cases_percent'] = worse_cases_percent
    return data


# class ChartItemDataSerializer(serializers.Serializer):
#     label = serializers.CharField(source='label')
#     count = serializers.IntegerField(source='count')
#     percent = serializers.FloatField(source='percent')
#
#     class Meta:
#         fields = [
#             'label',
#             'count',
#             'percent',
#         ]
#
#     def update(self, instance, validated_data):
#         pass
#
#     def create(self, validated_data):
#         pass


class CommonChartSerializer(serializers.Serializer):
    class Meta:
        fields = [
            'chart_items', 'user_positions', 'data_number',
        ]

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class GradePointAverageChartSerializer(CommonChartSerializer):

    def save(self, **kwargs):
        self._data = dict()
        chart = self.instance
        qs = ChartItemData.objects.filter(chart=chart)
        data_number = qs.aggregate(Sum('count')).get('count__sum')
        if data_number == 0.0:
            data_number = 1.0
        items_qs = ChartItemData.objects.filter(chart=chart).annotate(percent=F('count') / data_number)
        user_store_based_positions = self.get_user_positions(chart)

        self._data['title'] = chart.title

        self._data['label_range'] = form_models.Education.GPA_VIEW_LABEL_RANGE

        self._data['chart_items'] = self.get_chart_items(items_qs)

        self._data['user_positions'] = \
            get_store_to_view_labels(user_store_based_positions,
                                     form_models.Education.convert_gpa_store_to_view_label)

        self._data['data_number'] = data_number

        self._data['user_status'] = get_user_status(user_store_based_positions,
                                                    items_qs,
                                                    form_models.Education.compare_gpa_labels)

    def get_chart_items(self, qs):
        return get_converted_chart_items(qs,
                                         form_models.Education.convert_gpa_store_to_view_label
                                         )

    def get_user_positions(self, obj):
        sdi_id = self.context.get('student_detailed_info', None)
        if sdi_id is not None:
            try:
                sdi = form_models.StudentDetailedInfo.objects.get(id=sdi_id)
                return form_models.Education.get_gpa_user_store_based_positions(sdi)
            except form_models.StudentDetailedInfo.DoesNotExist:
                return None
        return None


class PublicationsCountChartSerializer(CommonChartSerializer):

    def save(self, **kwargs):
        self._data = dict()
        chart = self.instance
        qs = ChartItemData.objects.filter(chart=chart)
        data_number = qs.aggregate(Sum('count')).get('count__sum')
        if data_number == 0.0:
            data_number = 1.0
        items_qs = ChartItemData.objects.filter(chart=chart).annotate(percent=F('count') / data_number)
        user_store_based_positions = self.get_user_positions(chart)
        self._data['title'] = chart.title

        self._data['label_range'] = None

        self._data['chart_items'] = self.get_chart_items(items_qs)

        self._data['user_positions'] = \
            get_store_to_view_labels(user_store_based_positions,
                                     form_models.Publication.convert_count_chart_store_to_view_label)

        self._data['data_number'] = data_number

        self._data['user_status'] = get_user_status(user_store_based_positions,
                                                    items_qs,
                                                    form_models.Publication.compare_publication_count_labels)

    def get_chart_items(self, qs):
        return get_converted_chart_items(qs,
                                         form_models.Publication.convert_count_chart_store_to_view_label)

    def get_user_positions(self, obj):
        sdi_id = self.context.get('student_detailed_info', None)
        if sdi_id is not None:
            try:
                sdi = form_models.StudentDetailedInfo.objects.get(id=sdi_id)
                return form_models.Publication.get_publication_count_user_store_based_positions(
                    sdi)
            except form_models.StudentDetailedInfo.DoesNotExist:
                return None
        return None


class PublicationTypeChartSerializer(CommonChartSerializer):

    def save(self, **kwargs):
        self._data = dict()
        chart = self.instance
        qs = ChartItemData.objects.filter(chart=chart)
        data_number = qs.aggregate(Sum('count')).get('count__sum')
        if data_number == 0.0:
            data_number = 1.0
        items_qs = ChartItemData.objects.filter(chart=chart).annotate(percent=F('count') / data_number)
        user_store_based_positions = self.get_user_positions(chart)
        self._data['title'] = chart.title

        self._data['label_range'] = None

        self._data['chart_items'] = self.get_chart_items(items_qs)

        self._data['user_positions'] = \
            get_store_to_view_labels(user_store_based_positions,
                                     )

        self._data['data_number'] = data_number

        self._data['user_status'] = None

    def get_chart_items(self, qs):
        return get_unchanged_chart_items(qs)

    def get_user_positions(self, obj):
        sdi_id = self.context.get('student_detailed_info', None)
        if sdi_id is not None:
            try:
                sdi = form_models.StudentDetailedInfo.objects.get(id=sdi_id)
                return form_models.Publication.get_publication_type_user_store_based_positions(
                    sdi)
            except form_models.StudentDetailedInfo.DoesNotExist:
                return None
        return None


class PublicationsScoreChartSerializer(CommonChartSerializer):

    def save(self, **kwargs):
        self._data = dict()
        chart = self.instance
        qs = ChartItemData.objects.filter(chart=chart)
        data_number = qs.aggregate(Sum('count')).get('count__sum')
        if data_number == 0.0:
            data_number = 1.0
        items_qs = ChartItemData.objects.filter(chart=chart).annotate(percent=F('count') / data_number)
        user_store_based_positions = self.get_user_positions(chart)
        self._data['title'] = chart.title

        self._data['label_range'] = form_models.Publication.PUBLICATIONS_SCORE__VIEW_LABEL_RANGE

        self._data['chart_items'] = self.get_chart_items(items_qs)

        self._data['user_positions'] =\
            get_store_to_view_labels(user_store_based_positions,
                                     form_models.Publication.convert_publications_score__store_to_view_label)

        self._data['data_number'] = data_number

        self._data['user_status'] = get_user_status(user_store_based_positions,
                                                    items_qs,
                                                    form_models.Publication.compare_publications_score_labels)

    def get_chart_items(self, qs):
        return get_converted_chart_items(qs,
                                         form_models.Publication.convert_publications_score__store_to_view_label)

    def get_user_positions(self, obj):
        sdi_id = self.context.get('student_detailed_info', None)
        if sdi_id is not None:
            try:
                sdi = form_models.StudentDetailedInfo.objects.get(id=sdi_id)
                return form_models.Publication.get_publications_score_user_store_based_positions(
                    sdi)
            except form_models.StudentDetailedInfo.DoesNotExist:
                return None


class PublicationImpactFactorChartSerializer(CommonChartSerializer):

    def save(self, **kwargs):
        self._data = dict()
        chart = self.instance
        qs = ChartItemData.objects.filter(chart=chart)
        data_number = qs.aggregate(Sum('count')).get('count__sum')
        if data_number == 0.0:
            data_number = 1.0
        items_qs = ChartItemData.objects.filter(chart=chart).annotate(percent=F('count') / data_number)
        user_store_based_positions = self.get_user_positions(chart)
        self._data['title'] = chart.title

        self._data['label_range'] = None

        self._data['chart_items'] = self.get_chart_items(items_qs)

        self._data['user_positions'] = \
            get_store_to_view_labels(user_store_based_positions,
                                     )

        self._data['data_number'] = data_number

        self._data['user_status'] = \
            get_user_status(user_store_based_positions,
                            items_qs,
                            form_models.Publication.compare_publication_impact_factor_labels)

    def get_chart_items(self, qs):
        return get_unchanged_chart_items(qs)

    def get_user_positions(self, obj):
        sdi_id = self.context.get('student_detailed_info', None)
        if sdi_id is not None:
            try:
                sdi = form_models.StudentDetailedInfo.objects.get(id=sdi_id)
                return form_models.Publication.\
                    get_publication_impact_factor_user_store_based_positions(sdi)
            except form_models.StudentDetailedInfo.DoesNotExist:
                return None


class PowerfulRecommendationChartSerializer(CommonChartSerializer):

    def save(self, **kwargs):
        self._data = dict()
        chart = self.instance
        qs = ChartItemData.objects.filter(chart=chart)
        data_number = qs.aggregate(Sum('count')).get('count__sum')
        if data_number == 0.0:
            data_number = 1.0
        items_qs = ChartItemData.objects.filter(chart=chart).annotate(percent=F('count') / data_number)
        user_store_based_positions = self.get_user_positions(chart)
        self._data['title'] = chart.title

        self._data['label_range'] = None

        self._data['chart_items'] = self.get_chart_items(items_qs)

        self._data['user_positions'] = \
            get_store_to_view_labels(user_store_based_positions,
                                     )

        self._data['data_number'] = data_number

        self._data['user_status'] = get_user_status(user_store_based_positions,
                                                    items_qs,
                                                    form_models.StudentDetailedInfo.
                                                    compare_powerful_recommendation_labels)

    def get_chart_items(self, qs):
        return get_unchanged_chart_items(qs)

    def get_user_positions(self, obj):
        sdi_id = self.context.get('student_detailed_info', None)
        if sdi_id is not None:
            try:
                sdi = form_models.StudentDetailedInfo.objects.get(id=sdi_id)
                return [sdi.get_powerful_recommendation__store_label()]
            except form_models.StudentDetailedInfo.DoesNotExist:
                return None


class OlympiadChartSerializer(CommonChartSerializer):

    def save(self, **kwargs):
        self._data = dict()
        chart = self.instance
        qs = ChartItemData.objects.filter(chart=chart)
        data_number = qs.aggregate(Sum('count')).get('count__sum')
        if data_number == 0.0:
            data_number = 1.0
        items_qs = ChartItemData.objects.filter(chart=chart).annotate(percent=F('count') / data_number)
        user_store_based_positions = self.get_user_positions(chart)
        self._data['title'] = chart.title

        self._data['label_range'] = None

        self._data['chart_items'] = self.get_chart_items(items_qs)

        self._data['user_positions'] = \
            get_store_to_view_labels(user_store_based_positions,
                                     )

        self._data['data_number'] = data_number

        self._data['user_status'] = get_user_status(user_store_based_positions,
                                                    items_qs,
                                                    form_models.StudentDetailedInfo.compare_olympiad_labels)

    def get_chart_items(self, qs):
        return get_unchanged_chart_items(qs)

    def get_user_positions(self, obj):
        sdi_id = self.context.get('student_detailed_info', None)
        if sdi_id is not None:
            try:
                sdi = form_models.StudentDetailedInfo.objects.get(id=sdi_id)
                return [sdi.get_olympiad__store_label()]
            except form_models.StudentDetailedInfo.DoesNotExist:
                return None


class RelatedWorkExperienceChartSerializer(CommonChartSerializer):

    def save(self, **kwargs):
        self._data = dict()
        chart = self.instance
        qs = ChartItemData.objects.filter(chart=chart)
        data_number = qs.aggregate(Sum('count')).get('count__sum')
        if data_number == 0:
            data_number = 1
        items_qs = ChartItemData.objects.filter(chart=chart).annotate(percent=F('count') / data_number)
        user_store_based_positions = self.get_user_positions(chart)
        self._data['title'] = chart.title

        self._data[
            'label_range'] = form_models.StudentDetailedInfo.RELATED_WORK_EXPERIENCE_VIEW_LABEL_RANGE

        self._data['chart_items'] = self.get_chart_items(items_qs)

        self._data['user_positions'] = \
            get_store_to_view_labels(user_store_based_positions,
                                     form_models.StudentDetailedInfo.convert_related_work_store_to_view_label)

        self._data['data_number'] = data_number

        self._data['user_status'] = get_user_status(user_store_based_positions,
                                                    items_qs,
                                                    form_models.StudentDetailedInfo.compare_related_work_labels,
                                                    form_models.StudentDetailedInfo.convert_related_work_store_to_view_label
                                                    )

    def get_chart_items(self, qs):
        return get_converted_chart_items(qs,
                                         form_models.StudentDetailedInfo.convert_related_work_store_to_view_label,
                                         )

    def get_user_positions(self, obj):
        sdi_id = self.context.get('student_detailed_info', None)
        if sdi_id is not None:
            try:
                sdi = form_models.StudentDetailedInfo.objects.get(id=sdi_id)
                return [sdi.get_related_work__store_label()]
            except form_models.StudentDetailedInfo.DoesNotExist:
                return None
        return None


class ToeflChartSerializer(CommonChartSerializer):

    def save(self, **kwargs):
        self._data = dict()
        chart = self.instance
        qs = ChartItemData.objects.filter(chart=chart)
        data_number = qs.aggregate(Sum('count')).get('count__sum')
        if data_number == 0.0:
            data_number = 1.0
        items_qs = ChartItemData.objects.filter(chart=chart).annotate(percent=F('count') / data_number)
        user_store_based_positions = self.get_user_positions(chart)
        self._data['title'] = chart.title

        self._data[
            'label_range'] = ad_models.RegularLanguageCertificate.TOEFL__VIEW_LABEL_RANGE

        self._data['chart_items'] = self.get_chart_items(items_qs)

        self._data['user_positions'] = \
            get_store_to_view_labels(user_store_based_positions,
                                     ad_models.RegularLanguageCertificate.convert_toefl_store_to_view_label)

        self._data['data_number'] = data_number

        self._data['user_status'] = get_user_status(user_store_based_positions,
                                                    items_qs,
                                                    ad_models.RegularLanguageCertificate.compare_toefl_labels)

    def get_chart_items(self, qs):
        return get_converted_chart_items(qs,
                                         ad_models.RegularLanguageCertificate.convert_toefl_store_to_view_label
                                         )

    def get_user_positions(self, obj):
        sdi_id = self.context.get('student_detailed_info', None)
        if sdi_id is not None:
            try:
                sdi = form_models.StudentDetailedInfo.objects.get(id=sdi_id)
                return ad_models.RegularLanguageCertificate.get_toefl_user_store_based_positions(
                    sdi)
            except form_models.StudentDetailedInfo.DoesNotExist:
                return None
        return None


class IeltsChartSerializer(CommonChartSerializer):

    def save(self, **kwargs):
        self._data = dict()
        chart = self.instance
        qs = ChartItemData.objects.filter(chart=chart)
        data_number = qs.aggregate(Sum('count')).get('count__sum')
        if data_number == 0.0:
            data_number = 1.0
        items_qs = ChartItemData.objects.filter(chart=chart).annotate(percent=F('count') / data_number)
        user_store_based_positions = self.get_user_positions(chart)
        self._data['title'] = chart.title

        self._data[
            'label_range'] = ad_models.RegularLanguageCertificate.IELTS__VIEW_LABEL_RANGE

        self._data['chart_items'] = self.get_chart_items(items_qs)

        self._data['user_positions'] = \
            get_store_to_view_labels(user_store_based_positions,
                                     ad_models.RegularLanguageCertificate.convert_ielts_store_to_view_label)

        self._data['data_number'] = data_number

        self._data['user_status'] = get_user_status(user_store_based_positions,
                                                    items_qs,
                                                    ad_models.RegularLanguageCertificate.compare_ielts_labels)

    def get_chart_items(self, qs):
        return get_converted_chart_items(qs,
                                         ad_models.RegularLanguageCertificate.convert_ielts_store_to_view_label,
                                         )

    def get_user_positions(self, obj):
        sdi_id = self.context.get('student_detailed_info', None)
        if sdi_id is not None:
            try:
                sdi = form_models.StudentDetailedInfo.objects.get(id=sdi_id)
                return ad_models.RegularLanguageCertificate.get_ielts_user_store_based_positions(
                    sdi)
            except form_models.StudentDetailedInfo.DoesNotExist:
                return None
        return None


class GMATChartSerializer(CommonChartSerializer):

    def save(self, **kwargs):
        self._data = dict()
        chart = self.instance
        qs = ChartItemData.objects.filter(chart=chart)
        data_number = qs.aggregate(Sum('count')).get('count__sum')
        if data_number == 0.0:
            data_number = 1.0
        items_qs = ChartItemData.objects.filter(chart=chart).annotate(percent=F('count') / data_number)
        user_store_based_positions = self.get_user_positions(chart)

        self._data['title'] = chart.title

        self._data['label_range'] = ad_models.GMATCertificate.TOTAL_VIEW_LABEL_RANGE

        self._data['chart_items'] = self.get_chart_items(items_qs)

        self._data['user_positions'] = \
            get_store_to_view_labels(user_store_based_positions,
                                     ad_models.GMATCertificate.convert_store_to_view_label)

        self._data['data_number'] = data_number

        self._data['user_status'] = get_user_status(user_store_based_positions,
                                                    items_qs,
                                                    ad_models.GMATCertificate.compare_labels)

    def get_chart_items(self, qs):
        return get_converted_chart_items(qs,
                                         ad_models.GMATCertificate.convert_store_to_view_label
                                         )

    def get_user_positions(self, obj):
        sdi_id = self.context.get('student_detailed_info', None)
        if sdi_id is not None:
            try:
                sdi = form_models.StudentDetailedInfo.objects.get(id=sdi_id)
                return ad_models.GMATCertificate.get_user_store_based_positions(sdi)
            except form_models.StudentDetailedInfo.DoesNotExist:
                return None
        return None


class GREGeneralWritingChartSerializer(CommonChartSerializer):

    def save(self, **kwargs):
        self._data = dict()
        chart = self.instance
        qs = ChartItemData.objects.filter(chart=chart)
        data_number = qs.aggregate(Sum('count')).get('count__sum')
        if data_number == 0.0:
            data_number = 1.0
        items_qs = ChartItemData.objects.filter(chart=chart).annotate(percent=F('count') / data_number)
        user_store_based_positions = self.get_user_positions(chart)

        self._data['title'] = chart.title

        self._data['label_range'] = ad_models.GREGeneralCertificate.WRITING_VIEW_LABEL_RANGE

        self._data['chart_items'] = self.get_chart_items(items_qs)

        self._data['user_positions'] = \
            get_store_to_view_labels(user_store_based_positions,
                                     ad_models.GREGeneralCertificate.convert_writing_store_to_view_label)

        self._data['data_number'] = data_number

        self._data['user_status'] = get_user_status(user_store_based_positions,
                                                    items_qs,
                                                    ad_models.GREGeneralCertificate.compare_writing_labels)

    def get_chart_items(self, qs):
        return get_converted_chart_items(qs,
                                         ad_models.GREGeneralCertificate.convert_writing_store_to_view_label
                                         )

    def get_user_positions(self, obj):
        sdi_id = self.context.get('student_detailed_info', None)
        if sdi_id is not None:
            try:
                sdi = form_models.StudentDetailedInfo.objects.get(id=sdi_id)
                return ad_models.GREGeneralCertificate.get_writing_user_store_based_positions(
                    sdi)
            except form_models.StudentDetailedInfo.DoesNotExist:
                return None
        return None


class GREGeneralQuantitativeAndVerbalChartSerializer(CommonChartSerializer):

    def save(self, **kwargs):
        self._data = dict()
        chart = self.instance
        qs = ChartItemData.objects.filter(chart=chart)
        data_number = qs.aggregate(Sum('count')).get('count__sum')
        if data_number == 0.0:
            data_number = 1.0
        items_qs = ChartItemData.objects.filter(chart=chart).annotate(percent=F('count') / data_number)
        user_store_based_positions = self.get_user_positions(chart)

        self._data['title'] = chart.title

        self._data['label_range'] = ad_models.GREGeneralCertificate.Q_AND_V_VIEW_LABEL_RANGE

        self._data['chart_items'] = self.get_chart_items(items_qs)

        self._data['user_positions'] = \
            get_store_to_view_labels(user_store_based_positions,
                                     ad_models.GREGeneralCertificate.convert_q_and_v_store_to_view_label)

        self._data['data_number'] = data_number

        self._data['user_status'] = get_user_status(user_store_based_positions,
                                                    items_qs,
                                                    ad_models.GREGeneralCertificate.compare_q_and_v_labels)

    def get_chart_items(self, qs):
        return get_converted_chart_items(qs,
                                         ad_models.GREGeneralCertificate.convert_q_and_v_store_to_view_label
                                         )

    def get_user_positions(self, obj):
        sdi_id = self.context.get('student_detailed_info', None)
        if sdi_id is not None:
            try:
                sdi = form_models.StudentDetailedInfo.objects.get(id=sdi_id)
                return ad_models.GREGeneralCertificate.get_q_and_v_user_store_based_positions(
                    sdi)
            except form_models.StudentDetailedInfo.DoesNotExist:
                return None
        return None


class GRESubjectTotalChartSerializer(CommonChartSerializer):

    def save(self, **kwargs):
        self._data = dict()
        chart = self.instance
        qs = ChartItemData.objects.filter(chart=chart)
        data_number = qs.aggregate(Sum('count')).get('count__sum')
        if data_number == 0.0:
            data_number = 1.0
        items_qs = ChartItemData.objects.filter(chart=chart).annotate(percent=F('count') / data_number)
        user_store_based_positions = self.get_user_positions(chart)
        self._data['title'] = chart.title

        self._data['label_range'] = ad_models.GRESubjectCertificate.TOTAL_VIEW_LABEL_RANGE

        self._data['chart_items'] = self.get_chart_items(items_qs)

        self._data['user_positions'] = \
            get_store_to_view_labels(user_store_based_positions,
                                     ad_models.GRESubjectCertificate.convert_total_store_to_view_label)

        self._data['data_number'] = data_number

        self._data['user_status'] = get_user_status(user_store_based_positions,
                                                    items_qs,
                                                    ad_models.GRESubjectCertificate.compare_total_labels)

    def get_chart_items(self, qs):
        return get_converted_chart_items(qs,
                                         ad_models.GRESubjectCertificate.convert_total_store_to_view_label
                                         )

    def get_user_positions(self, obj):
        sdi_id = self.context.get('student_detailed_info', None)
        if sdi_id is not None:
            try:
                sdi = form_models.StudentDetailedInfo.objects.get(id=sdi_id)
                return ad_models.GRESubjectCertificate.get_total_user_store_based_positions(
                    sdi
                )
            except form_models.StudentDetailedInfo.DoesNotExist:
                return None
        return None


class DuolingoChartSerializer(CommonChartSerializer):

    def save(self, **kwargs):
        self._data = dict()
        chart = self.instance
        qs = ChartItemData.objects.filter(chart=chart)
        data_number = qs.aggregate(Sum('count')).get('count__sum')
        if data_number == 0.0:
            data_number = 1.0
        items_qs = ChartItemData.objects.filter(chart=chart).annotate(percent=F('count') / data_number)
        user_store_based_positions = self.get_user_positions(chart)
        self._data['title'] = chart.title

        self._data['label_range'] = ad_models.DuolingoCertificate.OVERALL_VIEW_LABEL_RANGE

        self._data['chart_items'] = self.get_chart_items(items_qs)

        self._data['user_positions'] = \
            get_store_to_view_labels(user_store_based_positions,
                                     ad_models.DuolingoCertificate.convert_store_to_view_label)

        self._data['data_number'] = data_number

        self._data['user_status'] = get_user_status(user_store_based_positions,
                                                    items_qs,
                                                    ad_models.DuolingoCertificate.compare_labels)

    def get_chart_items(self, qs):
        return get_converted_chart_items(qs,
                                         ad_models.DuolingoCertificate.convert_store_to_view_label,
                                         )

    def get_user_positions(self, obj):
        sdi_id = self.context.get('student_detailed_info', None)
        if sdi_id is not None:
            try:
                sdi = form_models.StudentDetailedInfo.objects.get(id=sdi_id)
                return ad_models.DuolingoCertificate.get__user_store_based_positions(sdi)
            except form_models.StudentDetailedInfo.DoesNotExist:
                return None
        return None
