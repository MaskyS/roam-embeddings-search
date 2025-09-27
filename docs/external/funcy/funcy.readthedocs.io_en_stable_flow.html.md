---
url: "https://funcy.readthedocs.io/en/stable/flow.html"
title: "Flow — funcy 2.0 documentation"
---

- »
- Flow
- [Edit on GitHub](https://github.com/Suor/funcy/blob/13fac0037c109a9e4649fc8ee343be17647f7407/docs/flow.rst)

* * *

# Flow [¶](https://funcy.readthedocs.io/en/stable/flow.html\#flow "Permalink to this headline")

@silent [¶](https://funcy.readthedocs.io/en/stable/flow.html#silent "Permalink to this definition")

Ignore all real exceptions (descendants of `Exception`). Handy for cleaning data such as user input:

```
brand_id = silent(int)(request.GET['brand_id'])
ids = keep(silent(int), request.GET.getlist('id'))

```

And in data import/transform:

```
get_greeting = compose(silent(string.lower), re_finder(r'(\w+)!'))
map(get_greeting, ['a!', ' B!', 'c.'])
# -> ['a', 'b', None]

```

Note

Avoid silencing non-primitive functions, use [`@ignore()`](https://funcy.readthedocs.io/en/stable/flow.html#ignore) instead and even then be careful not to swallow exceptions unintentionally.

@ignore( _errors_, _default=None_) [¶](https://funcy.readthedocs.io/en/stable/flow.html#ignore "Permalink to this definition")

Same as [`@silent`](https://funcy.readthedocs.io/en/stable/flow.html#silent), but able to specify `errors` to catch and `default` to return in case of error caught. `errors` can either be exception class or a tuple of them.

suppress( _\*errors_) [¶](https://funcy.readthedocs.io/en/stable/flow.html#suppress "Permalink to this definition")

A context manager which suppresses given exceptions under its scope:

```
with suppress(HttpError):
    # Assume this request can fail, and we are ok with it
    make_http_request()

```

nullcontext( _enter\_result=None_) [¶](https://funcy.readthedocs.io/en/stable/flow.html#nullcontext "Permalink to this definition")

A noop context manager that returns `enter_result` from `__enter__`:

```
ctx = nullcontext()
if threads:
    ctx = op_thread_lock

with ctx:
    # ... do stuff

```

@once [¶](https://funcy.readthedocs.io/en/stable/flow.html#once "Permalink to this definition")@once\_per\_args [¶](https://funcy.readthedocs.io/en/stable/flow.html#once_per_args "Permalink to this definition")@once\_per( _\*argnames_) [¶](https://funcy.readthedocs.io/en/stable/flow.html#once_per "Permalink to this definition")

Call function only once, once for every combination of values of its arguments or once for every combination of given arguments. Thread safe. Handy for various initialization purposes:

```
# Global initialization
@once
def initialize_cache():
    conn = some.Connection(...)
    # ... set up everything

# Per argument initialization
@once_per_args
def initialize_language(lang):
    conf = load_language_conf(lang)
    # ... set up language

# Setup each class once
class SomeManager(Manager):
    @once_per('cls')
    def _initialize_class(self, cls):
        pre_save.connect(self._pre_save, sender=cls)
        # ... set up signals, no dups

```

raiser( _exception\_or\_class=Exception_, _\*args_, _\*\*kwargs_) [¶](https://funcy.readthedocs.io/en/stable/flow.html#raiser "Permalink to this definition")

Constructs function that raises given exception with given arguments on any invocation. You may pass a string instead of exception as a shortcut:

```
mocker.patch('mod.Class.propname', property(raiser("Shouldn't be called")))

```

This will raise an `Exception` with a corresponding message.

@reraise( _errors_, _into_) [¶](https://funcy.readthedocs.io/en/stable/flow.html#reraise "Permalink to this definition")

Intercepts any error of `errors` classes and reraises it as `into` error. Can be used as decorator or a context manager:

```
with reraise(json.JSONDecodeError, SuspiciousOperation('Invalid JSON')):
    return json.loads(text)

```

`into` can also be a callable to transform the error before reraising:

```
@reraise(requests.RequestsError, lambda e: MyAPIError(error_desc(e)))
def api_call(...):
    # ...

```

@retry( _tries_, _errors=Exception_, _timeout=0_, _filter\_errors=None_) [¶](https://funcy.readthedocs.io/en/stable/flow.html#retry "Permalink to this definition")

Every call of the decorated function is tried up to `tries` times. The first attempt counts as a try. Retries occur when any subclass of `errors` is raised, where\`\`errors\`\` is an exception class or a list/tuple of exception classes. There will be a delay in `timeout` seconds between tries.

A common use is to wrap some unreliable action:

```
@retry(3, errors=HttpError)
def download_image(url):
    # ... make http request
    return image

```

Errors to retry may addtionally be filtered with `filter_errors` when classes are not specific enough:

```
@retry(3, errors=HttpError, filter_errors=lambda e: e.status_code >= 500)
def download_image(url):
    # ...

```

You can pass a callable as `timeout` to achieve exponential delays or other complex behavior:

```
@retry(3, errors=HttpError, timeout=lambda a: 2 ** a)
def download_image(url):
    # ... make http request
    return image

```

fallback( _\*approaches_) [¶](https://funcy.readthedocs.io/en/stable/flow.html#fallback "Permalink to this definition")

Tries several approaches until one works. Each approach is either callable or a tuple `(callable, errors)`, where errors is an exception class or a tuple of classes, which signal to fall back to next approach. If `errors` is not supplied then fall back is done for any `Exception`:

```
fallback(
    (partial(send_mail, ADMIN_EMAIL, message), SMTPException),
    partial(log.error, message),          # Handle any Exception
    (raiser(FeedbackError, "Failed"), ()) # Handle nothing
)

```

limit\_error\_rate( _fails_, _timeout_, _exception=ErrorRateExceeded_) [¶](https://funcy.readthedocs.io/en/stable/flow.html#limit_error_rate "Permalink to this definition")

If function fails to complete `fails` times in a row, calls to it will be intercepted for `timeout` with `exception` raised instead. A clean way to short-circuit function taking too long to fail:

```
@limit_error_rate(fails=5, timeout=60,
                  exception=RequestError('Temporary unavailable'))
def do_request(query):
    # ... make a http request
    return data

```

Can be combined with [`ignore()`](https://funcy.readthedocs.io/en/stable/flow.html#ignore) to silently stop trying for a while:

```
@ignore(ErrorRateExceeded, default={'id': None, 'name': 'Unknown'})
@limit_error_rate(fails=5, timeout=60)
def get_user(id):
    # ... make a http request
    return data

```

throttle( _period_) [¶](https://funcy.readthedocs.io/en/stable/flow.html#throttle "Permalink to this definition")

Only runs a decorated function once in a `period`:

```
@throttle(60)
def process_beat(pk, progress):
    Model.objects.filter(pk=pk).update(beat=timezone.now(), progress=progress)

# Processing something, update progress info no more often then once a minute
for i in ...:
    process_beat(pk, i / n)
    # ... do actual processing

```

@collecting [¶](https://funcy.readthedocs.io/en/stable/flow.html#collecting "Permalink to this definition")

Transforms generator or other iterator returning function into list returning one.

Handy to prevent quirky iterator-returning properties:

```
@property
@collecting
def path_up(self):
    node = self
    while node:
        yield node
        node = node.parent

```

Also makes list constructing functions beautifully yielding.

@joining( _sep_) [¶](https://funcy.readthedocs.io/en/stable/flow.html#joining "Permalink to this definition")

Wraps common python idiom “collect then join” into a decorator. Transforms generator or alike into function, returning string of joined results. Automatically converts all elements to separator type for convenience.

Goes well with generators with some ad-hoc logic within:

```
@joining(', ')
def car_desc(self):
    yield self.year_made
    if self.engine_volume: yield '%s cc' % self.engine_volume
    if self.transmission:  yield self.get_transmission_display()
    if self.gear:          yield self.get_gear_display()
    # ...

```

Use `bytes` separator to get bytes result:

```
@joining(b' ')
def car_desc(self):
    yield self.year_made
    # ...

```

See also [`str_join()`](https://funcy.readthedocs.io/en/stable/strings.html#str_join).

@post\_processing( _func_) [¶](https://funcy.readthedocs.io/en/stable/flow.html#post_processing "Permalink to this definition")

Passes decorated function result through `func`. This is the generalization of [`@collecting`](https://funcy.readthedocs.io/en/stable/flow.html#collecting) and [`@joining()`](https://funcy.readthedocs.io/en/stable/flow.html#joining). Could save you writing a decorator or serve as an extended comprehension:

```
@post_processing(dict)
def make_cond(request):
    if request.GET['new']:
        yield 'year__gt', 2000
    for key, value in request.GET.items():
        if value == '':
            continue
        # ...

```

@wrap\_with( _ctx_) [¶](https://funcy.readthedocs.io/en/stable/flow.html#wrap_with "Permalink to this definition")

Turns a context manager into a decorator:

```
@wrap_with(threading.Lock())
def protected_func(...):
    # ...

```

**count _(start=0, step=1)_**

Makes infinite iterator of values:

`start, start + step, start + 2*step, ...`

**cycle _(seq)_**

Cycles passed sequence indefinitely

yielding its elements one by one.

**repeat _(item\[, n\])_**

Makes an iterator yielding _item_ for _n_ times

or indefinitely if _n_ is omitted.

**repeatedly _(f\[, n\])_**

Takes a function of no args, presumably with side effects,

and returns an infinite (or length _n_) iterator of calls to it.

**iterate _(f, x)_**

Returns an infinite iterator of `x, f(x), f(f(x)), ...`

**re\_all _(regex, s, flags=0)_**

Lists all matches of _regex_ in _s_.

**re\_iter _(regex, s, flags=0)_**

Iterates over matches of _regex_ in _s_.

**first _(seq)_**

Returns the first item in the sequence.

Returns `None` if the sequence is empty.

**second _(seq)_**

Returns second item in the sequence.

Returns `None` if there are less than two items in it.

**last _(seq)_**

Returns the last item in the sequence.

Returns `None` if the sequence is empty.

**nth _(n, seq)_**

Returns nth item in the sequence

or `None` if no such item exists.

**some _(\[pred, \]seq)_**

Finds first item in _seq_ passing _pred_

or first that is true if _pred_ is omitted.

**take _(n, seq)_**

Returns a list of first _n_ items in the sequence,

or all items if there are fewer than _n_.

**drop _(n, seq)_**

Skips first _n_ items in the sequence,

yields the rest.

**rest _(seq)_**

Skips first item in the sequence, yields the rest.

**butlast _(seq)_**

Yields all elements of the sequence but last.

**takewhile _(\[pred, \]seq)_**

Yields _seq_ items as long as they pass _pred_.

**dropwhile _(\[pred, \]seq)_**

Skips elements of _seq_ while _pred_ passes

and then yields the rest.

**split\_at _(n, seq)_**

**lsplit\_at _(n, seq)_**

Splits the sequence at given position,

returning a tuple of its start and tail.

**split\_by _(pred, seq)_**

**lsplit\_by _(pred, seq)_**

Splits the start of the sequence,

consisting of items passing _pred_,

from the rest of it.

**map _(f, \*seqs)_**

**lmap _(f, \*seqs)_**

Extended versions of **map()** and **list(map())**

**mapcat _(f, \*seqs)_**

**lmapcat _(f, \*seqs)_**

Maps given sequence(s) and concatenates the results.

**keep _(\[f, \]\*seqs)_**

**lkeep _(\[f, \]\*seqs)_**

Maps _seq_ with _f_ and filters out falsy results.

Simply removes falsy values in one argument version.

**pluck _(key, mappings)_**

**lpluck _(key, mappings)_**

Yields or lists values for _key_ in each mapping.

**pluck\_attr _(attr, objects)_**

**lpluck\_attr _(attr, objects)_**

Yields or lists values of _attr_ of each object.

**invoke _(objects, name, \*args, \*\*kwargs)_**

**linvoke _(objects, name, \*args, \*\*kwargs)_**

Yields or lists results of the given method call

for each object in _objects_.

**@wrap\_prop _(ctx)_**

Wrap a property accessors with _ctx_.

**filter _(pred, seq)_**

**lfilter _(pred, seq)_**

Extended versions of **filter()** and **list(filter())**.

**remove _(pred, seq)_**

**lremove _(pred, seq)_**

Removes items from _seq_ passing given predicate.

**distinct _(seq, key=identity)_**

**ldistinct _(seq, key=identity)_**

Removes items having same _key_ from _seq_.

Preserves order.

**where _(mappings, \*\*cond)_**

**lwhere _(mappings, \*\*cond)_**

Selects _mappings_ containing all pairs in _cond_.

**without _(seq, \*items)_**

**lwithout _(seq, \*items)_**

Returns sequence without _items_,

preserves order.

**cat _(seqs)_**

**lcat _(seqs)_**

Concatenates passed sequences.

**concat _(\*seqs)_**

**lconcat _(\*seqs)_**

Concatenates several sequences.

**flatten _(seq, follow=is\_seqcont)_**

**lflatten _(seq, follow=is\_seqcont)_**

Flattens arbitrary nested sequence,

dives into when `follow(item)` is truthy.

**interleave _(\*seqs)_**

Yields first item of each sequence,

then second one and so on.

**interpose _(sep, seq)_**

Yields items of _seq_ separated by _sep_.

**lzip _(\*seqs)_**

List version of **zip()**

**chunks _(n, \[step, \]seq)_**

**lchunks _(n, \[step, \]seq)_**

Chunks _seq_ into parts of length _n_ or less.

Skips _step_ items between chunks.

**partition _(n, \[step, \]seq)_**

**lpartition _(n, \[step, \]seq)_**

Partitions _seq_ into parts of length _n_.

Skips _step_ items between parts.

Non-fitting tail is ignored.

**partition\_by _(f, seq)_**

**lpartition\_by _(f, seq)_**

Partition _seq_ into continuous chunks

with constant value of _f_.

**split _(pred, seq)_**

**lsplit _(pred, seq)_**

Splits _seq_ items which pass _pred_

from the ones that don't.

**count\_by _(f, seq)_**

Counts numbers of occurrences of values of _f_

on elements of _seq_.

**count\_reps _(seq)_**

Counts repetitions of each value in _seq_.

**group\_by _(f, seq)_**

Groups items of _seq_ by `f(item)`.

**group\_by\_keys _(get\_keys, seq)_**

Groups elements of _seq_ by multiple keys.

**group\_values _(seq)_**

Groups values of `(key, value)` pairs by keys.

**ilen _(seq)_**

Consumes the given iterator and returns its length.

**reductions _(f, seq\[, acc\])_**

**lreductions _(f, seq\[, acc\])_**

Constructs intermediate reductions of _seq_ by _f_.

**sums _(seq\[, acc\])_**

**lsums _(seq\[, acc\])_**

Returns a sequence of partial sums of _seq_.

**all _(\[pred, \]seq)_**

Checks if all items in _seq_ pass _pred_.

**any _(\[pred, \]seq)_**

Checks if any item in _seq_ passes _pred_.

**none _(\[pred, \]seq)_**

Checks if none of the items in _seq_ pass _pred_.

**one _(\[pred, \]seq)_**

Checks if exactly one item in _seq_ passes _pred_.

**pairwise _(seq)_**

Yields all pairs of neighboring items in _seq_.

**with\_prev _(seq, fill=None)_**

Yields each item from _seq_ with the one preceding it.

**with\_next _(seq, fill=None)_**

Yields each item from _seq_ with the next one.

**zip\_values _(\*dicts)_**

Yields tuples of corresponding values of given _dicts_.

**zip\_dicts _(\*dicts)_**

Yields tuples like `(key, val1, val2, ...)`

for each common key in all given _dicts_.

**tree\_leaves _(root, follow=is\_seqcont, children=iter)_**

**ltree\_leaves _(root, follow=is\_seqcont, children=iter)_**

Lists or iterates over tree leaves.

**tree\_nodes _(root, follow=is\_seqcont, children=iter)_**

**ltree\_nodes _(root, follow=is\_seqcont, children=iter)_**

Lists or iterates over tree nodes.

**merge _(\*colls)_**

Merges several collections of same type into one:

dicts, sets, lists, tuples, iterators or strings

For dicts later values take precedence.

**merge\_with _(f, \*dicts)_**

Merges several _dicts_ combining values with given function.

**join _(colls)_**

Joins several collections of same type into one.

Same as **merge()** but accepts sequence of collections.

**join\_with _(f, \*dicts)_**

Joins several _dicts_ combining values with given function.

**walk _(f, coll)_**

Maps _coll_ with _f_, but preserves collection type.

**walk\_keys _(f, coll)_**

Walks keys of _coll_, mapping them with _f_.

Works with dicts and collections of pairs.

**walk\_values _(f, coll)_**

Walks values of _coll_, mapping them with _f_.

Works with dicts and collections of pairs.

**select _(pred, coll)_**

Filters elements of _coll_ by _pred_

constructing a collection of same type.

**select\_keys _(pred, coll)_**

Select part of _coll_ with keys passing _pred_.

Works with dicts and collections of pairs.

**select\_values _(pred, coll)_**

Select part of _coll_ with values passing _pred_.

Works with dicts and collections of pairs.

**compact _(coll)_**

Removes falsy values from given collection.

All collections functions work with dicts.

These are targeted specifically at them.

**flip _(mapping)_**

Flip passed dict swapping its keys and values.

**zipdict _(keys, vals)_**

Creates a dict with _keys_ mapped to the corresponding _vals_.

**itervalues _(coll)_**

Yields values of the given collection.

**iteritems _(coll)_**

Yields `(key, value)` pairs of the given collection.

**project _(mapping, keys)_**

Leaves only given keys in _mapping_.

**omit _(mapping, keys)_**

Removes given keys from _mapping_.

**empty _(coll)_**

Returns an empty collection of the same type as _coll_.

**get\_in _(coll, path, default=None)_**

Returns a value at _path_ in the given nested collection.

**get\_lax _(coll, path, default=None)_**

Returns a value at _path_ in the given nested collection.

Ignores `TypeError` s.

**set\_in _(coll, path, value)_**

Creates a copy of _coll_ with the _value_ set at _path_.

**update\_in _(coll, path, update, default=None)_**

Creates a copy of _coll_ with a value updated at _path_.

**del\_in _(coll, path)_**

Creates a copy of _coll_ with _path_ removed.

**has\_path _(coll, path)_**

Tests whether _path_ exists in a nested _coll_.

Most of functions in this section support extended semantics.

**identity _(x)_**

Returns its argument.

**constantly _(x)_**

Creates a function accepting any args, but always returning _x_.

**func\_partial _(func, \*args, \*\*kwargs)_**

Like **partial()** but returns a real function.

**partial _(func, \*args, \*\*kwargs)_**

Returns partial application of _func_.

**rpartial _(func, \*args)_**

Partially applies last arguments to _func_.

**iffy _(\[pred, \]action\[, default=identity\])_**

Creates a function, which conditionally applies _action_ or _default_.

**caller _(\*args, \*\*kwargs)_**

Creates a function calling its argument with passed arguments.

**re\_finder _(regex, flags=0)_**

Creates a function finding _regex_ in passed string.

**re\_tester _(regex, flags=0)_**

Creates a predicate testing passed strings with _regex_.

**complement _(pred)_**

Constructs a complementary predicate.

**autocurry _(func)_**

Creates a version of _func_ returning its partial applications

until sufficient arguments are passed.

**curry _(func\[, n\])_**

Curries _func_ into a chain of one argument functions.

Arguments are passed from left to right.

**rcurry _(func\[, n\])_**

Curries _func_ from right to left.

**compose _(\*fs)_**

Composes passed functions.

**rcompose _(\*fs)_**

Composes _fs_, calling them from left to right.

**juxt _(\*fs)_**

**ljuxt _(\*fs)_**

Constructs a juxtaposition of the given functions.

Result returns a list or an iterator of results of _fs_.

**all\_fn _(\*fs)_**

Constructs a predicate,

which holds when all _fs_ hold.

**any\_fn _(\*fs)_**

Constructs a predicate,

which holds when any of _fs_ holds.

**none\_fn _(\*fs)_**

Constructs a predicate,

which holds when none of _fs_ hold.

**one\_fn _(\*fs)_**

Constructs a predicate,

which holds when exactly one of _fs_ holds.

**some\_fn _(\*fs)_**

Constructs a function, which calls _fs_ one by one

and returns first truthy result.

**is\_distinct _(\*fs)_**

Checks if all elements in the collection are different.

**isa _(\*types)_**

Creates a function checking if its argument

is of any of given _types_.

**is\_iter _(value)_**

Checks whether _value_ is an iterator.

**is\_mapping _(value)_**

Checks whether _value_ is a mapping.

**is\_set _(value)_**

Checks whether _value_ is a set.

**is\_list _(value)_**

Checks whether _value_ is a list.

**is\_tuple _(value)_**

Checks whether _value_ is a tuple.

**is\_seq _(value)_**

Checks whether _value_ is a `Sequence`.

**is\_mapping _(value)_**

Checks whether _value_ is a mapping.

**is\_seqcoll _(value)_**

Checks whether _value_ is a list or a tuple,

which are both sequences and collections.

**is\_seqcont _(value)_**

Checks whether _value_ is a list, a tuple or an iterator,

which are both sequences and containers.

**iterable _(value)_**

Checks whether _value_ is iterable.

**@decorator**

Transforms a flat wrapper into a decorator.

**@wraps**

An utility to pass function metadata

from wrapped function to a wrapper.

**unwrap _(func)_**

Get the object wrapped by _func_.

**@once**

Let function execute only once.

Noop all subsequent calls.

**@once\_per _(\*argnames)_**

Call function only once for every combination

of the given arguments.

**@once\_per\_args**

Call function only once for every combination

of values of its arguments.

**@collecting**

Transforms a generator into list returning function.

**@joining _(sep)_**

Joins decorated function results with _sep_.

**@post\_processing _(func)_**

Post processes decorated function result with _func_.

**@throttle _(period)_**

Only runs a decorated function once per _period_.

**@wrap\_with _(ctx)_**

Turn context manager into a decorator.

**nullcontext _(enter\_result=None)_**

A noop context manager.

**@retry _(tries, errors=Exception, timeout=0, filter\_errors=None)_**

Tries decorated function up to _tries_ times.

Retries only on specified _errors_.

**@silent**

Alters function to ignore all exceptions.

**@ignore _(errors, default=None)_**

Alters function to ignore _errors_,

returning _default_ instead.

**suppress _(\*errors)_**

The context manager suppressing _errors_ in its block.

**@limit\_error\_rate _(fails, timeout, ...)_**

If function fails to complete _fails_ times in a row,

calls to it will be blocked for _timeout_ seconds.

**fallback _(\*approaches)_**

Tries several approaches until one works.

Each approach has a form of `(callable, errors)`.

**raiser _(exception=Exception, \*args, \*\*kwargs)_**

Constructs function that raises the given exception

with given arguments on any invocation.

**@reraise _(errors, into)_**

Intercepts _errors_ and reraises them as _into_ exception.

**tap _(x, label=None)_**

Prints _x_ and then returns it.

**@log\_calls _(print\_func, errors=True, stack=True)_**

**@print\_calls _(errors=True, stack=True)_**

Logs or prints all function calls,

including arguments, results and raised exceptions.

**@log\_enters _(print\_func)_**

**@print\_enters**

Logs or prints on each enter to a function.

**@log\_exits _(print\_func, errors=True, stack=True)_**

**@print\_exits _(errors=True, stack=True)_**

Logs or prints on each exit from a function.

**@log\_errors _(print\_func, label=None, stack=True)_**

**@print\_errors _(label=None, stack=True)_**

Logs or prints all errors within a function or block.

**@log\_durations _(print\_func, label=None)_**

**@print\_durations _(label=None)_**

Times each function call or block execution.

**log\_iter\_durations _(seq, print\_func, label=None)_**

**print\_iter\_durations _(seq, label=None)_**

Times processing of each item in _seq_.

**@memoize _(\*, key\_func=None)_**

Memoizes a decorated function results.

**@cache _(timeout, \*, key\_func=None)_**

Caches a function results for _timeout_ seconds.

**@cached\_property**

Creates a property caching its result.

**@cached\_readonly**

Creates a read-only property caching its result.

**@make\_lookuper**

Creates a cached function with prefilled memory.

**@silent\_lookuper**

Creates a cached function with prefilled memory.

Ignores memory misses, returning `None`.

**re\_find _(regex, s, flags=0)_**

Matches _regex_ against the given string,

returns the match in the simplest possible form.

**re\_test _(regex, s, flags=0)_**

Tests whether _regex_ matches against _s_.

**cut\_prefix _(s, prefix)_**

Cuts prefix from given string if it's present.

**cut\_suffix _(s, suffix)_**

Cuts suffix from given string if it's present.

**str\_join _(\[sep="", \]seq)_**

Joins the given sequence with _sep_.

Forces stringification of _seq_ items.

**@monkey _(cls\_or\_module, name=None)_**

Monkey-patches class or module.

class **LazyObject _(init)_**

Creates an object setting itself up on first use.

**isnone _(x)_**

Checks if _x_ is _None_.

**notnone _(x)_**

Checks if _x_ is not _None_.

**inc _(x)_**

Increments its argument by 1.

**dec _(x)_**

Decrements its argument by 1.

**even _(x)_**

Checks if _x_ is even.

**odd _(x)_**

Checks if _x_ is odd.

Versions[latest](https://funcy.readthedocs.io/en/latest/flow.html)**[stable](https://funcy.readthedocs.io/en/stable/flow.html)**[2.0](https://funcy.readthedocs.io/en/2.0/flow.html)[1.18](https://funcy.readthedocs.io/en/1.18/flow.html)[1.17](https://funcy.readthedocs.io/en/1.17/flow.html)[1.16](https://funcy.readthedocs.io/en/1.16/flow.html)[1.15](https://funcy.readthedocs.io/en/1.15/flow.html)[1.14](https://funcy.readthedocs.io/en/1.14/flow.html)[1.13](https://funcy.readthedocs.io/en/1.13/flow.html)[1.11](https://funcy.readthedocs.io/en/1.11/flow.html)[1.10.3](https://funcy.readthedocs.io/en/1.10.3/flow.html)[1.10.2](https://funcy.readthedocs.io/en/1.10.2/flow.html)[1.10.1](https://funcy.readthedocs.io/en/1.10.1/flow.html)[1.10](https://funcy.readthedocs.io/en/1.10/flow.html)[1.9](https://funcy.readthedocs.io/en/1.9/flow.html)[1.8](https://funcy.readthedocs.io/en/1.8/flow.html)[1.7.5](https://funcy.readthedocs.io/en/1.7.5/flow.html)[1.7.4](https://funcy.readthedocs.io/en/1.7.4/flow.html)[1.7.3](https://funcy.readthedocs.io/en/1.7.3/flow.html)[1.7.2](https://funcy.readthedocs.io/en/1.7.2/flow.html)[1.7.1](https://funcy.readthedocs.io/en/1.7.1/flow.html)[1.7](https://funcy.readthedocs.io/en/1.7/flow.html)[1.6](https://funcy.readthedocs.io/en/1.6/flow.html)[1.5](https://funcy.readthedocs.io/en/1.5/flow.html)[1.4](https://funcy.readthedocs.io/en/1.4/flow.html)[1.3](https://funcy.readthedocs.io/en/1.3/flow.html)[1.1](https://funcy.readthedocs.io/en/1.1/flow.html)[1.0.0](https://funcy.readthedocs.io/en/1.0.0/flow.html)[0.10.1](https://funcy.readthedocs.io/en/0.10.1/flow.html)On Read the Docs[Project Home](https://app.readthedocs.org/projects/funcy/?utm_source=funcy&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/funcy/builds/?utm_source=funcy&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=funcy&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=funcy&utm_content=flyout)