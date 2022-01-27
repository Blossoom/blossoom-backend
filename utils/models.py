from django.utils.timesince import timesince


class BasicTimesince:
    """ Provide timesince information instead of date
    Example: 5 days ago
    """

    def FORMAT(self):
        return "now" if timesince(self.created) in "0 minutes"\
        else timesince(self.created, depth=1) + ' ago'
