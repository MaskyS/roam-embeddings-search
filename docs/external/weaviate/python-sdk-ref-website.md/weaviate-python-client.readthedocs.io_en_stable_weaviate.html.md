---
url: "https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html"
title: "weaviate — Weaviate Python Client 4.16.10 documentation"
---

- [Home](https://weaviate-python-client.readthedocs.io/en/stable/index.html)
- [Weaviate Library](https://weaviate-python-client.readthedocs.io/en/stable/modules.html)
- weaviate
- [View page source](https://weaviate-python-client.readthedocs.io/en/stable/_sources/weaviate.rst.txt)

* * *

# weaviate [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html\#module-weaviate "Link to this heading")

Weaviate Python Client Library used to interact with a Weaviate instance.

_class_ weaviate.WeaviateClient( _connection\_params=None_, _embedded\_options=None_, _auth\_client\_secret=None_, _additional\_headers=None_, _additional\_config=None_, _skip\_init\_checks=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/client.html#WeaviateClient) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient "Link to this definition")

The v4 Python-native Weaviate Client class that encapsulates Weaviate functionalities in one object.

WARNING: This client is only compatible with Weaviate v1.23.6 and higher!

A Client instance creates all the needed objects to interact with Weaviate, and connects all of
them to the same Weaviate instance. See below the Attributes of the Client instance. For the
per attribute functionality see that attribute’s documentation.

backup [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient.backup "Link to this definition")

Backup object instance connected to the same Weaviate instance as the Client.
This namespace contains all the functionality to upload data in batches to Weaviate for all collections and tenants.

Type:

[\_Backup](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup._Backup "weaviate.backup._Backup")

batch [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient.batch "Link to this definition")

BatchClient object instance connected to the same Weaviate instance as the Client.
This namespace contains all functionality to backup data.

Type:

[\_BatchClientWrapper](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.batch.html#weaviate.collections.batch.client._BatchClientWrapper "weaviate.collections.batch.client._BatchClientWrapper")

cluster [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient.cluster "Link to this definition")

Cluster object instance connected to the same Weaviate instance as the Client.
This namespace contains all functionality to inspect the connected Weaviate cluster.

Type:

[\_Cluster](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.cluster.html#weaviate.cluster._Cluster "weaviate.cluster._Cluster")

collections [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient.collections "Link to this definition")

Collections object instance connected to the same Weaviate instance as the Client.
This namespace contains all the functionality to manage Weaviate data collections. It is your main entry point for all
collection-related functionality. Use it to retrieve collection objects using client.collections.get(“MyCollection”)
or to create new collections using client.collections.create(“MyCollection”, …).

Type:

[\_Collections](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.collections.html#weaviate.collections.collections._Collections "weaviate.collections.collections._Collections")

debug [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient.debug "Link to this definition")

Debug object instance connected to the same Weaviate instance as the Client.
This namespace contains functionality used to debug Weaviate clusters. As such, it is deemed experimental and is subject to change.
We can make no guarantees about the stability of this namespace nor the potential for future breaking changes. Use at your own risk.

Type:

[\_Debug](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.debug.html#weaviate.debug._Debug "weaviate.debug._Debug")

roles [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient.roles "Link to this definition")

Roles object instance connected to the same Weaviate instance as the Client.
This namespace contains all functionality to manage Weaviate’s RBAC functionality.

Type:

[\_Roles](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac._Roles "weaviate.rbac._Roles")

users [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient.users "Link to this definition")

Users object instance connected to the same Weaviate instance as the Client.
This namespace contains all functionality to manage Weaviate users.

Type:

[\_Users](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.users.html#weaviate.users._Users "weaviate.users._Users")

Initialise a WeaviateClient class instance to use when interacting with Weaviate.

Use this specific initializer when you want to create a custom Client specific to your Weaviate setup.

To simplify connections to Weaviate Cloud or local instances, use the [`weaviate.connect_to_weaviate_cloud()`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.connect_to_weaviate_cloud "weaviate.connect_to_weaviate_cloud")
or [`weaviate.connect_to_local()`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.connect_to_local "weaviate.connect_to_local") helper functions.

Parameters:

- **connection\_params** ( [_ConnectionParams_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ConnectionParams "weaviate.connect.base.ConnectionParams") _\|_ _None_) – The connection parameters to use for the underlying HTTP requests.

- **embedded\_options** ( [_EmbeddedOptions_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedOptions "weaviate.embedded.EmbeddedOptions") _\|_ _None_) – The options to use when provisioning an embedded Weaviate instance.

- **auth\_client\_secret** ( [_\_BearerToken_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._BearerToken "weaviate.auth._BearerToken") _\|_ [_\_ClientPassword_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") _\|_ [_\_ClientCredentials_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") _\|_ [_\_APIKey_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._APIKey "weaviate.auth._APIKey") _\|_ _None_) – Authenticate to weaviate by using one of the given authentication modes:
\- weaviate.auth.AuthBearerToken to use existing access and (optionally, but recommended) refresh tokens
\- weaviate.auth.AuthClientPassword to use username and password for oidc Resource Owner Password flow
\- weaviate.auth.AuthClientCredentials to use a client secret for oidc client credential flow

- **additional\_headers** ( _dict_ _\|_ _None_) – Additional headers to include in the requests. Can be used to set OpenAI/HuggingFace/Cohere etc. keys.
[Here](https://weaviate.io/developers/weaviate/modules/reader-generator-modules/generative-openai#providing-the-key-to-weaviate) is an
example of how to set API keys within this parameter.

- **additional\_config** ( [_AdditionalConfig_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") _\|_ _None_) – Additional and advanced configuration options for Weaviate.

- **skip\_init\_checks** ( _bool_) – If set to True then the client will not perform any checks including ensuring that weaviate has started.
This is useful for air-gapped environments and high-performance setups.


close() [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient.close "Link to this definition")

In order to clean up any resources used by the client, call this method when you are done with it.

If you do not do this, memory leaks may occur due to stale connections.
This method also closes the embedded database if one was started.

Return type:

None \| _Awaitable_\[None\]

connect() [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient.connect "Link to this definition")

Connect to the Weaviate instance performing all the necessary checks.

If you have specified skip\_init\_checks in the constructor then this method will not perform any runtime checks
to ensure that Weaviate is running and ready to accept requests. This is useful for air-gapped environments and high-performance setups.

This method is idempotent and will only perform the checks once. Any subsequent calls do nothing while client.is\_connected() == True.

Raises:

- [**WeaviateConnectionError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateConnectionError "weaviate.exceptions.WeaviateConnectionError") – If the network connection to weaviate fails.

- [**UnexpectedStatusCodeError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If weaviate reports a none OK status.


Return type:

None \| _Awaitable_\[None\]

get\_meta() [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient.get_meta "Link to this definition")

Get the meta endpoint description of weaviate.

Returns:

The dict describing the weaviate configuration.

Raises:

[**UnexpectedStatusCodeError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If Weaviate reports a none OK status.

Return type:

dict \| _Awaitable_\[dict\]

get\_open\_id\_configuration() [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient.get_open_id_configuration "Link to this definition")

Get the openid-configuration.

Returns:

The configuration or None if not configured.

Raises:

[**UnexpectedStatusCodeError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If Weaviate reports a none OK status.

Return type:

_Dict_\[str, _Any_\] \| None \| _Awaitable_\[ _Dict_\[str, _Any_\] \| None\]

graphql\_raw\_query( _gql\_query_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient.graphql_raw_query "Link to this definition")

Allows to send graphQL string queries, this should only be used for weaviate-features that are not yet supported.

Be cautious of injection risks when generating query strings.

Parameters:

**gql\_query** ( _str_) – GraphQL query as a string.

Returns:

A dict with the response from the GraphQL query.

Raises:

- **TypeError** – If gql\_query is not of type str.

- [**WeaviateConnectionError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateConnectionError "weaviate.exceptions.WeaviateConnectionError") – If the network connection to weaviate fails.

- [**UnexpectedStatusCodeError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If weaviate reports a none OK status.


Return type:

[_\_RawGQLReturn_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal._RawGQLReturn "weaviate.collections.classes.internal._RawGQLReturn") \| _Awaitable_\[ [_\_RawGQLReturn_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal._RawGQLReturn "weaviate.collections.classes.internal._RawGQLReturn")\]

is\_connected() [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient.is_connected "Link to this definition")

Check if the client is connected to Weaviate.

Returns:

True if the client is connected to Weaviate with an open connection pool, False otherwise.

Return type:

bool

is\_live() [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient.is_live "Link to this definition")Return type:

bool \| _Awaitable_\[bool\]

is\_ready() [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient.is_ready "Link to this definition")Return type:

bool \| _Awaitable_\[bool\]

_class_ weaviate.WeaviateAsyncClient( _connection\_params=None_, _embedded\_options=None_, _auth\_client\_secret=None_, _additional\_headers=None_, _additional\_config=None_, _skip\_init\_checks=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/client.html#WeaviateAsyncClient) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient "Link to this definition")

The v4 Python-native Weaviate Client class that encapsulates Weaviate functionalities in one object.

WARNING: This client is only compatible with Weaviate v1.23.6 and higher!

A Client instance creates all the needed objects to interact with Weaviate, and connects all of
them to the same Weaviate instance. See below the Attributes of the Client instance. For the
per attribute functionality see that attribute’s documentation.

backup [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient.backup "Link to this definition")

Backup object instance connected to the same Weaviate instance as the Client.
This namespace contains all the functionality to upload data in batches to Weaviate for all collections and tenants.

Type:

[\_BackupAsync](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup._BackupAsync "weaviate.backup._BackupAsync")

cluster [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient.cluster "Link to this definition")

Cluster object instance connected to the same Weaviate instance as the Client.
This namespace contains all functionality to inspect the connected Weaviate cluster.

Type:

[\_ClusterAsync](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.cluster.html#weaviate.cluster._ClusterAsync "weaviate.cluster._ClusterAsync")

collections [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient.collections "Link to this definition")

Collections object instance connected to the same Weaviate instance as the Client.
This namespace contains all the functionality to manage Weaviate data collections. It is your main entry point for all
collection-related functionality. Use it to retrieve collection objects using client.collections.get(“MyCollection”)
or to create new collections using client.collections.create(“MyCollection”, …).

Type:

[\_CollectionsAsync](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.collections.html#weaviate.collections.collections._CollectionsAsync "weaviate.collections.collections._CollectionsAsync")

debug [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient.debug "Link to this definition")

Debug object instance connected to the same Weaviate instance as the Client.
This namespace contains functionality used to debug Weaviate clusters. As such, it is deemed experimental and is subject to change.
We can make no guarantees about the stability of this namespace nor the potential for future breaking changes. Use at your own risk.

Type:

[\_DebugAsync](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.debug.html#weaviate.debug._DebugAsync "weaviate.debug._DebugAsync")

roles [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient.roles "Link to this definition")

Roles object instance connected to the same Weaviate instance as the Client.
This namespace contains all functionality to manage Weaviate’s RBAC functionality.

Type:

[\_RolesAsync](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac._RolesAsync "weaviate.rbac._RolesAsync")

users [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient.users "Link to this definition")

Users object instance connected to the same Weaviate instance as the Client.
This namespace contains all functionality to manage Weaviate users.

Type:

[\_UsersAsync](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.users.html#weaviate.users._UsersAsync "weaviate.users._UsersAsync")

Initialise a WeaviateAsyncClient class instance to use when interacting with Weaviate.

Use this specific initializer when you want to create a custom Client specific to your Weaviate setup.

To simplify connections to Weaviate Cloud or local instances, use the [`weaviate.use_async_with_weaviate_cloud()`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.use_async_with_weaviate_cloud "weaviate.use_async_with_weaviate_cloud")
or [`weaviate.use_async_with_local()`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.use_async_with_local "weaviate.use_async_with_local") helper functions.

Parameters:

- **connection\_params** ( [_ConnectionParams_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ConnectionParams "weaviate.connect.base.ConnectionParams") _\|_ _None_) – The connection parameters to use for the underlying HTTP requests.

- **embedded\_options** ( [_EmbeddedOptions_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedOptions "weaviate.embedded.EmbeddedOptions") _\|_ _None_) – The options to use when provisioning an embedded Weaviate instance.

- **auth\_client\_secret** ( [_\_BearerToken_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._BearerToken "weaviate.auth._BearerToken") _\|_ [_\_ClientPassword_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") _\|_ [_\_ClientCredentials_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") _\|_ [_\_APIKey_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._APIKey "weaviate.auth._APIKey") _\|_ _None_) – Authenticate to weaviate by using one of the given authentication modes:
\- weaviate.auth.AuthBearerToken to use existing access and (optionally, but recommended) refresh tokens
\- weaviate.auth.AuthClientPassword to use username and password for oidc Resource Owner Password flow
\- weaviate.auth.AuthClientCredentials to use a client secret for oidc client credential flow

- **additional\_headers** ( _dict_ _\|_ _None_) –

Additional headers to include in the requests. Can be used to set OpenAI/HuggingFace/Cohere etc. keys.
[Here](https://weaviate.io/developers/weaviate/modules/reader-generator-modules/generative-openai#providing-the-key-to-weaviate) is an
example of how to set API keys within this parameter.

- **additional\_config** ( [_AdditionalConfig_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") _\|_ _None_) – Additional and advanced configuration options for Weaviate.

- **skip\_init\_checks** ( _bool_) – If set to True then the client will not perform any checks including ensuring that weaviate has started.
This is useful for air-gapped environments and high-performance setups.


close() [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient.close "Link to this definition")

In order to clean up any resources used by the client, call this method when you are done with it.

If you do not do this, memory leaks may occur due to stale connections.
This method also closes the embedded database if one was started.

Return type:

None \| _Awaitable_\[None\]

connect() [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient.connect "Link to this definition")

Connect to the Weaviate instance performing all the necessary checks.

If you have specified skip\_init\_checks in the constructor then this method will not perform any runtime checks
to ensure that Weaviate is running and ready to accept requests. This is useful for air-gapped environments and high-performance setups.

This method is idempotent and will only perform the checks once. Any subsequent calls do nothing while client.is\_connected() == True.

Raises:

- [**WeaviateConnectionError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateConnectionError "weaviate.exceptions.WeaviateConnectionError") – If the network connection to weaviate fails.

- [**UnexpectedStatusCodeError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If weaviate reports a none OK status.


Return type:

None \| _Awaitable_\[None\]

get\_meta() [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient.get_meta "Link to this definition")

Get the meta endpoint description of weaviate.

Returns:

The dict describing the weaviate configuration.

Raises:

[**UnexpectedStatusCodeError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If Weaviate reports a none OK status.

Return type:

dict \| _Awaitable_\[dict\]

get\_open\_id\_configuration() [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient.get_open_id_configuration "Link to this definition")

Get the openid-configuration.

Returns:

The configuration or None if not configured.

Raises:

[**UnexpectedStatusCodeError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If Weaviate reports a none OK status.

Return type:

_Dict_\[str, _Any_\] \| None \| _Awaitable_\[ _Dict_\[str, _Any_\] \| None\]

graphql\_raw\_query( _gql\_query_) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient.graphql_raw_query "Link to this definition")

Allows to send graphQL string queries, this should only be used for weaviate-features that are not yet supported.

Be cautious of injection risks when generating query strings.

Parameters:

**gql\_query** ( _str_) – GraphQL query as a string.

Returns:

A dict with the response from the GraphQL query.

Raises:

- **TypeError** – If gql\_query is not of type str.

- [**WeaviateConnectionError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateConnectionError "weaviate.exceptions.WeaviateConnectionError") – If the network connection to weaviate fails.

- [**UnexpectedStatusCodeError**](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If weaviate reports a none OK status.


Return type:

[_\_RawGQLReturn_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal._RawGQLReturn "weaviate.collections.classes.internal._RawGQLReturn") \| _Awaitable_\[ [_\_RawGQLReturn_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal._RawGQLReturn "weaviate.collections.classes.internal._RawGQLReturn")\]

is\_connected() [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient.is_connected "Link to this definition")

Check if the client is connected to Weaviate.

Returns:

True if the client is connected to Weaviate with an open connection pool, False otherwise.

Return type:

bool

is\_live() [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient.is_live "Link to this definition")Return type:

bool \| _Awaitable_\[bool\]

is\_ready() [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient.is_ready "Link to this definition")Return type:

bool \| _Awaitable_\[bool\]

weaviate.connect\_to\_custom( _http\_host_, _http\_port_, _http\_secure_, _grpc\_host_, _grpc\_port_, _grpc\_secure_, _headers=None_, _additional\_config=None_, _auth\_credentials=None_, _skip\_init\_checks=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/helpers.html#connect_to_custom) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.connect_to_custom "Link to this definition")

Connect to a Weaviate instance with custom connection parameters.

If this is not sufficient for your customization needs then instantiate a weaviate.WeaviateClient instance directly.

This method handles automatically connecting to Weaviate but not automatically closing the connection. Once you are done with the client
you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
in a with statement, which will automatically close the connection when the context is exited. See the examples below for details.

Parameters:

- **http\_host** ( _str_) – The host to use for the underlying REST and GraphQL API calls.

- **http\_port** ( _int_) – The port to use for the underlying REST and GraphQL API calls.

- **http\_secure** ( _bool_) – Whether to use https for the underlying REST and GraphQL API calls.

- **grpc\_host** ( _str_) – The host to use for the underlying gRPC API.

- **grpc\_port** ( _int_) – The port to use for the underlying gRPC API.

- **grpc\_secure** ( _bool_) – Whether to use a secure channel for the underlying gRPC API.

- **headers** ( _Dict_ _\[_ _str_ _,_ _str_ _\]_ _\|_ _None_) – Additional headers to include in the requests, e.g. API keys for Cloud vectorization.

- **additional\_config** ( [_AdditionalConfig_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") _\|_ _None_) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.

- **auth\_credentials** ( [_\_BearerToken_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._BearerToken "weaviate.auth._BearerToken") _\|_ [_\_ClientPassword_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") _\|_ [_\_ClientCredentials_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") _\|_ [_\_APIKey_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._APIKey "weaviate.auth._APIKey") _\|_ _None_) – The credentials to use for authentication with your Weaviate instance. This can be an API key, in which case pass a string or use weaviate.classes.init.Auth.api\_key(),
a bearer token, in which case use weaviate.classes.init.Auth.bearer\_token(), a client secret, in which case use weaviate.classes.init.Auth.client\_credentials()
or a username and password, in which case use weaviate.classes.init.Auth.client\_password().

- **skip\_init\_checks** ( _bool_) – Whether to skip the initialization checks when connecting to Weaviate.


Returns:

The client connected to the instance with the required parameters set appropriately.

Return type:

[_WeaviateClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient "weaviate.client.WeaviateClient")

Examples

```
>>> ################## Without Context Manager #############################
>>> import weaviate
>>> client = weaviate.connect_to_custom(
...     http_host="localhost",
...     http_port=8080,
...     http_secure=False,
...     grpc_host="localhost",
...     grpc_port=50051,
...     grpc_secure=False,
... )
>>> client.is_ready()
True
>>> client.close() # Close the connection when you are done with it.
>>> ################## With Context Manager #############################
>>> import weaviate
>>> with weaviate.connect_to_custom(
...     http_host="localhost",
...     http_port=8080,
...     http_secure=False,
...     grpc_host="localhost",
...     grpc_port=50051,
...     grpc_secure=False,
... ) as client:
...     client.is_ready()
True
>>> # The connection is automatically closed when the context is exited.

```

weaviate.connect\_to\_embedded( _hostname='127.0.0.1'_, _port=8079_, _grpc\_port=50050_, _headers=None_, _additional\_config=None_, _version='1.30.5'_, _persistence\_data\_path=None_, _binary\_path=None_, _environment\_variables=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/helpers.html#connect_to_embedded) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.connect_to_embedded "Link to this definition")

Connect to an embedded Weaviate instance.

This method handles automatically connecting to Weaviate but not automatically closing the connection. Once you are done with the client
you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
in a with statement, which will automatically close the connection when the context is exited. See the examples below for details.

See [the docs](https://weaviate.io/developers/weaviate/installation/embedded#embedded-options) for more details.

Parameters:

- **hostname** ( _str_) – The hostname to use for the underlying REST & GraphQL API calls.

- **port** ( _int_) – The port to use for the underlying REST and GraphQL API calls.

- **grpc\_port** ( _int_) – The port to use for the underlying gRPC API.

- **headers** ( _Dict_ _\[_ _str_ _,_ _str_ _\]_ _\|_ _None_) – Additional headers to include in the requests, e.g. API keys for Cloud vectorization.

- **additional\_config** ( [_AdditionalConfig_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") _\|_ _None_) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.

- **version** ( _str_) – Weaviate version to be used for the embedded instance.

- **persistence\_data\_path** ( _str_ _\|_ _None_) – Directory where the files making up the database are stored.
When the XDG\_DATA\_HOME env variable is set, the default value is: XDG\_DATA\_HOME/weaviate/
Otherwise it is: ~/.local/share/weaviate

- **binary\_path** ( _str_ _\|_ _None_) – Directory where to download the binary. If deleted, the client will download the binary again.
When the XDG\_CACHE\_HOME env variable is set, the default value is: XDG\_CACHE\_HOME/weaviate-embedded/
Otherwise it is: ~/.cache/weaviate-embedded

- **environment\_variables** ( _Dict_ _\[_ _str_ _,_ _str_ _\]_ _\|_ _None_) – Additional environment variables to be passed to the embedded instance for configuration.


Returns:

The client connected to the embedded instance with the required parameters set appropriately.

Return type:

[_WeaviateClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient "weaviate.client.WeaviateClient")

Examples

```
>>> import weaviate
>>> client = weaviate.connect_to_embedded(
...     port=8080,
...     grpc_port=50051,
... )
>>> client.is_ready()
True
>>> client.close() # Close the connection when you are done with it.
################## With Context Manager #############################
>>> import weaviate
>>> with weaviate.connect_to_embedded(
...     port=8080,
...     grpc_port=50051,
... ) as client:
...     client.is_ready()
True
>>> # The connection is automatically closed when the context is exited.

```

weaviate.connect\_to\_local( _host='localhost'_, _port=8080_, _grpc\_port=50051_, _headers=None_, _additional\_config=None_, _skip\_init\_checks=False_, _auth\_credentials=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/helpers.html#connect_to_local) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.connect_to_local "Link to this definition")

Connect to a local Weaviate instance deployed using Docker compose with standard port configurations.

This method handles automatically connecting to Weaviate but not automatically closing the connection. Once you are done with the client
you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
in a with statement, which will automatically close the connection when the context is exited. See the examples below for details.

Parameters:

- **host** ( _str_) – The host to use for the underlying REST and GraphQL API calls.

- **port** ( _int_) – The port to use for the underlying REST and GraphQL API calls.

- **grpc\_port** ( _int_) – The port to use for the underlying gRPC API.

- **headers** ( _Dict_ _\[_ _str_ _,_ _str_ _\]_ _\|_ _None_) – Additional headers to include in the requests, e.g. API keys for Cloud vectorization.

- **additional\_config** ( [_AdditionalConfig_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") _\|_ _None_) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.

- **skip\_init\_checks** ( _bool_) – Whether to skip the initialization checks when connecting to Weaviate.

- **auth\_credentials** ( _str_ _\|_ [_\_BearerToken_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._BearerToken "weaviate.auth._BearerToken") _\|_ [_\_ClientPassword_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") _\|_ [_\_ClientCredentials_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") _\|_ [_\_APIKey_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._APIKey "weaviate.auth._APIKey") _\|_ _None_) – The credentials to use for authentication with your Weaviate instance. This can be an API key, in which case pass a string or use weaviate.classes.init.Auth.api\_key(),
a bearer token, in which case use weaviate.classes.init.Auth.bearer\_token(), a client secret, in which case use weaviate.classes.init.Auth.client\_credentials()
or a username and password, in which case use weaviate.classes.init.Auth.client\_password().


Return type:

The client connected to the local instance with default parameters set as

Examples

```
>>> ################## Without Context Manager #############################
>>> import weaviate
>>> client = weaviate.connect_to_local(
...     host="localhost",
...     port=8080,
...     grpc_port=50051,
... )
>>> client.is_ready()
True
>>> client.close() # Close the connection when you are done with it.
>>> ################## With Context Manager #############################
>>> import weaviate
>>> with weaviate.connect_to_local(
...     host="localhost",
...     port=8080,
...     grpc_port=50051,
... ) as client:
...     client.is_ready()
True
>>> # The connection is automatically closed when the context is exited.

```

weaviate.connect\_to\_wcs( _cluster\_url_, _auth\_credentials_, _headers=None_, _additional\_config=None_, _skip\_init\_checks=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/helpers.html#connect_to_wcs) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.connect_to_wcs "Link to this definition")

Deprecated since version 4.6.2.

This method is deprecated and will be removed in a future release. Use [`connect_to_weaviate_cloud()`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.connect_to_weaviate_cloud "weaviate.connect_to_weaviate_cloud") instead.

Parameters:

- **cluster\_url** ( _str_)

- **auth\_credentials** ( _str_ _\|_ [_\_BearerToken_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._BearerToken "weaviate.auth._BearerToken") _\|_ [_\_ClientPassword_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") _\|_ [_\_ClientCredentials_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") _\|_ [_\_APIKey_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._APIKey "weaviate.auth._APIKey"))

- **headers** ( _Dict_ _\[_ _str_ _,_ _str_ _\]_ _\|_ _None_)

- **additional\_config** ( [_AdditionalConfig_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") _\|_ _None_)

- **skip\_init\_checks** ( _bool_)


Return type:

[_WeaviateClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient "weaviate.client.WeaviateClient")

weaviate.connect\_to\_weaviate\_cloud( _cluster\_url_, _auth\_credentials_, _headers=None_, _additional\_config=None_, _skip\_init\_checks=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/helpers.html#connect_to_weaviate_cloud) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.connect_to_weaviate_cloud "Link to this definition")

Connect to a Weaviate Cloud (WCD) instance.

This method handles automatically connecting to Weaviate but not automatically closing the connection. Once you are done with the client
you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
in a with statement, which will automatically close the connection when the context is exited. See the examples below for details.

Parameters:

- **cluster\_url** ( _str_) – The WCD cluster URL or hostname to connect to. Usually in the form: rAnD0mD1g1t5.something.weaviate.cloud

- **auth\_credentials** ( _str_ _\|_ [_\_BearerToken_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._BearerToken "weaviate.auth._BearerToken") _\|_ [_\_ClientPassword_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") _\|_ [_\_ClientCredentials_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") _\|_ [_\_APIKey_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._APIKey "weaviate.auth._APIKey")) – The credentials to use for authentication with your Weaviate instance. This can be an API key, in which case pass a string or use
weaviate.classes.init.Auth.api\_key(), a bearer token, in which case use weaviate.classes.init.Auth.bearer\_token(), a client secret,
in which case use weaviate.classes.init.Auth.client\_credentials() or a username and password, in which case use weaviate.classes.init.Auth.client\_password().

- **headers** ( _Dict_ _\[_ _str_ _,_ _str_ _\]_ _\|_ _None_) – Additional headers to include in the requests, e.g. API keys for third-party Cloud vectorization.

- **additional\_config** ( [_AdditionalConfig_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") _\|_ _None_) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.

- **skip\_init\_checks** ( _bool_) – Whether to skip the initialization checks when connecting to Weaviate.


Returns:

The client connected to the cluster with the required parameters set appropriately.

Return type:

[_WeaviateClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateClient "weaviate.client.WeaviateClient")

Examples

```
>>> ################## Without Context Manager #############################
>>> import weaviate
>>> client = weaviate.connect_to_weaviate_cloud(
...     cluster_url="rAnD0mD1g1t5.something.weaviate.cloud",
...     auth_credentials=weaviate.classes.init.Auth.api_key("my-api-key"),
... )
>>> client.is_ready()
True
>>> client.close() # Close the connection when you are done with it.
>>> ################## With Context Manager #############################
>>> import weaviate
>>> with weaviate.connect_to_weaviate_cloud(
...     cluster_url="rAnD0mD1g1t5.something.weaviate.cloud",
...     auth_credentials=weaviate.classes.init.Auth.api_key("my-api-key"),
... ) as client:
...     client.is_ready()
True
>>> # The connection is automatically closed when the context is exited.

```

weaviate.use\_async\_with\_custom( _http\_host_, _http\_port_, _http\_secure_, _grpc\_host_, _grpc\_port_, _grpc\_secure_, _headers=None_, _additional\_config=None_, _auth\_credentials=None_, _skip\_init\_checks=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/helpers.html#use_async_with_custom) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.use_async_with_custom "Link to this definition")

Create an async client object ready to connect to a Weaviate instance with custom connection parameters.

If this is not sufficient for your customization needs then instantiate a weaviate.WeaviateAsyncClient instance directly.

This method handles creating the WeaviateAsyncClient instance with relevant options to Weaviate Cloud connections but you must manually call await client.connect().
Once you are done with the client you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
in an async with statement, which will automatically open/close the connection when the context is entered/exited. See the examples below for details.

Parameters:

- **http\_host** ( _str_) – The host to use for the underlying REST and GraphQL API calls.

- **http\_port** ( _int_) – The port to use for the underlying REST and GraphQL API calls.

- **http\_secure** ( _bool_) – Whether to use https for the underlying REST and GraphQL API calls.

- **grpc\_host** ( _str_) – The host to use for the underlying gRPC API.

- **grpc\_port** ( _int_) – The port to use for the underlying gRPC API.

- **grpc\_secure** ( _bool_) – Whether to use a secure channel for the underlying gRPC API.

- **headers** ( _Dict_ _\[_ _str_ _,_ _str_ _\]_ _\|_ _None_) – Additional headers to include in the requests, e.g. API keys for Cloud vectorization.

- **additional\_config** ( [_AdditionalConfig_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") _\|_ _None_) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.

- **auth\_credentials** ( [_\_BearerToken_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._BearerToken "weaviate.auth._BearerToken") _\|_ [_\_ClientPassword_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") _\|_ [_\_ClientCredentials_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") _\|_ [_\_APIKey_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._APIKey "weaviate.auth._APIKey") _\|_ _None_) – The credentials to use for authentication with your Weaviate instance. This can be an API key, in which case pass a string or use weaviate.classes.init.Auth.api\_key(),
a bearer token, in which case use weaviate.classes.init.Auth.bearer\_token(), a client secret, in which case use weaviate.classes.init.Auth.client\_credentials()
or a username and password, in which case use weaviate.classes.init.Auth.client\_password().

- **skip\_init\_checks** ( _bool_) – Whether to skip the initialization checks when connecting to Weaviate.


Returns:

The client connected to the instance with the required parameters set appropriately.

Return type:

[_WeaviateAsyncClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient "weaviate.client.WeaviateAsyncClient")

Examples

```
>>> ################## Without Context Manager #############################
>>> import weaviate
>>> client = weaviate.use_async_with_custom(
...     http_host="localhost",
...     http_port=8080,
...     http_secure=False,
...     grpc_host="localhost",
...     grpc_port=50051,
...     grpc_secure=False,
... )
>>> await client.is_ready()
False # The connection is not ready yet, you must call `await client.connect()` to connect.
... await client.connect()
>>> await client.is_ready()
True
>>> await client.close() # Close the connection when you are done with it.
>>> ################## Async With Context Manager #############################
>>> import weaviate
>>> async with weaviate.use_async_with_custom(
...     http_host="localhost",
...     http_port=8080,
...     http_secure=False,
...     grpc_host="localhost",
...     grpc_port=50051,
...     grpc_secure=False,
... ) as client:
...     await client.is_ready()
True
>>> # The connection is automatically closed when the context is exited.

```

weaviate.use\_async\_with\_embedded( _hostname='127.0.0.1'_, _port=8079_, _grpc\_port=50050_, _headers=None_, _additional\_config=None_, _version='1.30.5'_, _persistence\_data\_path=None_, _binary\_path=None_, _environment\_variables=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/helpers.html#use_async_with_embedded) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.use_async_with_embedded "Link to this definition")

Create an async client object ready to connect to an embedded Weaviate instance.

If this is not sufficient for your customization needs then instantiate a weaviate.WeaviateAsyncClient instance directly.

This method handles creating the WeaviateAsyncClient instance with relevant options to Weaviate Cloud connections but you must manually call await client.connect().
Once you are done with the client you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
in an async with statement, which will automatically open/close the connection when the context is entered/exited. See the examples below for details.

See [the docs](https://weaviate.io/developers/weaviate/installation/embedded#embedded-options) for more details.

Parameters:

- **hostname** ( _str_) – The hostname to use for the underlying REST & GraphQL API calls.

- **port** ( _int_) – The port to use for the underlying REST and GraphQL API calls.

- **grpc\_port** ( _int_) – The port to use for the underlying gRPC API.

- **headers** ( _Dict_ _\[_ _str_ _,_ _str_ _\]_ _\|_ _None_) – Additional headers to include in the requests, e.g. API keys for Cloud vectorization.

- **additional\_config** ( [_AdditionalConfig_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") _\|_ _None_) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.

- **version** ( _str_) – Weaviate version to be used for the embedded instance.

- **persistence\_data\_path** ( _str_ _\|_ _None_) – Directory where the files making up the database are stored.
When the XDG\_DATA\_HOME env variable is set, the default value is: XDG\_DATA\_HOME/weaviate/
Otherwise it is: ~/.local/share/weaviate

- **binary\_path** ( _str_ _\|_ _None_) – Directory where to download the binary. If deleted, the client will download the binary again.
When the XDG\_CACHE\_HOME env variable is set, the default value is: XDG\_CACHE\_HOME/weaviate-embedded/
Otherwise it is: ~/.cache/weaviate-embedded

- **environment\_variables** ( _Dict_ _\[_ _str_ _,_ _str_ _\]_ _\|_ _None_) – Additional environment variables to be passed to the embedded instance for configuration.


Returns:

The client connected to the embedded instance with the required parameters set appropriately.

Return type:

[_WeaviateAsyncClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient "weaviate.client.WeaviateAsyncClient")

Examples

```
>>> import weaviate
>>> client = weaviate.use_async_with_embedded(
...     port=8080,
...     grpc_port=50051,
... )
>>> await client.is_ready()
False # The connection is not ready yet, you must call `await client.connect()` to connect.
... await client.connect()
>>> await client.is_ready()
True
################## With Context Manager #############################
>>> import weaviate
>>> async with weaviate.use_async_with_embedded(
...     port=8080,
...     grpc_port=50051,
... ) as client:
...     await client.is_ready()
True
>>> # The connection is automatically closed when the context is exited.

```

weaviate.use\_async\_with\_local( _host='localhost'_, _port=8080_, _grpc\_port=50051_, _headers=None_, _additional\_config=None_, _skip\_init\_checks=False_, _auth\_credentials=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/helpers.html#use_async_with_local) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.use_async_with_local "Link to this definition")

Create an async client object ready to connect to a local Weaviate instance deployed using Docker compose with standard port configurations.

This method handles creating the WeaviateAsyncClient instance with relevant options to Weaviate Cloud connections but you must manually call await client.connect().
Once you are done with the client you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
in an async with statement, which will automatically open/close the connection when the context is entered/exited. See the examples below for details.

Parameters:

- **host** ( _str_) – The host to use for the underlying REST and GraphQL API calls.

- **port** ( _int_) – The port to use for the underlying REST and GraphQL API calls.

- **grpc\_port** ( _int_) – The port to use for the underlying gRPC API.

- **headers** ( _Dict_ _\[_ _str_ _,_ _str_ _\]_ _\|_ _None_) – Additional headers to include in the requests, e.g. API keys for Cloud vectorization.

- **additional\_config** ( [_AdditionalConfig_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") _\|_ _None_) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.

- **skip\_init\_checks** ( _bool_) – Whether to skip the initialization checks when connecting to Weaviate.

- **auth\_credentials** ( _str_ _\|_ [_\_BearerToken_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._BearerToken "weaviate.auth._BearerToken") _\|_ [_\_ClientPassword_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") _\|_ [_\_ClientCredentials_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") _\|_ [_\_APIKey_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._APIKey "weaviate.auth._APIKey") _\|_ _None_) – The credentials to use for authentication with your Weaviate instance. This can be an API key, in which case pass a string or use weaviate.classes.init.Auth.api\_key(),
a bearer token, in which case use weaviate.classes.init.Auth.bearer\_token(), a client secret, in which case use weaviate.classes.init.Auth.client\_credentials()
or a username and password, in which case use weaviate.classes.init.Auth.client\_password().


Returns:

The async client ready to connect to the cluster with the required parameters set appropriately.

Return type:

[_WeaviateAsyncClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient "weaviate.client.WeaviateAsyncClient")

Examples

```
>>> ################## Without Context Manager #############################
>>> import weaviate
>>> client = weaviate.use_async_with_local(
...     host="localhost",
...     port=8080,
...     grpc_port=50051,
... )
>>> await client.is_ready()
False # The connection is not ready yet, you must call `await client.connect()` to connect.
... await client.connect()
>>> await client.is_ready()
True
>>> await client.close() # Close the connection when you are done with it.
>>> ################## With Context Manager #############################
>>> import weaviate
>>> async with weaviate.use_async_with_local(
...     host="localhost",
...     port=8080,
...     grpc_port=50051,
... ) as client:
...     await client.is_ready()
True
>>> # The connection is automatically closed when the context is exited.

```

weaviate.use\_async\_with\_weaviate\_cloud( _cluster\_url_, _auth\_credentials_, _headers=None_, _additional\_config=None_, _skip\_init\_checks=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/helpers.html#use_async_with_weaviate_cloud) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.use_async_with_weaviate_cloud "Link to this definition")

Create an async client object ready to connect to a Weaviate Cloud (WCD) instance.

This method handles creating the WeaviateAsyncClient instance with relevant options to Weaviate Cloud connections but you must manually call await client.connect().
Once you are done with the client you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
in an async with statement, which will automatically open/close the connection when the context is entered/exited. See the examples below for details.

Parameters:

- **cluster\_url** ( _str_) – The WCD cluster URL or hostname to connect to. Usually in the form: rAnD0mD1g1t5.something.weaviate.cloud

- **auth\_credentials** ( [_\_BearerToken_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._BearerToken "weaviate.auth._BearerToken") _\|_ [_\_ClientPassword_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") _\|_ [_\_ClientCredentials_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") _\|_ [_\_APIKey_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._APIKey "weaviate.auth._APIKey") _\|_ _None_) – The credentials to use for authentication with your Weaviate instance. This can be an API key, in which case pass a string or use weaviate.classes.init.Auth.api\_key(),
a bearer token, in which case use weaviate.classes.init.Auth.bearer\_token(), a client secret, in which case use weaviate.classes.init.Auth.client\_credentials()
or a username and password, in which case use weaviate.classes.init.Auth.client\_password().

- **headers** ( _Dict_ _\[_ _str_ _,_ _str_ _\]_ _\|_ _None_) – Additional headers to include in the requests, e.g. API keys for third-party Cloud vectorization.

- **additional\_config** ( [_AdditionalConfig_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") _\|_ _None_) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.

- **skip\_init\_checks** ( _bool_) – Whether to skip the initialization checks when connecting to Weaviate.


Returns:

The async client ready to connect to the cluster with the required parameters set appropriately.

Return type:

[_WeaviateAsyncClient_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.WeaviateAsyncClient "weaviate.client.WeaviateAsyncClient")

Examples

```
>>> ################## Without Context Manager #############################
>>> import weaviate
>>> client = weaviate.use_async_with_weaviate_cloud(
...     cluster_url="rAnD0mD1g1t5.something.weaviate.cloud",
...     auth_credentials=weaviate.classes.init.Auth.api_key("my-api-key"),
... )
>>> await client.is_ready()
False # The connection is not ready yet, you must call `await client.connect()` to connect.
... await client.connect()
>>> await client.is_ready()
True
>>> await client.close() # Close the connection when you are done with it.
>>> ################## With Context Manager #############################
>>> import weaviate
>>> async with weaviate.use_async_with_weaviate_cloud(
...     cluster_url="rAnD0mD1g1t5.something.weaviate.cloud",
...     auth_credentials=weaviate.classes.init.Auth.api_key("my-api-key"),
... ) as client:
...     await client.is_ready()
True

```

# Subpackages [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html\#subpackages "Link to this heading")

- [weaviate.backup](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html)
  - [`BackupStorage`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.BackupStorage)
  - [`_BackupAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup._BackupAsync)
  - [`_Backup`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup._Backup)
  - [weaviate.backup.backup](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#module-weaviate.backup.backup)
  - [weaviate.backup.backup\_location](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#module-weaviate.backup.backup_location)
- [weaviate.classes](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html)
  - [`ConsistencyLevel`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate.classes.ConsistencyLevel)
  - [weaviate.classes.aggregate](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#module-weaviate.classes.aggregate)
  - [weaviate.classes.backup](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#module-weaviate.classes.backup)
  - [weaviate.classes.batch](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#module-weaviate.classes.batch)
  - [weaviate.classes.config](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#module-weaviate.classes.config)
  - [weaviate.classes.data](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#module-weaviate.classes.data)
  - [weaviate.classes.debug](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#module-weaviate.classes.debug)
  - [weaviate.classes.generics](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#module-weaviate.classes.generics)
  - [weaviate.classes.init](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#module-weaviate.classes.init)
  - [weaviate.classes.query](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#module-weaviate.classes.query)
  - [weaviate.classes.rbac](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#module-weaviate.classes.rbac)
  - [weaviate.classes.tenants](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.classes.html#weaviate-classes-tenants)
- [weaviate.cluster](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.cluster.html)
  - [`_ClusterAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.cluster.html#weaviate.cluster._ClusterAsync)
  - [`_Cluster`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.cluster.html#weaviate.cluster._Cluster)
  - [weaviate.cluster.types](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.cluster.html#module-weaviate.cluster.types)
- [weaviate.collections](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html)
  - [`Collection`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.Collection)
  - [`CollectionAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#weaviate.collections.CollectionAsync)
  - [Subpackages](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.html#subpackages)
- [weaviate.connect](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html)
  - [`ConnectionV4`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ConnectionV4)
  - [`ConnectionParams`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ConnectionParams)
  - [`ProtocolParams`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ProtocolParams)
- [weaviate.debug](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.debug.html)
  - [`_Debug`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.debug.html#weaviate.debug._Debug)
  - [`_DebugAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.debug.html#weaviate.debug._DebugAsync)
  - [weaviate.debug.types](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.debug.html#module-weaviate.debug.types)
- [weaviate.gql](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html)
  - [weaviate.gql.aggregate](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#module-weaviate.gql.aggregate)
  - [weaviate.gql.filter](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#module-weaviate.gql.filter)
- [weaviate.outputs](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html)
  - [weaviate.outputs.aggregate](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#module-weaviate.outputs.aggregate)
  - [weaviate.outputs.backup](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#module-weaviate.outputs.backup)
  - [weaviate.outputs.batch](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#module-weaviate.outputs.batch)
  - [weaviate.outputs.cluster](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#module-weaviate.outputs.cluster)
  - [weaviate.outputs.config](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#module-weaviate.outputs.config)
  - [weaviate.outputs.data](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#module-weaviate.outputs.data)
  - [weaviate.outputs.query](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#module-weaviate.outputs.query)
  - [weaviate.outputs.rbac](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#module-weaviate.outputs.rbac)
  - [weaviate.outputs.tenants](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#module-weaviate.outputs.tenants)
- [weaviate.rbac](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html)
  - [`_RolesAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac._RolesAsync)
  - [`_Roles`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac._Roles)
  - [weaviate.rbac.models](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#module-weaviate.rbac.models)
  - [weaviate.rbac.roles](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate-rbac-roles)
- [weaviate.users](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.users.html)
  - [`_UsersAsync`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.users.html#weaviate.users._UsersAsync)
  - [`_Users`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.users.html#weaviate.users._Users)

## weaviate.auth [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html\#module-weaviate.auth "Link to this heading")

Authentication class definitions.

_class_ weaviate.auth.\_ClientCredentials( _client\_secret_, _scope=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/auth.html#_ClientCredentials) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientCredentials "Link to this definition")

Authenticate for the Client Credential flow using client secrets.

Acquire the client secret from your identify provider and set the appropriate scope. The client includes hardcoded
scopes for Azure, otherwise it needs to be supplied.
Scopes can be given as:

> - List of strings: \[“scope1”, “scope2”\]
>
> - space separated string: “scope1 scope2”

Parameters:

- **client\_secret** ( _str_)

- **scope** ( _str_ _\|_ _List_ _\[_ _str_ _\]_ _\|_ _None_)


client\_secret _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientCredentials.client_secret "Link to this definition")scope _:str\|List\[str\]\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientCredentials.scope "Link to this definition")_class_ weaviate.auth.\_ClientPassword( _username_, _password_, _scope=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/auth.html#_ClientPassword) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientPassword "Link to this definition")

Using username and password for authentication with Resource Owner Password flow.

For some providers the scope needs to contain “offline\_access” (and “openid” which is automatically added) to return
a refresh token. Without a refresh token the authentication will expire once the lifetime of the access token is up.
Scopes can be given as:

> - List of strings: \[“scope1”, “scope2”\]
>
> - space separated string: “scope1 scope2”

Parameters:

- **username** ( _str_)

- **password** ( _str_)

- **scope** ( _str_ _\|_ _List_ _\[_ _str_ _\]_ _\|_ _None_)


username _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientPassword.username "Link to this definition")password _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientPassword.password "Link to this definition")scope _:str\|List\[str\]\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientPassword.scope "Link to this definition")_class_ weaviate.auth.\_BearerToken( _access\_token_, _expires\_in=60_, _refresh\_token=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/auth.html#_BearerToken) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._BearerToken "Link to this definition")

Using a preexisting bearer/access token for authentication.

The expiration time of access tokens is given in seconds.

Only the access token is required. However, when no refresh token is
given, the authentication will expire once the lifetime of the
access token is up.

Parameters:

- **access\_token** ( _str_)

- **expires\_in** ( _int_)

- **refresh\_token** ( _str_ _\|_ _None_)


access\_token _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._BearerToken.access_token "Link to this definition")expires\_in _:int_ _=60_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._BearerToken.expires_in "Link to this definition")refresh\_token _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._BearerToken.refresh_token "Link to this definition")_class_ weaviate.auth.\_APIKey( _api\_key_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/auth.html#_APIKey) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._APIKey "Link to this definition")

Using the given API key to authenticate with weaviate.

Parameters:

**api\_key** ( _str_)

api\_key _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._APIKey.api_key "Link to this definition")_class_ weaviate.auth.Auth [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/auth.html#Auth) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth.Auth "Link to this definition")_static_ api\_key( _api\_key_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/auth.html#Auth.api_key) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth.Auth.api_key "Link to this definition")Parameters:

**api\_key** ( _str_)

Return type:

[_\_APIKey_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._APIKey "weaviate.auth._APIKey")

_static_ client\_credentials( _client\_secret_, _scope=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/auth.html#Auth.client_credentials) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth.Auth.client_credentials "Link to this definition")Parameters:

- **client\_secret** ( _str_)

- **scope** ( _str_ _\|_ _List_ _\[_ _str_ _\]_ _\|_ _None_)


Return type:

[_\_ClientCredentials_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials")

_static_ client\_password( _username_, _password_, _scope=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/auth.html#Auth.client_password) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth.Auth.client_password "Link to this definition")Parameters:

- **username** ( _str_)

- **password** ( _str_)

- **scope** ( _str_ _\|_ _List_ _\[_ _str_ _\]_ _\|_ _None_)


Return type:

[_\_ClientPassword_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword")

_static_ bearer\_token( _access\_token_, _expires\_in=60_, _refresh\_token=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/auth.html#Auth.bearer_token) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth.Auth.bearer_token "Link to this definition")Parameters:

- **access\_token** ( _str_)

- **expires\_in** ( _int_)

- **refresh\_token** ( _str_ _\|_ _None_)


Return type:

[_\_BearerToken_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth._BearerToken "weaviate.auth._BearerToken")

weaviate.auth.AuthApiKey [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth.AuthApiKey "Link to this definition")

Deprecated since version 4.0.0: Use [`api_key()`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth.Auth.api_key "weaviate.auth.Auth.api_key") instead.

weaviate.auth.AuthBearerToken [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth.AuthBearerToken "Link to this definition")

Deprecated since version 4.0.0: Use [`bearer_token()`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth.Auth.bearer_token "weaviate.auth.Auth.bearer_token") instead.

weaviate.auth.AuthClientCredentials [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth.AuthClientCredentials "Link to this definition")

Deprecated since version 4.0.0: Use [`client_credentials()`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth.Auth.client_credentials "weaviate.auth.Auth.client_credentials") instead.

weaviate.auth.AuthClientPassword [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth.AuthClientPassword "Link to this definition")

Deprecated since version 4.0.0: Use [`client_password()`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth.Auth.client_password "weaviate.auth.Auth.client_password") instead.

## weaviate.config [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html\#module-weaviate.config "Link to this heading")

_class_ weaviate.config.ConnectionConfig( _session\_pool\_connections:int=20_, _session\_pool\_maxsize:int=100_, _session\_pool\_max\_retries:int=3_, _session\_pool\_timeout:int=5_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/config.html#ConnectionConfig) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.ConnectionConfig "Link to this definition")Parameters:

- **session\_pool\_connections** ( _int_)

- **session\_pool\_maxsize** ( _int_)

- **session\_pool\_max\_retries** ( _int_)

- **session\_pool\_timeout** ( _int_)


session\_pool\_connections _:int_ _=20_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.ConnectionConfig.session_pool_connections "Link to this definition")session\_pool\_maxsize _:int_ _=100_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.ConnectionConfig.session_pool_maxsize "Link to this definition")session\_pool\_max\_retries _:int_ _=3_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.ConnectionConfig.session_pool_max_retries "Link to this definition")session\_pool\_timeout _:int_ _=5_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.ConnectionConfig.session_pool_timeout "Link to this definition")_class_ weaviate.config.Config( _grpc\_port\_experimental:Optional\[int\]=None_, _grpc\_secure\_experimental:bool=False_, _connection\_config:weaviate.config.ConnectionConfig=<factory>_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/config.html#Config) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Config "Link to this definition")Parameters:

- **grpc\_port\_experimental** ( _int_ _\|_ _None_)

- **grpc\_secure\_experimental** ( _bool_)

- **connection\_config** ( [_ConnectionConfig_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.ConnectionConfig "weaviate.config.ConnectionConfig"))


grpc\_port\_experimental _:int\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Config.grpc_port_experimental "Link to this definition")grpc\_secure\_experimental _:bool_ _=False_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Config.grpc_secure_experimental "Link to this definition")connection\_config _: [ConnectionConfig](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.ConnectionConfig "weaviate.config.ConnectionConfig")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Config.connection_config "Link to this definition")_pydanticmodel_ weaviate.config.Timeout [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/config.html#Timeout) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Timeout "Link to this definition")

Timeouts for the different operations in the client.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ init _:int\|float_ _=2_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Timeout.init "Link to this definition")Constraints:

- **ge** = 0


_field_ insert _:int\|float_ _=90_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Timeout.insert "Link to this definition")Constraints:

- **ge** = 0


_field_ query _:int\|float_ _=30_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Timeout.query "Link to this definition")Constraints:

- **ge** = 0


_pydanticmodel_ weaviate.config.Proxies [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/config.html#Proxies) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Proxies "Link to this definition")

Proxy configurations for sending requests to Weaviate through a proxy.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ grpc _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Proxies.grpc "Link to this definition")_field_ http _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Proxies.http "Link to this definition")_field_ https _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Proxies.https "Link to this definition")_pydanticmodel_ weaviate.config.AdditionalConfig [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/config.html#AdditionalConfig) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig "Link to this definition")

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

_field_ connection _: [ConnectionConfig](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.ConnectionConfig "weaviate.config.ConnectionConfig")_ _\[Optional\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig.connection "Link to this definition")_field_ proxies _:str\| [Proxies](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Proxies "weaviate.config.Proxies") \|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig.proxies "Link to this definition")_field_ timeout\_ _:Tuple\[int,int\]\| [Timeout](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Timeout "weaviate.config.Timeout")_ _\[Optional\]_ _(alias'timeout')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig.timeout_ "Link to this definition")_field_ trust\_env _:bool_ _=False_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig.trust_env "Link to this definition")_property_ timeout _: [Timeout](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.Timeout "weaviate.config.Timeout")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.config.AdditionalConfig.timeout "Link to this definition")

## weaviate.embedded [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html\#module-weaviate.embedded "Link to this heading")

_class_ weaviate.embedded.EmbeddedOptions( _persistence\_data\_path:str='/home/docs/.local/share/weaviate'_, _binary\_path:str='/home/docs/.cache/weaviate-embedded'_, _version:str='1.30.5'_, _port:int=8079_, _hostname:str='127.0.0.1'_, _additional\_env\_vars:Dict\[str,str\]\|None=None_, _grpc\_port:int=50060_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/embedded.html#EmbeddedOptions) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedOptions "Link to this definition")Parameters:

- **persistence\_data\_path** ( _str_)

- **binary\_path** ( _str_)

- **version** ( _str_)

- **port** ( _int_)

- **hostname** ( _str_)

- **additional\_env\_vars** ( _Dict_ _\[_ _str_ _,_ _str_ _\]_ _\|_ _None_)

- **grpc\_port** ( _int_)


persistence\_data\_path _:str_ _='/home/docs/.local/share/weaviate'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedOptions.persistence_data_path "Link to this definition")binary\_path _:str_ _='/home/docs/.cache/weaviate-embedded'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedOptions.binary_path "Link to this definition")version _:str_ _='1.30.5'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedOptions.version "Link to this definition")port _:int_ _=8079_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedOptions.port "Link to this definition")hostname _:str_ _='127.0.0.1'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedOptions.hostname "Link to this definition")additional\_env\_vars _:Dict\[str,str\]\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedOptions.additional_env_vars "Link to this definition")grpc\_port _:int_ _=50060_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedOptions.grpc_port "Link to this definition")weaviate.embedded.get\_random\_port() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/embedded.html#get_random_port) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.get_random_port "Link to this definition")Return type:

int

_class_ weaviate.embedded.EmbeddedV3( _options_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/embedded.html#EmbeddedV3) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedV3 "Link to this definition")Parameters:

**options** ( [_EmbeddedOptions_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedOptions "weaviate.embedded.EmbeddedOptions"))

is\_listening() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/embedded.html#EmbeddedV3.is_listening) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedV3.is_listening "Link to this definition")Return type:

bool

start() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/embedded.html#EmbeddedV3.start) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedV3.start "Link to this definition")Return type:

None

weaviate.embedded.EmbeddedDB [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedDB "Link to this definition")

alias of [`EmbeddedV3`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedV3 "weaviate.embedded.EmbeddedV3")

_class_ weaviate.embedded.EmbeddedV4( _options_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/embedded.html#EmbeddedV4) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedV4 "Link to this definition")Parameters:

**options** ( [_EmbeddedOptions_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedOptions "weaviate.embedded.EmbeddedOptions"))

is\_listening() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/embedded.html#EmbeddedV4.is_listening) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedV4.is_listening "Link to this definition")Return type:

bool

start() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/embedded.html#EmbeddedV4.start) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.embedded.EmbeddedV4.start "Link to this definition")Return type:

None

Versions[latest](https://weaviate-python-client.readthedocs.io/en/latest/weaviate.html)**[stable](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html)**[v4.16.10](https://weaviate-python-client.readthedocs.io/en/v4.16.10/weaviate.html)[v4.16.9](https://weaviate-python-client.readthedocs.io/en/v4.16.9/weaviate.html)[v4.16.8](https://weaviate-python-client.readthedocs.io/en/v4.16.8/weaviate.html)[v4.16.7](https://weaviate-python-client.readthedocs.io/en/v4.16.7/weaviate.html)[v4.16.6](https://weaviate-python-client.readthedocs.io/en/v4.16.6/weaviate.html)[v4.16.5](https://weaviate-python-client.readthedocs.io/en/v4.16.5/weaviate.html)[v4.16.4](https://weaviate-python-client.readthedocs.io/en/v4.16.4/weaviate.html)[v4.16.3](https://weaviate-python-client.readthedocs.io/en/v4.16.3/weaviate.html)[v4.16.2](https://weaviate-python-client.readthedocs.io/en/v4.16.2/weaviate.html)[v4.16.1](https://weaviate-python-client.readthedocs.io/en/v4.16.1/weaviate.html)[v4.16.0](https://weaviate-python-client.readthedocs.io/en/v4.16.0/weaviate.html)[v4.15.4](https://weaviate-python-client.readthedocs.io/en/v4.15.4/weaviate.html)[v4.15.3](https://weaviate-python-client.readthedocs.io/en/v4.15.3/weaviate.html)[v4.15.2](https://weaviate-python-client.readthedocs.io/en/v4.15.2/weaviate.html)[v4.15.1](https://weaviate-python-client.readthedocs.io/en/v4.15.1/weaviate.html)[v4.15.0](https://weaviate-python-client.readthedocs.io/en/v4.15.0/weaviate.html)[v4.14.4](https://weaviate-python-client.readthedocs.io/en/v4.14.4/weaviate.html)[v4.14.3](https://weaviate-python-client.readthedocs.io/en/v4.14.3/weaviate.html)[v4.14.2](https://weaviate-python-client.readthedocs.io/en/v4.14.2/weaviate.html)[v4.14.1](https://weaviate-python-client.readthedocs.io/en/v4.14.1/weaviate.html)[v4.14.0](https://weaviate-python-client.readthedocs.io/en/v4.14.0/weaviate.html)[v4.13.2](https://weaviate-python-client.readthedocs.io/en/v4.13.2/weaviate.html)[v4.13.1](https://weaviate-python-client.readthedocs.io/en/v4.13.1/weaviate.html)[v4.13.0](https://weaviate-python-client.readthedocs.io/en/v4.13.0/weaviate.html)[v4.12.1](https://weaviate-python-client.readthedocs.io/en/v4.12.1/weaviate.html)[v4.12.0](https://weaviate-python-client.readthedocs.io/en/v4.12.0/weaviate.html)[v4.11.3](https://weaviate-python-client.readthedocs.io/en/v4.11.3/weaviate.html)[v4.11.2](https://weaviate-python-client.readthedocs.io/en/v4.11.2/weaviate.html)[v4.11.1](https://weaviate-python-client.readthedocs.io/en/v4.11.1/weaviate.html)[v4.11.0](https://weaviate-python-client.readthedocs.io/en/v4.11.0/weaviate.html)[v4.10.4](https://weaviate-python-client.readthedocs.io/en/v4.10.4/weaviate.html)[v4.10.3](https://weaviate-python-client.readthedocs.io/en/v4.10.3/weaviate.html)[v4.10.2](https://weaviate-python-client.readthedocs.io/en/v4.10.2/weaviate.html)[v4.10.0](https://weaviate-python-client.readthedocs.io/en/v4.10.0/weaviate.html)[v4.9.6](https://weaviate-python-client.readthedocs.io/en/v4.9.6/weaviate.html)[v4.9.5](https://weaviate-python-client.readthedocs.io/en/v4.9.5/weaviate.html)[v4.9.4](https://weaviate-python-client.readthedocs.io/en/v4.9.4/weaviate.html)[v4.9.3](https://weaviate-python-client.readthedocs.io/en/v4.9.3/weaviate.html)[v4.9.2](https://weaviate-python-client.readthedocs.io/en/v4.9.2/weaviate.html)[v4.9.1](https://weaviate-python-client.readthedocs.io/en/v4.9.1/weaviate.html)[v4.9.0](https://weaviate-python-client.readthedocs.io/en/v4.9.0/weaviate.html)[v4.8.1](https://weaviate-python-client.readthedocs.io/en/v4.8.1/weaviate.html)[v4.8.0](https://weaviate-python-client.readthedocs.io/en/v4.8.0/weaviate.html)[v4.7.1](https://weaviate-python-client.readthedocs.io/en/v4.7.1/weaviate.html)[v4.7.0](https://weaviate-python-client.readthedocs.io/en/v4.7.0/weaviate.html)[v4.6.7](https://weaviate-python-client.readthedocs.io/en/v4.6.7/weaviate.html)[v4.6.6](https://weaviate-python-client.readthedocs.io/en/v4.6.6/weaviate.html)[v4.6.5](https://weaviate-python-client.readthedocs.io/en/v4.6.5/weaviate.html)[v4.6.4](https://weaviate-python-client.readthedocs.io/en/v4.6.4/weaviate.html)[v4.6.3](https://weaviate-python-client.readthedocs.io/en/v4.6.3/weaviate.html)[v4.6.2](https://weaviate-python-client.readthedocs.io/en/v4.6.2/weaviate.html)[v4.6.1](https://weaviate-python-client.readthedocs.io/en/v4.6.1/weaviate.html)[v4.6.0](https://weaviate-python-client.readthedocs.io/en/v4.6.0/weaviate.html)[v4.5.7](https://weaviate-python-client.readthedocs.io/en/v4.5.7/weaviate.html)[v4.5.6](https://weaviate-python-client.readthedocs.io/en/v4.5.6/weaviate.html)[v4.5.5](https://weaviate-python-client.readthedocs.io/en/v4.5.5/weaviate.html)[v4.5.4](https://weaviate-python-client.readthedocs.io/en/v4.5.4/weaviate.html)[v4.5.3](https://weaviate-python-client.readthedocs.io/en/v4.5.3/weaviate.html)[v4.5.2](https://weaviate-python-client.readthedocs.io/en/v4.5.2/weaviate.html)[v4.5.1](https://weaviate-python-client.readthedocs.io/en/v4.5.1/weaviate.html)[v4.5.0](https://weaviate-python-client.readthedocs.io/en/v4.5.0/weaviate.html)[v4.4.4](https://weaviate-python-client.readthedocs.io/en/v4.4.4/weaviate.html)[v4.4.3](https://weaviate-python-client.readthedocs.io/en/v4.4.3/weaviate.html)[v4.4.2](https://weaviate-python-client.readthedocs.io/en/v4.4.2/weaviate.html)[v4.4.1](https://weaviate-python-client.readthedocs.io/en/v4.4.1/weaviate.html)[v4.4.0](https://weaviate-python-client.readthedocs.io/en/v4.4.0/weaviate.html)[v3.26.2](https://weaviate-python-client.readthedocs.io/en/v3.26.2/weaviate.html)[v3.26.1](https://weaviate-python-client.readthedocs.io/en/v3.26.1/weaviate.html)[v3.26.0](https://weaviate-python-client.readthedocs.io/en/v3.26.0/weaviate.html)[v3.25.3](https://weaviate-python-client.readthedocs.io/en/v3.25.3/weaviate.html)[v3.25.2](https://weaviate-python-client.readthedocs.io/en/v3.25.2/weaviate.html)[v3.23.0](https://weaviate-python-client.readthedocs.io/en/v3.23.0/weaviate.html)[v3.22.1](https://weaviate-python-client.readthedocs.io/en/v3.22.1/weaviate.html)[v3.22.0](https://weaviate-python-client.readthedocs.io/en/v3.22.0/weaviate.html)[v3.21.0](https://weaviate-python-client.readthedocs.io/en/v3.21.0/weaviate.html)[v3.20.1](https://weaviate-python-client.readthedocs.io/en/v3.20.1/weaviate.html)[v3.20.0](https://weaviate-python-client.readthedocs.io/en/v3.20.0/weaviate.html)[v3.19.2](https://weaviate-python-client.readthedocs.io/en/v3.19.2/weaviate.html)[v3.19.1](https://weaviate-python-client.readthedocs.io/en/v3.19.1/weaviate.html)[v3.19.0](https://weaviate-python-client.readthedocs.io/en/v3.19.0/weaviate.html)[v3.18.0](https://weaviate-python-client.readthedocs.io/en/v3.18.0/weaviate.html)[v3.15.6](https://weaviate-python-client.readthedocs.io/en/v3.15.6/weaviate.html)[v3.15.5](https://weaviate-python-client.readthedocs.io/en/v3.15.5/weaviate.html)[v3.15.4](https://weaviate-python-client.readthedocs.io/en/v3.15.4/weaviate.html)[v3.15.3](https://weaviate-python-client.readthedocs.io/en/v3.15.3/weaviate.html)[v3.15.2](https://weaviate-python-client.readthedocs.io/en/v3.15.2/weaviate.html)[v3.15.1](https://weaviate-python-client.readthedocs.io/en/v3.15.1/weaviate.html)[v3.15.0](https://weaviate-python-client.readthedocs.io/en/v3.15.0/weaviate.html)[v3.14.0](https://weaviate-python-client.readthedocs.io/en/v3.14.0/weaviate.html)[v3.13.0](https://weaviate-python-client.readthedocs.io/en/v3.13.0/weaviate.html)[v3.12.0\_a](https://weaviate-python-client.readthedocs.io/en/v3.12.0_a/weaviate.html)[v3.11.0](https://weaviate-python-client.readthedocs.io/en/v3.11.0/weaviate.html)[v3.10.0](https://weaviate-python-client.readthedocs.io/en/v3.10.0/weaviate.html)[v3.9.0](https://weaviate-python-client.readthedocs.io/en/v3.9.0/weaviate.html)[v3.8.0](https://weaviate-python-client.readthedocs.io/en/v3.8.0/weaviate.html)[v3.7.0](https://weaviate-python-client.readthedocs.io/en/v3.7.0/weaviate.html)[v3.6.0](https://weaviate-python-client.readthedocs.io/en/v3.6.0/weaviate.html)[v3.5.1](https://weaviate-python-client.readthedocs.io/en/v3.5.1/weaviate.html)[v3.5.0](https://weaviate-python-client.readthedocs.io/en/v3.5.0/weaviate.html)[v3.4.1](https://weaviate-python-client.readthedocs.io/en/v3.4.1/weaviate.html)[v3.4.0](https://weaviate-python-client.readthedocs.io/en/v3.4.0/weaviate.html)[v3.3.3](https://weaviate-python-client.readthedocs.io/en/v3.3.3/weaviate.html)[v3.3.2](https://weaviate-python-client.readthedocs.io/en/v3.3.2/weaviate.html)[v3.3.1](https://weaviate-python-client.readthedocs.io/en/v3.3.1/weaviate.html)[v3.3.0](https://weaviate-python-client.readthedocs.io/en/v3.3.0/weaviate.html)[v3.2.5](https://weaviate-python-client.readthedocs.io/en/v3.2.5/weaviate.html)[v3.2.4](https://weaviate-python-client.readthedocs.io/en/v3.2.4/weaviate.html)[v3.2.3](https://weaviate-python-client.readthedocs.io/en/v3.2.3/weaviate.html)[v3.2.2](https://weaviate-python-client.readthedocs.io/en/v3.2.2/weaviate.html)[v3.2.1](https://weaviate-python-client.readthedocs.io/en/v3.2.1/weaviate.html)[v3.2.0](https://weaviate-python-client.readthedocs.io/en/v3.2.0/weaviate.html)[v3.1.1](https://weaviate-python-client.readthedocs.io/en/v3.1.1/weaviate.html)[v3.1.0](https://weaviate-python-client.readthedocs.io/en/v3.1.0/weaviate.html)[v3.0.0](https://weaviate-python-client.readthedocs.io/en/v3.0.0/weaviate.html)On Read the Docs[Project Home](https://app.readthedocs.org/projects/weaviate-python-client/?utm_source=weaviate-python-client&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/weaviate-python-client/builds/?utm_source=weaviate-python-client&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=weaviate-python-client&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=weaviate-python-client&utm_content=flyout)