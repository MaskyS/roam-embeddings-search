---
url: "https://funcy.readthedocs.io/en/stable/colls.html"
title: "Collections — funcy 2.0 documentation"
---

- »
- Collections
- [Edit on GitHub](https://github.com/Suor/funcy/blob/13fac0037c109a9e4649fc8ee343be17647f7407/docs/colls.rst)

* * *

# Collections [¶](https://funcy.readthedocs.io/en/stable/colls.html\#collections "Permalink to this headline")

## Unite [¶](https://funcy.readthedocs.io/en/stable/colls.html\#unite "Permalink to this headline")

merge( _\*colls_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#merge "Permalink to this definition")

Merges several collections of same type into one: dicts, sets, lists, tuples, iterators or strings. For dicts values of later dicts override values of former ones with same keys.

Can be used in variety of ways, but merging dicts is probably most common:

```
def utility(**options):
    defaults = {...}
    options = merge(defaults, options)
    ...

```

If you merge sequences and don’t need to preserve collection type, then use [`concat()`](https://funcy.readthedocs.io/en/stable/seqs.html#concat) or [`lconcat()`](https://funcy.readthedocs.io/en/stable/seqs.html#lconcat) instead.

join( _colls_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#join "Permalink to this definition")

Joins collections of same type into one. Same as [`merge()`](https://funcy.readthedocs.io/en/stable/colls.html#merge), but accepts iterable of collections.

Use [`cat()`](https://funcy.readthedocs.io/en/stable/seqs.html#cat) and [`lcat()`](https://funcy.readthedocs.io/en/stable/seqs.html#lcat) for non-type preserving sequence join.

## Transform and select [¶](https://funcy.readthedocs.io/en/stable/colls.html\#transform-and-select "Permalink to this headline")

All functions in this section support [Extended function semantics](https://funcy.readthedocs.io/en/stable/extended_fns.html#extended-fns).

walk( _f_, _coll_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#walk "Permalink to this definition")

Returns a collection of same type as `coll` consisting of its elements mapped with the given function:

```
walk(inc, {1, 2, 3}) # -> {2, 3, 4}
walk(inc, (1, 2, 3)) # -> (2, 3, 4)

```

When walking dict, `(key, value)` pairs are mapped, i.e. this lines [`flip()`](https://funcy.readthedocs.io/en/stable/colls.html#flip) dict:

```
swap = lambda (k, v): (v, k)
walk(swap, {1: 10, 2: 20})

```

[`walk()`](https://funcy.readthedocs.io/en/stable/colls.html#walk) works with strings too:

```
walk(lambda x: x * 2, 'ABC')   # -> 'AABBCC'
walk(compose(str, ord), 'ABC') # -> '656667'

```

One should use [`map()`](https://funcy.readthedocs.io/en/stable/seqs.html#map) when there is no need to preserve collection type.

walk\_keys( _f_, _coll_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#walk_keys "Permalink to this definition")

Walks keys of `coll`, mapping them with the given function. Works with mappings and collections of pairs:

```
walk_keys(str.upper, {'a': 1, 'b': 2}) # {'A': 1, 'B': 2}
walk_keys(int, json.loads(some_dict))  # restore key type lost in translation

```

Important to note that it preserves collection type whenever this is simple [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.11)"), [`defaultdict`](https://docs.python.org/3/library/collections.html#collections.defaultdict "(in Python v3.11)"), [`OrderedDict`](https://docs.python.org/3/library/collections.html#collections.OrderedDict "(in Python v3.11)") or any other mapping class or a collection of pairs.

walk\_values( _f_, _coll_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#walk_values "Permalink to this definition")

Walks values of `coll`, mapping them with the given function. Works with mappings and collections of pairs.

Common use is to process values somehow:

```
clean_values = walk_values(int, form_values)
sorted_groups = walk_values(sorted, groups)

```

Hint: you can use [`partial(sorted, key=...)`](https://funcy.readthedocs.io/en/stable/funcs.html#partial) instead of [`sorted()`](https://docs.python.org/3/library/functions.html#sorted "(in Python v3.11)") to sort in non-default way.

Note that `walk_values()` has special handling for [`defaultdicts`](https://docs.python.org/3/library/collections.html#collections.defaultdict "(in Python v3.11)"). It constructs new one with values mapped the same as for ordinary dict, but a default factory of new `defaultdict` would be a composition of `f` and old default factory:

```
d = defaultdict(lambda: 'default', a='hi', b='bye')
walk_values(str.upper, d)
# -> defaultdict(lambda: 'DEFAULT', a='HI', b='BYE')

```

select( _pred_, _coll_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#select "Permalink to this definition")

Filters elements of `coll` by `pred` constructing a collection of same type. When filtering a dict `pred` receives `(key, value)` pairs. See [`select_keys()`](https://funcy.readthedocs.io/en/stable/colls.html#select_keys) and [`select_values()`](https://funcy.readthedocs.io/en/stable/colls.html#select_values) to filter it by keys or values respectively:

```
select(even, {1, 2, 3, 10, 20})
# -> {2, 10, 20}

select(lambda (k, v): k == v, {1: 1, 2: 3})
# -> {1: 1}

```

select\_keys( _pred_, _coll_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#select_keys "Permalink to this definition")

Select part of a dict or a collection of pairs with keys passing the given predicate.

This way a public part of instance attributes dictionary could be selected:

```
is_public = complement(re_tester('^_'))
public = select_keys(is_public, instance.__dict__)

```

select\_values( _pred_, _coll_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#select_values "Permalink to this definition")

Select part of a dict or a collection of pairs with values passing the given predicate:

```
# Leave only str values
select_values(isa(str), values)

# Construct a dict of methods
select_values(inspect.isfunction, cls.__dict__)

```

compact( _coll_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#compact "Permalink to this definition")

Removes falsy values from given collection. When compacting a dict all keys with falsy values are removed.

Extract integer data from request:

```
compact(walk_values(silent(int), request_dict))

```

## Dict utils [¶](https://funcy.readthedocs.io/en/stable/colls.html\#dict-utils "Permalink to this headline")

merge\_with( _f_, _\*dicts_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#merge_with "Permalink to this definition")join\_with( _f_, _dicts_, _strict=False_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#join_with "Permalink to this definition")

Merge several dicts combining values for same key with given function:

```
merge_with(list, {1: 1}, {1: 10, 2: 2})
# -> {1: [1, 10], 2: [2]}

merge_with(sum, {1: 1}, {1: 10, 2: 2})
# -> {1: 11, 2: 2}

join_with(first, ({n % 3: n} for n in range(100, 110)))
# -> {0: 102, 1: 100, 2: 101}

```

Historically `join_with()` will return a dict as is if there is only one, which might be inconvenient. To always apply the summarization func use `strict` param:

```
join_with(list, [{1: 2}])              # {1: 2}
join_with(list, [{1: 2}], strict=True) # {1: [2]}
join_with(len, [{1: 2}], strict=True)  # {1: 1}

```

zipdict( _keys_, _vals_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#zipdict "Permalink to this definition")

Returns a dict with the `keys` mapped to the corresponding `vals`. Stops pairing on shorter sequence end:

```
zipdict('abcd', range(4))
# -> {'a': 0, 'b': 1, 'c': 2, 'd': 3}

zipdict('abc', count())
# -> {'a': 0, 'b': 1, 'c': 2}

```

flip( _mapping_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#flip "Permalink to this definition")

Flip passed dict swapping its keys and values. Also works for sequences of pairs. Preserves collection type:

```
flip(OrderedDict(['aA', 'bB']))
# -> OrderedDict([('A', 'a'), ('B', 'b')])

```

project( _mapping_, _keys_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#project "Permalink to this definition")

Returns a dict containing only those entries in `mapping` whose key is in `keys`.

Most useful to shrink some common data or options to predefined subset. One particular case is constructing a dict of used variables:

```
merge(project(__builtins__, names), project(globals(), names))

```

omit( _mapping_, _keys_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#omit "Permalink to this definition")

Returns a copy of `mapping` with `keys` omitted. Preserves collection type:

```
omit({'a': 1, 'b': 2, 'c': 3}, 'ac')
# -> {'b': 2}

```

zip\_values( _\*dicts_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#zip_values "Permalink to this definition")

Yields tuples of corresponding values of given dicts. Skips any keys not present in all of the dicts. Comes in handy when comparing two or more dicts:

```
error = sum((x - y) ** 2 for x, y in zip_values(result, reference))

```

zip\_dicts( _\*dicts_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#zip_dicts "Permalink to this definition")

Yields tuples like `key, (value1, value2, ...)` for each common key of all given dicts. A neat way to process several dicts at once:

```
changed_items = [id for id, (new, old) in zip_dicts(items, old_items)\
                 if abs(new - old) >= PRECISION]

lines = {id: cnt * price for id, (cnt, price) in zip_dicts(amounts, prices)}

```

See also [`zip_values()`](https://funcy.readthedocs.io/en/stable/colls.html#zip_values).

get\_in( _coll_, _path_, _default=None_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#get_in "Permalink to this definition")

Returns a value corresponding to `path` in nested collection:

```
get_in({"a": {"b": 42}}, ["a", "b"])    # -> 42
get_in({"a": {"b": 42}}, ["c"], "foo")  # -> "foo"

```

Note that missing key or index, i.e. KeyError and IndexError result into default being return, while trying to use non-int index for a list will result into TypeError. This way funcy stays strict on types.

get\_lax( _coll_, _path_, _default=None_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#get_lax "Permalink to this definition")

A version of [`get_in()`](https://funcy.readthedocs.io/en/stable/colls.html#get_in) that tolerates type along the path not working with an index:

```
get_lax([1, 2, 3], ["a"], "foo")  # -> "foo"
get_lax({"a": None}, ["a", "b"])  # -> None

```

set\_in( _coll_, _path_, _value_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#set_in "Permalink to this definition")

Creates a nested collection with the `value` set at specified `path`. Original collection is not changed:

```
set_in({"a": {"b": 42}}, ["a", "b"], 10)
# -> {"a": {"b": 10}}

set_in({"a": {"b": 42}}, ["a", "c"], 10)
# -> {"a": {"b": 42, "c": 10}}

```

update\_in( _coll_, _path_, _update_, _default=None_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#update_in "Permalink to this definition")

Creates a nested collection with a value at specified `path` updated:

```
update_in({"a": {}}, ["a", "cnt"], inc, default=0)
# -> {"a": {"cnt": 1}}

```

del\_in( _coll_, _path_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#del_in "Permalink to this definition")

Creates a nested collection with `path` removed:

```
del_in({"a": [1, 2, 3]}, ["a", 1])
# -> {"a": [1, 3]}

```

Returns the collection as is if the path is missing.

has\_path( _coll_, _path_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#has_path "Permalink to this definition")

Checks if path exists in the given nested collection:

```
has_path({"a": {"b": 42}}, ["a", "b"]) # -> True
has_path({"a": {"b": 42}}, ["c"])  # -> False
has_path({"a": [1, 2]}, ["a", 0])  # -> True

```

## Data manipulation [¶](https://funcy.readthedocs.io/en/stable/colls.html\#data-manipulation "Permalink to this headline")

where( _mappings_, _\*\*cond_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#where "Permalink to this definition")lwhere( _mappings_, _\*\*cond_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#lwhere "Permalink to this definition")

Looks through each value in given sequence of dicts and returns an iterator or a list of all the dicts that contain all key-value pairs in `cond`:

```
lwhere(plays, author="Shakespeare", year=1611)
# => [{"title": "Cymbeline", "author": "Shakespeare", "year": 1611},\
#     {"title": "The Tempest", "author": "Shakespeare", "year": 1611}]

```

Iterator version could be used for efficiency or when you don’t need the whole list.
E.g. you are looking for the first match:

```
first(where(plays, author="Shakespeare"))
# => {"title": "The Two Gentlemen of Verona", ...}

```

pluck( _key_, _mappings_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#pluck "Permalink to this definition")lpluck( _key_, _mappings_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#lpluck "Permalink to this definition")

Returns an iterator or a list of values for `key` in each mapping in the given sequence. Essentially a shortcut for:

```
map(operator.itemgetter(key), mappings)

```

pluck\_attr( _attr_, _objects_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#pluck_attr "Permalink to this definition")lpluck\_attr( _attr_, _objects_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#lpluck_attr "Permalink to this definition")

Returns an iterator or a list of values for `attr` in each object in the given sequence. Essentially a shortcut for:

```
map(operator.attrgetter(attr), objects)

```

Useful when dealing with collections of ORM objects:

```
users = User.query.all()
ids = lpluck_attr('id', users)

```

invoke( _objects_, _name_, _\*args_, _\*\*kwargs_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#invoke "Permalink to this definition")linvoke( _objects_, _name_, _\*args_, _\*\*kwargs_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#linvoke "Permalink to this definition")

Calls named method with given arguments for each object in `objects` and returns an iterator or a list of results.

## Content tests [¶](https://funcy.readthedocs.io/en/stable/colls.html\#content-tests "Permalink to this headline")

is\_distinct( _coll_, _key=identity_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#is_distinct "Permalink to this definition")

Checks if all elements in the collection are different:

```
assert is_distinct(field_names), "All fields should be named differently"

```

Uses `key` to differentiate values. This way one can check if all first letters of `words` are different:

```
is_distinct(words, key=0)

```

all(\[ _pred_, \] _seq_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#all "Permalink to this definition")

Checks if `pred` holds for every element in a `seq`. If `pred` is omitted checks if all elements of `seq` are truthy – same as in built-in [`all()`](https://docs.python.org/3/library/functions.html#all "(in Python v3.11)"):

```
they_are_ints = all(is_instance(n, int) for n in seq)
they_are_even = all(even, seq)

```

Note that, first example could be rewritten using [`isa()`](https://funcy.readthedocs.io/en/stable/types.html#isa) like this:

```
they_are_ints = all(isa(int), seq)

```

any(\[ _pred_, \] _seq_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#any "Permalink to this definition")

Returns `True` if `pred` holds for any item in given sequence. If `pred` is omitted checks if any element of `seq` is truthy.

Check if there is a needle in haystack, using [extended predicate semantics](https://funcy.readthedocs.io/en/stable/extended_fns.html#extended-fns):

```
any(r'needle', haystack_strings)

```

none(\[ _pred_, \] _seq_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#none "Permalink to this definition")

Checks if none of items in given sequence pass `pred` or is truthy if `pred` is omitted.

Just a stylish way to write `not any(...)`:

```
assert none(' ' in name for name in names), "Spaces in names not allowed"

# Or same using extended predicate semantics
assert none(' ', names), "..."

```

one(\[ _pred_, \] _seq_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#one "Permalink to this definition")

Returns true if exactly one of items in `seq` passes `pred`. Cheks for truthiness if `pred` is omitted.

some(\[ _pred_, \] _seq_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#some "Permalink to this definition")

Finds first item in `seq` passing `pred` or first that is true if `pred` is omitted.

## Low-level helpers [¶](https://funcy.readthedocs.io/en/stable/colls.html\#low-level-helpers "Permalink to this headline")

empty( _coll_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#empty "Permalink to this definition")

Returns an empty collection of the same type as `coll`.

iteritems( _coll_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#iteritems "Permalink to this definition")

Returns an iterator of items of a `coll`. This means `key, value` pairs for any dictionaries:

```
list(iteritems({1, 2, 42}))
# -> [1, 42, 2]

list(iteritems({'a': 1}))
# -> [('a', 1)]

```

itervalues( _coll_) [¶](https://funcy.readthedocs.io/en/stable/colls.html#itervalues "Permalink to this definition")

Returns an iterator of values of a `coll`. This means values for any dictionaries and just elements for other collections:

```
list(itervalues({1, 2, 42}))
# -> [1, 42, 2]

list(itervalues({'a': 1}))
# -> [1]

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

Versions[latest](https://funcy.readthedocs.io/en/latest/colls.html)**[stable](https://funcy.readthedocs.io/en/stable/colls.html)**[2.0](https://funcy.readthedocs.io/en/2.0/colls.html)[1.18](https://funcy.readthedocs.io/en/1.18/colls.html)[1.17](https://funcy.readthedocs.io/en/1.17/colls.html)[1.16](https://funcy.readthedocs.io/en/1.16/colls.html)[1.15](https://funcy.readthedocs.io/en/1.15/colls.html)[1.14](https://funcy.readthedocs.io/en/1.14/colls.html)[1.13](https://funcy.readthedocs.io/en/1.13/colls.html)[1.11](https://funcy.readthedocs.io/en/1.11/colls.html)[1.10.3](https://funcy.readthedocs.io/en/1.10.3/colls.html)[1.10.2](https://funcy.readthedocs.io/en/1.10.2/colls.html)[1.10.1](https://funcy.readthedocs.io/en/1.10.1/colls.html)[1.10](https://funcy.readthedocs.io/en/1.10/colls.html)[1.9](https://funcy.readthedocs.io/en/1.9/colls.html)[1.8](https://funcy.readthedocs.io/en/1.8/colls.html)[1.7.5](https://funcy.readthedocs.io/en/1.7.5/colls.html)[1.7.4](https://funcy.readthedocs.io/en/1.7.4/colls.html)[1.7.3](https://funcy.readthedocs.io/en/1.7.3/colls.html)[1.7.2](https://funcy.readthedocs.io/en/1.7.2/colls.html)[1.7.1](https://funcy.readthedocs.io/en/1.7.1/colls.html)[1.7](https://funcy.readthedocs.io/en/1.7/colls.html)[1.6](https://funcy.readthedocs.io/en/1.6/colls.html)[1.5](https://funcy.readthedocs.io/en/1.5/colls.html)[1.4](https://funcy.readthedocs.io/en/1.4/colls.html)[1.3](https://funcy.readthedocs.io/en/1.3/colls.html)[1.1](https://funcy.readthedocs.io/en/1.1/colls.html)[1.0.0](https://funcy.readthedocs.io/en/1.0.0/colls.html)[0.10.1](https://funcy.readthedocs.io/en/0.10.1/colls.html)On Read the Docs[Project Home](https://app.readthedocs.org/projects/funcy/?utm_source=funcy&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/funcy/builds/?utm_source=funcy&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=funcy&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=funcy&utm_content=flyout)