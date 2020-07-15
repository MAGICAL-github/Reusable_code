import weakref


class ValidArgument:
    """
    Data descriptor for easily validating an instance argument of a class.
    Allows type checking, lower and upper (inclusive) bound checking (refers to length if iterable, or number),
    checking inclusion in certain valid choices, and setting a default value.
    """

    def __init__(self, arg_name, type_, *, choices=None, lower_bound=None, upper_bound=None, default=None):
        self._type = type_
        self._arg_name = arg_name
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._choices = choices
        self._values = {}
        self._default = default

    def __get__(self, instance, owner_class):
        if instance is None:
            return self
        if id(instance) in self._values:
            return self._values[id(instance)][1]
        else:
            return self._default

    def __set__(self, instance, value='default'):
        if value == 'default':
            value = self._default

        if type(value) != self._type:
            raise TypeError(
                'Expected type {0} for {1} and got {2}.'.format(self._type.__name__, self._arg_name,
                                                                value.__class__.__name__))
        if hasattr(value, '__len__'):
            self._check_for_value_error(len(value))
        else:
            self._check_for_value_error(value)

        if self._choices is not None and value not in self._choices:
            raise ValueError("Expected {0} to be in {1} and got '{2}'.".format(self._arg_name, self._choices, value))

        self._values[id(instance)] = weakref.ref(instance, self._remove_object), value

    def _check_for_value_error(self, value):
        if self._upper_bound is not None and self._lower_bound is not None:
            if value < self._lower_bound or value > self._upper_bound:
                raise ValueError(
                    "{0} is out of bounds. Must be between [{2}-{3}] ({1}<{2} or {1}>{3}).".format(
                        self._arg_name, value,
                        self._lower_bound,
                        self._upper_bound))

        elif self._upper_bound is not None:
            if value > self._upper_bound:
                raise ValueError(
                    "{0} is out of bounds. Must be at most {2} ({1}>{2}).".format(self._arg_name, value,
                                                                                  self._upper_bound))

        elif self._lower_bound is not None:
            if value < self._lower_bound:
                raise ValueError(
                    "{0} is out of bounds. Must be at least {2} ({1}<{2}).".format(self._arg_name, value,
                                                                                   self._lower_bound))

    def _remove_object(self, weak_ref):
        reverse_lookup = [key for key, value in self._values.items() if value[0] is weak_ref]

        if len(reverse_lookup) > 0:
            key = reverse_lookup[0]
            del self._values[key]
