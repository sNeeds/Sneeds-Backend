from abroadin.base.mixins.validators import CreateM2MManagerMixin


def exclude_meta_fields_class_factory(base_class, exclude_fields):
    class MetaUpdatedClass(base_class):
        class Meta(base_class.Meta):
            fields = list(set(base_class.Meta.fields) - exclude_fields)

    meta_fields = base_class.Meta.fields
    if not set(exclude_fields) <= set(meta_fields):
        raise ValueError(
            f"Exclude_fields with value {exclude_fields} contains value that is"
            f" not in base_class.Meta.fields {meta_fields}."
        )

    return MetaUpdatedClass