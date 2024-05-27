from django import template


register = template.Library()

ban_word = ['екс', 'олов']

@register.filter()
def censor(value):
    if isinstance(value, str):
        for i in ban_word:
            value = value.replace(i[:], '*' * len(i[:]))
    return value
