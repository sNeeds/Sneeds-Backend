

def flex_run_python_decorator(func, app_name, model_name):
    """
    With this decorator we can use functions that can run for any app an d model that func supports and does
    operations on it.
    So the func should accept app_name and model_name in it's body. for example:

    def forwards_func(apps, schema_editor, app_name, model_name):
        Model = apps.get_model(app_name, model_name)
        for obj in Model.objects.all():
            ...
            do some works
            ...
    """
    def wrapper(apps, schema_editor):
        return func(apps, schema_editor, app_name, model_name)
    return wrapper
