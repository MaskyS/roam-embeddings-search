---
url: "https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html"
title: "weaviate.classes — Weaviate Python Client 4.16.10 documentation"
---

- [Home](https://weaviate-python-client.readthedocs.io/en/stable/index.html)
- [Weaviate Library](https://weaviate-python-client.readthedocs.io/en/stable/modules.html)
- [weaviate](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html)
- weaviate.classes
- [View page source](https://weaviate-python-client.readthedocs.io/en/stable/_sources/weaviate.classes.rst.txt)

* * *

# weaviate.classes [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html\#module-weaviate.classes "Link to this heading")

_class_ weaviate.classes.ConsistencyLevel( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#ConsistencyLevel) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.ConsistencyLevel "Link to this definition")

Bases: `str`, `BaseEnum`

The consistency levels when writing to Weaviate with replication enabled.

ALL [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.ConsistencyLevel.ALL "Link to this definition")

Wait for confirmation of write success from all, N, replicas.

ONE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.ConsistencyLevel.ONE "Link to this definition")

Wait for confirmation of write success from only one replica.

QUORUM [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.ConsistencyLevel.QUORUM "Link to this definition")

Wait for confirmation of write success from a quorum: N/2+1, of replicas.

ALL _='ALL'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id0 "Link to this definition")ONE _='ONE'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id1 "Link to this definition")QUORUM _='QUORUM'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id2 "Link to this definition")

## weaviate.classes.aggregate [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html\#module-weaviate.classes.aggregate "Link to this heading")

_pydanticmodel_ weaviate.classes.aggregate.GroupByAggregate [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#GroupByAggregate) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.aggregate.GroupByAggregate "Link to this definition")

Bases: [`_WeaviateInput`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._WeaviateInput "weaviate.collections.classes.types._WeaviateInput")

Define how the aggregations’s group-by operation should be performed.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ limit _:int\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.aggregate.GroupByAggregate.limit "Link to this definition")_field_ prop _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.aggregate.GroupByAggregate.prop "Link to this definition")\_to\_grpc() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#GroupByAggregate._to_grpc) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.aggregate.GroupByAggregate._to_grpc "Link to this definition")Return type:

_GroupBy_

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.aggregate.GroupByAggregate._abc_impl "Link to this definition")_class_ weaviate.classes.aggregate.Metrics( _property\__) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#Metrics) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.aggregate.Metrics "Link to this definition")

Bases: `object`

Define the metrics to be returned based on a property when aggregating over a collection.

Use the \_\_init\_\_ method to define the name to the property to be aggregated on.
Then use the text, integer, number, boolean, date\_, or reference methods to define the metrics to be returned.

See [the docs](https://weaviate.io/developers/weaviate/search/aggregate) for more details!

Parameters:

**property\_** ( _str_)

boolean( _count=False_, _percentage\_false=False_, _percentage\_true=False_, _total\_false=False_, _total\_true=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#Metrics.boolean) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.aggregate.Metrics.boolean "Link to this definition")

Define the metrics to be returned for a BOOL or BOOL\_ARRAY property when aggregating over a collection.

If none of the arguments are provided then all metrics will be returned.

Parameters:

- **count** ( _bool_) – Whether to include the number of objects that contain this property.

- **percentage\_false** ( _bool_) – Whether to include the percentage of objects that have a false value for this property.

- **percentage\_true** ( _bool_) – Whether to include the percentage of objects that have a true value for this property.

- **total\_false** ( _bool_) – Whether to include the total number of objects that have a false value for this property.

- **total\_true** ( _bool_) – Whether to include the total number of objects that have a true value for this property.


Returns:

A \_MetricsBoolean object that includes the metrics to be returned.

Return type:

[_\_MetricsBoolean_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate._MetricsBoolean "weaviate.collections.classes.aggregate._MetricsBoolean")

date\_( _count=False_, _maximum=False_, _median=False_, _minimum=False_, _mode=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#Metrics.date_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.aggregate.Metrics.date_ "Link to this definition")

Define the metrics to be returned for a DATE or DATE\_ARRAY property when aggregating over a collection.

If none of the arguments are provided then all metrics will be returned.

Parameters:

- **count** ( _bool_) – Whether to include the number of objects that contain this property.

- **maximum** ( _bool_) – Whether to include the maximum value of this property.

- **median** ( _bool_) – Whether to include the median value of this property.

- **minimum** ( _bool_) – Whether to include the minimum value of this property.

- **mode** ( _bool_) – Whether to include the mode value of this property.


Returns:

A \_MetricsDate object that includes the metrics to be returned.

Return type:

[_\_MetricsDate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate._MetricsDate "weaviate.collections.classes.aggregate._MetricsDate")

integer( _count=False_, _maximum=False_, _mean=False_, _median=False_, _minimum=False_, _mode=False_, _sum\_=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#Metrics.integer) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.aggregate.Metrics.integer "Link to this definition")

Define the metrics to be returned for an INT or INT\_ARRAY property when aggregating over a collection.

If none of the arguments are provided then all metrics will be returned.

Parameters:

- **count** ( _bool_) – Whether to include the number of objects that contain this property.

- **maximum** ( _bool_) – Whether to include the maximum value of this property.

- **mean** ( _bool_) – Whether to include the mean value of this property.

- **median** ( _bool_) – Whether to include the median value of this property.

- **minimum** ( _bool_) – Whether to include the minimum value of this property.

- **mode** ( _bool_) – Whether to include the mode value of this property.

- **sum** – Whether to include the sum of this property.

- **sum\_** ( _bool_)


Returns:

A \_MetricsInteger object that includes the metrics to be returned.

Return type:

[_\_MetricsInteger_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate._MetricsInteger "weaviate.collections.classes.aggregate._MetricsInteger")

number( _count=False_, _maximum=False_, _mean=False_, _median=False_, _minimum=False_, _mode=False_, _sum\_=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#Metrics.number) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.aggregate.Metrics.number "Link to this definition")

Define the metrics to be returned for a NUMBER or NUMBER\_ARRAY property when aggregating over a collection.

If none of the arguments are provided then all metrics will be returned.

Parameters:

- **count** ( _bool_) – Whether to include the number of objects that contain this property.

- **maximum** ( _bool_) – Whether to include the maximum value of this property.

- **mean** ( _bool_) – Whether to include the mean value of this property.

- **median** ( _bool_) – Whether to include the median value of this property.

- **minimum** ( _bool_) – Whether to include the minimum value of this property.

- **mode** ( _bool_) – Whether to include the mode value of this property.

- **sum** – Whether to include the sum of this property.

- **sum\_** ( _bool_)


Returns:

A \_MetricsNumber object that includes the metrics to be returned.

Return type:

[_\_MetricsNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate._MetricsNumber "weaviate.collections.classes.aggregate._MetricsNumber")

reference( _pointing\_to=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#Metrics.reference) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.aggregate.Metrics.reference "Link to this definition")

Define the metrics to be returned for a cross-reference property when aggregating over a collection.

If none of the arguments are provided then all metrics will be returned.

Parameters:

**pointing\_to** ( _bool_) – The UUIDs of the objects that are being pointed to.

Returns:

A \_MetricsReference object that includes the metrics to be returned.

Return type:

[_\_MetricsReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate._MetricsReference "weaviate.collections.classes.aggregate._MetricsReference")

text( _count=False_, _top\_occurrences\_count=False_, _top\_occurrences\_value=False_, _limit=None_, _min\_occurrences=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#Metrics.text) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.aggregate.Metrics.text "Link to this definition")

Define the metrics to be returned for a TEXT or TEXT\_ARRAY property when aggregating over a collection.

If none of the arguments are provided then all metrics will be returned.

Parameters:

- **count** ( _bool_) – Whether to include the number of objects that contain this property.

- **top\_occurrences\_count** ( _bool_) – Whether to include the number of the top occurrences of a property’s value.

- **top\_occurrences\_value** ( _bool_) – Whether to include the value of the top occurrences of a property’s value.

- **min\_occurrences** ( _int_ _\|_ _None_) – (Deprecated) The maximum number of top occurrences to return. Use limit instead.

- **limit** ( _int_ _\|_ _None_) – The maximum number of top occurrences to return.


Returns:

A \_MetricsStr object that includes the metrics to be returned.

Return type:

[_\_MetricsText_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate._MetricsText "weaviate.collections.classes.aggregate._MetricsText")

## weaviate.classes.backup [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html\#module-weaviate.classes.backup "Link to this heading")

_class_ weaviate.classes.backup.BackupCompressionLevel( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupCompressionLevel) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupCompressionLevel "Link to this definition")

Bases: `str`, `Enum`

Which compression level should be used to compress the backup.

DEFAULT _='DefaultCompression'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupCompressionLevel.DEFAULT "Link to this definition")BEST\_SPEED _='BestSpeed'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupCompressionLevel.BEST_SPEED "Link to this definition")BEST\_COMPRESSION _='BestCompression'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupCompressionLevel.BEST_COMPRESSION "Link to this definition")_pydanticmodel_ weaviate.classes.backup.BackupConfigCreate [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupConfigCreate) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupConfigCreate "Link to this definition")

Bases: [`_BackupConfigBase`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup._BackupConfigBase "weaviate.backup.backup._BackupConfigBase")

Options to configure the backup when creating a backup.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ CPUPercentage _:int\|None_ _=None_ _(alias'cpu\_percentage')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupConfigCreate.CPUPercentage "Link to this definition")_field_ ChunkSize _:int\|None_ _=None_ _(alias'chunk\_size')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupConfigCreate.ChunkSize "Link to this definition")_field_ CompressionLevel _: [BackupCompressionLevel](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupCompressionLevel "weaviate.backup.backup.BackupCompressionLevel") \|None_ _=None_ _(alias'compression\_level')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupConfigCreate.CompressionLevel "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupConfigCreate._abc_impl "Link to this definition")_pydanticmodel_ weaviate.classes.backup.BackupConfigRestore [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupConfigRestore) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupConfigRestore "Link to this definition")

Bases: [`_BackupConfigBase`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup._BackupConfigBase "weaviate.backup.backup._BackupConfigBase")

Options to configure the backup when restoring a backup.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ CPUPercentage _:int\|None_ _=None_ _(alias'cpu\_percentage')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupConfigRestore.CPUPercentage "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupConfigRestore._abc_impl "Link to this definition")_class_ weaviate.classes.backup.BackupStorage( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupStorage) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupStorage "Link to this definition")

Bases: `str`, `Enum`

Which backend should be used to write the backup to.

