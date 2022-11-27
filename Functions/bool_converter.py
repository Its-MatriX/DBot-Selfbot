def convert_to_bool(val):
    val = val.lower()

    if val in [
            'on', 'true', 'True', 'enable', '+', 'да', 'включить',
            'активировать', 'вкл'
    ]:
        return True

    elif val in [
            'off', 'false', 'False', 'disable', '-', 'нет', 'выключить',
            'деактивировать', 'выкл'
    ]:
        return False

    else:
        raise NameError('Unknown Boolean')