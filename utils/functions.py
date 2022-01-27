from django.apps import apps




def get_model_from_any_app(model_name):
    """ Search model using model_name without app_lable
    """

    for app_config in apps.get_app_configs():
        try:
            model = app_config.get_model(model_name)
            return model
        except LookupError as e:
            pass
    raise LookupError("Model not found")