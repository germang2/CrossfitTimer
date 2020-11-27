def validate_exists(field, value, errors):
    if not value:
        errors[field] = 'Ingrese un valor'


def validate_min(field, value, minimum, errors):
    validate_exists(field, value, errors)
    if not errors:
        if len(value) < minimum:
            errors[field] = f'Se aceptan minimo {minimum} caracteres'


def validate_max(field, value, maximum, errors):
    validate_exists(field, value, errors)
    if not errors:
        if len(value) > maximum:
            errors[field] = f'Se aceptan maximo {maximum} caracteres'


def type_data(field, value, class_type, errors):
    switch = {
        str: validate_string,
        int: validate_int,
        float: validate_float
    }
    function = switch[class_type]
    function(field, value, errors)


def validate_string(field, value, errors):
    try:
        if not isinstance(value, str):
            errors[field] = 'Debe ser un texto'
    except Exception as e:
        errors[field] = 'Debe ser un texto'
        print(e)


def validate_int(field, value, errors):
    try:
        val = int(value)
    except ValueError as e:
        errors[field] = 'Ingrese un numero entero'


def validate_float(field, value, errors):
    try:
        val = float(value)
    except ValueError as e:
        errors[field] = 'Ingrese un numero valido'
