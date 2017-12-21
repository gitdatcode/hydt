
def request_fields(fields=None):
    """this decorator serves two purposes:
        * it validates that the required fields are passed into the request
        * it will set the values of the required fields to a member of the
            controller as request_data

        if all of the requirements are not met, it will return a 403 and a list
        of errors

    usage:
        @request_fields({
            'required': ['email', 'first_name', 'last_name',]
            'optional' : ['sex', 'age']
        })
        def get(self,...):
            ....
    """

    fields = fields or {}

    def check(method):

        @functools.wraps(method)
        async def inner(self, *args, **kwargs):
            data = {}
            errors = []
            required = fields.get('required', {})
            optional = fields.get('optional', {})

            for field in required:
                val = self.get_arg(field, None)

                if not val:
                    msg = (get_message('FIELD_REQURIED')).format(field=field)

                    errors.append(msg)
                else:
                    data[field] = val

            for field in optional:
                val = self.get_arg(field)
                data[field] = val

            if len(errors):
                message = get_message('REQUIRED_FIELDS')

                return self.response(status=200, errors=errors,
                    message=message)
            else:
                self.request_data = data

                response = await method(self, *args, **kwargs)

                return response
        return inner
    return check
