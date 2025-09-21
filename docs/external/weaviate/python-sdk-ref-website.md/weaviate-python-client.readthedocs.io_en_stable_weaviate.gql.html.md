---
url: "https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html"
title: "weaviate.gql — Weaviate Python Client 4.16.10 documentation"
---

- [Home](https://weaviate-python-client.readthedocs.io/en/stable/index.html)
- [Weaviate Library](https://weaviate-python-client.readthedocs.io/en/stable/modules.html)
- [weaviate](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html)
- weaviate.gql
- [View page source](https://weaviate-python-client.readthedocs.io/en/stable/_sources/weaviate.gql.rst.txt)

* * *

# weaviate.gql [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html\#module-weaviate.gql "Link to this heading")

GraphQL module used to create get and/or aggregate GraphQL requests from Weaviate.

## weaviate.gql.aggregate [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html\#module-weaviate.gql.aggregate "Link to this heading")

GraphQL Aggregate command.

_class_ weaviate.gql.aggregate.Hybrid( _content:dict_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#Hybrid) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.Hybrid "Link to this definition")

Bases: `object`

Parameters:

**content** ( _dict_)

query _:str\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.Hybrid.query "Link to this definition")alpha _:float\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.Hybrid.alpha "Link to this definition")vector _:List\[float\]\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.Hybrid.vector "Link to this definition")properties _:List\[str\]\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.Hybrid.properties "Link to this definition")target\_vectors _:List\[str\]\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.Hybrid.target_vectors "Link to this definition")max\_vector\_distance _:List\[str\]\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.Hybrid.max_vector_distance "Link to this definition")_class_ weaviate.gql.aggregate.AggregateBuilder( _class\_name_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "Link to this definition")

Bases: [`GraphQL`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.GraphQL "weaviate.gql.filter.GraphQL")

AggregateBuilder class used to aggregate Weaviate objects.

Initialize a AggregateBuilder class instance.

Parameters:

**class\_name** ( _str_) – Class name of the objects to be aggregated.

with\_tenant( _tenant_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_tenant) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_tenant "Link to this definition")

Sets a tenant for the query.

Parameters:

**tenant** ( _str_)

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

with\_meta\_count() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_meta_count) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_meta_count "Link to this definition")

Set Meta Count to True.

Returns:

Updated AggregateBuilder.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

with\_object\_limit( _limit_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_object_limit) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_object_limit "Link to this definition")

Set objectLimit to limit vector search results used within the aggregation query only when with near<MEDIA> filter.

Parameters:

**limit** ( _int_) – The object limit.

Returns:

Updated AggregateBuilder.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

with\_limit( _limit_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_limit) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_limit "Link to this definition")

Set limit to limit the number of returned results from the aggregation query.

Parameters:

**limit** ( _int_) – The limit.

Returns:

Updated AggregateBuilder.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

with\_fields( _field_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_fields) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_fields "Link to this definition")

Include a field in the aggregate query.

Parameters:

**field** ( _str_) – Field to include in the aggregate query. e.g. ‘<property\_name> { count }’

Returns:

Updated AggregateBuilder.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

with\_where( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_where) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_where "Link to this definition")

Set ‘where’ filter.

Parameters:

**content** ( _dict_) – The where filter to include in the aggregate query. See examples below.

Returns:

Updated AggregateBuilder.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

with\_hybrid( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_hybrid) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_hybrid "Link to this definition")

Get objects using bm25 and vector, then combine the results using a reciprocal ranking algorithm.

Parameters:

**content** ( _dict_) – The content of the hybrid filter to set.

Returns:

Updated AggregateBuilder.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

with\_group\_by\_filter( _properties_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_group_by_filter) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_group_by_filter "Link to this definition")

Add a group by filter to the query. Might requires the user to set an additional group by clause using with\_fields(..).

Parameters:

**properties** ( _List_ _\[_ _str_ _\]_) – The list of properties that are included in the group by filter.
Generates a filter like: ‘groupBy: \[“property1”, “property2”\]’
from a list \[“property1”, “property2”\]

Returns:

Updated AggregateBuilder.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

with\_near\_text( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_near_text) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_near_text "Link to this definition")

Set nearText filter.

This filter can be used with text modules (text2vec).
E.g.: text2vec-contextionary, text2vec-transformers.
NOTE: The ‘autocorrect’ field is enabled only with the text-spellcheck Weaviate module.

Parameters:

**content** ( _dict_) – The content of the nearText filter to set. See examples below.

Returns:

Updated AggregateBuilder.

Raises:

**AttributeError** – If another ‘near’ filter was already set.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

with\_near\_vector( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_near_vector) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_near_vector "Link to this definition")

Set nearVector filter.

Parameters:

**content** ( _dict_) – The content of the nearVector filter to set. See examples below.

Returns:

Updated AggregateBuilder.

Raises:

**AttributeError** – If another ‘near’ filter was already set.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

