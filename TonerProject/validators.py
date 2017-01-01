from django.core.validators import RegexValidator, ValidationError


def validator_numerator(value):
    a = value[0:2]  # Первые две буквы
    n = value[3:10]  # Последние 7 цифр
    if value[2] != '-':
        raise ValidationError(u'%s не корректный номер заказа' % value)
    if not (a.isalpha() & a.isupper()):
        raise ValidationError(u'%s укажите первые две заглавные буквы кода' % value)
    if not n.isdigit():
        raise ValidationError(u'%s укажите цифровой номер заказа' % value)


def validator_warranty(value):
    if value < 0:
        raise ValidationError(u'%i - не может быть верным гарантийным сроком ' % value)
    if value > 60:
        raise ValidationError(u'%i - слишком большой гарантийный срок' % value)

numeric = RegexValidator(r'^[0-9]*$', message=u'Допустимы только цифровые символы.')
hexnumeric = RegexValidator(r'^[0-9a-fA-F]*$', message=u'Должен указывается в шестнадцатиричной системе.')
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message=u'Только буквенноцифровые символы допустимы.')
phone = RegexValidator(regex='^\d{10}$', message=u'Укажите правильный номер телефона')