FILESYSTEM _='filesystem'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupStorage.FILESYSTEM "Link to this definition")S3 _='s3'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupStorage.S3 "Link to this definition")GCS _='gcs'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupStorage.GCS "Link to this definition")AZURE _='azure'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupStorage.AZURE "Link to this definition")_class_ weaviate.classes.backup.BackupLocation [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup_location.html#BackupLocation) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupLocation "Link to this definition")

Bases: `object`

The dynamic path of a backup.

Azure [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupLocation.Azure "Link to this definition")

alias of [`_BackupLocationAzure`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationAzure "weaviate.backup.backup_location._BackupLocationAzure")

FileSystem [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupLocation.FileSystem "Link to this definition")

alias of [`_BackupLocationFilesystem`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationFilesystem "weaviate.backup.backup_location._BackupLocationFilesystem")

GCP [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupLocation.GCP "Link to this definition")

alias of [`_BackupLocationGCP`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationGCP "weaviate.backup.backup_location._BackupLocationGCP")

S3 [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.backup.BackupLocation.S3 "Link to this definition")

alias of [`_BackupLocationS3`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationS3 "weaviate.backup.backup_location._BackupLocationS3")

## weaviate.classes.batch [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html\#module-weaviate.classes.batch "Link to this heading")

_pydanticmodel_ weaviate.classes.batch.Shard [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/batch.html#Shard) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.batch.Shard "Link to this definition")

Bases: `BaseModel`

Use this class when defining a shard whose vector indexing process will be awaited for in a sync blocking fashion.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ collection _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.batch.Shard.collection "Link to this definition")_field_ tenant _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.batch.Shard.tenant "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.batch.Shard._abc_impl "Link to this definition")

## weaviate.classes.config [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html\#module-weaviate.classes.config "Link to this heading")

_class_ weaviate.classes.config.Configure [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#Configure) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Configure "Link to this definition")

Bases: `object`

Use this factory class to generate the correct object for use when using the collections.create() method. E.g., .multi\_tenancy() will return a MultiTenancyConfigCreate object to be used in the multi\_tenancy\_config argument.

Each class method provides options specific to the named configuration type in the function’s name. Under-the-hood data validation steps
will ensure that any mis-specifications are caught before the request is sent to Weaviate.

Generative [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Configure.Generative "Link to this definition")

alias of [`_Generative`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._Generative "weaviate.collections.classes.config._Generative")

MultiVectors [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Configure.MultiVectors "Link to this definition")

alias of `_MultiVectors`

NamedVectors [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Configure.NamedVectors "Link to this definition")

alias of [`_NamedVectors`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config_named_vectors._NamedVectors "weaviate.collections.classes.config_named_vectors._NamedVectors")

Reranker [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Configure.Reranker "Link to this definition")

alias of [`_Reranker`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._Reranker "weaviate.collections.classes.config._Reranker")

VectorIndex [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Configure.VectorIndex "Link to this definition")

alias of [`_VectorIndex`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config_vector_index._VectorIndex "weaviate.collections.classes.config_vector_index._VectorIndex")

Vectorizer [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Configure.Vectorizer "Link to this definition")

alias of [`_Vectorizer`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config_vectorizers._Vectorizer "weaviate.collections.classes.config_vectorizers._Vectorizer")

Vectors [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Configure.Vectors "Link to this definition")

alias of `_Vectors`

_static_ inverted\_index( _bm25\_b=None_, _bm25\_k1=None_, _cleanup\_interval\_seconds=None_, _index\_timestamps=None_, _index\_property\_length=None_, _index\_null\_state=None_, _stopwords\_preset=None_, _stopwords\_additions=None_, _stopwords\_removals=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#Configure.inverted_index) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Configure.inverted_index "Link to this definition")

Create an InvertedIndexConfigCreate object to be used when defining the configuration of the keyword searching algorithm of Weaviate.

Parameters:

- **<https** ( _See \`the docs_) –

//weaviate.io/developers/weaviate/configuration/indexes#configure-the-inverted-index>\`\_ for details!

- **bm25\_b** ( _float_ _\|_ _None_)

- **bm25\_k1** ( _float_ _\|_ _None_)

- **cleanup\_interval\_seconds** ( _int_ _\|_ _None_)

- **index\_timestamps** ( _bool_ _\|_ _None_)

- **index\_property\_length** ( _bool_ _\|_ _None_)

- **index\_null\_state** ( _bool_ _\|_ _None_)

- **stopwords\_preset** ( [_StopwordsPreset_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.StopwordsPreset "weaviate.collections.classes.config.StopwordsPreset") _\|_ _None_)

- **stopwords\_additions** ( _List_ _\[_ _str_ _\]_ _\|_ _None_)

- **stopwords\_removals** ( _List_ _\[_ _str_ _\]_ _\|_ _None_)


Return type:

[_\_InvertedIndexConfigCreate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._InvertedIndexConfigCreate "weaviate.collections.classes.config._InvertedIndexConfigCreate")

_static_ multi\_tenancy( _enabled=True_, _auto\_tenant\_creation=None_, _auto\_tenant\_activation=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#Configure.multi_tenancy) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Configure.multi_tenancy "Link to this definition")

Create a MultiTenancyConfigCreate object to be used when defining the multi-tenancy configuration of Weaviate.

Parameters:

- **enabled** ( _bool_) – Whether multi-tenancy is enabled. Defaults to True.

- **auto\_tenant\_creation** ( _bool_ _\|_ _None_) – Automatically create nonexistent tenants during object creation. Defaults to None, which uses the server-defined default.

- **auto\_tenant\_activation** ( _bool_ _\|_ _None_) – Automatically turn tenants implicitly HOT when they are accessed. Defaults to None, which uses the server-defined default.


Return type:

[_\_MultiTenancyConfigCreate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._MultiTenancyConfigCreate "weaviate.collections.classes.config._MultiTenancyConfigCreate")

_static_ replication( _factor=None_, _async\_enabled=None_, _deletion\_strategy=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#Configure.replication) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Configure.replication "Link to this definition")

Create a ReplicationConfigCreate object to be used when defining the replication configuration of Weaviate.

NOTE: async\_enabled is only available with WeaviateDB >=v1.26.0

Parameters:

- **factor** ( _int_ _\|_ _None_) – The replication factor.

- **async\_enabled** ( _bool_ _\|_ _None_) – Enabled async replication.

- **deletion\_strategy** ( [_ReplicationDeletionStrategy_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.ReplicationDeletionStrategy "weaviate.collections.classes.config.ReplicationDeletionStrategy") _\|_ _None_) – How conflicts between different nodes about deleted objects are resolved.


Return type:

[_\_ReplicationConfigCreate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._ReplicationConfigCreate "weaviate.collections.classes.config._ReplicationConfigCreate")

_static_ sharding( _virtual\_per\_physical=None_, _desired\_count=None_, _actual\_count=None_, _desired\_virtual\_count=None_, _actual\_virtual\_count=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#Configure.sharding) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Configure.sharding "Link to this definition")

Create a ShardingConfigCreate object to be used when defining the sharding configuration of Weaviate.

NOTE: You can only use one of Sharding or Replication, not both.

See [the docs](https://weaviate.io/developers/weaviate/concepts/replication-architecture#replication-vs-sharding) for more details.

Parameters:

- **virtual\_per\_physical** ( _int_ _\|_ _None_) – The number of virtual shards per physical shard.

- **desired\_count** ( _int_ _\|_ _None_) – The desired number of physical shards.

- **actual\_count** ( _int_ _\|_ _None_) – The actual number of physical shards. This is a read-only field so has no effect.
It is kept for backwards compatibility but will be removed in a future release.

- **desired\_virtual\_count** ( _int_ _\|_ _None_) – The desired number of virtual shards.

- **actual\_virtual\_count** ( _int_ _\|_ _None_) – The actual number of virtual shards. This is a read-only field so has no effect.
It is kept for backwards compatibility but will be removed in a future release.


Return type:

[_\_ShardingConfigCreate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._ShardingConfigCreate "weaviate.collections.classes.config._ShardingConfigCreate")

_class_ weaviate.classes.config.ConsistencyLevel( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#ConsistencyLevel) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ConsistencyLevel "Link to this definition")

Bases: `str`, `BaseEnum`

The consistency levels when writing to Weaviate with replication enabled.

ALL [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ConsistencyLevel.ALL "Link to this definition")

Wait for confirmation of write success from all, N, replicas.

ONE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ConsistencyLevel.ONE "Link to this definition")

Wait for confirmation of write success from only one replica.

QUORUM [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ConsistencyLevel.QUORUM "Link to this definition")

Wait for confirmation of write success from a quorum: N/2+1, of replicas.

ALL _='ALL'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id6 "Link to this definition")ONE _='ONE'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id7 "Link to this definition")QUORUM _='QUORUM'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id8 "Link to this definition")_class_ weaviate.classes.config.Reconfigure [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#Reconfigure) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Reconfigure "Link to this definition")

Bases: `object`

Use this factory class to generate the correct xxxConfig object for use when using the collection.update() method.

Each staticmethod provides options specific to the named configuration type in the function’s name. Under-the-hood data validation steps
will ensure that any mis-specifications are caught before the request is sent to Weaviate. Only those configurations that are mutable are
available in this class. If you wish to update the configuration of an immutable aspect of your collection then you will have to delete
the collection and re-create it with the new configuration.

Generative [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Reconfigure.Generative "Link to this definition")

alias of [`_Generative`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._Generative "weaviate.collections.classes.config._Generative")

NamedVectors [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Reconfigure.NamedVectors "Link to this definition")

alias of [`_NamedVectorsUpdate`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config_named_vectors._NamedVectorsUpdate "weaviate.collections.classes.config_named_vectors._NamedVectorsUpdate")

Reranker [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Reconfigure.Reranker "Link to this definition")

alias of [`_Reranker`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._Reranker "weaviate.collections.classes.config._Reranker")

VectorIndex [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Reconfigure.VectorIndex "Link to this definition")

alias of [`_VectorIndexUpdate`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._VectorIndexUpdate "weaviate.collections.classes.config._VectorIndexUpdate")

Vectors [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Reconfigure.Vectors "Link to this definition")

alias of `_VectorsUpdate`

_static_ inverted\_index( _bm25\_b=None_, _bm25\_k1=None_, _cleanup\_interval\_seconds=None_, _stopwords\_additions=None_, _stopwords\_preset=None_, _stopwords\_removals=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#Reconfigure.inverted_index) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Reconfigure.inverted_index "Link to this definition")

Create an InvertedIndexConfigUpdate object.

Use this method when defining the inverted\_index\_config argument in collection.update().

Parameters:

- **<https** ( _See \`the docs_) –

//weaviate.io/developers/weaviate/configuration/indexes#configure-the-inverted-index>\`\_ for a more detailed view!

- **bm25\_b** ( _float_ _\|_ _None_)

- **bm25\_k1** ( _float_ _\|_ _None_)

- **cleanup\_interval\_seconds** ( _int_ _\|_ _None_)

- **stopwords\_additions** ( _List_ _\[_ _str_ _\]_ _\|_ _None_)

- **stopwords\_preset** ( [_StopwordsPreset_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.StopwordsPreset "weaviate.collections.classes.config.StopwordsPreset") _\|_ _None_)

- **stopwords\_removals** ( _List_ _\[_ _str_ _\]_ _\|_ _None_)


Return type:

[_\_InvertedIndexConfigUpdate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._InvertedIndexConfigUpdate "weaviate.collections.classes.config._InvertedIndexConfigUpdate")

_static_ multi\_tenancy( _auto\_tenant\_creation=None_, _auto\_tenant\_activation=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#Reconfigure.multi_tenancy) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Reconfigure.multi_tenancy "Link to this definition")

Create a MultiTenancyConfigUpdate object.

Use this method when defining the multi\_tenancy argument in collection.update().

Parameters:

- **auto\_tenant\_creation** ( _bool_ _\|_ _None_) – When set, implicitly creates nonexistent tenants during object creation

- **auto\_tenant\_activation** ( _bool_ _\|_ _None_) – Automatically turn tenants implicitly HOT when they are accessed. Defaults to None, which uses the server-defined default.


Return type:

[_\_MultiTenancyConfigUpdate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._MultiTenancyConfigUpdate "weaviate.collections.classes.config._MultiTenancyConfigUpdate")

_static_ replication( _factor=None_, _async\_enabled=None_, _deletion\_strategy=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#Reconfigure.replication) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Reconfigure.replication "Link to this definition")

Create a ReplicationConfigUpdate object.

Use this method when defining the replication\_config argument in collection.update().

Parameters:

- **factor** ( _int_ _\|_ _None_) – The replication factor.

- **async\_enabled** ( _bool_ _\|_ _None_) – Enable async replication.

- **deletion\_strategy** ( [_ReplicationDeletionStrategy_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.ReplicationDeletionStrategy "weaviate.collections.classes.config.ReplicationDeletionStrategy") _\|_ _None_) – How conflicts between different nodes about deleted objects are resolved.


Return type:

[_\_ReplicationConfigUpdate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._ReplicationConfigUpdate "weaviate.collections.classes.config._ReplicationConfigUpdate")

_class_ weaviate.classes.config.DataType( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#DataType) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType "Link to this definition")

Bases: `str`, `BaseEnum`

The available primitive data types in Weaviate.

TEXT [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.TEXT "Link to this definition")

Text data type.

TEXT\_ARRAY [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.TEXT_ARRAY "Link to this definition")

Text array data type.

INT [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.INT "Link to this definition")

Integer data type.

INT\_ARRAY [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.INT_ARRAY "Link to this definition")

Integer array data type.

BOOL [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.BOOL "Link to this definition")

Boolean data type.

BOOL\_ARRAY [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.BOOL_ARRAY "Link to this definition")

Boolean array data type.

NUMBER [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.NUMBER "Link to this definition")

Number data type.

NUMBER\_ARRAY [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.NUMBER_ARRAY "Link to this definition")

Number array data type.

DATE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.DATE "Link to this definition")

Date data type.

DATE\_ARRAY [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.DATE_ARRAY "Link to this definition")

Date array data type.

UUID [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.UUID "Link to this definition")

UUID data type.

UUID\_ARRAY [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.UUID_ARRAY "Link to this definition")

UUID array data type.

GEO\_COORDINATES [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.GEO_COORDINATES "Link to this definition")

Geo coordinates data type.

BLOB [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.BLOB "Link to this definition")

Blob data type.

PHONE\_NUMBER [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.PHONE_NUMBER "Link to this definition")

Phone number data type.

OBJECT [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.OBJECT "Link to this definition")

Object data type.

OBJECT\_ARRAY [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.DataType.OBJECT_ARRAY "Link to this definition")

Object array data type.

TEXT _='text'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id11 "Link to this definition")TEXT\_ARRAY _='text\[\]'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id12 "Link to this definition")INT _='int'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id13 "Link to this definition")INT\_ARRAY _='int\[\]'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id14 "Link to this definition")BOOL _='boolean'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id15 "Link to this definition")BOOL\_ARRAY _='boolean\[\]'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id16 "Link to this definition")NUMBER _='number'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id17 "Link to this definition")NUMBER\_ARRAY _='number\[\]'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id18 "Link to this definition")DATE _='date'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id19 "Link to this definition")DATE\_ARRAY _='date\[\]'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id20 "Link to this definition")UUID _='uuid'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id21 "Link to this definition")UUID\_ARRAY _='uuid\[\]'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id22 "Link to this definition")GEO\_COORDINATES _='geoCoordinates'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id23 "Link to this definition")BLOB _='blob'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id24 "Link to this definition")PHONE\_NUMBER _='phoneNumber'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id25 "Link to this definition")OBJECT _='object'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id26 "Link to this definition")OBJECT\_ARRAY _='object\[\]'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id27 "Link to this definition")_class_ weaviate.classes.config.GenerativeSearches( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#GenerativeSearches) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.GenerativeSearches "Link to this definition")

Bases: `str`, `BaseEnum`

The available generative search modules in Weaviate.

These modules generate text from text-based inputs.
See the [docs](https://weaviate.io/developers/weaviate/modules/reader-generator-modules) for more details.

AWS [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.GenerativeSearches.AWS "Link to this definition")

Weaviate module backed by AWS Bedrock generative models.

ANTHROPIC [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.GenerativeSearches.ANTHROPIC "Link to this definition")

Weaviate module backed by Anthropic generative models.

ANYSCALE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.GenerativeSearches.ANYSCALE "Link to this definition")

Weaviate module backed by Anyscale generative models.

COHERE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.GenerativeSearches.COHERE "Link to this definition")

Weaviate module backed by Cohere generative models.

DATABRICKS [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.GenerativeSearches.DATABRICKS "Link to this definition")

Weaviate module backed by Databricks generative models.

FRIENDLIAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.GenerativeSearches.FRIENDLIAI "Link to this definition")

Weaviate module backed by FriendliAI generative models.

MISTRAL [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.GenerativeSearches.MISTRAL "Link to this definition")

Weaviate module backed by Mistral generative models.

NVIDIA [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.GenerativeSearches.NVIDIA "Link to this definition")

Weaviate module backed by NVIDIA generative models.

OLLAMA [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.GenerativeSearches.OLLAMA "Link to this definition")

Weaviate module backed by generative models deployed on Ollama infrastructure.

OPENAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.GenerativeSearches.OPENAI "Link to this definition")

Weaviate module backed by OpenAI and Azure-OpenAI generative models.

PALM [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.GenerativeSearches.PALM "Link to this definition")

Weaviate module backed by PaLM generative models.

AWS _='generative-aws'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id28 "Link to this definition")ANTHROPIC _='generative-anthropic'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id29 "Link to this definition")ANYSCALE _='generative-anyscale'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id30 "Link to this definition")COHERE _='generative-cohere'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id31 "Link to this definition")DATABRICKS _='generative-databricks'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id32 "Link to this definition")DUMMY _='generative-dummy'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.GenerativeSearches.DUMMY "Link to this definition")FRIENDLIAI _='generative-friendliai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id33 "Link to this definition")MISTRAL _='generative-mistral'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id34 "Link to this definition")NVIDIA _='generative-nvidia'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id35 "Link to this definition")OLLAMA _='generative-ollama'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id36 "Link to this definition")OPENAI _='generative-openai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id37 "Link to this definition")PALM _='generative-palm'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id38 "Link to this definition")XAI _='generative-xai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.GenerativeSearches.XAI "Link to this definition")_class_ weaviate.classes.config.Integrations [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/integrations.html#Integrations) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Integrations "Link to this definition")

Bases: `object`

_static_ cohere( _\*_, _api\_key_, _base\_url=None_, _requests\_per\_minute\_embeddings=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/integrations.html#Integrations.cohere) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Integrations.cohere "Link to this definition")Parameters:

- **api\_key** ( _str_)

- **base\_url** ( _str_ _\|_ _None_)

- **requests\_per\_minute\_embeddings** ( _int_ _\|_ _None_)


Return type:

_\_IntegrationConfig_

_static_ huggingface( _\*_, _api\_key_, _requests\_per\_minute\_embeddings=None_, _base\_url=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/integrations.html#Integrations.huggingface) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Integrations.huggingface "Link to this definition")Parameters:

- **api\_key** ( _str_)

- **requests\_per\_minute\_embeddings** ( _int_ _\|_ _None_)

- **base\_url** ( _str_ _\|_ _None_)


Return type:

_\_IntegrationConfig_

_static_ jinaai( _\*_, _api\_key_, _requests\_per\_minute\_embeddings=None_, _base\_url=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/integrations.html#Integrations.jinaai) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Integrations.jinaai "Link to this definition")Parameters:

- **api\_key** ( _str_)

- **requests\_per\_minute\_embeddings** ( _int_ _\|_ _None_)

- **base\_url** ( _str_ _\|_ _None_)


Return type:

_\_IntegrationConfig_

_static_ mistral( _\*_, _api\_key_, _request\_per\_minute\_embeddings=None_, _tokens\_per\_minute\_embeddings=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/integrations.html#Integrations.mistral) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Integrations.mistral "Link to this definition")Parameters:

- **api\_key** ( _str_)

- **request\_per\_minute\_embeddings** ( _int_ _\|_ _None_)

- **tokens\_per\_minute\_embeddings** ( _int_ _\|_ _None_)


Return type:

_\_IntegrationConfig_

_static_ openai( _\*_, _api\_key_, _requests\_per\_minute\_embeddings=None_, _tokens\_per\_minute\_embeddings=None_, _organization=None_, _base\_url=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/integrations.html#Integrations.openai) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Integrations.openai "Link to this definition")Parameters:

- **api\_key** ( _str_)

- **requests\_per\_minute\_embeddings** ( _int_ _\|_ _None_)

- **tokens\_per\_minute\_embeddings** ( _int_ _\|_ _None_)

- **organization** ( _str_ _\|_ _None_)

- **base\_url** ( _str_ _\|_ _None_)


Return type:

_\_IntegrationConfig_

_static_ voyageai( _\*_, _api\_key_, _requests\_per\_minute\_embeddings=None_, _tokens\_per\_minute\_embeddings=None_, _base\_url=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/integrations.html#Integrations.voyageai) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Integrations.voyageai "Link to this definition")Parameters:

- **api\_key** ( _str_)

- **requests\_per\_minute\_embeddings** ( _int_ _\|_ _None_)

- **tokens\_per\_minute\_embeddings** ( _int_ _\|_ _None_)

- **base\_url** ( _str_ _\|_ _None_)


Return type:

_\_IntegrationConfig_

_pydanticmodel_ weaviate.classes.config.Multi2VecField [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config_vectorizers.html#Multi2VecField) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Multi2VecField "Link to this definition")

Bases: `BaseModel`

Use this class when defining the fields to use in the Multi2VecClip and Multi2VecBind vectorizers.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ name _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Multi2VecField.name "Link to this definition")_field_ weight _:float\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Multi2VecField.weight "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Multi2VecField._abc_impl "Link to this definition")_class_ weaviate.classes.config.MultiVectorAggregation( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config_vector_index.html#MultiVectorAggregation) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.MultiVectorAggregation "Link to this definition")

Bases: `str`, `BaseEnum`

Aggregation type to use for multivector indices.

MAX\_SIM [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.MultiVectorAggregation.MAX_SIM "Link to this definition")

Maximum similarity.

MAX\_SIM _='maxSim'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id39 "Link to this definition")_class_ weaviate.classes.config.ReplicationDeletionStrategy( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#ReplicationDeletionStrategy) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ReplicationDeletionStrategy "Link to this definition")

Bases: `str`, `BaseEnum`

How object deletions in multi node environments should be resolved.

PERMANENT\_DELETION [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ReplicationDeletionStrategy.PERMANENT_DELETION "Link to this definition")

Once an object has been deleted on one node it will be deleted on all nodes in case of conflicts.

NO\_AUTOMATED\_RESOLUTION [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ReplicationDeletionStrategy.NO_AUTOMATED_RESOLUTION "Link to this definition")

No deletion resolution.

DELETE\_ON\_CONFLICT _='DeleteOnConflict'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ReplicationDeletionStrategy.DELETE_ON_CONFLICT "Link to this definition")NO\_AUTOMATED\_RESOLUTION _='NoAutomatedResolution'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id40 "Link to this definition")TIME\_BASED\_RESOLUTION _='TimeBasedResolution'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ReplicationDeletionStrategy.TIME_BASED_RESOLUTION "Link to this definition")_pydanticmodel_ weaviate.classes.config.Property [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#Property) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property "Link to this definition")

Bases: [`_ConfigCreateModel`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config_base._ConfigCreateModel "weaviate.collections.classes.config_base._ConfigCreateModel")

This class defines the structure of a data property that a collection can have within Weaviate.

name [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property.name "Link to this definition")

The name of the property, REQUIRED.

data\_type [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property.data_type "Link to this definition")

The data type of the property, REQUIRED.

description [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property.description "Link to this definition")

A description of the property.

index\_filterable [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property.index_filterable "Link to this definition")

Whether the property should be filterable in the inverted index.

index\_range\_filters [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property.index_range_filters "Link to this definition")

Whether the property should support range filters in the inverted index.

index\_searchable [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property.index_searchable "Link to this definition")

Whether the property should be searchable in the inverted index.

nested\_properties [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property.nested_properties "Link to this definition")

nested properties for data type OBJECT and OBJECT\_ARRAY\`.

skip\_vectorization [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property.skip_vectorization "Link to this definition")

Whether to skip vectorization of the property. Defaults to False.

tokenization [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property.tokenization "Link to this definition")

The tokenization method to use for the inverted index. Defaults to None.

vectorize\_property\_name [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property.vectorize_property_name "Link to this definition")

Whether to vectorize the property name. Defaults to True.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ dataType _: [DataType](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.DataType "weaviate.collections.classes.config.DataType")_ _\[Required\]_ _(alias'data\_type')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property.dataType "Link to this definition")_field_ description _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id41 "Link to this definition")_field_ indexFilterable _:bool\|None_ _=None_ _(alias'index\_filterable')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property.indexFilterable "Link to this definition")_field_ indexRangeFilters _:bool\|None_ _=None_ _(alias'index\_range\_filters')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property.indexRangeFilters "Link to this definition")_field_ indexSearchable _:bool\|None_ _=None_ _(alias'index\_searchable')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property.indexSearchable "Link to this definition")_field_ name _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id42 "Link to this definition")Validated by:

- `_check_name`


_field_ nestedProperties _: [Property](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property "weaviate.classes.config.Property") \|List\[ [Property](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property "weaviate.classes.config.Property")\]\|None_ _=None_ _(alias'nested\_properties')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property.nestedProperties "Link to this definition")_field_ skip\_vectorization _:bool_ _=False_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id43 "Link to this definition")_field_ tokenization _: [Tokenization](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.Tokenization "weaviate.collections.classes.config.Tokenization") \|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id44 "Link to this definition")_field_ vectorize\_property\_name _:bool_ _=True_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id45 "Link to this definition")\_to\_dict( _vectorizers=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#Property._to_dict) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property._to_dict "Link to this definition")Parameters:

**vectorizers** ( _Sequence_ _\[_ [_Vectorizers_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config_vectorizers.Vectorizers "weaviate.collections.classes.config_vectorizers.Vectorizers") _\|_ [_\_EnumLikeStr_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config_base._EnumLikeStr "weaviate.collections.classes.config_base._EnumLikeStr") _\]_ _\|_ _None_)

Return type:

_Dict_\[str, _Any_\]

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Property._abc_impl "Link to this definition")_class_ weaviate.classes.config.PQEncoderDistribution( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config_vector_index.html#PQEncoderDistribution) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.PQEncoderDistribution "Link to this definition")

Bases: `str`, `BaseEnum`

Distribution of the PQ encoder.

LOG\_NORMAL [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.PQEncoderDistribution.LOG_NORMAL "Link to this definition")

Log-normal distribution.

NORMAL [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.PQEncoderDistribution.NORMAL "Link to this definition")

Normal distribution.

LOG\_NORMAL _='log-normal'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id46 "Link to this definition")NORMAL _='normal'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id47 "Link to this definition")_class_ weaviate.classes.config.PQEncoderType( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config_vector_index.html#PQEncoderType) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.PQEncoderType "Link to this definition")

Bases: `str`, `BaseEnum`

Type of the PQ encoder.

KMEANS [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.PQEncoderType.KMEANS "Link to this definition")

K-means encoder.

TILE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.PQEncoderType.TILE "Link to this definition")

Tile encoder.

KMEANS _='kmeans'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id48 "Link to this definition")TILE _='tile'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id49 "Link to this definition")_pydanticmodel_ weaviate.classes.config.ReferenceProperty [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#ReferenceProperty) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ReferenceProperty "Link to this definition")

Bases: [`_ReferencePropertyBase`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._ReferencePropertyBase "weaviate.collections.classes.config._ReferencePropertyBase")

This class defines properties that are cross references to a single target collection.

Use this class when you want to create a cross-reference in the collection’s config that is capable
of having only cross-references to a single other collection.

name [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ReferenceProperty.name "Link to this definition")

The name of the property, REQUIRED.

target\_collection [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ReferenceProperty.target_collection "Link to this definition")

The name of the target collection, REQUIRED.

description [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ReferenceProperty.description "Link to this definition")

A description of the property.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ description _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id50 "Link to this definition")_field_ target\_collection _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id51 "Link to this definition")MultiTarget [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ReferenceProperty.MultiTarget "Link to this definition")

alias of [`_ReferencePropertyMultiTarget`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._ReferencePropertyMultiTarget "weaviate.collections.classes.config._ReferencePropertyMultiTarget")

\_to\_dict() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#ReferenceProperty._to_dict) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ReferenceProperty._to_dict "Link to this definition")Return type:

_Dict_\[str, _Any_\]

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.ReferenceProperty._abc_impl "Link to this definition")_class_ weaviate.classes.config.Rerankers( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#Rerankers) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Rerankers "Link to this definition")

Bases: `str`, `BaseEnum`

The available reranker modules in Weaviate.

These modules rerank the results of a search query.
See the [docs](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules#re-ranking) for more details.

NONE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Rerankers.NONE "Link to this definition")

No reranker.

COHERE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Rerankers.COHERE "Link to this definition")

Weaviate module backed by Cohere reranking models.

TRANSFORMERS [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Rerankers.TRANSFORMERS "Link to this definition")

Weaviate module backed by Transformers reranking models.

VOYAGEAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Rerankers.VOYAGEAI "Link to this definition")

Weaviate module backed by VoyageAI reranking models.

JINAAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Rerankers.JINAAI "Link to this definition")

Weaviate module backed by JinaAI reranking models.

NVIDIA [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Rerankers.NVIDIA "Link to this definition")

Weaviate module backed by NVIDIA reranking models.

NONE _='none'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id53 "Link to this definition")COHERE _='reranker-cohere'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id54 "Link to this definition")TRANSFORMERS _='reranker-transformers'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id55 "Link to this definition")VOYAGEAI _='reranker-voyageai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id56 "Link to this definition")JINAAI _='reranker-jinaai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id57 "Link to this definition")NVIDIA _='reranker-nvidia'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id58 "Link to this definition")_class_ weaviate.classes.config.StopwordsPreset( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#StopwordsPreset) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.StopwordsPreset "Link to this definition")

Bases: `str`, `BaseEnum`

Preset stopwords to use in the Stopwords class.

EN [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.StopwordsPreset.EN "Link to this definition")

English stopwords.

NONE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.StopwordsPreset.NONE "Link to this definition")

No stopwords.

NONE _='none'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id59 "Link to this definition")EN _='en'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id60 "Link to this definition")_class_ weaviate.classes.config.Tokenization( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#Tokenization) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Tokenization "Link to this definition")

Bases: `str`, `BaseEnum`

The available inverted index tokenization methods for text properties in Weaviate.

WORD [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Tokenization.WORD "Link to this definition")

Tokenize by word.

WHITESPACE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Tokenization.WHITESPACE "Link to this definition")

Tokenize by whitespace.

LOWERCASE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Tokenization.LOWERCASE "Link to this definition")

Tokenize by lowercase.

FIELD [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Tokenization.FIELD "Link to this definition")

Tokenize by field.

GSE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Tokenization.GSE "Link to this definition")

Tokenize using GSE (for Chinese and Japanese).

TRIGRAM [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Tokenization.TRIGRAM "Link to this definition")

Tokenize into trigrams.

KAGOME\_JA [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Tokenization.KAGOME_JA "Link to this definition")

Tokenize using the ‘Kagome’ tokenizer (for Japanese).

KAGOME\_KR [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Tokenization.KAGOME_KR "Link to this definition")

Tokenize using the ‘Kagome’ tokenizer and a Korean MeCab dictionary (for Korean).

WORD _='word'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id61 "Link to this definition")WHITESPACE _='whitespace'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id62 "Link to this definition")LOWERCASE _='lowercase'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id63 "Link to this definition")FIELD _='field'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id64 "Link to this definition")GSE _='gse'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id65 "Link to this definition")TRIGRAM _='trigram'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id66 "Link to this definition")KAGOME\_JA _='kagome\_ja'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id67 "Link to this definition")KAGOME\_KR _='kagome\_kr'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id68 "Link to this definition")_class_ weaviate.classes.config.Vectorizers( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config_vectorizers.html#Vectorizers) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers "Link to this definition")

Bases: `str`, `Enum`

The available vectorization modules in Weaviate.

These modules encode binary data into lists of floats called vectors.
See the [docs](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules) for more details.

NONE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.NONE "Link to this definition")

No vectorizer.

TEXT2VEC\_AWS [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_AWS "Link to this definition")

Weaviate module backed by AWS text-based embedding models.

TEXT2VEC\_COHERE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_COHERE "Link to this definition")

Weaviate module backed by Cohere text-based embedding models.

TEXT2VEC\_CONTEXTIONARY [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_CONTEXTIONARY "Link to this definition")

Weaviate module backed by Contextionary text-based embedding models.

TEXT2VEC\_GPT4ALL [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_GPT4ALL "Link to this definition")

Weaviate module backed by GPT-4-All text-based embedding models.

TEXT2VEC\_HUGGINGFACE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_HUGGINGFACE "Link to this definition")

Weaviate module backed by HuggingFace text-based embedding models.

TEXT2VEC\_OPENAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_OPENAI "Link to this definition")

Weaviate module backed by OpenAI and Azure-OpenAI text-based embedding models.

TEXT2VEC\_PALM [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_PALM "Link to this definition")

Weaviate module backed by PaLM text-based embedding models.

TEXT2VEC\_TRANSFORMERS [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_TRANSFORMERS "Link to this definition")

Weaviate module backed by Transformers text-based embedding models.

TEXT2VEC\_JINAAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_JINAAI "Link to this definition")

Weaviate module backed by Jina AI text-based embedding models.

TEXT2VEC\_VOYAGEAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_VOYAGEAI "Link to this definition")

Weaviate module backed by Voyage AI text-based embedding models.

TEXT2VEC\_NVIDIA [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_NVIDIA "Link to this definition")

Weaviate module backed by NVIDIA text-based embedding models.

TEXT2VEC\_WEAVIATE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_WEAVIATE "Link to this definition")

Weaviate module backed by Weaviate’s self-hosted text-based embedding models.

IMG2VEC\_NEURAL [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.IMG2VEC_NEURAL "Link to this definition")

Weaviate module backed by a ResNet-50 neural network for images.

MULTI2VEC\_CLIP [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.MULTI2VEC_CLIP "Link to this definition")

Weaviate module backed by a Sentence-BERT CLIP model for images and text.

MULTI2VEC\_PALM [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.MULTI2VEC_PALM "Link to this definition")

Weaviate module backed by a palm model for images and text.

MULTI2VEC\_BIND [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.MULTI2VEC_BIND "Link to this definition")

Weaviate module backed by the ImageBind model for images, text, audio, depth, IMU, thermal, and video.

MULTI2VEC\_VOYAGEAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.MULTI2VEC_VOYAGEAI "Link to this definition")

Weaviate module backed by a Voyage AI multimodal embedding models.

MULTI2VEC\_NVIDIA [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.MULTI2VEC_NVIDIA "Link to this definition")

Weaviate module backed by NVIDIA multimodal embedding models.

REF2VEC\_CENTROID [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.REF2VEC_CENTROID "Link to this definition")

Weaviate module backed by a centroid-based model that calculates an object’s vectors from its referenced vectors.

NONE _='none'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id70 "Link to this definition")TEXT2COLBERT\_JINAAI _='text2colbert-jinaai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2COLBERT_JINAAI "Link to this definition")TEXT2VEC\_AWS _='text2vec-aws'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id71 "Link to this definition")TEXT2VEC\_COHERE _='text2vec-cohere'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id72 "Link to this definition")TEXT2VEC\_CONTEXTIONARY _='text2vec-contextionary'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id73 "Link to this definition")TEXT2VEC\_DATABRICKS _='text2vec-databricks'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_DATABRICKS "Link to this definition")TEXT2VEC\_GPT4ALL _='text2vec-gpt4all'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id74 "Link to this definition")TEXT2VEC\_HUGGINGFACE _='text2vec-huggingface'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id75 "Link to this definition")TEXT2VEC\_MISTRAL _='text2vec-mistral'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_MISTRAL "Link to this definition")TEXT2VEC\_MORPH _='text2vec-morph'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_MORPH "Link to this definition")TEXT2VEC\_MODEL2VEC _='text2vec-model2vec'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_MODEL2VEC "Link to this definition")TEXT2VEC\_NVIDIA _='text2vec-nvidia'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id76 "Link to this definition")TEXT2VEC\_OLLAMA _='text2vec-ollama'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.TEXT2VEC_OLLAMA "Link to this definition")TEXT2VEC\_OPENAI _='text2vec-openai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id77 "Link to this definition")TEXT2VEC\_PALM _='text2vec-palm'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id78 "Link to this definition")TEXT2VEC\_TRANSFORMERS _='text2vec-transformers'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id79 "Link to this definition")TEXT2VEC\_JINAAI _='text2vec-jinaai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id80 "Link to this definition")TEXT2VEC\_VOYAGEAI _='text2vec-voyageai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id81 "Link to this definition")TEXT2VEC\_WEAVIATE _='text2vec-weaviate'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id82 "Link to this definition")IMG2VEC\_NEURAL _='img2vec-neural'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id83 "Link to this definition")MULTI2VEC\_AWS _='multi2vec-aws'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.MULTI2VEC_AWS "Link to this definition")MULTI2VEC\_CLIP _='multi2vec-clip'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id84 "Link to this definition")MULTI2VEC\_COHERE _='multi2vec-cohere'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.MULTI2VEC_COHERE "Link to this definition")MULTI2VEC\_JINAAI _='multi2vec-jinaai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.MULTI2VEC_JINAAI "Link to this definition")MULTI2MULTI\_JINAAI _='multi2multivec-jinaai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.Vectorizers.MULTI2MULTI_JINAAI "Link to this definition")MULTI2VEC\_BIND _='multi2vec-bind'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id85 "Link to this definition")MULTI2VEC\_PALM _='multi2vec-palm'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id86 "Link to this definition")MULTI2VEC\_VOYAGEAI _='multi2vec-voyageai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id87 "Link to this definition")MULTI2VEC\_NVIDIA _='multi2vec-nvidia'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id88 "Link to this definition")REF2VEC\_CENTROID _='ref2vec-centroid'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id89 "Link to this definition")_class_ weaviate.classes.config.VectorDistances( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config_vectorizers.html#VectorDistances) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.VectorDistances "Link to this definition")

Bases: `str`, `Enum`

Vector similarity distance metric to be used in the VectorIndexConfig class.

To ensure optimal search results, we recommend reviewing whether your model provider advises a
specific distance metric and following their advice.

COSINE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.VectorDistances.COSINE "Link to this definition")

Cosine distance: [reference](https://en.wikipedia.org/wiki/Cosine_similarity)

DOT [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.VectorDistances.DOT "Link to this definition")

Dot distance: [reference](https://en.wikipedia.org/wiki/Dot_product)

L2\_SQUARED [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.VectorDistances.L2_SQUARED "Link to this definition")

L2 squared distance: [reference](https://en.wikipedia.org/wiki/Euclidean_distance)

HAMMING [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.VectorDistances.HAMMING "Link to this definition")

Hamming distance: [reference](https://en.wikipedia.org/wiki/Hamming_distance)

MANHATTAN [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.VectorDistances.MANHATTAN "Link to this definition")

Manhattan distance: [reference](https://en.wikipedia.org/wiki/Taxicab_geometry)

COSINE _='cosine'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id94 "Link to this definition")DOT _='dot'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id95 "Link to this definition")L2\_SQUARED _='l2-squared'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id96 "Link to this definition")HAMMING _='hamming'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id97 "Link to this definition")MANHATTAN _='manhattan'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id98 "Link to this definition")_class_ weaviate.classes.config.VectorFilterStrategy( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config_vector_index.html#VectorFilterStrategy) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.VectorFilterStrategy "Link to this definition")

Bases: `str`, `Enum`

Set the strategy when doing a filtered HNSW search.

SWEEPING [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.VectorFilterStrategy.SWEEPING "Link to this definition")

Do normal ANN search and skip nodes.

ACORN [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.config.VectorFilterStrategy.ACORN "Link to this definition")

Multi-hop search to find new candidates matching the filter.

SWEEPING _='sweeping'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id99 "Link to this definition")ACORN _='acorn'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id100 "Link to this definition")

## weaviate.classes.data [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html\#module-weaviate.classes.data "Link to this heading")

_class_ weaviate.classes.data.DataObject( _properties=None_, _uuid=None_, _vector=None_, _references=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/data.html#DataObject) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.DataObject "Link to this definition")

Bases: `Generic`\[ `P`, `R`\]

This class represents an entire object within a collection to be used when batching.

Parameters:

- **properties** ( _P_)

- **uuid** ( _str_ _\|_ _UUID_ _\|_ _None_)

- **vector** ( _Mapping_ _\[_ _str_ _,_ _Sequence_ _\[_ _int_ _\|_ _float_ _\]_ _\|_ _Sequence_ _\[_ _Sequence_ _\[_ _int_ _\|_ _float_ _\]_ _\]_ _\]_ _\|_ _Sequence_ _\[_ _int_ _\|_ _float_ _\]_ _\|_ _None_)

- **references** ( _R_)


properties _:P_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.DataObject.properties "Link to this definition")references _:R_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.DataObject.references "Link to this definition")uuid _:str\|UUID\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.DataObject.uuid "Link to this definition")vector _:Mapping\[str,Sequence\[int\|float\]\|Sequence\[Sequence\[int\|float\]\]\]\|Sequence\[int\|float\]\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.DataObject.vector "Link to this definition")_class_ weaviate.classes.data.DataReference( _from\_property_, _from\_uuid_, _to\_uuid_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/data.html#DataReference) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.DataReference "Link to this definition")

Bases: [`_DataReference`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.data._DataReference "weaviate.collections.classes.data._DataReference")

This class represents a reference between objects within a collection to be used when batching.

Parameters:

- **from\_property** ( _str_)

- **from\_uuid** ( _str_ _\|_ _UUID_)

- **to\_uuid** ( _str_ _\|_ _UUID_ _\|_ _List_ _\[_ _str_ _\|_ _UUID_ _\]_)


MultiTarget [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.DataReference.MultiTarget "Link to this definition")

alias of [`DataReferenceMulti`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.data.DataReferenceMulti "weaviate.collections.classes.data.DataReferenceMulti")

\_to\_beacons() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/data.html#DataReference._to_beacons) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.DataReference._to_beacons "Link to this definition")Return type:

_List_\[str\]

_pydanticmodel_ weaviate.classes.data.GeoCoordinate [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/types.html#GeoCoordinate) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.GeoCoordinate "Link to this definition")

Bases: [`_WeaviateInput`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._WeaviateInput "weaviate.collections.classes.types._WeaviateInput")

Input for the geo-coordinate datatype.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ latitude _:float_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.GeoCoordinate.latitude "Link to this definition")Constraints:

- **ge** = -90

- **le** = 90


_field_ longitude _:float_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.GeoCoordinate.longitude "Link to this definition")Constraints:

- **ge** = -180

- **le** = 180


\_to\_dict() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/types.html#GeoCoordinate._to_dict) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.GeoCoordinate._to_dict "Link to this definition")Return type:

_Dict_\[str, float\]

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.GeoCoordinate._abc_impl "Link to this definition")_pydanticmodel_ weaviate.classes.data.PhoneNumber [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/types.html#PhoneNumber) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.PhoneNumber "Link to this definition")

Bases: [`_PhoneNumberBase`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._PhoneNumberBase "weaviate.collections.classes.types._PhoneNumberBase")

Input for the phone number datatype.

default\_country should correspond to the ISO 3166-1 alpha-2 country code.
This is used to figure out the correct countryCode and international format if only a national number (e.g. 0123 4567) is provided.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ default\_country _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.PhoneNumber.default_country "Link to this definition")\_to\_dict() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/types.html#PhoneNumber._to_dict) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.PhoneNumber._to_dict "Link to this definition")Return type:

_Mapping_\[str, str\]

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.data.PhoneNumber._abc_impl "Link to this definition")

## weaviate.classes.debug [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html\#module-weaviate.classes.debug "Link to this heading")

_pydanticmodel_ weaviate.classes.debug.DebugRESTObject [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/debug/types.html#DebugRESTObject) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.debug.DebugRESTObject "Link to this definition")

Bases: `BaseModel`

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ collection _:str_ _\[Required\]_ _(alias'class')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.debug.DebugRESTObject.collection "Link to this definition")_field_ creation\_time _:datetime_ _\[Required\]_ _(alias'creationTimeUnix')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.debug.DebugRESTObject.creation_time "Link to this definition")_field_ last\_update\_time _:datetime_ _\[Required\]_ _(alias'lastUpdateTimeUnix')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.debug.DebugRESTObject.last_update_time "Link to this definition")_field_ properties _:Dict\[str,Any\]_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.debug.DebugRESTObject.properties "Link to this definition")_field_ tenant _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.debug.DebugRESTObject.tenant "Link to this definition")_field_ uuid _:UUID_ _\[Required\]_ _(alias'id')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.debug.DebugRESTObject.uuid "Link to this definition")_field_ vector _:list\[float\]\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.debug.DebugRESTObject.vector "Link to this definition")_field_ vectors _:Dict\[str,list\[float\]\]\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.debug.DebugRESTObject.vectors "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.debug.DebugRESTObject._abc_impl "Link to this definition")

## weaviate.classes.generics [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html\#module-weaviate.classes.generics "Link to this heading")

_class_ weaviate.classes.generics.CrossReferenceAnnotation( _include\_vector=False_, _metadata=None_, _target\_collection=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/internal.html#CrossReferenceAnnotation) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.generics.CrossReferenceAnnotation "Link to this definition")

Bases: `object`

Dataclass to be used when annotating a generic cross reference property with options for retrieving data from the cross referenced object when querying.

Example

```
>>> import typing
>>> import weaviate.classes as wvc
>>>
>>> class One(typing.TypedDict):
...     prop: str
>>>
>>> class Two(typing.TypedDict):
...     one: typing.Annotated[\
...         wvc.CrossReference[One],\
...         wvc.CrossReferenceAnnotation(include_vector=True)\
...     ]

```

Parameters:

- **include\_vector** ( _bool_)

- **metadata** ( [_MetadataQuery_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.MetadataQuery "weaviate.collections.classes.grpc.MetadataQuery") _\|_ _None_)

- **target\_collection** ( _str_ _\|_ _None_)


include\_vector _:bool_ _=False_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.generics.CrossReferenceAnnotation.include_vector "Link to this definition")metadata _: [MetadataQuery](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.MetadataQuery "weaviate.collections.classes.grpc.MetadataQuery") \|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.generics.CrossReferenceAnnotation.metadata "Link to this definition")target\_collection _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.generics.CrossReferenceAnnotation.target_collection "Link to this definition")

## weaviate.classes.init [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html\#module-weaviate.classes.init "Link to this heading")

_class_ weaviate.classes.init.Auth [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/auth.html#Auth) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.Auth "Link to this definition")

Bases: `object`

_static_ api\_key( _api\_key_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/auth.html#Auth.api_key) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.Auth.api_key "Link to this definition")Parameters:

**api\_key** ( _str_)

Return type:

[_\_APIKey_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._APIKey "weaviate.auth._APIKey")

_static_ bearer\_token( _access\_token_, _expires\_in=60_, _refresh\_token=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/auth.html#Auth.bearer_token) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.Auth.bearer_token "Link to this definition")Parameters:

- **access\_token** ( _str_)

- **expires\_in** ( _int_)

- **refresh\_token** ( _str_ _\|_ _None_)


Return type:

[_\_BearerToken_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._BearerToken "weaviate.auth._BearerToken")

_static_ client\_credentials( _client\_secret_, _scope=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/auth.html#Auth.client_credentials) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.Auth.client_credentials "Link to this definition")Parameters:

- **client\_secret** ( _str_)

- **scope** ( _str_ _\|_ _List_ _\[_ _str_ _\]_ _\|_ _None_)


Return type:

[_\_ClientCredentials_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials")

_static_ client\_password( _username_, _password_, _scope=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/auth.html#Auth.client_password) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.Auth.client_password "Link to this definition")Parameters:

- **username** ( _str_)

- **password** ( _str_)

- **scope** ( _str_ _\|_ _List_ _\[_ _str_ _\]_ _\|_ _None_)


Return type:

[_\_ClientPassword_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword")

_pydanticmodel_ weaviate.classes.init.AdditionalConfig [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/config.html#AdditionalConfig) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.AdditionalConfig "Link to this definition")

Bases: `BaseModel`

Use this class to specify the connection and proxy settings for your client when connecting to Weaviate.

When specifying the timeout, you can either provide a tuple with the query and insert timeouts, or a Timeout object.
The Timeout object gives you additional option to configure the init timeout, which controls how long the client
initialisation checks will wait for before throwing. This is useful when you have a slow network connection.

When specifying the proxies, be aware that supplying a URL (str) will populate all of the http, https, and grpc proxies.
In order for this to be possible, you must have a proxy that is capable of handling simultaneous HTTP/1.1 and HTTP/2 traffic.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ connection _: [ConnectionConfig](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.ConnectionConfig "weaviate.config.ConnectionConfig")_ _\[Optional\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.AdditionalConfig.connection "Link to this definition")_field_ proxies _:str\| [Proxies](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Proxies "weaviate.config.Proxies") \|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.AdditionalConfig.proxies "Link to this definition")_field_ timeout\_ _:Tuple\[int,int\]\| [Timeout](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Timeout "weaviate.config.Timeout")_ _\[Optional\]_ _(alias'timeout')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.AdditionalConfig.timeout_ "Link to this definition")_field_ trust\_env _:bool_ _=False_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.AdditionalConfig.trust_env "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.AdditionalConfig._abc_impl "Link to this definition")_property_ timeout _: [Timeout](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Timeout "weaviate.config.Timeout")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.AdditionalConfig.timeout "Link to this definition")_pydanticmodel_ weaviate.classes.init.Proxies [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/config.html#Proxies) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.Proxies "Link to this definition")

Bases: `BaseModel`

Proxy configurations for sending requests to Weaviate through a proxy.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ grpc _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.Proxies.grpc "Link to this definition")_field_ http _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.Proxies.http "Link to this definition")_field_ https _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.Proxies.https "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.Proxies._abc_impl "Link to this definition")_pydanticmodel_ weaviate.classes.init.Timeout [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/config.html#Timeout) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.Timeout "Link to this definition")

Bases: `BaseModel`

Timeouts for the different operations in the client.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ init _:int\|float_ _=2_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.Timeout.init "Link to this definition")Constraints:

- **ge** = 0


_field_ insert _:int\|float_ _=90_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.Timeout.insert "Link to this definition")Constraints:

- **ge** = 0


_field_ query _:int\|float_ _=30_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.Timeout.query "Link to this definition")Constraints:

- **ge** = 0


\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.init.Timeout._abc_impl "Link to this definition")

## weaviate.classes.query [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html\#module-weaviate.classes.query "Link to this heading")

_class_ weaviate.classes.query.Filter [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/filters.html#Filter) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Filter "Link to this definition")

Bases: `object`

This class is used to define filters to be used when querying and deleting from a collection.

It forms the root of a method chaining hierarchy that allows you to iteratively define filters that can
hop between objects through references in a formulaic way.

See [the docs](https://weaviate.io/developers/weaviate/search/filters) for more information.

_static_ all\_of( _filters_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/filters.html#Filter.all_of) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Filter.all_of "Link to this definition")

Combine all filters in the input list with an AND operator.

Parameters:

**filters** ( _List_ _\[_ [_\_Filters_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._Filters "weaviate.collections.classes.filters._Filters") _\]_)

Return type:

[_\_Filters_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._Filters "weaviate.collections.classes.filters._Filters")

_static_ any\_of( _filters_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/filters.html#Filter.any_of) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Filter.any_of "Link to this definition")

Combine all filters in the input list with an OR operator.

Parameters:

**filters** ( _List_ _\[_ [_\_Filters_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._Filters "weaviate.collections.classes.filters._Filters") _\]_)

Return type:

[_\_Filters_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._Filters "weaviate.collections.classes.filters._Filters")

_static_ by\_creation\_time() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/filters.html#Filter.by_creation_time) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Filter.by_creation_time "Link to this definition")

Define a filter based on the creation time to be used when querying and deleting from a collection.

Return type:

[_\_FilterByCreationTime_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._FilterByCreationTime "weaviate.collections.classes.filters._FilterByCreationTime")

_static_ by\_id() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/filters.html#Filter.by_id) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Filter.by_id "Link to this definition")

Define a filter based on the uuid to be used when querying and deleting from a collection.

Return type:

[_\_FilterById_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._FilterById "weaviate.collections.classes.filters._FilterById")

_static_ by\_property( _name_, _length=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/filters.html#Filter.by_property) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Filter.by_property "Link to this definition")

Define a filter based on a property to be used when querying and deleting from a collection.

Parameters:

- **name** ( _str_)

- **length** ( _bool_)


Return type:

[_\_FilterByProperty_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._FilterByProperty "weaviate.collections.classes.filters._FilterByProperty")

_static_ by\_ref( _link\_on_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/filters.html#Filter.by_ref) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Filter.by_ref "Link to this definition")

Define a filter based on a reference to be used when querying and deleting from a collection.

Parameters:

**link\_on** ( _str_)

Return type:

[_\_FilterByRef_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._FilterByRef "weaviate.collections.classes.filters._FilterByRef")

_static_ by\_ref\_count( _link\_on_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/filters.html#Filter.by_ref_count) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Filter.by_ref_count "Link to this definition")

Define a filter based on the number of references to be used when querying and deleting from a collection.

Parameters:

**link\_on** ( _str_)

Return type:

[_\_FilterByCount_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._FilterByCount "weaviate.collections.classes.filters._FilterByCount")

_static_ by\_ref\_multi\_target( _link\_on_, _target\_collection_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/filters.html#Filter.by_ref_multi_target) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Filter.by_ref_multi_target "Link to this definition")

Define a filter based on a reference to be used when querying and deleting from a collection.

Parameters:

- **link\_on** ( _str_)

- **target\_collection** ( _str_)


Return type:

[_\_FilterByRef_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._FilterByRef "weaviate.collections.classes.filters._FilterByRef")

_static_ by\_update\_time() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/filters.html#Filter.by_update_time) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Filter.by_update_time "Link to this definition")

Define a filter based on the update time to be used when querying and deleting from a collection.

Return type:

[_\_FilterByUpdateTime_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._FilterByUpdateTime "weaviate.collections.classes.filters._FilterByUpdateTime")

_pydanticmodel_ weaviate.classes.query.GeoCoordinate [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/types.html#GeoCoordinate) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GeoCoordinate "Link to this definition")

Bases: [`_WeaviateInput`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._WeaviateInput "weaviate.collections.classes.types._WeaviateInput")

Input for the geo-coordinate datatype.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ latitude _:float_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GeoCoordinate.latitude "Link to this definition")Constraints:

- **ge** = -90

- **le** = 90


_field_ longitude _:float_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GeoCoordinate.longitude "Link to this definition")Constraints:

- **ge** = -180

- **le** = 180


\_to\_dict() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/types.html#GeoCoordinate._to_dict) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GeoCoordinate._to_dict "Link to this definition")Return type:

_Dict_\[str, float\]

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GeoCoordinate._abc_impl "Link to this definition")_class_ weaviate.classes.query.GenerativeConfig [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/generative.html#GenerativeConfig) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GenerativeConfig "Link to this definition")

Bases: `object`

Use this factory class to create the correct object for the generative\_provider argument in the search methods of the .generate namespace.

Each staticmethod provides options specific to the named generative search module in the function’s name. Under-the-hood data validation steps
will ensure that any mis-specifications will be caught before the request is sent to Weaviate.

_static_ anthropic( _\*_, _base\_url=None_, _model=None_, _max\_tokens=None_, _stop\_sequences=None_, _temperature=None_, _top\_k=None_, _top\_p=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/generative.html#GenerativeConfig.anthropic) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GenerativeConfig.anthropic "Link to this definition")

Create a \_GenerativeAnthropic object for use when performing dynamic AI generation using the generative-anthropic module.

Parameters:

- **base\_url** ( _str_ _\|_ _None_) – The base URL to send the API request to. Defaults to None, which uses the server-defined default

- **model** ( _str_ _\|_ _None_) – The model to use. Defaults to None, which uses the server-defined default

- **max\_tokens** ( _int_ _\|_ _None_) – The maximum number of tokens to generate. Defaults to None, which uses the server-defined default

- **stop\_sequences** ( _List_ _\[_ _str_ _\]_ _\|_ _None_) – The stop sequences to use. Defaults to None, which uses the server-defined default

- **temperature** ( _float_ _\|_ _None_) – The temperature to use. Defaults to None, which uses the server-defined default

- **top\_k** ( _int_ _\|_ _None_) – The top K to use. Defaults to None, which uses the server-defined default

- **top\_p** ( _float_ _\|_ _None_) – The top P to use. Defaults to None, which uses the server-defined default


Return type:

_\_GenerativeConfigRuntime_

_static_ anyscale( _\*_, _base\_url=None_, _model=None_, _temperature=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/generative.html#GenerativeConfig.anyscale) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GenerativeConfig.anyscale "Link to this definition")

Create a \_GenerativeAnyscale object for use when performing dynamic AI generation using the generative-anyscale module.

Parameters:

- **base\_url** ( _str_ _\|_ _None_) – The base URL to send the API request to. Defaults to None, which uses the server-defined default

- **model** ( _str_ _\|_ _None_) – The model to use. Defaults to None, which uses the server-defined default

- **temperature** ( _float_ _\|_ _None_) – The temperature to use. Defaults to None, which uses the server-defined default


Return type:

_\_GenerativeConfigRuntime_

_static_ aws( _\*_, _endpoint=None_, _model=None_, _region=None_, _service=None_, _target\_model=None_, _target\_variant=None_, _temperature=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/generative.html#GenerativeConfig.aws) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GenerativeConfig.aws "Link to this definition")

Create a \_GenerativeAWS object for use when performing dynamic AI generation using the generative-aws module.

See the [documentation](https://weaviate.io/developers/weaviate/modules/reader-generator-modules/generative-aws)
for detailed usage.

Parameters:

- **endpoint** ( _str_ _\|_ _None_) – The endpoint to use when requesting the generation. Defaults to None, which uses the server-defined default

- **model** ( _str_ _\|_ _None_) – The model to use. Defaults to None, which uses the server-defined default

- **region** ( _str_ _\|_ _None_) – The AWS region to run the model from. Defaults to None, which uses the server-defined default

- **service** ( _Literal_ _\[_ _'bedrock'_ _,_ _'sagemaker'_ _\]_ _\|_ _str_ _\|_ _None_) – The AWS service to use. Defaults to None, which uses the server-defined default

- **target\_model** ( _str_ _\|_ _None_) – The target model to use. Defaults to None, which uses the server-defined default

- **target\_variant** ( _str_ _\|_ _None_) – The target variant to use. Defaults to None, which uses the server-defined default

- **temperature** ( _float_ _\|_ _None_) – The temperature to use. Defaults to None, which uses the server-defined default


Return type:

_\_GenerativeConfigRuntime_

_static_ azure\_openai( _\*_, _api\_version=None_, _base\_url=None_, _deployment\_id=None_, _frequency\_penalty=None_, _max\_tokens=None_, _model=None_, _presence\_penalty=None_, _resource\_name=None_, _stop=None_, _temperature=None_, _top\_p=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/generative.html#GenerativeConfig.azure_openai) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GenerativeConfig.azure_openai "Link to this definition")

Create a \_GenerativeOpenAI object for use when performing AI generation using the Azure-backed generative-openai module.

See the [documentation](https://weaviate.io/developers/weaviate/modules/reader-generator-modules/generative-openai)
for detailed usage.

Parameters:

- **api\_version** ( _str_ _\|_ _None_) – The API version to use. Defaults to None, which uses the server-defined default

- **base\_url** ( _str_ _\|_ _None_) – The base URL where the API request should go. Defaults to None, which uses the server-defined default

- **deployment\_id** ( _str_ _\|_ _None_) – The deployment ID to use. Defaults to None, which uses the server-defined default

- **frequency\_penalty** ( _float_ _\|_ _None_) – The frequency penalty to use. Defaults to None, which uses the server-defined default

- **max\_tokens** ( _int_ _\|_ _None_) – The maximum number of tokens to generate. Defaults to None, which uses the server-defined default

- **model** ( _str_ _\|_ _None_) – The model to use. Defaults to None, which uses the server-defined default

- **presence\_penalty** ( _float_ _\|_ _None_) – The presence penalty to use. Defaults to None, which uses the server-defined default

- **resource\_name** ( _str_ _\|_ _None_) – The name of the OpenAI resource to use. Defaults to None, which uses the server-defined default

- **stop** ( _List_ _\[_ _str_ _\]_ _\|_ _None_) – The stop sequences to use. Defaults to None, which uses the server-defined default

- **temperature** ( _float_ _\|_ _None_) – The temperature to use. Defaults to None, which uses the server-defined default

- **top\_p** ( _float_ _\|_ _None_) – The top P to use. Defaults to None, which uses the server-defined default


Return type:

_\_GenerativeConfigRuntime_

_static_ cohere( _\*_, _base\_url=None_, _k=None_, _max\_tokens=None_, _model=None_, _p=None_, _presence\_penalty=None_, _stop\_sequences=None_, _temperature=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/generative.html#GenerativeConfig.cohere) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GenerativeConfig.cohere "Link to this definition")

Create a \_GenerativeCohere object for use when performing AI generation using the generative-cohere module.

See the [documentation](https://weaviate.io/developers/weaviate/modules/reader-generator-modules/generative-cohere)
for detailed usage.

Parameters:

- **base\_url** ( _str_ _\|_ _None_) – The base URL where the API request should go. Defaults to None, which uses the server-defined default

- **k** ( _int_ _\|_ _None_) – The top K property to use. Defaults to None, which uses the server-defined default

- **max\_tokens** ( _int_ _\|_ _None_) – The maximum number of tokens to generate. Defaults to None, which uses the server-defined default

- **model** ( _str_ _\|_ _None_) – The model to use. Defaults to None, which uses the server-defined default

- **p** ( _float_ _\|_ _None_) – The top P property to use. Defaults to None, which uses the server-defined default

- **presence\_penalty** ( _float_ _\|_ _None_) – The presence penalty to use. Defaults to None, which uses the server-defined default

- **stop\_sequences** ( _List_ _\[_ _str_ _\]_ _\|_ _None_) – The stop sequences to use. Defaults to None, which uses the server-defined default

- **temperature** ( _float_ _\|_ _None_) – The temperature to use. Defaults to None, which uses the server-defined default


Return type:

_\_GenerativeConfigRuntime_

_static_ databricks( _\*_, _endpoint_, _frequency\_penalty=None_, _log\_probs=None_, _max\_tokens=None_, _model=None_, _n=None_, _presence\_penalty=None_, _stop=None_, _temperature=None_, _top\_log\_probs=None_, _top\_p=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/generative.html#GenerativeConfig.databricks) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GenerativeConfig.databricks "Link to this definition")

Create a \_GenerativeDatabricks object for use when performing AI generation using the generative-databricks module.

Parameters:

- **endpoint** ( _str_) – The URL where the API request should go. Defaults to None, which uses the server-defined default

- **frequency\_penalty** ( _float_ _\|_ _None_) – The frequency penalty to use. Defaults to None, which uses the server-defined default

- **log\_probs** ( _bool_ _\|_ _None_) – Whether to log probabilities. Defaults to None, which uses the server-defined default

- **max\_tokens** ( _int_ _\|_ _None_) – The maximum number of tokens to generate. Defaults to None, which uses the server-defined default

- **model** ( _str_ _\|_ _None_) – The model to use. Defaults to None, which uses the server-defined default

- **n** ( _int_ _\|_ _None_) – The number of sequences to generate. Defaults to None, which uses the server-defined default

- **presence\_penalty** ( _float_ _\|_ _None_) – The presence penalty to use. Defaults to None, which uses the server-defined default

- **stop** ( _List_ _\[_ _str_ _\]_ _\|_ _None_) – The stop sequences to use. Defaults to None, which uses the server-defined default

- **temperature** ( _float_ _\|_ _None_) – The temperature to use. Defaults to None, which uses the server-defined default

- **top\_log\_probs** ( _int_ _\|_ _None_) – The top log probabilities to use. Defaults to None, which uses the server-defined default

- **top\_p** ( _float_ _\|_ _None_) – The top P value to use. Defaults to None, which uses the server-defined default


Return type:

_\_GenerativeConfigRuntime_

_static_ dummy() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/generative.html#GenerativeConfig.dummy) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GenerativeConfig.dummy "Link to this definition")

Create a \_GenerativeDummy object for use when performing AI generation using the generative-dummy module.

Return type:

_\_GenerativeConfigRuntime_

_static_ friendliai( _\*_, _base\_url=None_, _max\_tokens=None_, _model=None_, _n=None_, _temperature=None_, _top\_p=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/generative.html#GenerativeConfig.friendliai) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GenerativeConfig.friendliai "Link to this definition")

Create a \_GenerativeFriendliai object for use when performing AI generation using the generative-friendliai module.

Parameters:

- **base\_url** ( _str_ _\|_ _None_) – The base URL where the API request should go. Defaults to None, which uses the server-defined default

- **max\_tokens** ( _int_ _\|_ _None_) – The maximum number of tokens to generate. Defaults to None, which uses the server-defined default

- **model** ( _str_ _\|_ _None_) – The model to use. Defaults to None, which uses the server-defined default

- **n** ( _int_ _\|_ _None_) – The number of sequences to generate. Defaults to None, which uses the server-defined default

- **temperature** ( _float_ _\|_ _None_) – The temperature to use. Defaults to None, which uses the server-defined default

- **top\_p** ( _float_ _\|_ _None_) – The top P value to use. Defaults to None, which uses the server-defined default


Return type:

_\_GenerativeConfigRuntime_

_static_ google( _\*_, _api\_endpoint=None_, _endpoint\_id=None_, _frequency\_penalty=None_, _max\_tokens=None_, _model=None_, _presence\_penalty=None_, _project\_id=None_, _region=None_, _stop\_sequences=None_, _temperature=None_, _top\_k=None_, _top\_p=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/generative.html#GenerativeConfig.google) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GenerativeConfig.google "Link to this definition")

Create a \_GenerativeGoogle object for use when performing AI generation using the generative-google module.

See the [documentation](https://weaviate.io/developers/weaviate/model-providers/google/generative)
for detailed usage.

Parameters:

- **api\_endpoint** ( _str_ _\|_ _None_) – The API endpoint to use. Defaults to None, which uses the server-defined default

- **endpoint\_id** ( _str_ _\|_ _None_) – The endpoint ID to use. Defaults to None, which uses the server-defined default

- **frequency\_penalty** ( _float_ _\|_ _None_) – The frequency penalty to use. Defaults to None, which uses the server-defined default

- **max\_tokens** ( _int_ _\|_ _None_) – The maximum number of tokens to generate. Defaults to None, which uses the server-defined default

- **model** ( _str_ _\|_ _None_) – The model ID to use. Defaults to None, which uses the server-defined default

- **presence\_penalty** ( _float_ _\|_ _None_) – The presence penalty to use. Defaults to None, which uses the server-defined default

- **project\_id** ( _str_ _\|_ _None_) – The project ID to use. Defaults to None, which uses the server-defined default

- **region** ( _str_ _\|_ _None_) – The region to use. Defaults to None, which uses the server-defined default

- **stop\_sequences** ( _List_ _\[_ _str_ _\]_ _\|_ _None_) – The stop sequences to use. Defaults to None, which uses the server-defined default

- **temperature** ( _float_ _\|_ _None_) – The temperature to use. Defaults to None, which uses the server-defined default

- **top\_k** ( _int_ _\|_ _None_) – The top K to use. Defaults to None, which uses the server-defined default

- **top\_p** ( _float_ _\|_ _None_) – The top P to use. Defaults to None, which uses the server-defined default


Return type:

_\_GenerativeConfigRuntime_

_static_ mistral( _\*_, _base\_url=None_, _max\_tokens=None_, _model=None_, _temperature=None_, _top\_p=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/generative.html#GenerativeConfig.mistral) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GenerativeConfig.mistral "Link to this definition")

Create a \_GenerativeMistral object for use when performing AI generation using the generative-mistral module.

Parameters:

- **base\_url** ( _str_ _\|_ _None_) – The base URL where the API request should go. Defaults to None, which uses the server-defined default

- **max\_tokens** ( _int_ _\|_ _None_) – The maximum number of tokens to generate. Defaults to None, which uses the server-defined default

- **model** ( _str_ _\|_ _None_) – The model to use. Defaults to None, which uses the server-defined default

- **temperature** ( _float_ _\|_ _None_) – The temperature to use. Defaults to None, which uses the server-defined default

- **top\_p** ( _float_ _\|_ _None_) – The top P value to use. Defaults to None, which uses the server-defined default


Return type:

_\_GenerativeConfigRuntime_

_static_ nvidia( _\*_, _base\_url=None_, _max\_tokens=None_, _model=None_, _temperature=None_, _top\_p=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/generative.html#GenerativeConfig.nvidia) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GenerativeConfig.nvidia "Link to this definition")

Create a \_GenerativeNvidia object for use when performing AI generation using the generative-nvidia module.

Parameters:

- **base\_url** ( _str_ _\|_ _None_) – The base URL where the API request should go. Defaults to None, which uses the server-defined default

- **max\_tokens** ( _int_ _\|_ _None_) – The maximum number of tokens to generate. Defaults to None, which uses the server-defined default

- **model** ( _str_ _\|_ _None_) – The model to use. Defaults to None, which uses the server-defined default

- **temperature** ( _float_ _\|_ _None_) – The temperature to use. Defaults to None, which uses the server-defined default

- **top\_p** ( _float_ _\|_ _None_) – The top P value to use. Defaults to None, which uses the server-defined default


Return type:

_\_GenerativeConfigRuntime_

_static_ ollama( _\*_, _api\_endpoint=None_, _model=None_, _temperature=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/generative.html#GenerativeConfig.ollama) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GenerativeConfig.ollama "Link to this definition")

Create a \_GenerativeOllama object for use when performing AI generation using the generative-ollama module.

Parameters:

- **api\_endpoint** ( _str_ _\|_ _None_) – The API endpoint to use. Defaults to None, which uses the server-defined default
Docker users may need to specify an alias, such as http://host.docker.internal:11434 so that the container can access the host machine.

- **model** ( _str_ _\|_ _None_) – The model to use. Defaults to None, which uses the server-defined default

- **temperature** ( _float_ _\|_ _None_) – The temperature to use. Defaults to None, which uses the server-defined default

- **images** – Any query-specific external images to use in the generation. Passing a string will assume a path to the image file and, if not found, will be treated as a base64-encoded string.
The number of images passed to the prompt will match the length of this field.

- **grouped\_task\_image\_properties** – Any internal image properties to use in the generation sourced from the object’s properties returned by the retrieval step.
The number of images passed to the prompt will match the value of limit in the search query.


Return type:

_\_GenerativeConfigRuntime_

_static_ openai( _\*_, _api\_version=None_, _base\_url=None_, _deployment\_id=None_, _frequency\_penalty=None_, _max\_tokens=None_, _model=None_, _presence\_penalty=None_, _resource\_name=None_, _stop=None_, _temperature=None_, _top\_p=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/generative.html#GenerativeConfig.openai) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GenerativeConfig.openai "Link to this definition")

Create a \_GenerativeOpenAI object for use when performing AI generation using the OpenAI-backed generative-openai module.

See the [documentation](https://weaviate.io/developers/weaviate/modules/reader-generator-modules/generative-openai)
for detailed usage.

Parameters:

- **api\_version** ( _str_ _\|_ _None_) – The API version to use. Defaults to None, which uses the server-defined default

- **base\_url** ( _str_ _\|_ _None_) – The base URL where the API request should go. Defaults to None, which uses the server-defined default

- **deployment\_id** ( _str_ _\|_ _None_) – The deployment ID to use. Defaults to None, which uses the server-defined default

- **frequency\_penalty** ( _float_ _\|_ _None_) – The frequency penalty to use. Defaults to None, which uses the server-defined default

- **max\_tokens** ( _int_ _\|_ _None_) – The maximum number of tokens to generate. Defaults to None, which uses the server-defined default

- **model** ( _str_ _\|_ _None_) – The model to use. Defaults to None, which uses the server-defined default

- **presence\_penalty** ( _float_ _\|_ _None_) – The presence penalty to use. Defaults to None, which uses the server-defined default

- **resource\_name** ( _str_ _\|_ _None_) – The name of the OpenAI resource to use. Defaults to None, which uses the server-defined default

- **stop** ( _List_ _\[_ _str_ _\]_ _\|_ _None_) – The stop sequences to use. Defaults to None, which uses the server-defined default

- **temperature** ( _float_ _\|_ _None_) – The temperature to use. Defaults to None, which uses the server-defined default

- **top\_p** ( _float_ _\|_ _None_) – The top P to use. Defaults to None, which uses the server-defined default


Return type:

_\_GenerativeConfigRuntime_

_static_ xai( _\*_, _base\_url=None_, _max\_tokens=None_, _model=None_, _temperature=None_, _top\_p=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/generative.html#GenerativeConfig.xai) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GenerativeConfig.xai "Link to this definition")

Create a \_GenerativeXAI object for use when performing AI generation using the generative-xai module.

See the [documentation](https://weaviate.io/developers/weaviate/modules/reader-generator-modules/generative-xai)
for detailed usage.

Parameters:

- **base\_url** ( _str_ _\|_ _None_) – The base URL where the API request should go. Defaults to None, which uses the server-defined default

- **max\_tokens** ( _int_ _\|_ _None_) – The maximum number of tokens to generate. Defaults to None, which uses the server-defined default

- **model** ( _str_ _\|_ _None_) – The model to use. Defaults to None, which uses the server-defined default

- **temperature** ( _float_ _\|_ _None_) – The temperature to use. Defaults to None, which uses the server-defined default

- **top\_p** ( _float_ _\|_ _None_) – The top P to use. Defaults to None, which uses the server-defined default


Return type:

_\_GenerativeConfigRuntime_

_pydanticmodel_ weaviate.classes.query.GroupBy [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#GroupBy) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GroupBy "Link to this definition")

Bases: [`_WeaviateInput`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._WeaviateInput "weaviate.collections.classes.types._WeaviateInput")

Define how the query’s group-by operation should be performed.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ number\_of\_groups _:int_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GroupBy.number_of_groups "Link to this definition")_field_ objects\_per\_group _:int_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GroupBy.objects_per_group "Link to this definition")_field_ prop _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GroupBy.prop "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.GroupBy._abc_impl "Link to this definition")_class_ weaviate.classes.query.HybridFusion( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#HybridFusion) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.HybridFusion "Link to this definition")

Bases: `str`, `BaseEnum`

Define how the query’s hybrid fusion operation should be performed.

RANKED _='FUSION\_TYPE\_RANKED'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.HybridFusion.RANKED "Link to this definition")RELATIVE\_SCORE _='FUSION\_TYPE\_RELATIVE\_SCORE'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.HybridFusion.RELATIVE_SCORE "Link to this definition")_class_ weaviate.classes.query.HybridVector [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#HybridVector) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.HybridVector "Link to this definition")

Bases: `object`

Use this factory class to define the appropriate classes needed when defining near text and near vector sub-searches in hybrid queries.

_static_ near\_text( _query_, _\*_, _certainty=None_, _distance=None_, _move\_to=None_, _move\_away=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#HybridVector.near_text) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.HybridVector.near_text "Link to this definition")

Define a near text search to be used within a hybrid query.

Parameters:

- **query** ( _str_ _\|_ _List_ _\[_ _str_ _\]_) – The text to search for as a string or a list of strings.

- **certainty** ( _float_ _\|_ _None_) – The minimum similarity score to return. If not specified, the default certainty specified by the server is used.

- **distance** ( _float_ _\|_ _None_) – The maximum distance to search. If not specified, the default distance specified by the server is used.

- **move\_to** ( [_Move_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.Move "weaviate.collections.classes.grpc.Move") _\|_ _None_) – Define the concepts that should be moved towards in the vector space during the search.

- **move\_away** ( [_Move_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.Move "weaviate.collections.classes.grpc.Move") _\|_ _None_) – Define the concepts that should be moved away from in the vector space during the search.


Returns:

A \_HybridNearText object to be used in the vector parameter of the query.hybrid and generate.hybrid search methods.

Return type:

[_\_HybridNearText_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._HybridNearText "weaviate.collections.classes.grpc._HybridNearText")

_static_ near\_vector( _vector_, _\*_, _certainty=None_, _distance=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#HybridVector.near_vector) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.HybridVector.near_vector "Link to this definition")

Define a near vector search to be used within a hybrid query.

Parameters:

- **certainty** ( _float_ _\|_ _None_) – The minimum similarity score to return. If not specified, the default certainty specified by the server is used.

- **distance** ( _float_ _\|_ _None_) – The maximum distance to search. If not specified, the default distance specified by the server is used.

- **vector** ( _Sequence_ _\[_ _int_ _\|_ _float_ _\]_ _\|_ _Sequence_ _\[_ _Sequence_ _\[_ _int_ _\|_ _float_ _\]_ _\]_ _\|_ _Mapping_ _\[_ _str_ _,_ _Sequence_ _\[_ _int_ _\|_ _float_ _\]_ _\|_ _Sequence_ _\[_ _Sequence_ _\[_ _int_ _\|_ _float_ _\]_ _\]_ _\|_ [_\_ListOfVectorsQuery_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#id219 "weaviate.collections.classes.grpc._ListOfVectorsQuery") _\[_ _Sequence_ _\[_ _Union_ _\[_ _int_ _,_ _float_ _\]_ _\]_ _\]_ _\|_ [_\_ListOfVectorsQuery_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#id219 "weaviate.collections.classes.grpc._ListOfVectorsQuery") _\[_ _Sequence_ _\[_ _Sequence_ _\[_ _Union_ _\[_ _int_ _,_ _float_ _\]_ _\]_ _\]_ _\]_ _\]_)


Returns:

A \_HybridNearVector object to be used in the vector parameter of the query.hybrid and generate.hybrid search methods.

Return type:

[_\_HybridNearVector_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._HybridNearVector "weaviate.collections.classes.grpc._HybridNearVector")

weaviate.classes.query.BM25Operator [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.BM25Operator "Link to this definition")

alias of [`BM25OperatorFactory`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.BM25OperatorFactory "weaviate.collections.classes.grpc.BM25OperatorFactory")

_pydanticmodel_ weaviate.classes.query.MetadataQuery [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#MetadataQuery) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.MetadataQuery "Link to this definition")

Bases: [`_WeaviateInput`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._WeaviateInput "weaviate.collections.classes.types._WeaviateInput")

Define which metadata should be returned in the query’s results.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ certainty _:bool_ _=False_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.MetadataQuery.certainty "Link to this definition")_field_ creation\_time _:bool_ _=False_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.MetadataQuery.creation_time "Link to this definition")_field_ distance _:bool_ _=False_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.MetadataQuery.distance "Link to this definition")_field_ explain\_score _:bool_ _=False_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.MetadataQuery.explain_score "Link to this definition")_field_ is\_consistent _:bool_ _=False_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.MetadataQuery.is_consistent "Link to this definition")_field_ last\_update\_time _:bool_ _=False_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.MetadataQuery.last_update_time "Link to this definition")_field_ score _:bool_ _=False_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.MetadataQuery.score "Link to this definition")_classmethod_ full() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#MetadataQuery.full) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.MetadataQuery.full "Link to this definition")

Return a MetadataQuery with all fields set to True.

Return type:

[_MetadataQuery_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.MetadataQuery "weaviate.collections.classes.grpc.MetadataQuery")

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.MetadataQuery._abc_impl "Link to this definition")_class_ weaviate.classes.query.Metrics( _property\__) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#Metrics) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Metrics "Link to this definition")

Bases: `object`

Define the metrics to be returned based on a property when aggregating over a collection.

Use the \_\_init\_\_ method to define the name to the property to be aggregated on.
Then use the text, integer, number, boolean, date\_, or reference methods to define the metrics to be returned.

See [the docs](https://weaviate.io/developers/weaviate/search/aggregate) for more details!

Parameters:

**property\_** ( _str_)

boolean( _count=False_, _percentage\_false=False_, _percentage\_true=False_, _total\_false=False_, _total\_true=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#Metrics.boolean) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Metrics.boolean "Link to this definition")

Define the metrics to be returned for a BOOL or BOOL\_ARRAY property when aggregating over a collection.

If none of the arguments are provided then all metrics will be returned.

Parameters:

- **count** ( _bool_) – Whether to include the number of objects that contain this property.

- **percentage\_false** ( _bool_) – Whether to include the percentage of objects that have a false value for this property.

- **percentage\_true** ( _bool_) – Whether to include the percentage of objects that have a true value for this property.

- **total\_false** ( _bool_) – Whether to include the total number of objects that have a false value for this property.

- **total\_true** ( _bool_) – Whether to include the total number of objects that have a true value for this property.


Returns:

A \_MetricsBoolean object that includes the metrics to be returned.

Return type:

[_\_MetricsBoolean_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate._MetricsBoolean "weaviate.collections.classes.aggregate._MetricsBoolean")

date\_( _count=False_, _maximum=False_, _median=False_, _minimum=False_, _mode=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#Metrics.date_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Metrics.date_ "Link to this definition")

Define the metrics to be returned for a DATE or DATE\_ARRAY property when aggregating over a collection.

If none of the arguments are provided then all metrics will be returned.

Parameters:

- **count** ( _bool_) – Whether to include the number of objects that contain this property.

- **maximum** ( _bool_) – Whether to include the maximum value of this property.

- **median** ( _bool_) – Whether to include the median value of this property.

- **minimum** ( _bool_) – Whether to include the minimum value of this property.

- **mode** ( _bool_) – Whether to include the mode value of this property.


Returns:

A \_MetricsDate object that includes the metrics to be returned.

Return type:

[_\_MetricsDate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate._MetricsDate "weaviate.collections.classes.aggregate._MetricsDate")

integer( _count=False_, _maximum=False_, _mean=False_, _median=False_, _minimum=False_, _mode=False_, _sum\_=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#Metrics.integer) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Metrics.integer "Link to this definition")

Define the metrics to be returned for an INT or INT\_ARRAY property when aggregating over a collection.

If none of the arguments are provided then all metrics will be returned.

Parameters:

- **count** ( _bool_) – Whether to include the number of objects that contain this property.

- **maximum** ( _bool_) – Whether to include the maximum value of this property.

- **mean** ( _bool_) – Whether to include the mean value of this property.

- **median** ( _bool_) – Whether to include the median value of this property.

- **minimum** ( _bool_) – Whether to include the minimum value of this property.

- **mode** ( _bool_) – Whether to include the mode value of this property.

- **sum** – Whether to include the sum of this property.

- **sum\_** ( _bool_)


Returns:

A \_MetricsInteger object that includes the metrics to be returned.

Return type:

[_\_MetricsInteger_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate._MetricsInteger "weaviate.collections.classes.aggregate._MetricsInteger")

number( _count=False_, _maximum=False_, _mean=False_, _median=False_, _minimum=False_, _mode=False_, _sum\_=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#Metrics.number) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Metrics.number "Link to this definition")

Define the metrics to be returned for a NUMBER or NUMBER\_ARRAY property when aggregating over a collection.

If none of the arguments are provided then all metrics will be returned.

Parameters:

- **count** ( _bool_) – Whether to include the number of objects that contain this property.

- **maximum** ( _bool_) – Whether to include the maximum value of this property.

- **mean** ( _bool_) – Whether to include the mean value of this property.

- **median** ( _bool_) – Whether to include the median value of this property.

- **minimum** ( _bool_) – Whether to include the minimum value of this property.

- **mode** ( _bool_) – Whether to include the mode value of this property.

- **sum** – Whether to include the sum of this property.

- **sum\_** ( _bool_)


Returns:

A \_MetricsNumber object that includes the metrics to be returned.

Return type:

[_\_MetricsNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate._MetricsNumber "weaviate.collections.classes.aggregate._MetricsNumber")

reference( _pointing\_to=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#Metrics.reference) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Metrics.reference "Link to this definition")

Define the metrics to be returned for a cross-reference property when aggregating over a collection.

If none of the arguments are provided then all metrics will be returned.

Parameters:

**pointing\_to** ( _bool_) – The UUIDs of the objects that are being pointed to.

Returns:

A \_MetricsReference object that includes the metrics to be returned.

Return type:

[_\_MetricsReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate._MetricsReference "weaviate.collections.classes.aggregate._MetricsReference")

text( _count=False_, _top\_occurrences\_count=False_, _top\_occurrences\_value=False_, _limit=None_, _min\_occurrences=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#Metrics.text) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Metrics.text "Link to this definition")

Define the metrics to be returned for a TEXT or TEXT\_ARRAY property when aggregating over a collection.

If none of the arguments are provided then all metrics will be returned.

Parameters:

- **count** ( _bool_) – Whether to include the number of objects that contain this property.

- **top\_occurrences\_count** ( _bool_) – Whether to include the number of the top occurrences of a property’s value.

- **top\_occurrences\_value** ( _bool_) – Whether to include the value of the top occurrences of a property’s value.

- **min\_occurrences** ( _int_ _\|_ _None_) – (Deprecated) The maximum number of top occurrences to return. Use limit instead.

- **limit** ( _int_ _\|_ _None_) – The maximum number of top occurrences to return.


Returns:

A \_MetricsStr object that includes the metrics to be returned.

Return type:

[_\_MetricsText_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate._MetricsText "weaviate.collections.classes.aggregate._MetricsText")

_class_ weaviate.classes.query.Move( _force_, _objects=None_, _concepts=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#Move) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Move "Link to this definition")

Bases: `object`

Define how the query’s move operation should be performed.

Parameters:

- **force** ( _float_)

- **objects** ( _List_ _\[_ _str_ _\|_ _UUID_ _\]_ _\|_ _str_ _\|_ _UUID_ _\|_ _None_)

- **concepts** ( _List_ _\[_ _str_ _\]_ _\|_ _str_ _\|_ _None_)


_property_\_concepts\_list _:List\[str\]\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Move._concepts_list "Link to this definition")_property_\_objects\_list _:List\[str\]\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Move._objects_list "Link to this definition")\_to\_gql\_payload() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#Move._to_gql_payload) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Move._to_gql_payload "Link to this definition")Return type:

dict

_class_ weaviate.classes.query.NearMediaType( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#NearMediaType) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.NearMediaType "Link to this definition")

Bases: `str`, `Enum`

The different types of media that can be used in a near\_media query to leverage the multi2vec-\* modules.

All are available when using multi2vec-bind but only IMAGE is available when using multi2vec-clip.

AUDIO _='audio'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.NearMediaType.AUDIO "Link to this definition")DEPTH _='depth'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.NearMediaType.DEPTH "Link to this definition")IMAGE _='image'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.NearMediaType.IMAGE "Link to this definition")IMU _='imu'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.NearMediaType.IMU "Link to this definition")THERMAL _='thermal'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.NearMediaType.THERMAL "Link to this definition")VIDEO _='video'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.NearMediaType.VIDEO "Link to this definition")_pydanticmodel_ weaviate.classes.query.QueryNested [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#QueryNested) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.QueryNested "Link to this definition")

Bases: [`_WeaviateInput`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._WeaviateInput "weaviate.collections.classes.types._WeaviateInput")

Define the query-time return properties of a nested property.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ name _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.QueryNested.name "Link to this definition")_field_ properties _:PROPERTIES_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.QueryNested.properties "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.QueryNested._abc_impl "Link to this definition")_pydanticmodel_ weaviate.classes.query.QueryReference [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#QueryReference) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.QueryReference "Link to this definition")

Bases: [`_QueryReference`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._QueryReference "weaviate.collections.classes.grpc._QueryReference")

Define a query-time reference to a single-target property when querying through cross-references.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

MultiTarget [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.QueryReference.MultiTarget "Link to this definition")

alias of [`_QueryReferenceMultiTarget`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._QueryReferenceMultiTarget "weaviate.collections.classes.grpc._QueryReferenceMultiTarget")

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.QueryReference._abc_impl "Link to this definition")_class_ weaviate.classes.query.NearVector [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#NearVector) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.NearVector "Link to this definition")

Bases: `object`

Factory class to use when defining near vector queries with multiple vectors in near\_vector() and hybrid() methods.

_static_ list\_of\_vectors( _\*vectors_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#NearVector.list_of_vectors) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.NearVector.list_of_vectors "Link to this definition")

Define a many-vectors query to be used within a near vector search, i.e. multiple vectors over a single-vector space.

Parameters:

**vectors** ( _V_)

Return type:

[_\_ListOfVectorsQuery_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#id219 "weaviate.collections.classes.grpc._ListOfVectorsQuery")

_pydanticmodel_ weaviate.classes.query.Rerank [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#Rerank) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Rerank "Link to this definition")

Bases: [`_WeaviateInput`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._WeaviateInput "weaviate.collections.classes.types._WeaviateInput")

Define how the query’s rerank operation should be performed.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ prop _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Rerank.prop "Link to this definition")_field_ query _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Rerank.query "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Rerank._abc_impl "Link to this definition")_class_ weaviate.classes.query.Sort [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#Sort) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Sort "Link to this definition")

Bases: `object`

Define how the query’s sort operation should be performed using the available static methods.

_static_ by\_creation\_time( _ascending=True_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#Sort.by_creation_time) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Sort.by_creation_time "Link to this definition")

Sort by an object’s creation time.

Parameters:

**ascending** ( _bool_)

Return type:

[_\_Sorting_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._Sorting "weaviate.collections.classes.grpc._Sorting")

_static_ by\_id( _ascending=True_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#Sort.by_id) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Sort.by_id "Link to this definition")

Sort by an object’s ID in the collection.

Parameters:

**ascending** ( _bool_)

Return type:

[_\_Sorting_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._Sorting "weaviate.collections.classes.grpc._Sorting")

_static_ by\_property( _name_, _ascending=True_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#Sort.by_property) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Sort.by_property "Link to this definition")

Sort by an object property in the collection.

Parameters:

- **name** ( _str_)

- **ascending** ( _bool_)


Return type:

[_\_Sorting_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._Sorting "weaviate.collections.classes.grpc._Sorting")

_static_ by\_update\_time( _ascending=True_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#Sort.by_update_time) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.Sort.by_update_time "Link to this definition")

Sort by an object’s last update time.

Parameters:

**ascending** ( _bool_)

Return type:

[_\_Sorting_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._Sorting "weaviate.collections.classes.grpc._Sorting")

_class_ weaviate.classes.query.TargetVectors [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#TargetVectors) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.TargetVectors "Link to this definition")

Bases: `object`

Define how the distances from different target vectors should be combined using the available methods.

_static_ average( _target\_vectors_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#TargetVectors.average) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.TargetVectors.average "Link to this definition")

Combine the distance from different target vectors by averaging them.

Parameters:

**target\_vectors** ( _List_ _\[_ _str_ _\]_)

Return type:

[_\_MultiTargetVectorJoin_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._MultiTargetVectorJoin "weaviate.collections.classes.grpc._MultiTargetVectorJoin")

_static_ manual\_weights( _weights_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#TargetVectors.manual_weights) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.TargetVectors.manual_weights "Link to this definition")

Combine the distance from different target vectors by summing them using manual weights.

Parameters:

**weights** ( _Dict_ _\[_ _str_ _,_ _float_ _\|_ _List_ _\[_ _float_ _\]_ _\]_)

Return type:

[_\_MultiTargetVectorJoin_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._MultiTargetVectorJoin "weaviate.collections.classes.grpc._MultiTargetVectorJoin")

_static_ minimum( _target\_vectors_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#TargetVectors.minimum) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.TargetVectors.minimum "Link to this definition")

Combine the distance from different target vectors by using the minimum distance.

Parameters:

**target\_vectors** ( _List_ _\[_ _str_ _\]_)

Return type:

[_\_MultiTargetVectorJoin_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._MultiTargetVectorJoin "weaviate.collections.classes.grpc._MultiTargetVectorJoin")

_static_ relative\_score( _weights_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#TargetVectors.relative_score) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.TargetVectors.relative_score "Link to this definition")

Combine the distance from different target vectors using score fusion.

Parameters:

**weights** ( _Dict_ _\[_ _str_ _,_ _float_ _\|_ _List_ _\[_ _float_ _\]_ _\]_)

Return type:

[_\_MultiTargetVectorJoin_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._MultiTargetVectorJoin "weaviate.collections.classes.grpc._MultiTargetVectorJoin")

_static_ sum( _target\_vectors_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#TargetVectors.sum) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.query.TargetVectors.sum "Link to this definition")

Combine the distance from different target vectors by summing them.

Parameters:

**target\_vectors** ( _List_ _\[_ _str_ _\]_)

Return type:

[_\_MultiTargetVectorJoin_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._MultiTargetVectorJoin "weaviate.collections.classes.grpc._MultiTargetVectorJoin")

## weaviate.classes.rbac [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html\#module-weaviate.classes.rbac "Link to this heading")

_class_ weaviate.classes.rbac.Actions [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#Actions) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Actions "Link to this definition")

Bases: `object`

Alias [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Actions.Alias "Link to this definition")

alias of [`AliasAction`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.AliasAction "weaviate.rbac.models.AliasAction")

Backups [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Actions.Backups "Link to this definition")

alias of [`BackupsAction`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.BackupsAction "weaviate.rbac.models.BackupsAction")

Cluster [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Actions.Cluster "Link to this definition")

alias of [`ClusterAction`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.ClusterAction "weaviate.rbac.models.ClusterAction")

Collections [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Actions.Collections "Link to this definition")

alias of [`CollectionsAction`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.CollectionsAction "weaviate.rbac.models.CollectionsAction")

Data [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Actions.Data "Link to this definition")

alias of [`DataAction`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.DataAction "weaviate.rbac.models.DataAction")

Groups [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Actions.Groups "Link to this definition")

alias of [`GroupAction`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.GroupAction "weaviate.rbac.models.GroupAction")

Nodes [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Actions.Nodes "Link to this definition")

alias of [`NodesAction`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.NodesAction "weaviate.rbac.models.NodesAction")

Replicate [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Actions.Replicate "Link to this definition")

alias of [`ReplicateAction`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.ReplicateAction "weaviate.rbac.models.ReplicateAction")

Roles [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Actions.Roles "Link to this definition")

alias of [`RolesAction`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.RolesAction "weaviate.rbac.models.RolesAction")

Tenants [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Actions.Tenants "Link to this definition")

alias of [`TenantsAction`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.TenantsAction "weaviate.rbac.models.TenantsAction")

Users [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Actions.Users "Link to this definition")

alias of [`UsersAction`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.UsersAction "weaviate.rbac.models.UsersAction")

_class_ weaviate.classes.rbac.Permissions [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#Permissions) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Permissions "Link to this definition")

Bases: `object`

Groups [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Permissions.Groups "Link to this definition")

alias of [`GroupsPermissions`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.GroupsPermissions "weaviate.rbac.models.GroupsPermissions")

Nodes [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Permissions.Nodes "Link to this definition")

alias of [`NodesPermissions`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.NodesPermissions "weaviate.rbac.models.NodesPermissions")

_static_ alias( _\*_, _alias_, _collection_, _create=False_, _read=False_, _update=False_, _delete=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#Permissions.alias) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Permissions.alias "Link to this definition")Parameters:

- **alias** ( _str_ _\|_ _Sequence_ _\[_ _str_ _\]_)

- **collection** ( _str_ _\|_ _Sequence_ _\[_ _str_ _\]_)

- **create** ( _bool_)

- **read** ( _bool_)

- **update** ( _bool_)

- **delete** ( _bool_)


Return type:

_List_\[ [_\_Permission_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#id40 "weaviate.rbac.models._Permission")\]

_static_ backup( _\*_, _collection_, _manage=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#Permissions.backup) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Permissions.backup "Link to this definition")Parameters:

- **collection** ( _str_ _\|_ _Sequence_ _\[_ _str_ _\]_)

- **manage** ( _bool_)


Return type:

_List_\[ [_\_Permission_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#id40 "weaviate.rbac.models._Permission")\]

_static_ cluster( _\*_, _read=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#Permissions.cluster) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Permissions.cluster "Link to this definition")Parameters:

**read** ( _bool_)

Return type:

_List_\[ [_\_Permission_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#id40 "weaviate.rbac.models._Permission")\]

_static_ collections( _\*_, _collection_, _create\_collection=False_, _read\_config=False_, _update\_config=False_, _delete\_collection=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#Permissions.collections) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Permissions.collections "Link to this definition")Parameters:

- **collection** ( _str_ _\|_ _Sequence_ _\[_ _str_ _\]_)

- **create\_collection** ( _bool_)

- **read\_config** ( _bool_)

- **update\_config** ( _bool_)

- **delete\_collection** ( _bool_)


Return type:

_List_\[ [_\_Permission_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#id40 "weaviate.rbac.models._Permission")\]

_static_ data( _\*_, _collection_, _tenant=None_, _create=False_, _read=False_, _update=False_, _delete=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#Permissions.data) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Permissions.data "Link to this definition")Parameters:

- **collection** ( _str_ _\|_ _Sequence_ _\[_ _str_ _\]_)

- **tenant** ( _str_ _\|_ _Sequence_ _\[_ _str_ _\]_ _\|_ _None_)

- **create** ( _bool_)

- **read** ( _bool_)

- **update** ( _bool_)

- **delete** ( _bool_)


Return type:

_List_\[ [_\_Permission_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#id40 "weaviate.rbac.models._Permission")\]

_static_ replicate( _\*_, _collection_, _shard=None_, _create=False_, _read=False_, _update=False_, _delete=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#Permissions.replicate) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Permissions.replicate "Link to this definition")Parameters:

- **collection** ( _str_ _\|_ _Sequence_ _\[_ _str_ _\]_)

- **shard** ( _str_ _\|_ _Sequence_ _\[_ _str_ _\]_ _\|_ _None_)

- **create** ( _bool_)

- **read** ( _bool_)

- **update** ( _bool_)

- **delete** ( _bool_)


Return type:

_List_\[ [_\_Permission_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#id40 "weaviate.rbac.models._Permission")\]

_static_ roles( _\*_, _role_, _create=False_, _read=False_, _update=False_, _delete=False_, _scope=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#Permissions.roles) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Permissions.roles "Link to this definition")Parameters:

- **role** ( _str_ _\|_ _Sequence_ _\[_ _str_ _\]_)

- **create** ( _bool_)

- **read** ( _bool_)

- **update** ( _bool_)

- **delete** ( _bool_)

- **scope** ( [_RoleScope_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.RoleScope "weaviate.rbac.models.RoleScope") _\|_ _None_)


Return type:

_List_\[ [_\_Permission_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#id40 "weaviate.rbac.models._Permission")\]

_static_ tenants( _\*_, _collection_, _tenant=None_, _create=False_, _read=False_, _update=False_, _delete=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#Permissions.tenants) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Permissions.tenants "Link to this definition")Parameters:

- **collection** ( _str_ _\|_ _Sequence_ _\[_ _str_ _\]_)

- **tenant** ( _str_ _\|_ _Sequence_ _\[_ _str_ _\]_ _\|_ _None_)

- **create** ( _bool_)

- **read** ( _bool_)

- **update** ( _bool_)

- **delete** ( _bool_)


Return type:

_List_\[ [_\_Permission_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#id40 "weaviate.rbac.models._Permission")\]

_static_ users( _\*_, _user_, _create=False_, _read=False_, _update=False_, _delete=False_, _assign\_and\_revoke=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#Permissions.users) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.Permissions.users "Link to this definition")Parameters:

- **user** ( _str_ _\|_ _Sequence_ _\[_ _str_ _\]_)

- **create** ( _bool_)

- **read** ( _bool_)

- **update** ( _bool_)

- **delete** ( _bool_)

- **assign\_and\_revoke** ( _bool_)


Return type:

_List_\[ [_\_Permission_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#id40 "weaviate.rbac.models._Permission")\]

_class_ weaviate.classes.rbac.RoleScope( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#RoleScope) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.RoleScope "Link to this definition")

Bases: `str`, `BaseEnum`

Scope of the role permission.

MATCH _='match'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.RoleScope.MATCH "Link to this definition")ALL _='all'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.rbac.RoleScope.ALL "Link to this definition")

## weaviate.classes.tenants [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html\#weaviate-classes-tenants "Link to this heading")

_pydanticmodel_ weaviate.classes.tenants.Tenant [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/tenants.html#Tenant) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.Tenant "Link to this definition")

Bases: `BaseModel`

Tenant class used to describe a tenant in Weaviate.

name [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.Tenant.name "Link to this definition")

The name of the tenant.

activity\_status [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.Tenant.activity_status "Link to this definition")

TenantActivityStatus, default: “HOT”

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ activityStatus _: [\_TenantActivistatusServerValues](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.tenants._TenantActivistatusServerValues "weaviate.collections.classes.tenants._TenantActivistatusServerValues")_ _=\_TenantActivistatusServerValues.HOT_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.Tenant.activityStatus "Link to this definition")_field_ activityStatusInternal _: [TenantActivityStatus](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.tenants.TenantActivityStatus "weaviate.collections.classes.tenants.TenantActivityStatus")_ _=TenantActivityStatus.ACTIVE_ _(alias'activity\_status')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.Tenant.activityStatusInternal "Link to this definition")_field_ name _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id108 "Link to this definition")\_model\_post\_init( _user\_input_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/tenants.html#Tenant._model_post_init) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.Tenant._model_post_init "Link to this definition")Parameters:

**user\_input** ( _bool_)

Return type:

None

model\_post\_init( _\_Tenant\_\_context_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/tenants.html#Tenant.model_post_init) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.Tenant.model_post_init "Link to this definition")

Override this method to perform additional initialization after \_\_init\_\_ and model\_construct.
This is useful if you want to do some validation that requires the entire model to be initialized.

Parameters:

**\_Tenant\_\_context** ( _Any_)

Return type:

None

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.Tenant._abc_impl "Link to this definition")_property_ activity\_status _: [TenantActivityStatus](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.tenants.TenantActivityStatus "weaviate.collections.classes.tenants.TenantActivityStatus")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id109 "Link to this definition")

Getter for the activity status of the tenant.

_pydanticmodel_ weaviate.classes.tenants.TenantCreate [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/tenants.html#TenantCreate) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantCreate "Link to this definition")

Bases: `BaseModel`

Tenant class used to describe a tenant to create in Weaviate.

name [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantCreate.name "Link to this definition")

the name of the tenant.

activity\_status [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantCreate.activity_status "Link to this definition")

TenantCreateActivityStatus, default: “HOT”

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ activityStatus _: [\_TenantActivistatusServerValues](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.tenants._TenantActivistatusServerValues "weaviate.collections.classes.tenants._TenantActivistatusServerValues")_ _=\_TenantActivistatusServerValues.HOT_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantCreate.activityStatus "Link to this definition")_field_ activityStatusInternal _: [TenantCreateActivityStatus](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.tenants.TenantCreateActivityStatus "weaviate.collections.classes.tenants.TenantCreateActivityStatus")_ _=TenantCreateActivityStatus.ACTIVE_ _(alias'activity\_status')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantCreate.activityStatusInternal "Link to this definition")_field_ name _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id110 "Link to this definition")model\_post\_init( _\_TenantCreate\_\_context_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/tenants.html#TenantCreate.model_post_init) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantCreate.model_post_init "Link to this definition")

Override this method to perform additional initialization after \_\_init\_\_ and model\_construct.
This is useful if you want to do some validation that requires the entire model to be initialized.

Parameters:

**\_TenantCreate\_\_context** ( _Any_)

Return type:

None

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantCreate._abc_impl "Link to this definition")_property_ activity\_status _: [TenantCreateActivityStatus](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.tenants.TenantCreateActivityStatus "weaviate.collections.classes.tenants.TenantCreateActivityStatus")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id111 "Link to this definition")

Getter for the activity status of the tenant.

_pydanticmodel_ weaviate.classes.tenants.TenantUpdate [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/tenants.html#TenantUpdate) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantUpdate "Link to this definition")

Bases: `BaseModel`

Tenant class used to describe a tenant to create in Weaviate.

name [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantUpdate.name "Link to this definition")

The name of the tenant.

activity\_status [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantUpdate.activity_status "Link to this definition")

TenantUpdateActivityStatus, default: “HOT”

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ activityStatus _: [\_TenantActivistatusServerValues](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.tenants._TenantActivistatusServerValues "weaviate.collections.classes.tenants._TenantActivistatusServerValues")_ _=\_TenantActivistatusServerValues.HOT_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantUpdate.activityStatus "Link to this definition")_field_ activityStatusInternal _: [TenantUpdateActivityStatus](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.tenants.TenantUpdateActivityStatus "weaviate.collections.classes.tenants.TenantUpdateActivityStatus")_ _=TenantUpdateActivityStatus.ACTIVE_ _(alias'activity\_status')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantUpdate.activityStatusInternal "Link to this definition")_field_ name _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id112 "Link to this definition")model\_post\_init( _\_TenantUpdate\_\_context_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/tenants.html#TenantUpdate.model_post_init) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantUpdate.model_post_init "Link to this definition")

Override this method to perform additional initialization after \_\_init\_\_ and model\_construct.
This is useful if you want to do some validation that requires the entire model to be initialized.

Parameters:

**\_TenantUpdate\_\_context** ( _Any_)

Return type:

None

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantUpdate._abc_impl "Link to this definition")_property_ activity\_status _: [TenantUpdateActivityStatus](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.tenants.TenantUpdateActivityStatus "weaviate.collections.classes.tenants.TenantUpdateActivityStatus")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id113 "Link to this definition")

Getter for the activity status of the tenant.

_class_ weaviate.classes.tenants.TenantActivityStatus( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/tenants.html#TenantActivityStatus) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantActivityStatus "Link to this definition")

Bases: `str`, `Enum`

TenantActivityStatus class used to describe the activity status of a tenant in Weaviate.

ACTIVE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantActivityStatus.ACTIVE "Link to this definition")

The tenant is fully active and can be used.

INACTIVE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantActivityStatus.INACTIVE "Link to this definition")

The tenant is not active, files stored locally.

OFFLOADED [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantActivityStatus.OFFLOADED "Link to this definition")

The tenant is not active, files stored on the cloud.

OFFLOADING [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantActivityStatus.OFFLOADING "Link to this definition")

The tenant is in the process of being offloaded.

ONLOADING [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantActivityStatus.ONLOADING "Link to this definition")

The tenant is in the process of being activated.

HOT [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantActivityStatus.HOT "Link to this definition")

DEPRECATED, please use ACTIVE. The tenant is fully active and can be used.

COLD [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantActivityStatus.COLD "Link to this definition")

DEPRECATED, please use INACTIVE. The tenant is not active, files stored locally.

FROZEN [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantActivityStatus.FROZEN "Link to this definition")

DEPRECATED, please use OFFLOADED. The tenant is not active, files stored on the cloud.

ACTIVE _='ACTIVE'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id114 "Link to this definition")INACTIVE _='INACTIVE'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id115 "Link to this definition")OFFLOADED _='OFFLOADED'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id116 "Link to this definition")OFFLOADING _='OFFLOADING'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id117 "Link to this definition")ONLOADING _='ONLOADING'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id118 "Link to this definition")HOT _='HOT'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id119 "Link to this definition")COLD _='COLD'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id120 "Link to this definition")FROZEN _='FROZEN'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id121 "Link to this definition")_class_ weaviate.classes.tenants.TenantCreateActivityStatus( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/tenants.html#TenantCreateActivityStatus) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantCreateActivityStatus "Link to this definition")

Bases: `str`, `Enum`

TenantActivityStatus class used to describe the activity status of a tenant to create in Weaviate.

ACTIVE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantCreateActivityStatus.ACTIVE "Link to this definition")

The tenant is fully active and can be used.

INACTIVE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantCreateActivityStatus.INACTIVE "Link to this definition")

The tenant is not active, files stored locally.

HOT [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantCreateActivityStatus.HOT "Link to this definition")

DEPRECATED, please use ACTIVE. The tenant is fully active and can be used.

COLD [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantCreateActivityStatus.COLD "Link to this definition")

DEPRECATED, please use INACTIVE. The tenant is not active, files stored locally.

ACTIVE _='ACTIVE'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id122 "Link to this definition")INACTIVE _='INACTIVE'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id123 "Link to this definition")HOT _='HOT'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id124 "Link to this definition")COLD _='COLD'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id125 "Link to this definition")_class_ weaviate.classes.tenants.TenantUpdateActivityStatus( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/tenants.html#TenantUpdateActivityStatus) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantUpdateActivityStatus "Link to this definition")

Bases: `str`, `Enum`

TenantActivityStatus class used to describe the activity status of a tenant to update in Weaviate.

ACTIVE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantUpdateActivityStatus.ACTIVE "Link to this definition")

The tenant is fully active and can be used.

INACTIVE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantUpdateActivityStatus.INACTIVE "Link to this definition")

The tenant is not active, files stored locally.

OFFLOADED [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantUpdateActivityStatus.OFFLOADED "Link to this definition")

The tenant is not active, files stored on the cloud.

HOT [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantUpdateActivityStatus.HOT "Link to this definition")

DEPRECATED, please use ACTIVE. The tenant is fully active and can be used.

COLD [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantUpdateActivityStatus.COLD "Link to this definition")

DEPRECATED, please use INACTIVE. The tenant is not active, files stored locally.

FROZEN [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.tenants.TenantUpdateActivityStatus.FROZEN "Link to this definition")

DEPRECATED, please use OFFLOADED. The tenant is not active, files stored on the cloud.

ACTIVE _='ACTIVE'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id126 "Link to this definition")INACTIVE _='INACTIVE'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id127 "Link to this definition")OFFLOADED _='OFFLOADED'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id128 "Link to this definition")HOT _='HOT'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id129 "Link to this definition")COLD _='COLD'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id130 "Link to this definition")FROZEN _='FROZEN'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#id131 "Link to this definition")

Versions[latest](https://weaviate-python-client.readthedocs.io/en/latest/weaviate.classes.html)**[stable](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html)**[v4.16.10](https://weaviate-python-client.readthedocs.io/en/v4.16.10/weaviate.classes.html)[v4.16.9](https://weaviate-python-client.readthedocs.io/en/v4.16.9/weaviate.classes.html)[v4.16.8](https://weaviate-python-client.readthedocs.io/en/v4.16.8/weaviate.classes.html)[v4.16.7](https://weaviate-python-client.readthedocs.io/en/v4.16.7/weaviate.classes.html)[v4.16.6](https://weaviate-python-client.readthedocs.io/en/v4.16.6/weaviate.classes.html)[v4.16.5](https://weaviate-python-client.readthedocs.io/en/v4.16.5/weaviate.classes.html)[v4.16.4](https://weaviate-python-client.readthedocs.io/en/v4.16.4/weaviate.classes.html)[v4.16.3](https://weaviate-python-client.readthedocs.io/en/v4.16.3/weaviate.classes.html)[v4.16.2](https://weaviate-python-client.readthedocs.io/en/v4.16.2/weaviate.classes.html)[v4.16.1](https://weaviate-python-client.readthedocs.io/en/v4.16.1/weaviate.classes.html)[v4.16.0](https://weaviate-python-client.readthedocs.io/en/v4.16.0/weaviate.classes.html)[v4.15.4](https://weaviate-python-client.readthedocs.io/en/v4.15.4/weaviate.classes.html)[v4.15.3](https://weaviate-python-client.readthedocs.io/en/v4.15.3/weaviate.classes.html)[v4.15.2](https://weaviate-python-client.readthedocs.io/en/v4.15.2/weaviate.classes.html)[v4.15.1](https://weaviate-python-client.readthedocs.io/en/v4.15.1/weaviate.classes.html)[v4.15.0](https://weaviate-python-client.readthedocs.io/en/v4.15.0/weaviate.classes.html)[v4.14.4](https://weaviate-python-client.readthedocs.io/en/v4.14.4/weaviate.classes.html)[v4.14.3](https://weaviate-python-client.readthedocs.io/en/v4.14.3/weaviate.classes.html)[v4.14.2](https://weaviate-python-client.readthedocs.io/en/v4.14.2/weaviate.classes.html)[v4.14.1](https://weaviate-python-client.readthedocs.io/en/v4.14.1/weaviate.classes.html)[v4.14.0](https://weaviate-python-client.readthedocs.io/en/v4.14.0/weaviate.classes.html)[v4.13.2](https://weaviate-python-client.readthedocs.io/en/v4.13.2/weaviate.classes.html)[v4.13.1](https://weaviate-python-client.readthedocs.io/en/v4.13.1/weaviate.classes.html)[v4.13.0](https://weaviate-python-client.readthedocs.io/en/v4.13.0/weaviate.classes.html)[v4.12.1](https://weaviate-python-client.readthedocs.io/en/v4.12.1/weaviate.classes.html)[v4.12.0](https://weaviate-python-client.readthedocs.io/en/v4.12.0/weaviate.classes.html)[v4.11.3](https://weaviate-python-client.readthedocs.io/en/v4.11.3/weaviate.classes.html)[v4.11.2](https://weaviate-python-client.readthedocs.io/en/v4.11.2/weaviate.classes.html)[v4.11.1](https://weaviate-python-client.readthedocs.io/en/v4.11.1/weaviate.classes.html)[v4.11.0](https://weaviate-python-client.readthedocs.io/en/v4.11.0/weaviate.classes.html)[v4.10.4](https://weaviate-python-client.readthedocs.io/en/v4.10.4/weaviate.classes.html)[v4.10.3](https://weaviate-python-client.readthedocs.io/en/v4.10.3/weaviate.classes.html)[v4.10.2](https://weaviate-python-client.readthedocs.io/en/v4.10.2/weaviate.classes.html)[v4.10.0](https://weaviate-python-client.readthedocs.io/en/v4.10.0/weaviate.classes.html)[v4.9.6](https://weaviate-python-client.readthedocs.io/en/v4.9.6/weaviate.classes.html)[v4.9.5](https://weaviate-python-client.readthedocs.io/en/v4.9.5/weaviate.classes.html)[v4.9.4](https://weaviate-python-client.readthedocs.io/en/v4.9.4/weaviate.classes.html)[v4.9.3](https://weaviate-python-client.readthedocs.io/en/v4.9.3/weaviate.classes.html)[v4.9.2](https://weaviate-python-client.readthedocs.io/en/v4.9.2/weaviate.classes.html)[v4.9.1](https://weaviate-python-client.readthedocs.io/en/v4.9.1/weaviate.classes.html)[v4.9.0](https://weaviate-python-client.readthedocs.io/en/v4.9.0/weaviate.classes.html)[v4.8.1](https://weaviate-python-client.readthedocs.io/en/v4.8.1/weaviate.classes.html)[v4.8.0](https://weaviate-python-client.readthedocs.io/en/v4.8.0/weaviate.classes.html)[v4.7.1](https://weaviate-python-client.readthedocs.io/en/v4.7.1/weaviate.classes.html)[v4.7.0](https://weaviate-python-client.readthedocs.io/en/v4.7.0/weaviate.classes.html)[v4.6.7](https://weaviate-python-client.readthedocs.io/en/v4.6.7/weaviate.classes.html)[v4.6.6](https://weaviate-python-client.readthedocs.io/en/v4.6.6/weaviate.classes.html)[v4.6.5](https://weaviate-python-client.readthedocs.io/en/v4.6.5/weaviate.classes.html)[v4.6.4](https://weaviate-python-client.readthedocs.io/en/v4.6.4/weaviate.classes.html)[v4.6.3](https://weaviate-python-client.readthedocs.io/en/v4.6.3/weaviate.classes.html)[v4.6.2](https://weaviate-python-client.readthedocs.io/en/v4.6.2/weaviate.classes.html)[v4.6.1](https://weaviate-python-client.readthedocs.io/en/v4.6.1/weaviate.classes.html)[v4.6.0](https://weaviate-python-client.readthedocs.io/en/v4.6.0/weaviate.classes.html)[v4.5.7](https://weaviate-python-client.readthedocs.io/en/v4.5.7/weaviate.classes.html)[v4.5.6](https://weaviate-python-client.readthedocs.io/en/v4.5.6/weaviate.classes.html)[v4.5.5](https://weaviate-python-client.readthedocs.io/en/v4.5.5/weaviate.classes.html)[v4.5.4](https://weaviate-python-client.readthedocs.io/en/v4.5.4/weaviate.classes.html)[v4.5.3](https://weaviate-python-client.readthedocs.io/en/v4.5.3/weaviate.classes.html)[v4.5.2](https://weaviate-python-client.readthedocs.io/en/v4.5.2/weaviate.classes.html)[v4.5.1](https://weaviate-python-client.readthedocs.io/en/v4.5.1/weaviate.classes.html)[v4.5.0](https://weaviate-python-client.readthedocs.io/en/v4.5.0/weaviate.classes.html)[v4.4.4](https://weaviate-python-client.readthedocs.io/en/v4.4.4/weaviate.classes.html)[v4.4.3](https://weaviate-python-client.readthedocs.io/en/v4.4.3/weaviate.classes.html)[v4.4.2](https://weaviate-python-client.readthedocs.io/en/v4.4.2/weaviate.classes.html)[v4.4.1](https://weaviate-python-client.readthedocs.io/en/v4.4.1/weaviate.classes.html)[v4.4.0](https://weaviate-python-client.readthedocs.io/en/v4.4.0/weaviate.classes.html)[v3.26.2](https://weaviate-python-client.readthedocs.io/en/v3.26.2/weaviate.classes.html)[v3.26.1](https://weaviate-python-client.readthedocs.io/en/v3.26.1/weaviate.classes.html)[v3.26.0](https://weaviate-python-client.readthedocs.io/en/v3.26.0/weaviate.classes.html)[v3.25.3](https://weaviate-python-client.readthedocs.io/en/v3.25.3/weaviate.classes.html)[v3.25.2](https://weaviate-python-client.readthedocs.io/en/v3.25.2/weaviate.classes.html)[v3.23.0](https://weaviate-python-client.readthedocs.io/en/v3.23.0/weaviate.classes.html)[v3.22.1](https://weaviate-python-client.readthedocs.io/en/v3.22.1/weaviate.classes.html)[v3.22.0](https://weaviate-python-client.readthedocs.io/en/v3.22.0/weaviate.classes.html)[v3.21.0](https://weaviate-python-client.readthedocs.io/en/v3.21.0/weaviate.classes.html)[v3.20.1](https://weaviate-python-client.readthedocs.io/en/v3.20.1/weaviate.classes.html)[v3.20.0](https://weaviate-python-client.readthedocs.io/en/v3.20.0/weaviate.classes.html)[v3.19.2](https://weaviate-python-client.readthedocs.io/en/v3.19.2/weaviate.classes.html)[v3.19.1](https://weaviate-python-client.readthedocs.io/en/v3.19.1/weaviate.classes.html)[v3.19.0](https://weaviate-python-client.readthedocs.io/en/v3.19.0/weaviate.classes.html)[v3.18.0](https://weaviate-python-client.readthedocs.io/en/v3.18.0/weaviate.classes.html)[v3.15.6](https://weaviate-python-client.readthedocs.io/en/v3.15.6/weaviate.classes.html)[v3.15.5](https://weaviate-python-client.readthedocs.io/en/v3.15.5/weaviate.classes.html)[v3.15.4](https://weaviate-python-client.readthedocs.io/en/v3.15.4/weaviate.classes.html)[v3.15.3](https://weaviate-python-client.readthedocs.io/en/v3.15.3/weaviate.classes.html)[v3.15.2](https://weaviate-python-client.readthedocs.io/en/v3.15.2/weaviate.classes.html)[v3.15.1](https://weaviate-python-client.readthedocs.io/en/v3.15.1/weaviate.classes.html)[v3.15.0](https://weaviate-python-client.readthedocs.io/en/v3.15.0/weaviate.classes.html)[v3.14.0](https://weaviate-python-client.readthedocs.io/en/v3.14.0/weaviate.classes.html)[v3.13.0](https://weaviate-python-client.readthedocs.io/en/v3.13.0/weaviate.classes.html)[v3.12.0\_a](https://weaviate-python-client.readthedocs.io/en/v3.12.0_a/weaviate.classes.html)[v3.11.0](https://weaviate-python-client.readthedocs.io/en/v3.11.0/weaviate.classes.html)[v3.10.0](https://weaviate-python-client.readthedocs.io/en/v3.10.0/weaviate.classes.html)[v3.9.0](https://weaviate-python-client.readthedocs.io/en/v3.9.0/weaviate.classes.html)[v3.8.0](https://weaviate-python-client.readthedocs.io/en/v3.8.0/weaviate.classes.html)[v3.7.0](https://weaviate-python-client.readthedocs.io/en/v3.7.0/weaviate.classes.html)[v3.6.0](https://weaviate-python-client.readthedocs.io/en/v3.6.0/weaviate.classes.html)[v3.5.1](https://weaviate-python-client.readthedocs.io/en/v3.5.1/weaviate.classes.html)[v3.5.0](https://weaviate-python-client.readthedocs.io/en/v3.5.0/weaviate.classes.html)[v3.4.1](https://weaviate-python-client.readthedocs.io/en/v3.4.1/weaviate.classes.html)[v3.4.0](https://weaviate-python-client.readthedocs.io/en/v3.4.0/weaviate.classes.html)[v3.3.3](https://weaviate-python-client.readthedocs.io/en/v3.3.3/weaviate.classes.html)[v3.3.2](https://weaviate-python-client.readthedocs.io/en/v3.3.2/weaviate.classes.html)[v3.3.1](https://weaviate-python-client.readthedocs.io/en/v3.3.1/weaviate.classes.html)[v3.3.0](https://weaviate-python-client.readthedocs.io/en/v3.3.0/weaviate.classes.html)[v3.2.5](https://weaviate-python-client.readthedocs.io/en/v3.2.5/weaviate.classes.html)[v3.2.4](https://weaviate-python-client.readthedocs.io/en/v3.2.4/weaviate.classes.html)[v3.2.3](https://weaviate-python-client.readthedocs.io/en/v3.2.3/weaviate.classes.html)[v3.2.2](https://weaviate-python-client.readthedocs.io/en/v3.2.2/weaviate.classes.html)[v3.2.1](https://weaviate-python-client.readthedocs.io/en/v3.2.1/weaviate.classes.html)[v3.2.0](https://weaviate-python-client.readthedocs.io/en/v3.2.0/weaviate.classes.html)[v3.1.1](https://weaviate-python-client.readthedocs.io/en/v3.1.1/weaviate.classes.html)[v3.1.0](https://weaviate-python-client.readthedocs.io/en/v3.1.0/weaviate.classes.html)[v3.0.0](https://weaviate-python-client.readthedocs.io/en/v3.0.0/weaviate.classes.html)On Read the Docs[Project Home](https://app.readthedocs.org/projects/weaviate-python-client/?utm_source=weaviate-python-client&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/weaviate-python-client/builds/?utm_source=weaviate-python-client&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=weaviate-python-client&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=weaviate-python-client&utm_content=flyout)