with\_near\_object( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_near_object) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_near_object "Link to this definition")

Set nearObject filter.

Parameters:

**content** ( _dict_) – The content of the nearObject filter to set. See examples below.

Returns:

Updated AggregateBuilder.

Raises:

**AttributeError** – If another ‘near’ filter was already set.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

with\_near\_image( _content_, _encode=True_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_near_image) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_near_image "Link to this definition")

Set nearImage filter.

Parameters:

- **content** ( _dict_) – The content of the nearImage filter to set. See examples below.

- **encode** ( _bool_) – Whether to encode the content\[“image”\] to base64 and convert to string. If True, the
content\[“image”\] can be an image path or a file opened in binary read mode. If False,
the content\[“image”\] MUST be a base64 encoded string (NOT bytes, i.e. NOT binary
string that looks like this: b’BASE64ENCODED’ but simple ‘BASE64ENCODED’).
By default True.


Returns:

Updated AggregateBuilder.

Raises:

**AttributeError** – If another ‘near’ filter was already set.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder._abc_impl "Link to this definition")with\_near\_audio( _content_, _encode=True_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_near_audio) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_near_audio "Link to this definition")

Set nearAudio filter.

Parameters:

- **content** ( _dict_) – The content of the nearAudio filter to set. See examples below.

- **encode** ( _bool_) – Whether to encode the content\[“audio”\] to base64 and convert to string. If True, the
content\[“audio”\] can be an audio path or a file opened in binary read mode. If False,
the content\[“audio”\] MUST be a base64 encoded string (NOT bytes, i.e. NOT binary
string that looks like this: b’BASE64ENCODED’ but simple ‘BASE64ENCODED’).
By default True.


Returns:

Updated AggregateBuilder.

Raises:

**AttributeError** – If another ‘near’ filter was already set.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

with\_near\_video( _content_, _encode=True_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_near_video) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_near_video "Link to this definition")

Set nearVideo filter.

Parameters:

- **content** ( _dict_) – The content of the nearVideo filter to set. See examples below.

- **encode** ( _bool_) – Whether to encode the content\[“video”\] to base64 and convert to string. If True, the
content\[“video”\] can be an video path or a file opened in binary read mode. If False,
the content\[“video”\] MUST be a base64 encoded string (NOT bytes, i.e. NOT binary
string that looks like this: b’BASE64ENCODED’ but simple ‘BASE64ENCODED’).
By default True.


Returns:

Updated AggregateBuilder.

Raises:

**AttributeError** – If another ‘near’ filter was already set.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

with\_near\_depth( _content_, _encode=True_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_near_depth) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_near_depth "Link to this definition")

Set nearDepth filter.

Parameters:

- **content** ( _dict_) – The content of the nearDepth filter to set. See examples below.

- **encode** ( _bool_) – Whether to encode the content\[“depth”\] to base64 and convert to string. If True, the
content\[“depth”\] can be an depth path or a file opened in binary read mode. If False,
the content\[“depth”\] MUST be a base64 encoded string (NOT bytes, i.e. NOT binary
string that looks like this: b’BASE64ENCODED’ but simple ‘BASE64ENCODED’).
By default True.


Returns:

Updated AggregateBuilder.

Raises:

**AttributeError** – If another ‘near’ filter was already set.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

with\_near\_thermal( _content_, _encode=True_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_near_thermal) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_near_thermal "Link to this definition")

Set nearThermal filter.

Parameters:

- **content** ( _dict_) – The content of the nearThermal filter to set. See examples below.

- **encode** ( _bool_) – Whether to encode the content\[“thermal”\] to base64 and convert to string. If True, the
content\[“thermal”\] can be an thermal path or a file opened in binary read mode. If False,
the content\[“thermal”\] MUST be a base64 encoded string (NOT bytes, i.e. NOT binary
string that looks like this: b’BASE64ENCODED’ but simple ‘BASE64ENCODED’).
By default True.


Returns:

Updated AggregateBuilder.

Raises:

**AttributeError** – If another ‘near’ filter was already set.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

with\_near\_imu( _content_, _encode=True_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.with_near_imu) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_near_imu "Link to this definition")

Set nearIMU filter.

Parameters:

- **content** ( _dict_) – The content of the nearIMU filter to set. See examples below.

- **encode** ( _bool_) – Whether to encode the content\[“thermal”\] to base64 and convert to string. If True, the
content\[“thermal”\] can be an thermal path or a file opened in binary read mode. If False,
the content\[“thermal”\] MUST be a base64 encoded string (NOT bytes, i.e. NOT binary
string that looks like this: b’BASE64ENCODED’ but simple ‘BASE64ENCODED’).
By default True.


Returns:

Updated AggregateBuilder.

Raises:

**AttributeError** – If another ‘near’ filter was already set.

Return type:

