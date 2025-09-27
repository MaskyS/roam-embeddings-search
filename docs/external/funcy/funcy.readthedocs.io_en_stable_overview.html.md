---
url: "https://funcy.readthedocs.io/en/stable/overview.html"
title: "Overview — funcy 2.0 documentation"
---

- »
- Overview
- [Edit on GitHub](https://github.com/Suor/funcy/blob/13fac0037c109a9e4649fc8ee343be17647f7407/docs/overview.rst)

* * *

# Overview [¶](https://funcy.readthedocs.io/en/stable/overview.html\#overview "Permalink to this headline")

Start with:

```
pip install funcy

```

Import stuff from funcy to make things happen:

```
from funcy import whatever, you, need

```

Merge collections of same type
(works for dicts, sets, lists, tuples, iterators and even strings):

```
merge(coll1, coll2, coll3, ...)
join(colls)
merge_with(sum, dict1, dict2, ...)

```

Walk through collection, creating its transform (like map but preserves type):

```
walk(str.upper, {'a', 'b'})            # {'A', 'B'}
walk(reversed, {'a': 1, 'b': 2})       # {1: 'a', 2: 'b'}
walk_keys(double, {'a': 1, 'b': 2})    # {'aa': 1, 'bb': 2}
walk_values(inc, {'a': 1, 'b': 2})     # {'a': 2, 'b': 3}

```

Select a part of collection:

```
select(even, {1,2,3,10,20})                  # {2,10,20}
select(r'^a', ('a','b','ab','ba'))           # ('a','ab')
select_keys(callable, {str: '', None: None}) # {str: ''}
compact({2, None, 1, 0})                     # {1,2}

```

Manipulate sequences:

```
take(4, iterate(double, 1)) # [1, 2, 4, 8]
first(drop(3, count(10)))   # 13

lremove(even, [1, 2, 3])    # [1, 3]
lconcat([1, 2], [5, 6])     # [1, 2, 5, 6]
lcat(map(range, range(4)))  # [0, 0, 1, 0, 1, 2]
lmapcat(range, range(4))    # same
flatten(nested_structure)   # flat iter
distinct('abacbdd')         # iter('abcd')

lsplit(odd, range(5))       # ([1, 3], [0, 2, 4])
lsplit_at(2, range(5))      # ([0, 1], [2, 3, 4])
group_by(mod3, range(5))    # {0: [0, 3], 1: [1, 4], 2: [2]}

lpartition(2, range(5))     # [[0, 1], [2, 3]]
chunks(2, range(5))         # iter: [0, 1], [2, 3], [4]
pairwise(range(5))          # iter: [0, 1], [1, 2], ...

```

And functions:

```
partial(add, 1)             # inc
curry(add)(1)(2)            # 3
compose(inc, double)(10)    # 21
complement(even)            # odd
all_fn(isa(int), even)      # is_even_int

one_third = rpartial(operator.div, 3.0)
has_suffix = rcurry(str.endswith, 2)

```

Create decorators easily:

```
@decorator
def log(call):
    print call._func.__name__, call._args
    return call()

```

Abstract control flow:

```
walk_values(silent(int), {'a': '1', 'b': 'no'})
# => {'a': 1, 'b': None}

@once
def initialize():
    "..."

with suppress(OSError):
    os.remove('some.file')

@ignore(ErrorRateExceeded)
@limit_error_rate(fails=5, timeout=60)
@retry(tries=2, errors=(HttpError, ServiceDown))
def some_unreliable_action(...):
    "..."

class MyUser(AbstractBaseUser):
    @cached_property
    def public_phones(self):
        return self.phones.filter(public=True)

```

Ease debugging:

```
squares = {tap(x, 'x'): tap(x * x, 'x^2') for x in [3, 4]}
# x: 3
# x^2: 9
# ...

@print_exits
def some_func(...):
    "..."

@log_calls(log.info, errors=False)
@log_errors(log.exception)
def some_suspicious_function(...):
    "..."

with print_durations('Creating models'):
    Model.objects.create(...)
    # ...
# 10.2 ms in Creating models

```

Versions[latest](https://funcy.readthedocs.io/en/latest/overview.html)**[stable](https://funcy.readthedocs.io/en/stable/overview.html)**[2.0](https://funcy.readthedocs.io/en/2.0/overview.html)[1.18](https://funcy.readthedocs.io/en/1.18/overview.html)[1.17](https://funcy.readthedocs.io/en/1.17/overview.html)[1.16](https://funcy.readthedocs.io/en/1.16/overview.html)[1.15](https://funcy.readthedocs.io/en/1.15/overview.html)[1.14](https://funcy.readthedocs.io/en/1.14/overview.html)[1.13](https://funcy.readthedocs.io/en/1.13/overview.html)[1.11](https://funcy.readthedocs.io/en/1.11/overview.html)[1.10.3](https://funcy.readthedocs.io/en/1.10.3/overview.html)[1.10.2](https://funcy.readthedocs.io/en/1.10.2/overview.html)[1.10.1](https://funcy.readthedocs.io/en/1.10.1/overview.html)[1.10](https://funcy.readthedocs.io/en/1.10/overview.html)[1.9](https://funcy.readthedocs.io/en/1.9/overview.html)[1.8](https://funcy.readthedocs.io/en/1.8/overview.html)[1.7.5](https://funcy.readthedocs.io/en/1.7.5/overview.html)[1.7.4](https://funcy.readthedocs.io/en/1.7.4/overview.html)[1.7.3](https://funcy.readthedocs.io/en/1.7.3/overview.html)[1.7.2](https://funcy.readthedocs.io/en/1.7.2/overview.html)[1.7.1](https://funcy.readthedocs.io/en/1.7.1/overview.html)[1.7](https://funcy.readthedocs.io/en/1.7/overview.html)[1.6](https://funcy.readthedocs.io/en/1.6/overview.html)[1.5](https://funcy.readthedocs.io/en/1.5/overview.html)[1.4](https://funcy.readthedocs.io/en/1.4/overview.html)[1.3](https://funcy.readthedocs.io/en/1.3/overview.html)[1.1](https://funcy.readthedocs.io/en/1.1/overview.html)[1.0.0](https://funcy.readthedocs.io/en/1.0.0/overview.html)[0.10.1](https://funcy.readthedocs.io/en/0.10.1/overview.html)On Read the Docs[Project Home](https://app.readthedocs.org/projects/funcy/?utm_source=funcy&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/funcy/builds/?utm_source=funcy&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=funcy&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=funcy&utm_content=flyout)