import time

from abroadin.apps.estimation.form.models import StudentDetailedInfo
from . import tags


class Tagger:

    def __init__(self, tag_classes: iter):
        self.tag_classes = tag_classes
        self.tags_field_title = {}
        self.set_field_title()

    def set_field_title(self):
        for tag_class in self.tag_classes:
            assert tag_class.annotation_field not in self.tags_field_title, \
                'Duplicate tag annotation field found! {} from {} class'.format(tag_class.annotation_field, tag_class)
            assert tag_class.title not in self.tags_field_title.values(), \
                'Duplicate tag title found! {} from {} class'.format(tag_class.title, tag_class)
            self.tags_field_title[tag_class.annotation_field] = tag_class.title

    def tag_queryset(self, queryset, sdi: StudentDetailedInfo):
        start_time_ = time.time()
        for tag_class in self.tag_classes:
            start_time = time.time()
            queryset = tag_class().tag_queryset(queryset, sdi)
            print(tag_class.title, time.time() - start_time)
        print('end of loop', time.time() - start_time_)
        return queryset

    def tag_queryset2(self, queryset, sdi: StudentDetailedInfo):
        annotation_dict = {}
        for tag_class in self.tag_classes:
            annotation_dict.update(tag_class().get_annotation_dict(queryset, sdi))
        return queryset.annotate(**annotation_dict)

    def tag_queryset3(self, queryset, sdi: StudentDetailedInfo):
        # start_time_ = time.time()
        for tag_class in self.tag_classes:
            # start_time = time.time()
            queryset = tag_class().tag_queryset2(queryset, sdi)
            # print(tag_class.title, time.time() - start_time)
        # print('end of loop', time.time() - start_time_)
        return queryset

    def tag_object(self, obj, sdi: StudentDetailedInfo):
        for tag_class in self.tag_classes:
            obj = tag_class().tag_object(obj, sdi)
        return obj

    def tag_object2(self, obj, sdi: StudentDetailedInfo):
        object_queryset = obj.__class__.objects.filter(pk=obj.pk)
        annotation_dict = {}
        for tag_class in self.tag_classes:
            annotation_dict.update(tag_class().get_annotation_dict(object_queryset, sdi))
        return object_queryset.annotate(annotation_dict).first()


SimilarProfilesTagger = Tagger(tag_classes=[
    tags.SimilarGPA,
    tags.ExactGPA,

    tags.ExactHomeUniversity,
    tags.SimilarHomeUniversity,

    tags.ExactHomeMajor,
    tags.SimilarHomeMajor,

    tags.ExactDestinationMajor,
    tags.SimilarDestinationMajor,

])