[_AggregateBuilder_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder")

build() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/aggregate.html#AggregateBuilder.build) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.build "Link to this definition")

Build the query and return the string.

Returns:

The GraphQL query as a string.

Return type:

str

## weaviate.gql.filter [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html\#module-weaviate.gql.filter "Link to this heading")

GraphQL filters for Get and Aggregate commands. GraphQL abstract class for GraphQL commands to inherit from.

_class_ weaviate.gql.filter.MediaType( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#MediaType) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.MediaType "Link to this definition")

Bases: `Enum`

IMAGE _='image'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.MediaType.IMAGE "Link to this definition")AUDIO _='audio'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.MediaType.AUDIO "Link to this definition")VIDEO _='video'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.MediaType.VIDEO "Link to this definition")THERMAL _='thermal'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.MediaType.THERMAL "Link to this definition")DEPTH _='depth'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.MediaType.DEPTH "Link to this definition")IMU _='imu'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.MediaType.IMU "Link to this definition")_class_ weaviate.gql.filter.GraphQL [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#GraphQL) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.GraphQL "Link to this definition")

Bases: `ABC`

A base abstract class for GraphQL commands, such as Get, Aggregate.

_abstractmethod_ build() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#GraphQL.build) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.GraphQL.build "Link to this definition")

Build method to be overloaded by the child classes. It should return the GraphQL query as a str.

Returns:

The query.

Return type:

str

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.GraphQL._abc_impl "Link to this definition")_class_ weaviate.gql.filter.Filter( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#Filter) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Filter "Link to this definition")

Bases: `ABC`

A base abstract class for all filters.

Initialize a Filter class instance.

Parameters:

**content** ( _dict_) – The content of the Filter clause.

_property_ content _:dict_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Filter.content "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Filter._abc_impl "Link to this definition")_class_ weaviate.gql.filter.NearText( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#NearText) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearText "Link to this definition")

Bases: [`Filter`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Filter "weaviate.gql.filter.Filter")

NearText class used to filter weaviate objects.

Can be used with text models only (text2vec), e.g.: text2vec-contextionary, text2vec-transformers.

Initialize a NearText class instance.

Parameters:

**content** ( _dict_) – The content of the nearText clause.

Raises:

- **TypeError** – If ‘content’ is not of type dict.

- **ValueError** – If ‘content’ has key “certainty”/”distance” but the value is not float.


\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearText._abc_impl "Link to this definition")_class_ weaviate.gql.filter.NearVector( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#NearVector) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearVector "Link to this definition")

Bases: [`Filter`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Filter "weaviate.gql.filter.Filter")

NearVector class used to filter weaviate objects.

Initialize a NearVector class instance.

Parameters:

**content** ( _dict_) – The content of the nearVector clause.

Raises:

- **TypeError** – If ‘content’ is not of type dict.

- **KeyError** – If ‘content’ does not contain “vector”.

- **TypeError** – If ‘content\[“vector”\]’ is not of type list.

- **AttributeError** – If invalid ‘content’ keys are provided.

- **ValueError** – If ‘content’ has key “certainty”/”distance” but the value is not float.


\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearVector._abc_impl "Link to this definition")_class_ weaviate.gql.filter.NearObject( _content_, _is\_server\_version\_14_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#NearObject) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearObject "Link to this definition")

Bases: [`Filter`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Filter "weaviate.gql.filter.Filter")

NearObject class used to filter weaviate objects.

Initialize a NearVector class instance.

Parameters:

- **content** ( _dict_) – The content of the nearVector clause.

- **is\_server\_version\_14** ( _bool_) – Whether the Server version is >= 1.14.0.


Raises:

- **TypeError** – If ‘content’ is not of type dict.

- **ValueError** – If ‘content’ has key “certainty”/”distance” but the value is not float.

- **TypeError** – If ‘id’/’beacon’ key does not have a value of type str!


\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearObject._abc_impl "Link to this definition")_class_ weaviate.gql.filter.Ask( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#Ask) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Ask "Link to this definition")

Bases: [`Filter`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Filter "weaviate.gql.filter.Filter")

Ask class used to filter weaviate objects by asking a question.

Initialize a Ask class instance.

Parameters:

**content** ( _dict_) – The content of the ask clause.

Raises:

- **TypeError** – If ‘content’ is not of type dict.

- **ValueError** – If ‘content’ has key “certainty”/”distance” but the value is not float.

- **TypeError** – If ‘content’ has key “properties” but the type is not list or str.


\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Ask._abc_impl "Link to this definition")_class_ weaviate.gql.filter.NearMedia( _content_, _media\_type_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#NearMedia) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearMedia "Link to this definition")

Bases: [`Filter`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Filter "weaviate.gql.filter.Filter")

Initialize a NearMedia class instance.

Parameters:

- **content** ( _dict_) – The content of the near<Media> clause.

- **media\_type** ( [_MediaType_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.MediaType "weaviate.gql.filter.MediaType"))


Raises:

- **TypeError** – If ‘content’ is not of type dict.

- **TypeError** – If ‘content\[“<media>”\]’ is not of type str.

- **ValueError** – If ‘content’ has key “certainty”/”distance” but the value is not float.


\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearMedia._abc_impl "Link to this definition")_class_ weaviate.gql.filter.NearImage( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#NearImage) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearImage "Link to this definition")

Bases: [`NearMedia`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearMedia "weaviate.gql.filter.NearMedia")

NearImage class used to filter weaviate objects.

Initialize a NearImage class instance.

Parameters:

**content** ( _dict_) – The content of the nearImage clause.

Raises:

- **TypeError** – If ‘content’ is not of type dict.

- **TypeError** – If ‘content\[“image”\]’ is not of type str.

- **ValueError** – If ‘content’ has key “certainty”/”distance” but the value is not float.


\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearImage._abc_impl "Link to this definition")_class_ weaviate.gql.filter.NearVideo( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#NearVideo) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearVideo "Link to this definition")

Bases: [`NearMedia`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearMedia "weaviate.gql.filter.NearMedia")

NearVideo class used to filter weaviate objects.

Initialize a NearVideo class instance.

Parameters:

**content** ( _dict_) – The content of the nearVideo clause.

Raises:

- **TypeError** – If ‘content’ is not of type dict.

- **TypeError** – If ‘content\[“video”\]’ is not of type str.

- **ValueError** – If ‘content’ has key “certainty”/”distance” but the value is not float.


\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearVideo._abc_impl "Link to this definition")_class_ weaviate.gql.filter.NearAudio( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#NearAudio) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearAudio "Link to this definition")

Bases: [`NearMedia`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearMedia "weaviate.gql.filter.NearMedia")

NearAudio class used to filter weaviate objects.

Initialize a NearAudio class instance.

Parameters:

**content** ( _dict_) – The content of the nearAudio clause.

Raises:

- **TypeError** – If ‘content’ is not of type dict.

- **TypeError** – If ‘content\[“audio”\]’ is not of type str.

- **ValueError** – If ‘content’ has key “certainty”/”distance” but the value is not float.


\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearAudio._abc_impl "Link to this definition")_class_ weaviate.gql.filter.NearDepth( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#NearDepth) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearDepth "Link to this definition")

Bases: [`NearMedia`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearMedia "weaviate.gql.filter.NearMedia")

NearDepth class used to filter weaviate objects.

Initialize a NearDepth class instance.

Parameters:

**content** ( _dict_) – The content of the nearDepth clause.

Raises:

- **TypeError** – If ‘content’ is not of type dict.

- **TypeError** – If ‘content\[“depth”\]’ is not of type str.

- **ValueError** – If ‘content’ has key “certainty”/”distance” but the value is not float.


\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearDepth._abc_impl "Link to this definition")_class_ weaviate.gql.filter.NearThermal( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#NearThermal) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearThermal "Link to this definition")

Bases: [`NearMedia`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearMedia "weaviate.gql.filter.NearMedia")

NearThermal class used to filter weaviate objects.

Initialize a NearThermal class instance.

Parameters:

**content** ( _dict_) – The content of the nearThermal clause.

Raises:

- **TypeError** – If ‘content’ is not of type dict.

- **TypeError** – If ‘content\[“thermal”\]’ is not of type str.

- **ValueError** – If ‘content’ has key “certainty”/”distance” but the value is not float.


\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearThermal._abc_impl "Link to this definition")_class_ weaviate.gql.filter.NearIMU( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#NearIMU) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearIMU "Link to this definition")

Bases: [`NearMedia`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearMedia "weaviate.gql.filter.NearMedia")

NearIMU class used to filter weaviate objects.

Initialize a NearIMU class instance.

Parameters:

**content** ( _dict_) – The content of the nearIMU clause.

Raises:

- **TypeError** – If ‘content’ is not of type dict.

- **TypeError** – If ‘content\[“imu”\]’ is not of type str.

- **ValueError** – If ‘content’ has key “certainty”/”distance” but the value is not float.


\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearIMU._abc_impl "Link to this definition")_class_ weaviate.gql.filter.Sort( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#Sort) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Sort "Link to this definition")

Bases: [`Filter`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Filter "weaviate.gql.filter.Filter")

Sort filter class used to sort weaviate objects.

Initialize a Where filter class instance.

Parameters:

**content** ( _dict_ _\|_ _list_) – The content of the sort filter clause or a single clause.

Raises:

- **TypeError** – If ‘content’ is not of type dict.

- **ValueError** – If a mandatory key is missing in the filter content.


add( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#Sort.add) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Sort.add "Link to this definition")

Add more sort clauses to the already existing sort clauses.

Parameters:

**content** ( _dict_ _\|_ _list_) – The content of the sort filter clause or a single clause to be added to the already
existing ones.

Raises:

- **TypeError** – If ‘content’ is not of type dict.

- **ValueError** – If a mandatory key is missing in the filter content.


Return type:

None

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Sort._abc_impl "Link to this definition")_class_ weaviate.gql.filter.Where( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#Where) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Where "Link to this definition")

Bases: [`Filter`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Filter "weaviate.gql.filter.Filter")

Where filter class used to filter weaviate objects.

Initialize a Where filter class instance.

Parameters:

**content** ( _dict_) – The content of the where filter clause.

Raises:

- **TypeError** – If ‘content’ is not of type dict.

- **ValueError** – If a mandatory key is missing in the filter content.


\_parse\_filter( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#Where._parse_filter) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Where._parse_filter "Link to this definition")

Set filter fields for the Where filter.

Parameters:

**content** ( _dict_) – The content of the where filter clause.

Raises:

**ValueError** – If ‘content’ is missing required fields.

Return type:

None

\_parse\_operator( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#Where._parse_operator) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Where._parse_operator "Link to this definition")

Set operator fields for the Where filter.

Parameters:

**content** ( _dict_) – The content of the where filter clause.

Raises:

**ValueError** – If ‘content’ is missing required fields.

Return type:

None

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Where._abc_impl "Link to this definition")weaviate.gql.filter.\_convert\_value\_type( _\_type_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#_convert_value_type) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter._convert_value_type "Link to this definition")

Convert the value type to match json formatting required by the Weaviate-defined GraphQL endpoints.

NOTE: This is crucially different to the Batch REST endpoints wherein
the where filter is also used.

Parameters:

**\_type** ( _str_) – The Python-defined type to be converted.

Returns:

The string interpretation of the type in Weaviate-defined json format.

Return type:

str

weaviate.gql.filter.\_render\_list( _input\_list_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#_render_list) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter._render_list "Link to this definition")

Convert a list of values to string (lowercased) to match json formatting.

Parameters:

**input\_list** ( _list_) – The value to be converted

Returns:

The string interpretation of the value in json format.

Return type:

str

weaviate.gql.filter.\_render\_list\_date( _input\_list_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#_render_list_date) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter._render_list_date "Link to this definition")Parameters:

**input\_list** ( _list_)

Return type:

str

weaviate.gql.filter.\_check\_is\_list( _value_, _\_type_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#_check_is_list) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter._check_is_list "Link to this definition")

Checks whether the provided value is a list to match the given value\_type.

Parameters:

- **value** ( _Any_) – The value to be checked.

- **\_type** ( _str_) – The type to be checked against.


Raises:

**TypeError** – If the value is not a list.

Return type:

None

weaviate.gql.filter.\_check\_is\_not\_list( _value_, _\_type_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#_check_is_not_list) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter._check_is_not_list "Link to this definition")

Checks whether the provided value is a list to match the given value\_type.

Parameters:

- **value** ( _Any_) – The value to be checked.

- **\_type** ( _str_) – The type to be checked against.


Raises:

**TypeError** – If the value is a list.

Return type:

None

weaviate.gql.filter.\_geo\_range\_to\_str( _value_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#_geo_range_to_str) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter._geo_range_to_str "Link to this definition")

Convert the valueGeoRange object to match json formatting.

Parameters:

**value** ( _dict_) – The value to be converted.

Returns:

The string interpretation of the value in json format.

Return type:

str

weaviate.gql.filter.\_bool\_to\_str( _value_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#_bool_to_str) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter._bool_to_str "Link to this definition")

Convert a bool value to string (lowercased) to match json formatting.

Parameters:

**value** ( _bool_) – The value to be converted

Returns:

The string interpretation of the value in json format.

Return type:

str

weaviate.gql.filter.\_check\_direction\_clause( _direction_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#_check_direction_clause) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter._check_direction_clause "Link to this definition")

Validate the direction sub clause.

Parameters:

**direction** ( _dict_) – A sub clause of the Explore filter.

Raises:

- **TypeError** – If ‘direction’ is not a dict.

- **TypeError** – If the value of the “force” key is not float.

- **ValueError** – If no “force” key in the ‘direction’.


Return type:

None

weaviate.gql.filter.\_check\_concept( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#_check_concept) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter._check_concept "Link to this definition")

Validate the concept sub clause.

Parameters:

**content** ( _dict_) – An Explore (sub) clause to check for ‘concepts’.

Raises:

- **ValueError** – If no “concepts” key in the ‘content’ dict.

- **TypeError** – If the value of the “concepts” is of wrong type.


Return type:

None

weaviate.gql.filter.\_check\_objects( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#_check_objects) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter._check_objects "Link to this definition")

Validate the objects sub clause of the move clause.

Parameters:

**content** ( _dict_) – An Explore (sub) clause to check for ‘objects’.

Raises:

- **ValueError** – If no “concepts” key in the ‘content’ dict.

- **TypeError** – If the value of the “concepts” is of wrong type.


Return type:

None

weaviate.gql.filter.\_check\_type( _var\_name_, _value_, _dtype_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#_check_type) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter._check_type "Link to this definition")

Check key-value type.

Parameters:

- **var\_name** ( _str_) – The variable name for which to check the type (used for error message)!

- **value** ( _Any_) – The value for which to check the type.

- **dtype** ( _Tuple_ _\[_ _type_ _,_ _type_ _\]_ _\|_ _type_) – The expected data type of the value.


Raises:

**TypeError** – If the value type does not match the expected dtype.

Return type:

None

weaviate.gql.filter.\_find\_value\_type( _content_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#_find_value_type) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter._find_value_type "Link to this definition")

Find the correct type of the content.

Parameters:

**content** ( _dict_) – The content for which to find the appropriate data type.

Returns:

The correct data type.

Raises:

**ValueError** – If missing required fields.

Return type:

str

weaviate.gql.filter.\_move\_clause\_objects\_to\_str( _objects_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/gql/filter.html#_move_clause_objects_to_str) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter._move_clause_objects_to_str "Link to this definition")

Creates the Weaviate moveTo/moveAwayFrom clause given the list of objects.

Parameters:

**objects** ( _list_) – The list of objects to be used for the moveTo/moveAwayFrom clause.

Returns:

The moveTo/moveAwayFrom clause as a string.

Return type:

str

Versions[latest](https://weaviate-python-client.readthedocs.io/en/latest/weaviate.gql.html)**[stable](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html)**[v4.16.10](https://weaviate-python-client.readthedocs.io/en/v4.16.10/weaviate.gql.html)[v4.16.9](https://weaviate-python-client.readthedocs.io/en/v4.16.9/weaviate.gql.html)[v4.16.8](https://weaviate-python-client.readthedocs.io/en/v4.16.8/weaviate.gql.html)[v4.16.7](https://weaviate-python-client.readthedocs.io/en/v4.16.7/weaviate.gql.html)[v4.16.6](https://weaviate-python-client.readthedocs.io/en/v4.16.6/weaviate.gql.html)[v4.16.5](https://weaviate-python-client.readthedocs.io/en/v4.16.5/weaviate.gql.html)[v4.16.4](https://weaviate-python-client.readthedocs.io/en/v4.16.4/weaviate.gql.html)[v4.16.3](https://weaviate-python-client.readthedocs.io/en/v4.16.3/weaviate.gql.html)[v4.16.2](https://weaviate-python-client.readthedocs.io/en/v4.16.2/weaviate.gql.html)[v4.16.1](https://weaviate-python-client.readthedocs.io/en/v4.16.1/weaviate.gql.html)[v4.16.0](https://weaviate-python-client.readthedocs.io/en/v4.16.0/weaviate.gql.html)[v4.15.4](https://weaviate-python-client.readthedocs.io/en/v4.15.4/weaviate.gql.html)[v4.15.3](https://weaviate-python-client.readthedocs.io/en/v4.15.3/weaviate.gql.html)[v4.15.2](https://weaviate-python-client.readthedocs.io/en/v4.15.2/weaviate.gql.html)[v4.15.1](https://weaviate-python-client.readthedocs.io/en/v4.15.1/weaviate.gql.html)[v4.15.0](https://weaviate-python-client.readthedocs.io/en/v4.15.0/weaviate.gql.html)[v4.14.4](https://weaviate-python-client.readthedocs.io/en/v4.14.4/weaviate.gql.html)[v4.14.3](https://weaviate-python-client.readthedocs.io/en/v4.14.3/weaviate.gql.html)[v4.14.2](https://weaviate-python-client.readthedocs.io/en/v4.14.2/weaviate.gql.html)[v4.14.1](https://weaviate-python-client.readthedocs.io/en/v4.14.1/weaviate.gql.html)[v4.14.0](https://weaviate-python-client.readthedocs.io/en/v4.14.0/weaviate.gql.html)[v4.13.2](https://weaviate-python-client.readthedocs.io/en/v4.13.2/weaviate.gql.html)[v4.13.1](https://weaviate-python-client.readthedocs.io/en/v4.13.1/weaviate.gql.html)[v4.13.0](https://weaviate-python-client.readthedocs.io/en/v4.13.0/weaviate.gql.html)[v4.12.1](https://weaviate-python-client.readthedocs.io/en/v4.12.1/weaviate.gql.html)[v4.12.0](https://weaviate-python-client.readthedocs.io/en/v4.12.0/weaviate.gql.html)[v4.11.3](https://weaviate-python-client.readthedocs.io/en/v4.11.3/weaviate.gql.html)[v4.11.2](https://weaviate-python-client.readthedocs.io/en/v4.11.2/weaviate.gql.html)[v4.11.1](https://weaviate-python-client.readthedocs.io/en/v4.11.1/weaviate.gql.html)[v4.11.0](https://weaviate-python-client.readthedocs.io/en/v4.11.0/weaviate.gql.html)[v4.10.4](https://weaviate-python-client.readthedocs.io/en/v4.10.4/weaviate.gql.html)[v4.10.3](https://weaviate-python-client.readthedocs.io/en/v4.10.3/weaviate.gql.html)[v4.10.2](https://weaviate-python-client.readthedocs.io/en/v4.10.2/weaviate.gql.html)[v4.10.0](https://weaviate-python-client.readthedocs.io/en/v4.10.0/weaviate.gql.html)[v4.9.6](https://weaviate-python-client.readthedocs.io/en/v4.9.6/weaviate.gql.html)[v4.9.5](https://weaviate-python-client.readthedocs.io/en/v4.9.5/weaviate.gql.html)[v4.9.4](https://weaviate-python-client.readthedocs.io/en/v4.9.4/weaviate.gql.html)[v4.9.3](https://weaviate-python-client.readthedocs.io/en/v4.9.3/weaviate.gql.html)[v4.9.2](https://weaviate-python-client.readthedocs.io/en/v4.9.2/weaviate.gql.html)[v4.9.1](https://weaviate-python-client.readthedocs.io/en/v4.9.1/weaviate.gql.html)[v4.9.0](https://weaviate-python-client.readthedocs.io/en/v4.9.0/weaviate.gql.html)[v4.8.1](https://weaviate-python-client.readthedocs.io/en/v4.8.1/weaviate.gql.html)[v4.8.0](https://weaviate-python-client.readthedocs.io/en/v4.8.0/weaviate.gql.html)[v4.7.1](https://weaviate-python-client.readthedocs.io/en/v4.7.1/weaviate.gql.html)[v4.7.0](https://weaviate-python-client.readthedocs.io/en/v4.7.0/weaviate.gql.html)[v4.6.7](https://weaviate-python-client.readthedocs.io/en/v4.6.7/weaviate.gql.html)[v4.6.6](https://weaviate-python-client.readthedocs.io/en/v4.6.6/weaviate.gql.html)[v4.6.5](https://weaviate-python-client.readthedocs.io/en/v4.6.5/weaviate.gql.html)[v4.6.4](https://weaviate-python-client.readthedocs.io/en/v4.6.4/weaviate.gql.html)[v4.6.3](https://weaviate-python-client.readthedocs.io/en/v4.6.3/weaviate.gql.html)[v4.6.2](https://weaviate-python-client.readthedocs.io/en/v4.6.2/weaviate.gql.html)[v4.6.1](https://weaviate-python-client.readthedocs.io/en/v4.6.1/weaviate.gql.html)[v4.6.0](https://weaviate-python-client.readthedocs.io/en/v4.6.0/weaviate.gql.html)[v4.5.7](https://weaviate-python-client.readthedocs.io/en/v4.5.7/weaviate.gql.html)[v4.5.6](https://weaviate-python-client.readthedocs.io/en/v4.5.6/weaviate.gql.html)[v4.5.5](https://weaviate-python-client.readthedocs.io/en/v4.5.5/weaviate.gql.html)[v4.5.4](https://weaviate-python-client.readthedocs.io/en/v4.5.4/weaviate.gql.html)[v4.5.3](https://weaviate-python-client.readthedocs.io/en/v4.5.3/weaviate.gql.html)[v4.5.2](https://weaviate-python-client.readthedocs.io/en/v4.5.2/weaviate.gql.html)[v4.5.1](https://weaviate-python-client.readthedocs.io/en/v4.5.1/weaviate.gql.html)[v4.5.0](https://weaviate-python-client.readthedocs.io/en/v4.5.0/weaviate.gql.html)[v4.4.4](https://weaviate-python-client.readthedocs.io/en/v4.4.4/weaviate.gql.html)[v4.4.3](https://weaviate-python-client.readthedocs.io/en/v4.4.3/weaviate.gql.html)[v4.4.2](https://weaviate-python-client.readthedocs.io/en/v4.4.2/weaviate.gql.html)[v4.4.1](https://weaviate-python-client.readthedocs.io/en/v4.4.1/weaviate.gql.html)[v4.4.0](https://weaviate-python-client.readthedocs.io/en/v4.4.0/weaviate.gql.html)[v3.26.2](https://weaviate-python-client.readthedocs.io/en/v3.26.2/weaviate.gql.html)[v3.26.1](https://weaviate-python-client.readthedocs.io/en/v3.26.1/weaviate.gql.html)[v3.26.0](https://weaviate-python-client.readthedocs.io/en/v3.26.0/weaviate.gql.html)[v3.25.3](https://weaviate-python-client.readthedocs.io/en/v3.25.3/weaviate.gql.html)[v3.25.2](https://weaviate-python-client.readthedocs.io/en/v3.25.2/weaviate.gql.html)[v3.23.0](https://weaviate-python-client.readthedocs.io/en/v3.23.0/weaviate.gql.html)[v3.22.1](https://weaviate-python-client.readthedocs.io/en/v3.22.1/weaviate.gql.html)[v3.22.0](https://weaviate-python-client.readthedocs.io/en/v3.22.0/weaviate.gql.html)[v3.21.0](https://weaviate-python-client.readthedocs.io/en/v3.21.0/weaviate.gql.html)[v3.20.1](https://weaviate-python-client.readthedocs.io/en/v3.20.1/weaviate.gql.html)[v3.20.0](https://weaviate-python-client.readthedocs.io/en/v3.20.0/weaviate.gql.html)[v3.19.2](https://weaviate-python-client.readthedocs.io/en/v3.19.2/weaviate.gql.html)[v3.19.1](https://weaviate-python-client.readthedocs.io/en/v3.19.1/weaviate.gql.html)[v3.19.0](https://weaviate-python-client.readthedocs.io/en/v3.19.0/weaviate.gql.html)[v3.18.0](https://weaviate-python-client.readthedocs.io/en/v3.18.0/weaviate.gql.html)[v3.15.6](https://weaviate-python-client.readthedocs.io/en/v3.15.6/weaviate.gql.html)[v3.15.5](https://weaviate-python-client.readthedocs.io/en/v3.15.5/weaviate.gql.html)[v3.15.4](https://weaviate-python-client.readthedocs.io/en/v3.15.4/weaviate.gql.html)[v3.15.3](https://weaviate-python-client.readthedocs.io/en/v3.15.3/weaviate.gql.html)[v3.15.2](https://weaviate-python-client.readthedocs.io/en/v3.15.2/weaviate.gql.html)[v3.15.1](https://weaviate-python-client.readthedocs.io/en/v3.15.1/weaviate.gql.html)[v3.15.0](https://weaviate-python-client.readthedocs.io/en/v3.15.0/weaviate.gql.html)[v3.14.0](https://weaviate-python-client.readthedocs.io/en/v3.14.0/weaviate.gql.html)[v3.13.0](https://weaviate-python-client.readthedocs.io/en/v3.13.0/weaviate.gql.html)[v3.12.0\_a](https://weaviate-python-client.readthedocs.io/en/v3.12.0_a/weaviate.gql.html)[v3.11.0](https://weaviate-python-client.readthedocs.io/en/v3.11.0/weaviate.gql.html)[v3.10.0](https://weaviate-python-client.readthedocs.io/en/v3.10.0/weaviate.gql.html)[v3.9.0](https://weaviate-python-client.readthedocs.io/en/v3.9.0/weaviate.gql.html)[v3.8.0](https://weaviate-python-client.readthedocs.io/en/v3.8.0/weaviate.gql.html)[v3.7.0](https://weaviate-python-client.readthedocs.io/en/v3.7.0/weaviate.gql.html)[v3.6.0](https://weaviate-python-client.readthedocs.io/en/v3.6.0/weaviate.gql.html)[v3.5.1](https://weaviate-python-client.readthedocs.io/en/v3.5.1/weaviate.gql.html)[v3.5.0](https://weaviate-python-client.readthedocs.io/en/v3.5.0/weaviate.gql.html)[v3.4.1](https://weaviate-python-client.readthedocs.io/en/v3.4.1/weaviate.gql.html)[v3.4.0](https://weaviate-python-client.readthedocs.io/en/v3.4.0/weaviate.gql.html)[v3.3.3](https://weaviate-python-client.readthedocs.io/en/v3.3.3/weaviate.gql.html)[v3.3.2](https://weaviate-python-client.readthedocs.io/en/v3.3.2/weaviate.gql.html)[v3.3.1](https://weaviate-python-client.readthedocs.io/en/v3.3.1/weaviate.gql.html)[v3.3.0](https://weaviate-python-client.readthedocs.io/en/v3.3.0/weaviate.gql.html)[v3.2.5](https://weaviate-python-client.readthedocs.io/en/v3.2.5/weaviate.gql.html)[v3.2.4](https://weaviate-python-client.readthedocs.io/en/v3.2.4/weaviate.gql.html)[v3.2.3](https://weaviate-python-client.readthedocs.io/en/v3.2.3/weaviate.gql.html)[v3.2.2](https://weaviate-python-client.readthedocs.io/en/v3.2.2/weaviate.gql.html)[v3.2.1](https://weaviate-python-client.readthedocs.io/en/v3.2.1/weaviate.gql.html)[v3.2.0](https://weaviate-python-client.readthedocs.io/en/v3.2.0/weaviate.gql.html)[v3.1.1](https://weaviate-python-client.readthedocs.io/en/v3.1.1/weaviate.gql.html)[v3.1.0](https://weaviate-python-client.readthedocs.io/en/v3.1.0/weaviate.gql.html)[v3.0.0](https://weaviate-python-client.readthedocs.io/en/v3.0.0/weaviate.gql.html)On Read the Docs[Project Home](https://app.readthedocs.org/projects/weaviate-python-client/?utm_source=weaviate-python-client&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/weaviate-python-client/builds/?utm_source=weaviate-python-client&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=weaviate-python-client&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=weaviate-python-client&utm_content=flyout)