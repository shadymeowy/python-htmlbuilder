class Builder:
    __slots__ = ('data', 'tags')

    def __init__(self):
        self.data = []
        self.tags = []

    def tag(self, tag, *args, **kwargs):
        self._tag(tag, False, args, kwargs.items())
        return self

    def stag(self, tag, *args, **kwargs):
        self._tag(tag, True, args, kwargs.items())
        return self

    def text(self, txt):
        self.data.append(txt)
        return self

    def _attr(self, arr):
        for k, v in arr:
            self.text(' {0}="{1}"'.format(k.replace('_', '-'), _str(v)))

    def _tag(self, tag, selfclose, a1, a2):
        self.text('<' + tag)
        self._attr(a1)
        self._attr(a2)
        if selfclose:
            self.text('/>')
        else:
            self.tags.append(tag)
            self.text('>')

    def __enter__(self):
        pass

    def endtag(self):
        if len(self.tags) > 0:
            self.text('</{0}>'.format(self.tags.pop()))

    def __exit__(self, t, v, trace):
        self.endtag()

    def result(self):
        if len(self.tags) > 0:
            raise Exception()
        else:
            r = ''.join(self.data)
            self.data = []
            return r


class FancyFunction:
    __slots__ = ('fun', 'rkey', 'r')

    def __init__(self, fun):
        self.fun = fun
        self.rkey = None

        def r(*args, **kargs):
            return (self.fun)(self.rkey, *args, **kargs)
        self.r = r

    def __getattr__(self, key, *args, **kargs):
        self.rkey = key
        return self.r

    def __call__(self, *args, **kargs):
        return (self.fun)(*args, **kargs)


def _str(x):
    if isinstance(x, str):
        return x
    elif isinstance(x, dict):
        r = []
        for k, v in x.items():
            r.append(k)
            r.append(':')
            r.append(_str(v))
            r.append(';')
        return ''.join(r)
    else:
        return str(x)


def css(**kargs):
    r = []
    for k, v in kargs.items():
        r.append(k)
        r.append(':')
        r.append(_str(v))
        r.append(';')
    return ''.join(r)


def builder(f=None):
    b = Builder()
    tag = FancyFunction(b.tag)
    stag = FancyFunction(b.stag)
    text = b.text
    result = b.result
    if f:
        def r(*args, **kargs):
            f(tag, stag, text, *args, **kargs)
            return result()
        return r
    else:
        return tag, stag, text, result
