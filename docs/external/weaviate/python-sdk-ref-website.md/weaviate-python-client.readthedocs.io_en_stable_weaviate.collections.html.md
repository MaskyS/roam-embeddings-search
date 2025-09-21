---
url: "https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html"
title: "weaviate.collections — Weaviate Python Client 4.16.10 documentation"
---

- [Home](https://weaviate-python-client.readthedocs.io/en/stable/index.html)
- [Weaviate Library](https://weaviate-python-client.readthedocs.io/en/stable/modules.html)
- [weaviate](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html)
- weaviate.collections
- [View page source](https://weaviate-python-client.readthedocs.io/en/stable/_sources/weaviate.collections.rst.txt)

* * *

# weaviate.collections [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html\#module-weaviate.collections "Link to this heading")

_class_ weaviate.collections.Collection( _connection_, _name_, _validate\_arguments_, _consistency\_level=None_, _tenant=None_, _properties=None_, _references=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/collection/sync.html#Collection) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection "Link to this definition")

The collection class is the main entry point for interacting with a collection in Weaviate.

This class is returned by the client.collections.create and client.collections.get methods. It provides
access to all the methods available to you when interacting with a collection in Weaviate.

You should not need to instantiate this class yourself but it may be useful to import this as a type when
performing type hinting of functions that depend on a collection object.

Parameters:

- **connection** ( _ConnectionSync_)

- **name** ( _str_)

- **validate\_arguments** ( _bool_)

- **consistency\_level** ( [_ConsistencyLevel_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.ConsistencyLevel "weaviate.collections.classes.config.ConsistencyLevel") _\|_ _None_)

- **tenant** ( _str_ _\|_ _None_)

- **properties** ( _Type_ _\[_ [_Properties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties") _\]_ _\|_ _None_)

- **references** ( _Type_ _\[_ [_References_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References") _\]_ _\|_ _None_)


aggregate [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection.aggregate "Link to this definition")

This namespace includes all the querying methods available to you when using Weaviate’s standard aggregation capabilities.

aggregate\_group\_by [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection.aggregate_group_by "Link to this definition")

This namespace includes all the aggregate methods available to you when using Weaviate’s aggregation group-by capabilities.

config [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection.config "Link to this definition")

This namespace includes all the CRUD methods available to you when modifying the configuration of the collection in Weaviate.

data [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection.data "Link to this definition")

This namespace includes all the CUD methods available to you when modifying the data of the collection in Weaviate.

generate [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection.generate "Link to this definition")

This namespace includes all the querying methods available to you when using Weaviate’s generative capabilities.

query\_group\_by [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection.query_group_by "Link to this definition")

This namespace includes all the querying methods available to you when using Weaviate’s querying group-by capabilities.

query [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection.query "Link to this definition")

This namespace includes all the querying methods available to you when using Weaviate’s standard query capabilities.

tenants [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection.tenants "Link to this definition")

This namespace includes all the CRUD methods available to you when modifying the tenants of a multi-tenancy-enabled collection in Weaviate.

exists() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/collection/sync.html#Collection.exists) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection.exists "Link to this definition")

Check if the collection exists in Weaviate.

Return type:

bool

iterator( _include\_vector=False_, _return\_metadata=None_, _\*_, _return\_properties=None_, _return\_references=None_, _after=None_, _cache\_size=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/collection/sync.html#Collection.iterator) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection.iterator "Link to this definition")

Use this method to return an iterator over the objects in the collection.

This iterator keeps a record of the last object that it returned to be used in each subsequent call to
Weaviate. Once the collection is exhausted, the iterator exits.

If return\_properties is not provided, all the properties of each object will be
requested from Weaviate except for its vector as this is an expensive operation. Specify include\_vector
to request the vector back as well. In addition, if return\_references=None then none of the references
are returned. Use wvc.QueryReference to specify which references to return.

Parameters:

- **include\_vector** ( _bool_) – Whether to include the vector in the metadata of the returned objects.

- **return\_metadata** ( _List_ _\[_ _Literal_ _\[_ _'creation\_time'_ _,_ _'last\_update\_time'_ _,_ _'distance'_ _,_ _'certainty'_ _,_ _'score'_ _,_ _'explain\_score'_ _,_ _'is\_consistent'_ _\]_ _\]_ _\|_ _~weaviate.collections.classes.grpc.MetadataQuery_ _\|_ _None_) – The metadata to return with each object.

- **return\_properties** ( _Sequence_ _\[_ _str_ _\|_ [_QueryNested_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.QueryNested "weaviate.collections.classes.grpc.QueryNested") _\]_ _\|_ _str_ _\|_ [_QueryNested_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.QueryNested "weaviate.collections.classes.grpc.QueryNested") _\|_ _bool_ _\|_ _Type_ _\[_ [_TProperties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties") _\]_ _\|_ _None_) – The properties to return with each object.

- **return\_references** ( [_\_QueryReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._QueryReference "weaviate.collections.classes.grpc._QueryReference") _\|_ _Sequence_ _\[_ [_\_QueryReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._QueryReference "weaviate.collections.classes.grpc._QueryReference") _\]_ _\|_ _Type_ _\[_ [_TReferences_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences") _\]_ _\|_ _None_) – The references to return with each object.

- **after** ( _str_ _\|_ _UUID_ _\|_ _None_) – The cursor to use to mark the initial starting point of the iterator in the collection.

- **cache\_size** ( _int_ _\|_ _None_) – How many objects should be fetched in each request to Weaviate during the iteration. The default is 100.


Raises:

**WeaviateGRPCQueryError** – If the request to the Weaviate server fails.

Return type:

[_\_ObjectIterator_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectIterator "weaviate.collections.iterator._ObjectIterator")\[ [_Properties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties"), [_References_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\] \| [_\_ObjectIterator_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectIterator "weaviate.collections.iterator._ObjectIterator")\[ [_Properties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties"), _Mapping_\[str, [_\_CrossReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal._CrossReference "weaviate.collections.classes.internal._CrossReference")\[ _Mapping_\[str, None \| str \| bool \| int \| float \| _datetime_ \| _UUID_ \| [_GeoCoordinate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.GeoCoordinate "weaviate.collections.classes.types.GeoCoordinate") \| [_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.PhoneNumber "weaviate.collections.classes.types.PhoneNumber") \| [_\_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._PhoneNumber "weaviate.collections.classes.types._PhoneNumber") \| _Mapping_\[str, WeaviateField\] \| _Sequence_\[str\] \| _Sequence_\[bool\] \| _Sequence_\[int\] \| _Sequence_\[float\] \| _Sequence_\[ _datetime_\] \| _Sequence_\[ _UUID_\] \| _Sequence_\[ _Mapping_\[str, WeaviateField\]\]\], CrossReferences\]\]\] \| [_\_ObjectIterator_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectIterator "weaviate.collections.iterator._ObjectIterator")\[ [_Properties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties"), [_TReferences_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences")\] \| [_\_ObjectIterator_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectIterator "weaviate.collections.iterator._ObjectIterator")\[ [_TProperties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [_References_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\] \| [_\_ObjectIterator_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectIterator "weaviate.collections.iterator._ObjectIterator")\[ [_TProperties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), _Mapping_\[str, [_\_CrossReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal._CrossReference "weaviate.collections.classes.internal._CrossReference")\[ _Mapping_\[str, None \| str \| bool \| int \| float \| _datetime_ \| _UUID_ \| [_GeoCoordinate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.GeoCoordinate "weaviate.collections.classes.types.GeoCoordinate") \| [_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.PhoneNumber "weaviate.collections.classes.types.PhoneNumber") \| [_\_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._PhoneNumber "weaviate.collections.classes.types._PhoneNumber") \| _Mapping_\[str, WeaviateField\] \| _Sequence_\[str\] \| _Sequence_\[bool\] \| _Sequence_\[int\] \| _Sequence_\[float\] \| _Sequence_\[ _datetime_\] \| _Sequence_\[ _UUID_\] \| _Sequence_\[ _Mapping_\[str, WeaviateField\]\]\], CrossReferences\]\]\] \| [_\_ObjectIterator_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectIterator "weaviate.collections.iterator._ObjectIterator")\[ [_TProperties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [_TReferences_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences")\]

shards() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/collection/sync.html#Collection.shards) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection.shards "Link to this definition")

Get the statuses of all the shards of this collection.

Returns:

The list of shards belonging to this collection.

Raises:

- [**WeaviateConnectionError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateConnectionError "weaviate.exceptions.WeaviateConnectionError") – If the network connection to weaviate fails.

- [**UnexpectedStatusCodeError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If weaviate reports a none OK status.

- **weaviate.EmptyResponseError** – If the response is empty.


Return type:

_List_\[ [_Shard_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.cluster.Shard "weaviate.collections.classes.cluster.Shard")\]

with\_consistency\_level( _consistency\_level_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/collection/sync.html#Collection.with_consistency_level) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection.with_consistency_level "Link to this definition")

Use this method to return a collection object specific to a single consistency level.

If replication is not configured for this collection then Weaviate will throw an error.

This method does not send a request to Weaviate. It only returns a new collection object that is specific
to the consistency level you specify.

Parameters:

**consistency\_level** ( [_ConsistencyLevel_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.ConsistencyLevel "weaviate.collections.classes.config.ConsistencyLevel")) – The consistency level to use.

Return type:

[_Collection_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.collection.html#weaviate.collections.collection.Collection "weaviate.collections.collection.sync.Collection")\[ [_Properties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties"), [_References_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\]

with\_tenant( _tenant_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/collection/sync.html#Collection.with_tenant) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection.with_tenant "Link to this definition")

Use this method to return a collection object specific to a single tenant.

If multi-tenancy is not configured for this collection then Weaviate will throw an error.

This method does not send a request to Weaviate. It only returns a new collection object that is specific
to the tenant you specify.

Parameters:

**tenant** ( _str_ _\|_ [_Tenant_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.tenants.Tenant "weaviate.collections.classes.tenants.Tenant")) – The tenant to use. Can be str or wvc.tenants.Tenant.

Return type:

[_Collection_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.collection.html#weaviate.collections.collection.Collection "weaviate.collections.collection.sync.Collection")\[ [_Properties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties"), [_References_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\]

aggregate _: [\_AggregateCollection](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.aggregate._AggregateCollection "weaviate.collections.aggregate._AggregateCollection")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#id0 "Link to this definition")

This namespace includes all the querying methods available to you when using Weaviate’s standard aggregation capabilities.

backup _: [\_CollectionBackup](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.backups.html#weaviate.collections.backups._CollectionBackup "weaviate.collections.backups.sync._CollectionBackup")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection.backup "Link to this definition")

This namespace includes all the backup methods available to you when backing up a collection in Weaviate.

batch _: [\_BatchCollectionWrapper](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.batch.html#weaviate.collections.batch.collection._BatchCollectionWrapper "weaviate.collections.batch.collection._BatchCollectionWrapper")\[ [Properties](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties")\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection.batch "Link to this definition")

This namespace contains all the functionality to upload data in batches to Weaviate for this specific collection.

config _: [\_ConfigCollection](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.config.html#weaviate.collections.config._ConfigCollection "weaviate.collections.config.sync._ConfigCollection")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#id1 "Link to this definition")

This namespace includes all the CRUD methods available to you when modifying the configuration of the collection in Weaviate.

data _: [\_DataCollection](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.data.html#weaviate.collections.data._DataCollection "weaviate.collections.data.sync._DataCollection")\[ [Properties](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties")\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#id2 "Link to this definition")

This namespace includes all the CUD methods available to you when modifying the data of the collection in Weaviate.

generate _: [\_GenerateCollection](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.generate._GenerateCollection "weaviate.collections.generate._GenerateCollection")\[ [Properties](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties"), [References](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#id3 "Link to this definition")

This namespace includes all the querying methods available to you when using Weaviate’s generative capabilities.

query _: [\_QueryCollection](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.query._QueryCollection "weaviate.collections.query._QueryCollection")\[ [Properties](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties"), [References](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#id4 "Link to this definition")

This namespace includes all the querying methods available to you when using Weaviate’s standard query capabilities.

tenants _: [\_Tenants](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.tenants.html#weaviate.collections.tenants._Tenants "weaviate.collections.tenants.sync._Tenants")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#id5 "Link to this definition")

This namespace includes all the CRUD methods available to you when modifying the tenants of a multi-tenancy-enabled collection in Weaviate.

_class_ weaviate.collections.CollectionAsync( _connection_, _name_, _validate\_arguments_, _consistency\_level=None_, _tenant=None_, _properties=None_, _references=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/collection/async_.html#CollectionAsync) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync "Link to this definition")

The collection class is the main entry point for interacting with a collection in Weaviate.

This class is returned by the client.collections.create and client.collections.get methods. It provides
access to all the methods available to you when interacting with a collection in Weaviate.

You should not need to instantiate this class yourself but it may be useful to import this as a type when
performing type hinting of functions that depend on a collection object.

Parameters:

- **connection** ( _ConnectionAsync_)

- **name** ( _str_)

- **validate\_arguments** ( _bool_)

- **consistency\_level** ( [_ConsistencyLevel_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.ConsistencyLevel "weaviate.collections.classes.config.ConsistencyLevel") _\|_ _None_)

- **tenant** ( _str_ _\|_ _None_)

- **properties** ( _Type_ _\[_ [_Properties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties") _\]_ _\|_ _None_)

- **references** ( _Type_ _\[_ [_References_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References") _\]_ _\|_ _None_)


aggregate [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.aggregate "Link to this definition")

This namespace includes all the querying methods available to you when using Weaviate’s standard aggregation capabilities.

aggregate\_group\_by [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.aggregate_group_by "Link to this definition")

This namespace includes all the aggregate methods available to you when using Weaviate’s aggregation group-by capabilities.

config [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.config "Link to this definition")

This namespace includes all the CRUD methods available to you when modifying the configuration of the collection in Weaviate.

data [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.data "Link to this definition")

This namespace includes all the CUD methods available to you when modifying the data of the collection in Weaviate.

generate [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.generate "Link to this definition")

This namespace includes all the querying methods available to you when using Weaviate’s generative capabilities.

query\_group\_by [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.query_group_by "Link to this definition")

This namespace includes all the querying methods available to you when using Weaviate’s querying group-by capabilities.

query [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.query "Link to this definition")

This namespace includes all the querying methods available to you when using Weaviate’s standard query capabilities.

tenants [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.tenants "Link to this definition")

This namespace includes all the CRUD methods available to you when modifying the tenants of a multi-tenancy-enabled collection in Weaviate.

_async_ exists() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/collection/async_.html#CollectionAsync.exists) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.exists "Link to this definition")

Check if the collection exists in Weaviate.

Return type:

bool

iterator( _include\_vector=False_, _return\_metadata=None_, _\*_, _return\_properties=None_, _return\_references=None_, _after=None_, _cache\_size=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/collection/async_.html#CollectionAsync.iterator) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.iterator "Link to this definition")

Use this method to return an iterator over the objects in the collection.

This iterator keeps a record of the last object that it returned to be used in each subsequent call to
Weaviate. Once the collection is exhausted, the iterator exits.

If return\_properties is not provided, all the properties of each object will be
requested from Weaviate except for its vector as this is an expensive operation. Specify include\_vector
to request the vector back as well. In addition, if return\_references=None then none of the references
are returned. Use wvc.QueryReference to specify which references to return.

Parameters:

- **include\_vector** ( _bool_) – Whether to include the vector in the metadata of the returned objects.

- **return\_metadata** ( _List_ _\[_ _Literal_ _\[_ _'creation\_time'_ _,_ _'last\_update\_time'_ _,_ _'distance'_ _,_ _'certainty'_ _,_ _'score'_ _,_ _'explain\_score'_ _,_ _'is\_consistent'_ _\]_ _\]_ _\|_ _~weaviate.collections.classes.grpc.MetadataQuery_ _\|_ _None_) – The metadata to return with each object.

- **return\_properties** ( _Sequence_ _\[_ _str_ _\|_ [_QueryNested_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.QueryNested "weaviate.collections.classes.grpc.QueryNested") _\]_ _\|_ _str_ _\|_ [_QueryNested_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.QueryNested "weaviate.collections.classes.grpc.QueryNested") _\|_ _bool_ _\|_ _Type_ _\[_ [_TProperties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties") _\]_ _\|_ _None_) – The properties to return with each object.

- **return\_references** ( [_\_QueryReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._QueryReference "weaviate.collections.classes.grpc._QueryReference") _\|_ _Sequence_ _\[_ [_\_QueryReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._QueryReference "weaviate.collections.classes.grpc._QueryReference") _\]_ _\|_ _Type_ _\[_ [_TReferences_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences") _\]_ _\|_ _None_) – The references to return with each object.

- **after** ( _str_ _\|_ _UUID_ _\|_ _None_) – The cursor to use to mark the initial starting point of the iterator in the collection.

- **cache\_size** ( _int_ _\|_ _None_) – How many objects should be fetched in each request to Weaviate during the iteration. The default is 100.


Raises:

**WeaviateGRPCQueryError** – If the request to the Weaviate server fails.

Return type:

[_\_ObjectAIterator_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectAIterator "weaviate.collections.iterator._ObjectAIterator")\[ [_Properties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties"), [_References_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\] \| [_\_ObjectAIterator_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectAIterator "weaviate.collections.iterator._ObjectAIterator")\[ [_Properties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties"), _Mapping_\[str, [_\_CrossReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal._CrossReference "weaviate.collections.classes.internal._CrossReference")\[ _Mapping_\[str, None \| str \| bool \| int \| float \| _datetime_ \| _UUID_ \| [_GeoCoordinate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.GeoCoordinate "weaviate.collections.classes.types.GeoCoordinate") \| [_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.PhoneNumber "weaviate.collections.classes.types.PhoneNumber") \| [_\_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._PhoneNumber "weaviate.collections.classes.types._PhoneNumber") \| _Mapping_\[str, WeaviateField\] \| _Sequence_\[str\] \| _Sequence_\[bool\] \| _Sequence_\[int\] \| _Sequence_\[float\] \| _Sequence_\[ _datetime_\] \| _Sequence_\[ _UUID_\] \| _Sequence_\[ _Mapping_\[str, WeaviateField\]\]\], CrossReferences\]\]\] \| [_\_ObjectAIterator_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectAIterator "weaviate.collections.iterator._ObjectAIterator")\[ [_Properties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties"), [_TReferences_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences")\] \| [_\_ObjectAIterator_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectAIterator "weaviate.collections.iterator._ObjectAIterator")\[ [_TProperties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [_References_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\] \| [_\_ObjectAIterator_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectAIterator "weaviate.collections.iterator._ObjectAIterator")\[ [_TProperties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), _Mapping_\[str, [_\_CrossReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal._CrossReference "weaviate.collections.classes.internal._CrossReference")\[ _Mapping_\[str, None \| str \| bool \| int \| float \| _datetime_ \| _UUID_ \| [_GeoCoordinate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.GeoCoordinate "weaviate.collections.classes.types.GeoCoordinate") \| [_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.PhoneNumber "weaviate.collections.classes.types.PhoneNumber") \| [_\_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._PhoneNumber "weaviate.collections.classes.types._PhoneNumber") \| _Mapping_\[str, WeaviateField\] \| _Sequence_\[str\] \| _Sequence_\[bool\] \| _Sequence_\[int\] \| _Sequence_\[float\] \| _Sequence_\[ _datetime_\] \| _Sequence_\[ _UUID_\] \| _Sequence_\[ _Mapping_\[str, WeaviateField\]\]\], CrossReferences\]\]\] \| [_\_ObjectAIterator_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectAIterator "weaviate.collections.iterator._ObjectAIterator")\[ [_TProperties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [_TReferences_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences")\]

_async_ length() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/collection/async_.html#CollectionAsync.length) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.length "Link to this definition")

Get the total number of objects in the collection.

Return type:

int

_async_ shards() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/collection/async_.html#CollectionAsync.shards) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.shards "Link to this definition")

Get the statuses of all the shards of this collection.

Returns:

The list of shards belonging to this collection.

Raises:

- [**WeaviateConnectionError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateConnectionError "weaviate.exceptions.WeaviateConnectionError") – If the network connection to weaviate fails.

- [**UnexpectedStatusCodeError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If weaviate reports a none OK status.

- **weaviate.EmptyResponseError** – If the response is empty.


Return type:

_List_\[ [_Shard_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.cluster.Shard "weaviate.collections.classes.cluster.Shard")\]

_async_ to\_string() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/collection/async_.html#CollectionAsync.to_string) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.to_string "Link to this definition")

Return a string representation of the collection object.

Return type:

str

with\_consistency\_level( _consistency\_level_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/collection/async_.html#CollectionAsync.with_consistency_level) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.with_consistency_level "Link to this definition")

Use this method to return a collection object specific to a single consistency level.

If replication is not configured for this collection then Weaviate will throw an error.

This method does not send a request to Weaviate. It only returns a new collection object that is specific
to the consistency level you specify.

Parameters:

**consistency\_level** ( [_ConsistencyLevel_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.ConsistencyLevel "weaviate.collections.classes.config.ConsistencyLevel") _\|_ _None_) – The consistency level to use.

Return type:

[_CollectionAsync_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.collection.html#weaviate.collections.collection.CollectionAsync "weaviate.collections.collection.async_.CollectionAsync")\[ [_Properties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties"), [_References_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\]

with\_tenant( _tenant_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/collection/async_.html#CollectionAsync.with_tenant) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.with_tenant "Link to this definition")

Use this method to return a collection object specific to a single tenant.

If multi-tenancy is not configured for this collection then Weaviate will throw an error.

This method does not send a request to Weaviate. It only returns a new collection object that is specific
to the tenant you specify.

Parameters:

**tenant** ( _str_ _\|_ [_Tenant_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.tenants.Tenant "weaviate.collections.classes.tenants.Tenant") _\|_ _None_) – The tenant to use. Can be str or wvc.tenants.Tenant.

Return type:

[_CollectionAsync_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.collection.html#weaviate.collections.collection.CollectionAsync "weaviate.collections.collection.async_.CollectionAsync")\[ [_Properties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties"), [_References_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\]

aggregate _: [\_AggregateCollectionAsync](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.aggregate._AggregateCollectionAsync "weaviate.collections.aggregate._AggregateCollectionAsync")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#id6 "Link to this definition")

This namespace includes all the querying methods available to you when using Weaviate’s standard aggregation capabilities.

backup _: [\_CollectionBackupAsync](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.backups.html#weaviate.collections.backups._CollectionBackupAsync "weaviate.collections.backups.async_._CollectionBackupAsync")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync.backup "Link to this definition")

This namespace includes all the backup methods available to you when backing up a collection in Weaviate.

config [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#id7 "Link to this definition")

This namespace includes all the CRUD methods available to you when modifying the configuration of the collection in Weaviate.

data [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#id8 "Link to this definition")

This namespace includes all the CUD methods available to you when modifying the data of the collection in Weaviate.

generate _: [\_GenerateCollectionAsync](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.generate._GenerateCollectionAsync "weaviate.collections.generate._GenerateCollectionAsync")\[ [Properties](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.Properties "weaviate.collections.classes.types.Properties"), [References](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#id9 "Link to this definition")

This namespace includes all the querying methods available to you when using Weaviate’s generative capabilities.

query [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#id10 "Link to this definition")

This namespace includes all the querying methods available to you when using Weaviate’s standard query capabilities.

tenants [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#id11 "Link to this definition")

This namespace includes all the CRUD methods available to you when modifying the tenants of a multi-tenancy-enabled collection in Weaviate.

## Subpackages [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html\#subpackages "Link to this heading")

- [weaviate.collections.aggregations](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.aggregations.html)
- [weaviate.collections.backups](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.backups.html)
- [weaviate.collections.batch](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.batch.html)
- [weaviate.collections.classes](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html)
- [weaviate.collections.cluster](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.cluster.html)
- [weaviate.collections.collection](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.collection.html)
- [weaviate.collections.collections](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.collections.html)
- [weaviate.collections.config](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.config.html)
- [weaviate.collections.data](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.data.html)
- [weaviate.collections.grpc](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.grpc.html)
- [weaviate.collections.queries](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.html)
- [weaviate.collections.tenants](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.tenants.html)

### weaviate.collections.aggregate [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html\#module-weaviate.collections.aggregate "Link to this heading")

_class_ weaviate.collections.aggregate.\_AggregateCollectionAsync( _connection_, _name_, _consistency\_level_, _tenant_, _validate\_arguments_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/aggregate.html#_AggregateCollectionAsync) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.aggregate._AggregateCollectionAsync "Link to this definition")

Bases: [`_HybridAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.aggregations.html#weaviate.collections.aggregations.hybrid._HybridAsync "weaviate.collections.aggregations.hybrid.async_._HybridAsync"), [`_NearImageAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.aggregations.html#weaviate.collections.aggregations.near_image._NearImageAsync "weaviate.collections.aggregations.near_image.async_._NearImageAsync"), [`_NearObjectAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.aggregations.html#weaviate.collections.aggregations.near_object._NearObjectAsync "weaviate.collections.aggregations.near_object.async_._NearObjectAsync"), [`_NearTextAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.aggregations.html#weaviate.collections.aggregations.near_text._NearTextAsync "weaviate.collections.aggregations.near_text.async_._NearTextAsync"), [`_NearVectorAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.aggregations.html#weaviate.collections.aggregations.near_vector._NearVectorAsync "weaviate.collections.aggregations.near_vector.async_._NearVectorAsync"), [`_OverAllAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.aggregations.html#weaviate.collections.aggregations.over_all._OverAllAsync "weaviate.collections.aggregations.over_all.async_._OverAllAsync")

Parameters:

- **connection** ( _ConnectionType_)

- **name** ( _str_)

- **consistency\_level** ( [_ConsistencyLevel_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.ConsistencyLevel "weaviate.collections.classes.config.ConsistencyLevel") _\|_ _None_)

- **tenant** ( _str_ _\|_ _None_)

- **validate\_arguments** ( _bool_)


_class_ weaviate.collections.aggregate.\_AggregateCollection( _connection_, _name_, _consistency\_level_, _tenant_, _validate\_arguments_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/aggregate.html#_AggregateCollection) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.aggregate._AggregateCollection "Link to this definition")

Bases: [`_Hybrid`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.aggregations.html#weaviate.collections.aggregations.hybrid._Hybrid "weaviate.collections.aggregations.hybrid.sync._Hybrid"), [`_NearImage`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.aggregations.html#weaviate.collections.aggregations.near_image._NearImage "weaviate.collections.aggregations.near_image.sync._NearImage"), [`_NearObject`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.aggregations.html#weaviate.collections.aggregations.near_object._NearObject "weaviate.collections.aggregations.near_object.sync._NearObject"), [`_NearText`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.aggregations.html#weaviate.collections.aggregations.near_text._NearText "weaviate.collections.aggregations.near_text.sync._NearText"), [`_NearVector`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.aggregations.html#weaviate.collections.aggregations.near_vector._NearVector "weaviate.collections.aggregations.near_vector.sync._NearVector"), [`_OverAll`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.aggregations.html#weaviate.collections.aggregations.over_all._OverAll "weaviate.collections.aggregations.over_all.sync._OverAll")

Parameters:

- **connection** ( _ConnectionType_)

- **name** ( _str_)

- **consistency\_level** ( [_ConsistencyLevel_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.ConsistencyLevel "weaviate.collections.classes.config.ConsistencyLevel") _\|_ _None_)

- **tenant** ( _str_ _\|_ _None_)

- **validate\_arguments** ( _bool_)


### weaviate.collections.filters [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html\#module-weaviate.collections.filters "Link to this heading")

_class_ weaviate.collections.filters.\_FilterToGRPC [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/filters.html#_FilterToGRPC) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToGRPC "Link to this definition")

Bases: `object`

_static_ convert( _weav\_filter:Literal\[None\]_)→None [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/filters.html#_FilterToGRPC.convert) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToGRPC.convert "Link to this definition")_static_ convert( _weav\_filter:[\_Filters](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._Filters "weaviate.collections.classes.filters._Filters")_)→Filters_static_\_FilterToGRPC\_\_and\_or\_filter( _weav\_filter_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToGRPC._FilterToGRPC__and_or_filter "Link to this definition")Parameters:

**weav\_filter** ( [_\_Filters_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._Filters "weaviate.collections.classes.filters._Filters"))

Return type:

_Filters_ \| None

_static_\_FilterToGRPC\_\_filter\_to\_bool\_list( _value_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToGRPC._FilterToGRPC__filter_to_bool_list "Link to this definition")Parameters:

**value** ( _int_ _\|_ _float_ _\|_ _str_ _\|_ _bool_ _\|_ _datetime_ _\|_ _UUID_ _\|_ [_\_GeoCoordinateFilter_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._GeoCoordinateFilter "weaviate.collections.classes.filters._GeoCoordinateFilter") _\|_ _None_ _\|_ _Sequence_ _\[_ _str_ _\]_ _\|_ _Sequence_ _\[_ _bool_ _\]_ _\|_ _Sequence_ _\[_ _int_ _\]_ _\|_ _Sequence_ _\[_ _float_ _\]_ _\|_ _Sequence_ _\[_ _datetime_ _\]_ _\|_ _Sequence_ _\[_ _str_ _\|_ _UUID_ _\]_)

Return type:

_BooleanArray_ \| None

_static_\_FilterToGRPC\_\_filter\_to\_float\_list( _value_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToGRPC._FilterToGRPC__filter_to_float_list "Link to this definition")Parameters:

**value** ( _int_ _\|_ _float_ _\|_ _str_ _\|_ _bool_ _\|_ _datetime_ _\|_ _UUID_ _\|_ [_\_GeoCoordinateFilter_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._GeoCoordinateFilter "weaviate.collections.classes.filters._GeoCoordinateFilter") _\|_ _None_ _\|_ _Sequence_ _\[_ _str_ _\]_ _\|_ _Sequence_ _\[_ _bool_ _\]_ _\|_ _Sequence_ _\[_ _int_ _\]_ _\|_ _Sequence_ _\[_ _float_ _\]_ _\|_ _Sequence_ _\[_ _datetime_ _\]_ _\|_ _Sequence_ _\[_ _str_ _\|_ _UUID_ _\]_)

Return type:

_NumberArray_ \| None

_static_\_FilterToGRPC\_\_filter\_to\_geo( _value_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToGRPC._FilterToGRPC__filter_to_geo "Link to this definition")Parameters:

**value** ( _int_ _\|_ _float_ _\|_ _str_ _\|_ _bool_ _\|_ _datetime_ _\|_ _UUID_ _\|_ [_\_GeoCoordinateFilter_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._GeoCoordinateFilter "weaviate.collections.classes.filters._GeoCoordinateFilter") _\|_ _None_ _\|_ _Sequence_ _\[_ _str_ _\]_ _\|_ _Sequence_ _\[_ _bool_ _\]_ _\|_ _Sequence_ _\[_ _int_ _\]_ _\|_ _Sequence_ _\[_ _float_ _\]_ _\|_ _Sequence_ _\[_ _datetime_ _\]_ _\|_ _Sequence_ _\[_ _str_ _\|_ _UUID_ _\]_)

Return type:

_GeoCoordinatesFilter_ \| None

_static_\_FilterToGRPC\_\_filter\_to\_int\_list( _value_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToGRPC._FilterToGRPC__filter_to_int_list "Link to this definition")Parameters:

**value** ( _int_ _\|_ _float_ _\|_ _str_ _\|_ _bool_ _\|_ _datetime_ _\|_ _UUID_ _\|_ [_\_GeoCoordinateFilter_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._GeoCoordinateFilter "weaviate.collections.classes.filters._GeoCoordinateFilter") _\|_ _None_ _\|_ _Sequence_ _\[_ _str_ _\]_ _\|_ _Sequence_ _\[_ _bool_ _\]_ _\|_ _Sequence_ _\[_ _int_ _\]_ _\|_ _Sequence_ _\[_ _float_ _\]_ _\|_ _Sequence_ _\[_ _datetime_ _\]_ _\|_ _Sequence_ _\[_ _str_ _\|_ _UUID_ _\]_)

Return type:

_IntArray_ \| None

_static_\_FilterToGRPC\_\_filter\_to\_text( _value_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToGRPC._FilterToGRPC__filter_to_text "Link to this definition")Parameters:

**value** ( _int_ _\|_ _float_ _\|_ _str_ _\|_ _bool_ _\|_ _datetime_ _\|_ _UUID_ _\|_ [_\_GeoCoordinateFilter_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._GeoCoordinateFilter "weaviate.collections.classes.filters._GeoCoordinateFilter") _\|_ _None_ _\|_ _Sequence_ _\[_ _str_ _\]_ _\|_ _Sequence_ _\[_ _bool_ _\]_ _\|_ _Sequence_ _\[_ _int_ _\]_ _\|_ _Sequence_ _\[_ _float_ _\]_ _\|_ _Sequence_ _\[_ _datetime_ _\]_ _\|_ _Sequence_ _\[_ _str_ _\|_ _UUID_ _\]_)

Return type:

str \| None

_static_\_FilterToGRPC\_\_filter\_to\_text\_list( _value_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToGRPC._FilterToGRPC__filter_to_text_list "Link to this definition")Parameters:

**value** ( _int_ _\|_ _float_ _\|_ _str_ _\|_ _bool_ _\|_ _datetime_ _\|_ _UUID_ _\|_ [_\_GeoCoordinateFilter_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._GeoCoordinateFilter "weaviate.collections.classes.filters._GeoCoordinateFilter") _\|_ _None_ _\|_ _Sequence_ _\[_ _str_ _\]_ _\|_ _Sequence_ _\[_ _bool_ _\]_ _\|_ _Sequence_ _\[_ _int_ _\]_ _\|_ _Sequence_ _\[_ _float_ _\]_ _\|_ _Sequence_ _\[_ _datetime_ _\]_ _\|_ _Sequence_ _\[_ _str_ _\|_ _UUID_ _\]_)

Return type:

_TextArray_ \| None

_static_\_FilterToGRPC\_\_to\_target( _target_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToGRPC._FilterToGRPC__to_target "Link to this definition")Parameters:

**target** ( [_\_SingleTargetRef_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._SingleTargetRef "weaviate.collections.classes.filters._SingleTargetRef") _\|_ [_\_MultiTargetRef_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._MultiTargetRef "weaviate.collections.classes.filters._MultiTargetRef") _\|_ [_\_CountRef_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._CountRef "weaviate.collections.classes.filters._CountRef") _\|_ _str_)

Return type:

_FilterTarget_

_static_\_FilterToGRPC\_\_value\_filter( _weav\_filter_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToGRPC._FilterToGRPC__value_filter "Link to this definition")Parameters:

**weav\_filter** ( [_\_FilterValue_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._FilterValue "weaviate.collections.classes.filters._FilterValue"))

Return type:

_Filters_

_class_ weaviate.collections.filters.\_FilterToREST [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/filters.html#_FilterToREST) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToREST "Link to this definition")

Bases: `object`

_static_ convert( _weav\_filter_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/filters.html#_FilterToREST.convert) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToREST.convert "Link to this definition")Parameters:

**weav\_filter** ( [_\_Filters_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._Filters "weaviate.collections.classes.filters._Filters"))

Return type:

_Dict_\[str, _Any_\]

_static_\_FilterToREST\_\_and\_or\_filter( _weav\_filter_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToREST._FilterToREST__and_or_filter "Link to this definition")Parameters:

**weav\_filter** ( [_\_Filters_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._Filters "weaviate.collections.classes.filters._Filters"))

Return type:

_Dict_\[str, _Any_\]

_static_\_FilterToREST\_\_parse\_filter( _value_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToREST._FilterToREST__parse_filter "Link to this definition")Parameters:

**value** ( _int_ _\|_ _float_ _\|_ _str_ _\|_ _bool_ _\|_ _datetime_ _\|_ _UUID_ _\|_ [_\_GeoCoordinateFilter_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._GeoCoordinateFilter "weaviate.collections.classes.filters._GeoCoordinateFilter") _\|_ _None_ _\|_ _Sequence_ _\[_ _str_ _\]_ _\|_ _Sequence_ _\[_ _bool_ _\]_ _\|_ _Sequence_ _\[_ _int_ _\]_ _\|_ _Sequence_ _\[_ _float_ _\]_ _\|_ _Sequence_ _\[_ _datetime_ _\]_ _\|_ _Sequence_ _\[_ _str_ _\|_ _UUID_ _\]_)

Return type:

_Dict_\[str, _Any_\]

_static_\_FilterToREST\_\_to\_path( _target_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToREST._FilterToREST__to_path "Link to this definition")Parameters:

**target** ( [_\_SingleTargetRef_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._SingleTargetRef "weaviate.collections.classes.filters._SingleTargetRef") _\|_ [_\_MultiTargetRef_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._MultiTargetRef "weaviate.collections.classes.filters._MultiTargetRef") _\|_ [_\_CountRef_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._CountRef "weaviate.collections.classes.filters._CountRef") _\|_ _str_)

Return type:

_List_\[str\]

_static_\_FilterToREST\_\_value\_filter( _weav\_filter_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.filters._FilterToREST._FilterToREST__value_filter "Link to this definition")Parameters:

**weav\_filter** ( [_\_FilterValue_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._FilterValue "weaviate.collections.classes.filters._FilterValue"))

Return type:

_Dict_\[str, _Any_\]

### weaviate.collections.generate [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html\#module-weaviate.collections.generate "Link to this heading")

_class_ weaviate.collections.generate.\_GenerateCollectionAsync( _connection_, _name_, _consistency\_level_, _tenant_, _properties_, _references_, _validate\_arguments_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/generate.html#_GenerateCollectionAsync) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.generate._GenerateCollectionAsync "Link to this definition")

Bases: `Generic`\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_BM25GenerateAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.bm25.html#weaviate.collections.queries.bm25._BM25GenerateAsync "weaviate.collections.queries.bm25.generate.async_._BM25GenerateAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_FetchObjectsGenerateAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.fetch_objects.html#weaviate.collections.queries.fetch_objects._FetchObjectsGenerateAsync "weaviate.collections.queries.fetch_objects.generate.async_._FetchObjectsGenerateAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_FetchObjectsByIDsGenerateAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.fetch_objects_by_ids.html#weaviate.collections.queries.fetch_objects_by_ids._FetchObjectsByIDsGenerateAsync "weaviate.collections.queries.fetch_objects_by_ids.generate.async_._FetchObjectsByIDsGenerateAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_HybridGenerateAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.hybrid.html#weaviate.collections.queries.hybrid._HybridGenerateAsync "weaviate.collections.queries.hybrid.generate.async_._HybridGenerateAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearImageGenerateAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_image.html#weaviate.collections.queries.near_image._NearImageGenerateAsync "weaviate.collections.queries.near_image.generate.async_._NearImageGenerateAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearMediaGenerateAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_media.html#weaviate.collections.queries.near_media._NearMediaGenerateAsync "weaviate.collections.queries.near_media.generate.async_._NearMediaGenerateAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearObjectGenerateAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_object.html#weaviate.collections.queries.near_object._NearObjectGenerateAsync "weaviate.collections.queries.near_object.generate.async_._NearObjectGenerateAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearTextGenerateAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_text.html#weaviate.collections.queries.near_text._NearTextGenerateAsync "weaviate.collections.queries.near_text.generate.async_._NearTextGenerateAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearVectorGenerateAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_vector.html#weaviate.collections.queries.near_vector._NearVectorGenerateAsync "weaviate.collections.queries.near_vector.generate.async_._NearVectorGenerateAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\]

Parameters:

- **connection** ( _ConnectionType_)

- **name** ( _str_)

- **consistency\_level** ( [_ConsistencyLevel_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.ConsistencyLevel "weaviate.collections.classes.config.ConsistencyLevel") _\|_ _None_)

- **tenant** ( _str_ _\|_ _None_)

- **properties** ( _Type_ _\[_ _Mapping_ _\[_ _str_ _,_ _None_ _\|_ _str_ _\|_ _bool_ _\|_ _int_ _\|_ _float_ _\|_ _datetime_ _\|_ _UUID_ _\|_ [_GeoCoordinate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.GeoCoordinate "weaviate.collections.classes.types.GeoCoordinate") _\|_ [_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.PhoneNumber "weaviate.collections.classes.types.PhoneNumber") _\|_ [_\_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._PhoneNumber "weaviate.collections.classes.types._PhoneNumber") _\|_ _Mapping_ _\[_ _str_ _,_ _WeaviateField_ _\]_ _\|_ _Sequence_ _\[_ _str_ _\]_ _\|_ _Sequence_ _\[_ _bool_ _\]_ _\|_ _Sequence_ _\[_ _int_ _\]_ _\|_ _Sequence_ _\[_ _float_ _\]_ _\|_ _Sequence_ _\[_ _datetime_ _\]_ _\|_ _Sequence_ _\[_ _UUID_ _\]_ _\|_ _Sequence_ _\[_ _Mapping_ _\[_ _str_ _,_ _WeaviateField_ _\]_ _\]_ _\]_ _\]_ _\|_ _None_)

- **references** ( _Type_ _\[_ _Mapping_ _\[_ _str_ _,_ _Any_ _\]_ _\|_ _None_ _\]_ _\|_ _None_)

- **validate\_arguments** ( _bool_)


_class_ weaviate.collections.generate.\_GenerateCollection( _connection_, _name_, _consistency\_level_, _tenant_, _properties_, _references_, _validate\_arguments_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/generate.html#_GenerateCollection) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.generate._GenerateCollection "Link to this definition")

Bases: `Generic`\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_BM25Generate`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.bm25.html#weaviate.collections.queries.bm25._BM25Generate "weaviate.collections.queries.bm25.generate.sync._BM25Generate")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_FetchObjectsGenerate`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.fetch_objects.html#weaviate.collections.queries.fetch_objects._FetchObjectsGenerate "weaviate.collections.queries.fetch_objects.generate.sync._FetchObjectsGenerate")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_FetchObjectsByIDsGenerate`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.fetch_objects_by_ids.html#weaviate.collections.queries.fetch_objects_by_ids._FetchObjectsByIDsGenerate "weaviate.collections.queries.fetch_objects_by_ids.generate.sync._FetchObjectsByIDsGenerate")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_HybridGenerate`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.hybrid.html#weaviate.collections.queries.hybrid._HybridGenerate "weaviate.collections.queries.hybrid.generate.sync._HybridGenerate")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearImageGenerate`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_image.html#weaviate.collections.queries.near_image._NearImageGenerate "weaviate.collections.queries.near_image.generate.sync._NearImageGenerate")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearMediaGenerate`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_media.html#weaviate.collections.queries.near_media._NearMediaGenerate "weaviate.collections.queries.near_media.generate.sync._NearMediaGenerate")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearObjectGenerate`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_object.html#weaviate.collections.queries.near_object._NearObjectGenerate "weaviate.collections.queries.near_object.generate.sync._NearObjectGenerate")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearTextGenerate`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_text.html#weaviate.collections.queries.near_text._NearTextGenerate "weaviate.collections.queries.near_text.generate.sync._NearTextGenerate")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearVectorGenerate`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_vector.html#weaviate.collections.queries.near_vector._NearVectorGenerate "weaviate.collections.queries.near_vector.generate.sync._NearVectorGenerate")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\]

Parameters:

- **connection** ( _ConnectionType_)

- **name** ( _str_)

- **consistency\_level** ( [_ConsistencyLevel_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.ConsistencyLevel "weaviate.collections.classes.config.ConsistencyLevel") _\|_ _None_)

- **tenant** ( _str_ _\|_ _None_)

- **properties** ( _Type_ _\[_ _Mapping_ _\[_ _str_ _,_ _None_ _\|_ _str_ _\|_ _bool_ _\|_ _int_ _\|_ _float_ _\|_ _datetime_ _\|_ _UUID_ _\|_ [_GeoCoordinate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.GeoCoordinate "weaviate.collections.classes.types.GeoCoordinate") _\|_ [_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.PhoneNumber "weaviate.collections.classes.types.PhoneNumber") _\|_ [_\_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._PhoneNumber "weaviate.collections.classes.types._PhoneNumber") _\|_ _Mapping_ _\[_ _str_ _,_ _WeaviateField_ _\]_ _\|_ _Sequence_ _\[_ _str_ _\]_ _\|_ _Sequence_ _\[_ _bool_ _\]_ _\|_ _Sequence_ _\[_ _int_ _\]_ _\|_ _Sequence_ _\[_ _float_ _\]_ _\|_ _Sequence_ _\[_ _datetime_ _\]_ _\|_ _Sequence_ _\[_ _UUID_ _\]_ _\|_ _Sequence_ _\[_ _Mapping_ _\[_ _str_ _,_ _WeaviateField_ _\]_ _\]_ _\]_ _\]_ _\|_ _None_)

- **references** ( _Type_ _\[_ _Mapping_ _\[_ _str_ _,_ _Any_ _\]_ _\|_ _None_ _\]_ _\|_ _None_)

- **validate\_arguments** ( _bool_)


### weaviate.collections.iterator [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html\#module-weaviate.collections.iterator "Link to this heading")

_class_ weaviate.collections.iterator.\_IteratorInputs( _include\_vector:bool_, _return\_metadata:List\[Literal\['creation\_time','last\_update\_time','distance','certainty','score','explain\_score','is\_consistent'\]\]\| [weaviate.collections.classes.grpc.MetadataQuery](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.MetadataQuery "weaviate.collections.classes.grpc.MetadataQuery") \|NoneType_, _return\_properties:Sequence\[str\| [weaviate.collections.classes.grpc.QueryNested](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.QueryNested "weaviate.collections.classes.grpc.QueryNested")\]\|str\| [weaviate.collections.classes.grpc.QueryNested](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.QueryNested "weaviate.collections.classes.grpc.QueryNested") \|bool\|Type\[ [TProperties](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties")\]\|NoneType_, _return\_references:[weaviate.collections.classes.grpc.\_QueryReference](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._QueryReference "weaviate.collections.classes.grpc._QueryReference") \|Sequence\[ [weaviate.collections.classes.grpc.\_QueryReference](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._QueryReference "weaviate.collections.classes.grpc._QueryReference")\]\|Type\[ [TReferences](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences")\]\|NoneType_, _after:str\|uuid.UUID\|NoneType_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/iterator.html#_IteratorInputs) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._IteratorInputs "Link to this definition")

Bases: `Generic`\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`TReferences`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences")\]

Parameters:

- **include\_vector** ( _bool_)

- **return\_metadata** ( _List_ _\[_ _Literal_ _\[_ _'creation\_time'_ _,_ _'last\_update\_time'_ _,_ _'distance'_ _,_ _'certainty'_ _,_ _'score'_ _,_ _'explain\_score'_ _,_ _'is\_consistent'_ _\]_ _\]_ _\|_ _~weaviate.collections.classes.grpc.MetadataQuery_ _\|_ _None_)

- **return\_properties** ( _Sequence_ _\[_ _str_ _\|_ [_QueryNested_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.QueryNested "weaviate.collections.classes.grpc.QueryNested") _\]_ _\|_ _str_ _\|_ [_QueryNested_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.QueryNested "weaviate.collections.classes.grpc.QueryNested") _\|_ _bool_ _\|_ _Type_ _\[_ [_TProperties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties") _\]_ _\|_ _None_)

- **return\_references** ( [_\_QueryReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._QueryReference "weaviate.collections.classes.grpc._QueryReference") _\|_ _Sequence_ _\[_ [_\_QueryReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._QueryReference "weaviate.collections.classes.grpc._QueryReference") _\]_ _\|_ _Type_ _\[_ [_TReferences_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences") _\]_ _\|_ _None_)

- **after** ( _str_ _\|_ _UUID_ _\|_ _None_)


include\_vector _:bool_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._IteratorInputs.include_vector "Link to this definition")return\_metadata _:List\[Literal\['creation\_time','last\_update\_time','distance','certainty','score','explain\_score','is\_consistent'\]\]\| [MetadataQuery](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.MetadataQuery "weaviate.collections.classes.grpc.MetadataQuery") \|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._IteratorInputs.return_metadata "Link to this definition")return\_properties _:Sequence\[str\| [QueryNested](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.QueryNested "weaviate.collections.classes.grpc.QueryNested")\]\|str\| [QueryNested](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.QueryNested "weaviate.collections.classes.grpc.QueryNested") \|bool\|Type\[ [TProperties](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties")\]\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._IteratorInputs.return_properties "Link to this definition")return\_references _: [\_QueryReference](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._QueryReference "weaviate.collections.classes.grpc._QueryReference") \|Sequence\[ [\_QueryReference](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._QueryReference "weaviate.collections.classes.grpc._QueryReference")\]\|Type\[ [TReferences](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences")\]\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._IteratorInputs.return_references "Link to this definition")after _:str\|UUID\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._IteratorInputs.after "Link to this definition")weaviate.collections.iterator.\_parse\_after( _after_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/iterator.html#_parse_after) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._parse_after "Link to this definition")Parameters:

**after** ( _str_ _\|_ _UUID_ _\|_ _None_)

Return type:

_UUID_ \| None

_class_ weaviate.collections.iterator.\_ObjectIterator( _query_, _inputs_, _cache\_size=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/iterator.html#_ObjectIterator) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectIterator "Link to this definition")

Bases: `Generic`\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`TReferences`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences")\], `Iterable`\[ [`Object`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.Object "weaviate.collections.classes.internal.Object")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`TReferences`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences")\]\]

Parameters:

- **query** ( [_\_FetchObjectsQuery_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.fetch_objects.html#weaviate.collections.queries.fetch_objects._FetchObjectsQuery "weaviate.collections.queries.fetch_objects.query.sync._FetchObjectsQuery") _\[_ _Any_ _,_ _Any_ _\]_)

- **inputs** ( [_\_IteratorInputs_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._IteratorInputs "weaviate.collections.iterator._IteratorInputs") _\[_ [_TProperties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties") _,_ [_TReferences_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences") _\]_)

- **cache\_size** ( _int_ _\|_ _None_)


\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectIterator._abc_impl "Link to this definition")_class_ weaviate.collections.iterator.\_ObjectAIterator( _query_, _inputs_, _cache\_size=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/iterator.html#_ObjectAIterator) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectAIterator "Link to this definition")

Bases: `Generic`\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`TReferences`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences")\], `AsyncIterable`\[ [`Object`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.Object "weaviate.collections.classes.internal.Object")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`TReferences`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences")\]\]

Parameters:

- **query** ( [_\_FetchObjectsQueryAsync_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.fetch_objects.html#weaviate.collections.queries.fetch_objects._FetchObjectsQueryAsync "weaviate.collections.queries.fetch_objects.query.async_._FetchObjectsQueryAsync") _\[_ _Any_ _,_ _Any_ _\]_)

- **inputs** ( [_\_IteratorInputs_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._IteratorInputs "weaviate.collections.iterator._IteratorInputs") _\[_ [_TProperties_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties") _,_ [_TReferences_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TReferences "weaviate.collections.classes.types.TReferences") _\]_)

- **cache\_size** ( _int_ _\|_ _None_)


\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.iterator._ObjectAIterator._abc_impl "Link to this definition")

### weaviate.collections.orm [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html\#module-weaviate.collections.orm "Link to this heading")

### weaviate.collections.query [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html\#module-weaviate.collections.query "Link to this heading")

_class_ weaviate.collections.query.\_QueryCollectionAsync( _connection_, _name_, _consistency\_level_, _tenant_, _properties_, _references_, _validate\_arguments_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/query.html#_QueryCollectionAsync) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.query._QueryCollectionAsync "Link to this definition")

Bases: `Generic`\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_BM25QueryAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.bm25.html#weaviate.collections.queries.bm25._BM25QueryAsync "weaviate.collections.queries.bm25.query.async_._BM25QueryAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_FetchObjectByIDQueryAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.fetch_object_by_id.html#weaviate.collections.queries.fetch_object_by_id._FetchObjectByIDQueryAsync "weaviate.collections.queries.fetch_object_by_id.async_._FetchObjectByIDQueryAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_FetchObjectsByIDsQueryAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.fetch_objects_by_ids.html#weaviate.collections.queries.fetch_objects_by_ids._FetchObjectsByIDsQueryAsync "weaviate.collections.queries.fetch_objects_by_ids.query.async_._FetchObjectsByIDsQueryAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_FetchObjectsQueryAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.fetch_objects.html#weaviate.collections.queries.fetch_objects._FetchObjectsQueryAsync "weaviate.collections.queries.fetch_objects.query.async_._FetchObjectsQueryAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_HybridQueryAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.hybrid.html#weaviate.collections.queries.hybrid._HybridQueryAsync "weaviate.collections.queries.hybrid.query.async_._HybridQueryAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearImageQueryAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_image.html#weaviate.collections.queries.near_image._NearImageQueryAsync "weaviate.collections.queries.near_image.query.async_._NearImageQueryAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearMediaQueryAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_media.html#weaviate.collections.queries.near_media._NearMediaQueryAsync "weaviate.collections.queries.near_media.query.async_._NearMediaQueryAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearObjectQueryAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_object.html#weaviate.collections.queries.near_object._NearObjectQueryAsync "weaviate.collections.queries.near_object.query.async_._NearObjectQueryAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearTextQueryAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_text.html#weaviate.collections.queries.near_text._NearTextQueryAsync "weaviate.collections.queries.near_text.query.async_._NearTextQueryAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearVectorQueryAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_vector.html#weaviate.collections.queries.near_vector._NearVectorQueryAsync "weaviate.collections.queries.near_vector.query.async_._NearVectorQueryAsync")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\]

Parameters:

- **connection** ( _ConnectionType_)

- **name** ( _str_)

- **consistency\_level** ( [_ConsistencyLevel_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.ConsistencyLevel "weaviate.collections.classes.config.ConsistencyLevel") _\|_ _None_)

- **tenant** ( _str_ _\|_ _None_)

- **properties** ( _Type_ _\[_ _Mapping_ _\[_ _str_ _,_ _None_ _\|_ _str_ _\|_ _bool_ _\|_ _int_ _\|_ _float_ _\|_ _datetime_ _\|_ _UUID_ _\|_ [_GeoCoordinate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.GeoCoordinate "weaviate.collections.classes.types.GeoCoordinate") _\|_ [_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.PhoneNumber "weaviate.collections.classes.types.PhoneNumber") _\|_ [_\_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._PhoneNumber "weaviate.collections.classes.types._PhoneNumber") _\|_ _Mapping_ _\[_ _str_ _,_ _WeaviateField_ _\]_ _\|_ _Sequence_ _\[_ _str_ _\]_ _\|_ _Sequence_ _\[_ _bool_ _\]_ _\|_ _Sequence_ _\[_ _int_ _\]_ _\|_ _Sequence_ _\[_ _float_ _\]_ _\|_ _Sequence_ _\[_ _datetime_ _\]_ _\|_ _Sequence_ _\[_ _UUID_ _\]_ _\|_ _Sequence_ _\[_ _Mapping_ _\[_ _str_ _,_ _WeaviateField_ _\]_ _\]_ _\]_ _\]_ _\|_ _None_)

- **references** ( _Type_ _\[_ _Mapping_ _\[_ _str_ _,_ _Any_ _\]_ _\|_ _None_ _\]_ _\|_ _None_)

- **validate\_arguments** ( _bool_)


_class_ weaviate.collections.query.\_QueryCollection( _connection_, _name_, _consistency\_level_, _tenant_, _properties_, _references_, _validate\_arguments_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/query.html#_QueryCollection) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.query._QueryCollection "Link to this definition")

Bases: `Generic`\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_BM25Query`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.bm25.html#weaviate.collections.queries.bm25._BM25Query "weaviate.collections.queries.bm25.query.sync._BM25Query")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_FetchObjectByIDQuery`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.fetch_object_by_id.html#weaviate.collections.queries.fetch_object_by_id._FetchObjectByIDQuery "weaviate.collections.queries.fetch_object_by_id.sync._FetchObjectByIDQuery")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_FetchObjectsByIDsQuery`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.fetch_objects_by_ids.html#weaviate.collections.queries.fetch_objects_by_ids._FetchObjectsByIDsQuery "weaviate.collections.queries.fetch_objects_by_ids.query.sync._FetchObjectsByIDsQuery")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_FetchObjectsQuery`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.fetch_objects.html#weaviate.collections.queries.fetch_objects._FetchObjectsQuery "weaviate.collections.queries.fetch_objects.query.sync._FetchObjectsQuery")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_HybridQuery`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.hybrid.html#weaviate.collections.queries.hybrid._HybridQuery "weaviate.collections.queries.hybrid.query.sync._HybridQuery")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearImageQuery`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_image.html#weaviate.collections.queries.near_image._NearImageQuery "weaviate.collections.queries.near_image.query.sync._NearImageQuery")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearMediaQuery`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_media.html#weaviate.collections.queries.near_media._NearMediaQuery "weaviate.collections.queries.near_media.query.sync._NearMediaQuery")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearObjectQuery`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_object.html#weaviate.collections.queries.near_object._NearObjectQuery "weaviate.collections.queries.near_object.query.sync._NearObjectQuery")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearTextQuery`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_text.html#weaviate.collections.queries.near_text._NearTextQuery "weaviate.collections.queries.near_text.query.sync._NearTextQuery")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\], [`_NearVectorQuery`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.queries.near_vector.html#weaviate.collections.queries.near_vector._NearVectorQuery "weaviate.collections.queries.near_vector.query.sync._NearVectorQuery")\[ [`TProperties`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.TProperties "weaviate.collections.classes.types.TProperties"), [`References`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.References "weaviate.collections.classes.types.References")\]

Parameters:

- **connection** ( _ConnectionType_)

- **name** ( _str_)

- **consistency\_level** ( [_ConsistencyLevel_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config.ConsistencyLevel "weaviate.collections.classes.config.ConsistencyLevel") _\|_ _None_)

- **tenant** ( _str_ _\|_ _None_)

- **properties** ( _Type_ _\[_ _Mapping_ _\[_ _str_ _,_ _None_ _\|_ _str_ _\|_ _bool_ _\|_ _int_ _\|_ _float_ _\|_ _datetime_ _\|_ _UUID_ _\|_ [_GeoCoordinate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.GeoCoordinate "weaviate.collections.classes.types.GeoCoordinate") _\|_ [_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.PhoneNumber "weaviate.collections.classes.types.PhoneNumber") _\|_ [_\_PhoneNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._PhoneNumber "weaviate.collections.classes.types._PhoneNumber") _\|_ _Mapping_ _\[_ _str_ _,_ _WeaviateField_ _\]_ _\|_ _Sequence_ _\[_ _str_ _\]_ _\|_ _Sequence_ _\[_ _bool_ _\]_ _\|_ _Sequence_ _\[_ _int_ _\]_ _\|_ _Sequence_ _\[_ _float_ _\]_ _\|_ _Sequence_ _\[_ _datetime_ _\]_ _\|_ _Sequence_ _\[_ _UUID_ _\]_ _\|_ _Sequence_ _\[_ _Mapping_ _\[_ _str_ _,_ _WeaviateField_ _\]_ _\]_ _\]_ _\]_ _\|_ _None_)

- **references** ( _Type_ _\[_ _Mapping_ _\[_ _str_ _,_ _Any_ _\]_ _\|_ _None_ _\]_ _\|_ _None_)

- **validate\_arguments** ( _bool_)


Versions[latest](https://weaviate-python-client.readthedocs.io/en/latest/weaviate.collections.html)**[stable](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html)**[v4.16.10](https://weaviate-python-client.readthedocs.io/en/v4.16.10/weaviate.collections.html)[v4.16.9](https://weaviate-python-client.readthedocs.io/en/v4.16.9/weaviate.collections.html)[v4.16.8](https://weaviate-python-client.readthedocs.io/en/v4.16.8/weaviate.collections.html)[v4.16.7](https://weaviate-python-client.readthedocs.io/en/v4.16.7/weaviate.collections.html)[v4.16.6](https://weaviate-python-client.readthedocs.io/en/v4.16.6/weaviate.collections.html)[v4.16.5](https://weaviate-python-client.readthedocs.io/en/v4.16.5/weaviate.collections.html)[v4.16.4](https://weaviate-python-client.readthedocs.io/en/v4.16.4/weaviate.collections.html)[v4.16.3](https://weaviate-python-client.readthedocs.io/en/v4.16.3/weaviate.collections.html)[v4.16.2](https://weaviate-python-client.readthedocs.io/en/v4.16.2/weaviate.collections.html)[v4.16.1](https://weaviate-python-client.readthedocs.io/en/v4.16.1/weaviate.collections.html)[v4.16.0](https://weaviate-python-client.readthedocs.io/en/v4.16.0/weaviate.collections.html)[v4.15.4](https://weaviate-python-client.readthedocs.io/en/v4.15.4/weaviate.collections.html)[v4.15.3](https://weaviate-python-client.readthedocs.io/en/v4.15.3/weaviate.collections.html)[v4.15.2](https://weaviate-python-client.readthedocs.io/en/v4.15.2/weaviate.collections.html)[v4.15.1](https://weaviate-python-client.readthedocs.io/en/v4.15.1/weaviate.collections.html)[v4.15.0](https://weaviate-python-client.readthedocs.io/en/v4.15.0/weaviate.collections.html)[v4.14.4](https://weaviate-python-client.readthedocs.io/en/v4.14.4/weaviate.collections.html)[v4.14.3](https://weaviate-python-client.readthedocs.io/en/v4.14.3/weaviate.collections.html)[v4.14.2](https://weaviate-python-client.readthedocs.io/en/v4.14.2/weaviate.collections.html)[v4.14.1](https://weaviate-python-client.readthedocs.io/en/v4.14.1/weaviate.collections.html)[v4.14.0](https://weaviate-python-client.readthedocs.io/en/v4.14.0/weaviate.collections.html)[v4.13.2](https://weaviate-python-client.readthedocs.io/en/v4.13.2/weaviate.collections.html)[v4.13.1](https://weaviate-python-client.readthedocs.io/en/v4.13.1/weaviate.collections.html)[v4.13.0](https://weaviate-python-client.readthedocs.io/en/v4.13.0/weaviate.collections.html)[v4.12.1](https://weaviate-python-client.readthedocs.io/en/v4.12.1/weaviate.collections.html)[v4.12.0](https://weaviate-python-client.readthedocs.io/en/v4.12.0/weaviate.collections.html)[v4.11.3](https://weaviate-python-client.readthedocs.io/en/v4.11.3/weaviate.collections.html)[v4.11.2](https://weaviate-python-client.readthedocs.io/en/v4.11.2/weaviate.collections.html)[v4.11.1](https://weaviate-python-client.readthedocs.io/en/v4.11.1/weaviate.collections.html)[v4.11.0](https://weaviate-python-client.readthedocs.io/en/v4.11.0/weaviate.collections.html)[v4.10.4](https://weaviate-python-client.readthedocs.io/en/v4.10.4/weaviate.collections.html)[v4.10.3](https://weaviate-python-client.readthedocs.io/en/v4.10.3/weaviate.collections.html)[v4.10.2](https://weaviate-python-client.readthedocs.io/en/v4.10.2/weaviate.collections.html)[v4.10.0](https://weaviate-python-client.readthedocs.io/en/v4.10.0/weaviate.collections.html)[v4.9.6](https://weaviate-python-client.readthedocs.io/en/v4.9.6/weaviate.collections.html)[v4.9.5](https://weaviate-python-client.readthedocs.io/en/v4.9.5/weaviate.collections.html)[v4.9.4](https://weaviate-python-client.readthedocs.io/en/v4.9.4/weaviate.collections.html)[v4.9.3](https://weaviate-python-client.readthedocs.io/en/v4.9.3/weaviate.collections.html)[v4.9.2](https://weaviate-python-client.readthedocs.io/en/v4.9.2/weaviate.collections.html)[v4.9.1](https://weaviate-python-client.readthedocs.io/en/v4.9.1/weaviate.collections.html)[v4.9.0](https://weaviate-python-client.readthedocs.io/en/v4.9.0/weaviate.collections.html)[v4.8.1](https://weaviate-python-client.readthedocs.io/en/v4.8.1/weaviate.collections.html)[v4.8.0](https://weaviate-python-client.readthedocs.io/en/v4.8.0/weaviate.collections.html)[v4.7.1](https://weaviate-python-client.readthedocs.io/en/v4.7.1/weaviate.collections.html)[v4.7.0](https://weaviate-python-client.readthedocs.io/en/v4.7.0/weaviate.collections.html)[v4.6.7](https://weaviate-python-client.readthedocs.io/en/v4.6.7/weaviate.collections.html)[v4.6.6](https://weaviate-python-client.readthedocs.io/en/v4.6.6/weaviate.collections.html)[v4.6.5](https://weaviate-python-client.readthedocs.io/en/v4.6.5/weaviate.collections.html)[v4.6.4](https://weaviate-python-client.readthedocs.io/en/v4.6.4/weaviate.collections.html)[v4.6.3](https://weaviate-python-client.readthedocs.io/en/v4.6.3/weaviate.collections.html)[v4.6.2](https://weaviate-python-client.readthedocs.io/en/v4.6.2/weaviate.collections.html)[v4.6.1](https://weaviate-python-client.readthedocs.io/en/v4.6.1/weaviate.collections.html)[v4.6.0](https://weaviate-python-client.readthedocs.io/en/v4.6.0/weaviate.collections.html)[v4.5.7](https://weaviate-python-client.readthedocs.io/en/v4.5.7/weaviate.collections.html)[v4.5.6](https://weaviate-python-client.readthedocs.io/en/v4.5.6/weaviate.collections.html)[v4.5.5](https://weaviate-python-client.readthedocs.io/en/v4.5.5/weaviate.collections.html)[v4.5.4](https://weaviate-python-client.readthedocs.io/en/v4.5.4/weaviate.collections.html)[v4.5.3](https://weaviate-python-client.readthedocs.io/en/v4.5.3/weaviate.collections.html)[v4.5.2](https://weaviate-python-client.readthedocs.io/en/v4.5.2/weaviate.collections.html)[v4.5.1](https://weaviate-python-client.readthedocs.io/en/v4.5.1/weaviate.collections.html)[v4.5.0](https://weaviate-python-client.readthedocs.io/en/v4.5.0/weaviate.collections.html)[v4.4.4](https://weaviate-python-client.readthedocs.io/en/v4.4.4/weaviate.collections.html)[v4.4.3](https://weaviate-python-client.readthedocs.io/en/v4.4.3/weaviate.collections.html)[v4.4.2](https://weaviate-python-client.readthedocs.io/en/v4.4.2/weaviate.collections.html)[v4.4.1](https://weaviate-python-client.readthedocs.io/en/v4.4.1/weaviate.collections.html)[v4.4.0](https://weaviate-python-client.readthedocs.io/en/v4.4.0/weaviate.collections.html)[v3.26.2](https://weaviate-python-client.readthedocs.io/en/v3.26.2/weaviate.collections.html)[v3.26.1](https://weaviate-python-client.readthedocs.io/en/v3.26.1/weaviate.collections.html)[v3.26.0](https://weaviate-python-client.readthedocs.io/en/v3.26.0/weaviate.collections.html)[v3.25.3](https://weaviate-python-client.readthedocs.io/en/v3.25.3/weaviate.collections.html)[v3.25.2](https://weaviate-python-client.readthedocs.io/en/v3.25.2/weaviate.collections.html)[v3.23.0](https://weaviate-python-client.readthedocs.io/en/v3.23.0/weaviate.collections.html)[v3.22.1](https://weaviate-python-client.readthedocs.io/en/v3.22.1/weaviate.collections.html)[v3.22.0](https://weaviate-python-client.readthedocs.io/en/v3.22.0/weaviate.collections.html)[v3.21.0](https://weaviate-python-client.readthedocs.io/en/v3.21.0/weaviate.collections.html)[v3.20.1](https://weaviate-python-client.readthedocs.io/en/v3.20.1/weaviate.collections.html)[v3.20.0](https://weaviate-python-client.readthedocs.io/en/v3.20.0/weaviate.collections.html)[v3.19.2](https://weaviate-python-client.readthedocs.io/en/v3.19.2/weaviate.collections.html)[v3.19.1](https://weaviate-python-client.readthedocs.io/en/v3.19.1/weaviate.collections.html)[v3.19.0](https://weaviate-python-client.readthedocs.io/en/v3.19.0/weaviate.collections.html)[v3.18.0](https://weaviate-python-client.readthedocs.io/en/v3.18.0/weaviate.collections.html)[v3.15.6](https://weaviate-python-client.readthedocs.io/en/v3.15.6/weaviate.collections.html)[v3.15.5](https://weaviate-python-client.readthedocs.io/en/v3.15.5/weaviate.collections.html)[v3.15.4](https://weaviate-python-client.readthedocs.io/en/v3.15.4/weaviate.collections.html)[v3.15.3](https://weaviate-python-client.readthedocs.io/en/v3.15.3/weaviate.collections.html)[v3.15.2](https://weaviate-python-client.readthedocs.io/en/v3.15.2/weaviate.collections.html)[v3.15.1](https://weaviate-python-client.readthedocs.io/en/v3.15.1/weaviate.collections.html)[v3.15.0](https://weaviate-python-client.readthedocs.io/en/v3.15.0/weaviate.collections.html)[v3.14.0](https://weaviate-python-client.readthedocs.io/en/v3.14.0/weaviate.collections.html)[v3.13.0](https://weaviate-python-client.readthedocs.io/en/v3.13.0/weaviate.collections.html)[v3.12.0\_a](https://weaviate-python-client.readthedocs.io/en/v3.12.0_a/weaviate.collections.html)[v3.11.0](https://weaviate-python-client.readthedocs.io/en/v3.11.0/weaviate.collections.html)[v3.10.0](https://weaviate-python-client.readthedocs.io/en/v3.10.0/weaviate.collections.html)[v3.9.0](https://weaviate-python-client.readthedocs.io/en/v3.9.0/weaviate.collections.html)[v3.8.0](https://weaviate-python-client.readthedocs.io/en/v3.8.0/weaviate.collections.html)[v3.7.0](https://weaviate-python-client.readthedocs.io/en/v3.7.0/weaviate.collections.html)[v3.6.0](https://weaviate-python-client.readthedocs.io/en/v3.6.0/weaviate.collections.html)[v3.5.1](https://weaviate-python-client.readthedocs.io/en/v3.5.1/weaviate.collections.html)[v3.5.0](https://weaviate-python-client.readthedocs.io/en/v3.5.0/weaviate.collections.html)[v3.4.1](https://weaviate-python-client.readthedocs.io/en/v3.4.1/weaviate.collections.html)[v3.4.0](https://weaviate-python-client.readthedocs.io/en/v3.4.0/weaviate.collections.html)[v3.3.3](https://weaviate-python-client.readthedocs.io/en/v3.3.3/weaviate.collections.html)[v3.3.2](https://weaviate-python-client.readthedocs.io/en/v3.3.2/weaviate.collections.html)[v3.3.1](https://weaviate-python-client.readthedocs.io/en/v3.3.1/weaviate.collections.html)[v3.3.0](https://weaviate-python-client.readthedocs.io/en/v3.3.0/weaviate.collections.html)[v3.2.5](https://weaviate-python-client.readthedocs.io/en/v3.2.5/weaviate.collections.html)[v3.2.4](https://weaviate-python-client.readthedocs.io/en/v3.2.4/weaviate.collections.html)[v3.2.3](https://weaviate-python-client.readthedocs.io/en/v3.2.3/weaviate.collections.html)[v3.2.2](https://weaviate-python-client.readthedocs.io/en/v3.2.2/weaviate.collections.html)[v3.2.1](https://weaviate-python-client.readthedocs.io/en/v3.2.1/weaviate.collections.html)[v3.2.0](https://weaviate-python-client.readthedocs.io/en/v3.2.0/weaviate.collections.html)[v3.1.1](https://weaviate-python-client.readthedocs.io/en/v3.1.1/weaviate.collections.html)[v3.1.0](https://weaviate-python-client.readthedocs.io/en/v3.1.0/weaviate.collections.html)[v3.0.0](https://weaviate-python-client.readthedocs.io/en/v3.0.0/weaviate.collections.html)On Read the Docs[Project Home](https://app.readthedocs.org/projects/weaviate-python-client/?utm_source=weaviate-python-client&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/weaviate-python-client/builds/?utm_source=weaviate-python-client&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=weaviate-python-client&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=weaviate-python-client&utm_content=flyout)