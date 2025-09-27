---
url: "https://funcy.readthedocs.io/en/stable/seqs.html"
title: "Sequences — funcy 2.0 documentation"
---

- »
- Sequences
- [Edit on GitHub](https://github.com/Suor/funcy/blob/13fac0037c109a9e4649fc8ee343be17647f7407/docs/seqs.rst)

* * *

# Sequences [¶](https://funcy.readthedocs.io/en/stable/seqs.html\#sequences "Permalink to this headline")

This functions are aimed at manipulating finite and infinite sequences of values. Some functions have two flavors: one returning list and other returning possibly infinite iterator, the latter ones follow convention of prepending `i` before list-returning function name.

When working with sequences, see also [`itertools`](https://docs.python.org/3/library/itertools.html#module-itertools "(in Python v3.11)") standard module. Funcy reexports and aliases some functions from it.

## Generate [¶](https://funcy.readthedocs.io/en/stable/seqs.html\#generate "Permalink to this headline")

repeat( _item_\[, _n_\]) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#repeat "Permalink to this definition")

Makes an iterator yielding `item` for `n` times or indefinitely if `n` is omitted. `repeat` simply repeats given value, when you need to reevaluate something repeatedly use [`repeatedly()`](https://funcy.readthedocs.io/en/stable/seqs.html#repeatedly) instead.

When you just need a length `n` list or tuple of `item` you can use:

```
[item] * n
# or
(item,) * n

```

count( _start=0_, _step=1_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#count "Permalink to this definition")

Makes infinite iterator of values: `start, start + step, start + 2*step, ...`.

Could be used to generate sequence:

```
map(lambda x: x ** 2, count(1))
# -> 1, 4, 9, 16, ...

```

Or annotate sequence using [`zip()`](https://docs.python.org/3/library/functions.html#zip "(in Python v3.11)"):

```
zip(count(), 'abcd')
# -> (0, 'a'), (1, 'b'), (2, 'c'), (3, 'd')

# print code with BASIC-style numbered lines
for line in zip(count(10, 10), code.splitlines()):
    print '%d %s' % line

```

See also [`enumerate()`](https://docs.python.org/3/library/functions.html#enumerate "(in Python v3.11)") and original [`itertools.count()`](https://docs.python.org/3/library/itertools.html#itertools.count "(in Python v3.11)") documentation.

cycle( _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#cycle "Permalink to this definition")

Cycles passed `seq` indefinitely returning its elements one by one.

Useful when you need to cyclically decorate some sequence:

```
for n, parity in zip(count(), cycle(['even', 'odd'])):
    print '%d is %s' % (n, parity)

```

repeatedly( _f_\[, _n_\]) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#repeatedly "Permalink to this definition")

Takes a function of no args, presumably with side effects, and
returns an infinite (or length `n` if supplied) iterator of calls
to it.

For example, this call can be used to generate 10 random numbers:

```
repeatedly(random.random, 10)

```

Or one can create a length `n` list of freshly-created objects of same type:

```
repeatedly(list, n)

```

iterate( _f_, _x_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#iterate "Permalink to this definition")

Returns an infinite iterator of `x, f(x), f(f(x)), ...` etc.

Most common use is to generate some recursive sequence:

```
iterate(inc, 5)
# -> 5, 6, 7, 8, 9, ...

iterate(lambda x: x * 2, 1)
# -> 1, 2, 4, 8, 16, ...

step = lambda p: (p[1], p[0] + p[1])
map(first, iterate(step, (0, 1)))
# -> 0, 1, 1, 2, 3, 5, 8, ... (Fibonacci sequence)

```

## Manipulate [¶](https://funcy.readthedocs.io/en/stable/seqs.html\#manipulate "Permalink to this headline")

This section provides some robust tools for sequence slicing. Consider [Slicings](https://docs.python.org/3/reference/expressions.html#slicings "(in Python v3.11)") or [`itertools.islice()`](https://docs.python.org/3/library/itertools.html#itertools.islice "(in Python v3.11)") for more generic cases.

take( _n_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#take "Permalink to this definition")

Returns a list of the first `n` items in the sequence, or all items if there are fewer than `n`.

```
take(3, [2, 3, 4, 5]) # [2, 3, 4]
take(3, count(5))     # [5, 6, 7]
take(3, 'ab')         # ['a', 'b']

```

drop( _n_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#drop "Permalink to this definition")

Skips first `n` items in the sequence, returning iterator yielding rest of its items.

```
drop(3, [2, 3, 4, 5]) # iter([5])
drop(3, count(5))     # count(8)
drop(3, 'ab')         # empty iterator

```

first( _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#first "Permalink to this definition")

Returns the first item in the sequence. Returns `None` if the sequence is empty. Typical usage is choosing first of some generated variants:

```
# Get a text message of first failed validation rule
fail = first(rule.text for rule in rules if not rule.test(instance))

# Use simple pattern matching to construct form field widget
TYPE_TO_WIDGET = (
    [lambda f: f.choices,           lambda f: Select(choices=f.choices)],
    [lambda f: f.type == 'int',     lambda f: TextInput(coerce=int)],
    [lambda f: f.type == 'string',  lambda f: TextInput()],
    [lambda f: f.type == 'text',    lambda f: Textarea()],
    [lambda f: f.type == 'boolean', lambda f: Checkbox(f.label)],
)
return first(do(field) for cond, do in TYPE_TO_WIDGET if cond(field))

```

Other common use case is passing to [`map()`](https://funcy.readthedocs.io/en/stable/seqs.html#map) or [`lmap()`](https://funcy.readthedocs.io/en/stable/seqs.html#lmap). See last example in [`iterate()`](https://funcy.readthedocs.io/en/stable/seqs.html#iterate) for such example.

second( _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#second "Permalink to this definition")

Returns the second item in given sequence. Returns `None` if there are less than two items in it.

Could come in handy with sequences of pairs, e.g. [`dict.items()`](https://docs.python.org/3/library/stdtypes.html#dict.items "(in Python v3.11)"). Following code extract values of a dict sorted by keys:

```
map(second, sorted(some_dict.items()))

```

And this line constructs an ordered by value dict from a plain one:

```
OrderedDict(sorted(plain_dict.items(), key=second))

```

nth( _n_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#nth "Permalink to this definition")

Returns nth item in sequence or `None` if no one exists. Items are counted from 0, so it’s like indexed access but works for iterators. E.g. here is how one can get 6th line of some\_file:

```
nth(5, repeatedly(open('some_file').readline))

```

last( _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#last "Permalink to this definition")

Returns the last item in the sequence. Returns `None` if the sequence is empty. Tries to be efficient when sequence supports indexed or reversed access and fallbacks to iterating over it if not.

rest( _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#rest "Permalink to this definition")

Skips first item in the sequence, returning iterator starting just after it. A shortcut for [`drop(1, seq)`](https://funcy.readthedocs.io/en/stable/seqs.html#drop).

butlast( _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#butlast "Permalink to this definition")

Returns an iterator of all elements of the sequence but last.

ilen( _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#ilen "Permalink to this definition")

Calculates length of iterator. Will consume it or hang up if it’s infinite.

Especially useful in conjunction with filtering or slicing functions, for example, this way one can find common start length of two strings:

```
ilen(takewhile(lambda (x, y): x == y, zip(s1, s2)))

```

## Unite [¶](https://funcy.readthedocs.io/en/stable/seqs.html\#unite "Permalink to this headline")

concat( _\*seqs_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#concat "Permalink to this definition")lconcat( _\*seqs_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lconcat "Permalink to this definition")

Concats several sequences into single iterator or list.

[`concat()`](https://funcy.readthedocs.io/en/stable/seqs.html#concat) is an alias for [`itertools.chain()`](https://docs.python.org/3/library/itertools.html#itertools.chain "(in Python v3.11)").

cat( _seqs_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#cat "Permalink to this definition")lcat( _seqs_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lcat "Permalink to this definition")

Concatenates passed sequences. Useful when dealing with sequence of sequences, see [`concat()`](https://funcy.readthedocs.io/en/stable/seqs.html#concat) or [`lconcat()`](https://funcy.readthedocs.io/en/stable/seqs.html#lconcat) to join just a few sequences.

Flattening of various nested sequences is most common use:

```
# Flatten two level deep list
lcat(list_of_lists)

# Get a flat html of errors of a form
errors = cat(inline.errors() for inline in form)
error_text = '<br>'.join(errors)

# Brace expansion on product of sums
# (a + b)(t + pq)x == atx + apqx + btx + bpqx
terms = [['a', 'b'], ['t', 'pq'], ['x']]
lmap(lcat, product(*terms))
# [list('atx'), list('apqx'), list('btx'), list('bpqx')]

```

[`cat()`](https://funcy.readthedocs.io/en/stable/seqs.html#cat) is an alias for [`itertools.chain.from_iterable()`](https://docs.python.org/3/library/itertools.html#itertools.chain.from_iterable "(in Python v3.11)").

flatten( _seq_, _follow=is\_seqcont_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#flatten "Permalink to this definition")lflatten( _seq_, _follow=is\_seqcont_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lflatten "Permalink to this definition")

Flattens arbitrary nested sequence of values and other sequences. `follow` argument determines whether to unpack each item. By default it dives into lists, tuples and iterators, see [`is_seqcont()`](https://funcy.readthedocs.io/en/stable/types.html#is_seqcont) for further explanation.

See also [`cat()`](https://funcy.readthedocs.io/en/stable/seqs.html#cat) or [`lcat()`](https://funcy.readthedocs.io/en/stable/seqs.html#lcat) if you need to flatten strictly two-level sequence of sequences.

tree\_leaves( _root_, _follow=is\_seqcont_, _children=iter_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#tree_leaves "Permalink to this definition")ltree\_leaves( _root_, _follow=is\_seqcont_, _children=iter_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#ltree_leaves "Permalink to this definition")

A way to iterate or list over all the tree leaves. E.g. this is how you can list all descendants of a class:

```
ltree_leaves(Base, children=type.__subclasses__, follow=type.__subclasses__)

```

tree\_nodes( _root_, _follow=is\_seqcont_, _children=iter_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#tree_nodes "Permalink to this definition")ltree\_nodes( _root_, _follow=is\_seqcont_, _children=iter_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#ltree_nodes "Permalink to this definition")

A way to iterate or list over all the tree nodes. E.g. this is how you can iterate over all classes in hierarchy:

```
tree_nodes(Base, children=type.__subclasses__, follow=type.__subclasses__)

```

interleave( _\*seqs_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#interleave "Permalink to this definition")

Returns an iterator yielding first item in each sequence, then second and so on until some sequence ends. Numbers of items taken from all sequences are always equal.

interpose( _sep_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#interpose "Permalink to this definition")

Returns an iterator yielding elements of `seq` separated by `sep`.

This is like [`str.join()`](https://docs.python.org/3/library/stdtypes.html#str.join "(in Python v3.11)") for lists. This code is a part of a translator working with operation node:

```
def visit_BoolOp(self, node):
    # ... do generic visit
    node.code = lmapcat(translate, interpose(node.op, node.values))

```

lzip( _\*seqs_, _strict=False_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lzip "Permalink to this definition")

Joins given sequences into a list of tuples of corresponding first, second and later values. Essentially a list version of [`zip()`](https://docs.python.org/3/library/functions.html#zip "(in Python v3.11)") for Python 3.

## Transform and filter [¶](https://funcy.readthedocs.io/en/stable/seqs.html\#transform-and-filter "Permalink to this headline")

Most of functions in this section support [Extended function semantics](https://funcy.readthedocs.io/en/stable/extended_fns.html#extended-fns). Among other things it allows to rewrite examples using [`re_tester()`](https://funcy.readthedocs.io/en/stable/strings.html#re_tester) and [`re_finder()`](https://funcy.readthedocs.io/en/stable/strings.html#re_finder) tighter.

map( _f_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#map "Permalink to this definition")lmap( _f_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lmap "Permalink to this definition")

Extended versions of [`map()`](https://docs.python.org/3/library/functions.html#map "(in Python v3.11)") and its list version.

filter( _pred_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#filter "Permalink to this definition")lfilter( _pred_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lfilter "Permalink to this definition")

Extended versions of [`filter()`](https://docs.python.org/3/library/functions.html#filter "(in Python v3.11)") and its list version.

remove( _pred_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#remove "Permalink to this definition")lremove( _pred_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lremove "Permalink to this definition")

Returns an iterator or a list of items of `seq` that result in false when passed to `pred`. The results of this functions complement results of [`filter()`](https://funcy.readthedocs.io/en/stable/seqs.html#filter) and [`lfilter()`](https://funcy.readthedocs.io/en/stable/seqs.html#lfilter).

A handy use is passing [`re_tester()`](https://funcy.readthedocs.io/en/stable/strings.html#re_tester) result as `pred`. For example, this code removes any whitespace-only lines from list:

```
remove(re_tester('^\s+$'), lines)

```

Note, you can rewrite it shorter using [Extended function semantics](https://funcy.readthedocs.io/en/stable/extended_fns.html#extended-fns):

```
remove('^\s+$', lines)

```

keep(\[ _f_, \] _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#keep "Permalink to this definition")lkeep(\[ _f_, \] _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lkeep "Permalink to this definition")

Maps `seq` with given function and then filters out falsy elements. Simply removes falsy items when `f` is absent. In fact these functions are just handy shortcuts:

```
keep(f, seq)  == filter(bool, map(f, seq))
keep(seq)     == filter(bool, seq)

lkeep(f, seq) == lfilter(bool, map(f, seq))
lkeep(seq)    == lfilter(bool, seq)

```

Natural use case for [`keep()`](https://funcy.readthedocs.io/en/stable/seqs.html#keep) is data extraction or recognition that could eventually fail:

```
# Extract numbers from words
lkeep(re_finder(r'\d+'), words)

# Recognize as many colors by name as possible
lkeep(COLOR_BY_NAME.get, color_names)

```

An iterator version can be useful when you don’t need or not sure you need the whole sequence. For example, you can use [`first()`](https://funcy.readthedocs.io/en/stable/seqs.html#first) \- [`keep()`](https://funcy.readthedocs.io/en/stable/seqs.html#keep) combo to find out first match:

```
first(keep(COLOR_BY_NAME.get, color_name_candidates))

```

Alternatively, you can do the same with [`some()`](https://funcy.readthedocs.io/en/stable/colls.html#some) and [`map()`](https://funcy.readthedocs.io/en/stable/seqs.html#map).

One argument variant is a simple tool to keep your data free of falsy junk. This one returns non-empty description lines:

```
keep(description.splitlines())

```

Other common case is using generator expression instead of mapping function. Consider these two lines:

```
keep(f.name for f in fields)     # sugar generator expression
keep(attrgetter('name'), fields) # pure functions

```

mapcat( _f_, _\*seqs_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#mapcat "Permalink to this definition")lmapcat( _f_, _\*seqs_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lmapcat "Permalink to this definition")

Maps given sequence(s) and then concatenates results, essentially a shortcut for `cat(map(f, *seqs))`. Come in handy when extracting multiple values from every sequence item or transforming nested sequences:

```
# Get all the lines of all the texts in single flat list
mapcat(str.splitlines, bunch_of_texts)

# Extract all numbers from strings
mapcat(partial(re_all, r'\d+'), bunch_of_strings)

```

without( _seq_, _\*items_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#without "Permalink to this definition")lwithout( _seq_, _\*items_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lwithout "Permalink to this definition")

Returns sequence with `items` removed, preserves order.
Designed to work with a few `items`, this allows removing unhashable objects:

```
non_empty_lists = without(lists, [])

```

In case of large amount of unwanted elements one can use [`remove()`](https://funcy.readthedocs.io/en/stable/seqs.html#remove):

```
remove(set(unwanted_elements), seq)

```

Or simple set difference if order of sequence is irrelevant.

## Split and chunk [¶](https://funcy.readthedocs.io/en/stable/seqs.html\#split-and-chunk "Permalink to this headline")

split( _pred_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#split "Permalink to this definition")lsplit( _pred_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lsplit "Permalink to this definition")

Splits sequence items which pass predicate from the ones that don’t, essentially returning a tuple `filter(pred, seq), remove(pred, seq)`.

For example, this way one can separate private attributes of an instance from public ones:

```
private, public = lsplit(re_tester('^_'), dir(instance))

```

Split absolute and relative urls using extended predicate semantics:

```
absolute, relative = lsplit(r'^http://', urls)

```

split\_at( _n_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#split_at "Permalink to this definition")lsplit\_at( _n_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lsplit_at "Permalink to this definition")

Splits sequence at given position, returning a tuple of its start and tail.

split\_by( _pred_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#split_by "Permalink to this definition")lsplit\_by( _pred_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lsplit_by "Permalink to this definition")

Splits start of sequence, consisting of items passing predicate, from the rest of it. Works similar to `takewhile(pred, seq), dropwhile(pred, seq)`, but works with iterator `seq` correctly:

```
lsplit_by(bool, iter([-2, -1, 0, 1, 2]))
# [-2, -1], [0, 1, 2]

```

takewhile(\[ _pred_, \] _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#takewhile "Permalink to this definition")

Yeilds elements of `seq` as long as they pass `pred`. Stops on first one which makes predicate falsy:

```
# Extract first paragraph of text
takewhile(re_tester(r'\S'), text.splitlines())

# Build path from node to tree root
takewhile(bool, iterate(attrgetter('parent'), node))

```

dropwhile(\[ _pred_, \] _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#dropwhile "Permalink to this definition")

This is a mirror of [`takewhile()`](https://funcy.readthedocs.io/en/stable/seqs.html#takewhile). Skips elements of given sequence while `pred` is true and yields the rest of it:

```
# Skip leading whitespace-only lines
dropwhile(re_tester('^\s*$'), text_lines)

```

group\_by( _f_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#group_by "Permalink to this definition")

Groups elements of `seq` keyed by the result of `f`. The value at each key will be a list of the corresponding elements, in the order they appear in `seq`. Returns [`defaultdict(list)`](https://docs.python.org/3/library/collections.html#collections.defaultdict "(in Python v3.11)").

```
stats = group_by(len, ['a', 'ab', 'b'])
stats[1] # -> ['a', 'b']
stats[2] # -> ['ab']
stats[3] # -> [], since stats is defaultdict

```

One can use [`split()`](https://funcy.readthedocs.io/en/stable/seqs.html#split) when grouping by boolean predicate. See also [`itertools.groupby()`](https://docs.python.org/3/library/itertools.html#itertools.groupby "(in Python v3.11)").

group\_by\_keys( _get\_keys_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#group_by_keys "Permalink to this definition")

Groups elements of `seq` having multiple keys each into [`defaultdict(list)`](https://docs.python.org/3/library/collections.html#collections.defaultdict "(in Python v3.11)"). Can be used to reverse grouping:

```
posts_by_tag = group_by_keys(attrgetter('tags'), posts)
sentences_with_word = group_by_keys(str.split, sentences)

```

group\_values( _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#group_values "Permalink to this definition")

Groups values of `(key, value)` pairs. May think of it like `dict()` but collecting collisions:

```
group_values(keep(r'^--(\w+)=(.+)', sys.argv))

```

partition( _n_, \[ _step_, \] _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#partition "Permalink to this definition")lpartition( _n_, \[ _step_, \] _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lpartition "Permalink to this definition")

Iterates or lists over partitions of `n` items, at offsets `step` apart. If `step` is not supplied, defaults to `n`, i.e. the partitions do not overlap. Returns only full length- `n` partitions, in case there are not enough elements for last partition they are ignored.

Most common use is deflattening data:

```
# Make a dict from flat list of pairs
dict(partition(2, flat_list_of_pairs))

# Structure user credentials
{id: (name, password) for id, name, password in partition(3, users)}

```

A three argument variant of [`partition()`](https://funcy.readthedocs.io/en/stable/seqs.html#partition) can be used to process sequence items in context of their neighbors:

```
# Smooth data by averaging out with a sliding window
[sum(window) / n for window in partition(n, 1, data_points)]

```

Also look at [`pairwise()`](https://funcy.readthedocs.io/en/stable/seqs.html#pairwise) for similar use. Other use of [`partition()`](https://funcy.readthedocs.io/en/stable/seqs.html#partition) is processing sequence of data elements or jobs in chunks, but take a look at [`chunks()`](https://funcy.readthedocs.io/en/stable/seqs.html#chunks) for that.

chunks( _n_, \[ _step_, \] _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#chunks "Permalink to this definition")lchunks( _n_, \[ _step_, \] _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lchunks "Permalink to this definition")

Like [`partition()`](https://funcy.readthedocs.io/en/stable/seqs.html#partition), but may include partitions with fewer than `n` items at the end:

```
chunks(2, 'abcde')
# -> 'ab', 'cd', 'e'

chunks(2, 4, 'abcde')
# -> 'ab', 'e'

```

Handy for batch processing.

partition\_by( _f_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#partition_by "Permalink to this definition")lpartition\_by( _f_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lpartition_by "Permalink to this definition")

Partition `seq` into list of lists or iterator of iterators splitting at `f(item)` change.

## Data handling [¶](https://funcy.readthedocs.io/en/stable/seqs.html\#data-handling "Permalink to this headline")

distinct( _seq_, _key=identity_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#distinct "Permalink to this definition")ldistinct( _seq_, _key=identity_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#ldistinct "Permalink to this definition")

Returns unique items of the sequence with order preserved. If `key` is supplied then distinguishes values by comparing their keys.

Note

Elements of a sequence or their keys should be hashable.

with\_prev( _seq_, _fill=None_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#with_prev "Permalink to this definition")

Returns an iterator of a pair of each item with one preceding it. Yields fill or None as preceding element for first item.

Great for getting rid of clunky `prev` housekeeping in for loops. This way one can indent first line of each paragraph while printing text:

```
for line, prev in with_prev(text.splitlines()):
    if not prev:
        print '    ',
    print line

```

Use [`pairwise()`](https://funcy.readthedocs.io/en/stable/seqs.html#pairwise) to iterate only on full pairs.

with\_next( _seq_, _fill=None_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#with_next "Permalink to this definition")

Returns an iterator of a pair of each item with one next to it. Yields fill or None as next element for last item. See also [`with_prev()`](https://funcy.readthedocs.io/en/stable/seqs.html#with_prev) and [`pairwise()`](https://funcy.readthedocs.io/en/stable/seqs.html#pairwise).

pairwise( _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#pairwise "Permalink to this definition")

Yields pairs of items in `seq` like `(item0, item1), (item1, item2), ...`. A great way to process sequence items in a context of each neighbor:

```
# Check if seq is non-descending
all(left <= right for left, right in pairwise(seq))

```

count\_by( _f_, _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#count_by "Permalink to this definition")

Counts numbers of occurrences of values of `f` on elements of `seq`. Returns [`defaultdict(int)`](https://docs.python.org/3/library/collections.html#collections.defaultdict "(in Python v3.11)") of counts.

Calculating a histogram is one common use:

```
# Get a length histogram of given words
count_by(len, words)

```

count\_reps( _seq_) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#count_reps "Permalink to this definition")

Counts number of repetitions of each value in `seq`. Returns [`defaultdict(int)`](https://docs.python.org/3/library/collections.html#collections.defaultdict "(in Python v3.11)") of counts. This is faster and shorter alternative to `count_by(identity, ...)`

reductions( _f_, _seq_\[, _acc_\]) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#reductions "Permalink to this definition")lreductions( _f_, _seq_\[, _acc_\]) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lreductions "Permalink to this definition")

Returns a sequence of the intermediate values of the reduction of `seq` by `f`. In other words it yields a sequence like:

```
reduce(f, seq[:1], [acc]), reduce(f, seq[:2], [acc]), ...

```

You can use [`sums()`](https://funcy.readthedocs.io/en/stable/seqs.html#sums) or [`lsums()`](https://funcy.readthedocs.io/en/stable/seqs.html#lsums) for a common use of getting list of partial sums.

sums( _seq_\[, _acc_\]) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#sums "Permalink to this definition")lsums( _seq_\[, _acc_\]) [¶](https://funcy.readthedocs.io/en/stable/seqs.html#lsums "Permalink to this definition")

Same as [`reductions()`](https://funcy.readthedocs.io/en/stable/seqs.html#reductions) or [`lreductions()`](https://funcy.readthedocs.io/en/stable/seqs.html#lreductions) with reduce function fixed to addition.

Find out which straw will break camels back:

```
first(i for i, total in enumerate(sums(straw_weights))
        if total > camel_toughness)

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

Versions[latest](https://funcy.readthedocs.io/en/latest/seqs.html)**[stable](https://funcy.readthedocs.io/en/stable/seqs.html)**[2.0](https://funcy.readthedocs.io/en/2.0/seqs.html)[1.18](https://funcy.readthedocs.io/en/1.18/seqs.html)[1.17](https://funcy.readthedocs.io/en/1.17/seqs.html)[1.16](https://funcy.readthedocs.io/en/1.16/seqs.html)[1.15](https://funcy.readthedocs.io/en/1.15/seqs.html)[1.14](https://funcy.readthedocs.io/en/1.14/seqs.html)[1.13](https://funcy.readthedocs.io/en/1.13/seqs.html)[1.11](https://funcy.readthedocs.io/en/1.11/seqs.html)[1.10.3](https://funcy.readthedocs.io/en/1.10.3/seqs.html)[1.10.2](https://funcy.readthedocs.io/en/1.10.2/seqs.html)[1.10.1](https://funcy.readthedocs.io/en/1.10.1/seqs.html)[1.10](https://funcy.readthedocs.io/en/1.10/seqs.html)[1.9](https://funcy.readthedocs.io/en/1.9/seqs.html)[1.8](https://funcy.readthedocs.io/en/1.8/seqs.html)[1.7.5](https://funcy.readthedocs.io/en/1.7.5/seqs.html)[1.7.4](https://funcy.readthedocs.io/en/1.7.4/seqs.html)[1.7.3](https://funcy.readthedocs.io/en/1.7.3/seqs.html)[1.7.2](https://funcy.readthedocs.io/en/1.7.2/seqs.html)[1.7.1](https://funcy.readthedocs.io/en/1.7.1/seqs.html)[1.7](https://funcy.readthedocs.io/en/1.7/seqs.html)[1.6](https://funcy.readthedocs.io/en/1.6/seqs.html)[1.5](https://funcy.readthedocs.io/en/1.5/seqs.html)[1.4](https://funcy.readthedocs.io/en/1.4/seqs.html)[1.3](https://funcy.readthedocs.io/en/1.3/seqs.html)[1.1](https://funcy.readthedocs.io/en/1.1/seqs.html)[1.0.0](https://funcy.readthedocs.io/en/1.0.0/seqs.html)[0.10.1](https://funcy.readthedocs.io/en/0.10.1/seqs.html)On Read the Docs[Project Home](https://app.readthedocs.org/projects/funcy/?utm_source=funcy&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/funcy/builds/?utm_source=funcy&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=funcy&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=funcy&utm_content=flyout)