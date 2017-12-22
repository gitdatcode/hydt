
class Config:
    """super simple configuration object"""
    options = {}

    def __init__(self, **options):
        self.fill(**options)

    def fill(self, **options):
        options = options or {}

        for k, v in options.items():
            self.options[k] = v

    def __getattr__(self, attr):
        return self.options.get(attr, None)

    def __setattr__(self, attr, value):
        self.options[attr] = value


options = Config()
