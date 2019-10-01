def queryset2list(queryset):
    """
    Convert a queryset into a list
    :param queryset: the queryset to be converted.
    :return: the list corresponding to the queryset.
    """
    list = []
    for instance in queryset:
        list.append(instance)
    return list
