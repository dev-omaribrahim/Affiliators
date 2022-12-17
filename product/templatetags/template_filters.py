from django import template

register = template.Library()


@register.filter(name="clear_text")
def clear_text(value):
    # check if value list is empty or only contain 'None' word
    if not value or None in value or "None" in value and len(value) < 1:
        text = "----"
        return text
    else:
        # remove the brackets and ' quotes form the list
        text = " - ".join(value)
        return text
    # return value
