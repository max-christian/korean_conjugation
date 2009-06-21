import random
import types
from functools import partial

__all__ = ['an_integer', 'a_list', 'a_unicode', 'a_character', 'forall']

def evaluate(lazy_value):
    while hasattr(lazy_value, '__call__'):
        lazy_value = lazy_value()
    return lazy_value

def an_integer(low=0, high=100):
    return lambda: random.randint(low, high)

def a_list(item_generator=an_integer, size=(0, 100)):
    return lambda: [evaluate(item_generator) \
                    for _ in xrange(random.randint(size[0], size[1]))]

def a_unicode(size=(0, 100), minunicode=0, maxunicode=255):
    return lambda: u''.join(unichr(random.randint(minunicode, maxunicode)) \
                            for _ in xrange(random.randint(size[0], size[1])))

a_character = partial(a_unicode, size=(1, 1))

def forall(tries=100, **kwargs):
    def wrap(f):
        def wrapped():
            for _ in xrange(tries):
                random_kwargs = (dict((name, evaluate(lazy_value)) \
                                 for (name, lazy_value) in kwargs.iteritems()))
                if forall.verbose:
                    from pprint import pprint
                    pprint(random_kwargs)
                f(**random_kwargs)
        wrapped.__name__ = f.__name__
        return wrapped
    return wrap
forall.verbose = False # if enabled will print out the random test cases

@forall(tries=10, i=an_integer)
def test_an_integer(i):
    assert type(i) == int
    assert i >= 0 and i <= 100

@forall(tries=10, l=a_list(item_generator=an_integer))
def test_a_int_list(l):
    assert type(l) == list

@forall(tries=10, ul=a_list(item_generator=a_unicode))
def test_a_unicode_list(ul):
    assert type(ul) == list

@forall(tries=10, l=a_list(item_generator=an_integer, size=(10, 50)))
def test_a_list_size(l):
    assert len(l) <= 50 and len(l) >= 10

@forall(tries=10, u=a_unicode)
def test_a_unicode(u):
    assert type(u) == unicode

@forall(tries=10, u=a_unicode(size=(1,1)))
def test_a_unicode_size(u):
    assert len(u) == 1

def random_int_unicode_tuple():
    return lambda: (evaluate(an_integer), evaluate(a_unicode))

@forall(tries=10, l=a_list(item_generator=random_int_unicode_tuple))
def test_a_tupled_list(l):
    for x in l:
        assert type(x[0]) == int and type(x[1]) == unicode

@forall(tries=10, x=an_integer, y=an_integer)
def test_addition_associative(x, y):
    assert x + y == y + x

@forall(tries=10, l=a_list)
def test_reverse_reverse(l):
    assert list(reversed(list(reversed(l)))) == l

@forall(tries=10, c=a_character)
def test_a_character(c):
    assert len(c) == 1
