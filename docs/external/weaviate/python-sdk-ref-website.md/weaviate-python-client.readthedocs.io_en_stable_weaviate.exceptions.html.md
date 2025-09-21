---
url: "https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html"
title: "Weaviate Exceptions — Weaviate Python Client 4.16.10 documentation"
---

- [Home](https://weaviate-python-client.readthedocs.io/en/stable/index.html)
- Weaviate Exceptions
- [View page source](https://weaviate-python-client.readthedocs.io/en/stable/_sources/weaviate.exceptions.rst.txt)

* * *

# Weaviate Exceptions [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html\#module-weaviate.exceptions "Link to this heading")

Weaviate Exceptions.

_exception_ weaviate.exceptions.WeaviateBaseError( _message=''_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateBaseError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "Link to this definition")

Bases: `Exception`

Weaviate base exception that all Weaviate exceptions should inherit from.

This error can be used to catch any Weaviate exceptions.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

_exception_ weaviate.exceptions.UnexpectedStatusCodeError( _message_, _response_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#UnexpectedStatusCodeError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Is raised in case the status code returned from Weaviate is not handled in the client implementation and suggests an error.

Custom code can act on the attributes:
\- status\_code
\- json

Parameters:

- **message** ( _str_) – An error message specific to the context, in which the error occurred.

- **response** ( _Response_ _\|_ _AioRpcError_ _\|_ _Call_) – The request response of which the status code was unexpected.


_property_ status\_code _:int_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError.status_code "Link to this definition")_property_ error _:str\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError.error "Link to this definition")weaviate.exceptions.UnexpectedStatusCodeException [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeException "Link to this definition")

alias of [`UnexpectedStatusCodeError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError")

_exception_ weaviate.exceptions.ResponseCannotBeDecodedError( _location_, _response_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#ResponseCannotBeDecodedError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.ResponseCannotBeDecodedError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Raised when a weaviate response cannot be decoded to json.

Parameters:

- **location** ( _str_) – From which code path the exception was raised.

- **response** ( _Response_) – The request response of which the status code was unexpected.


_property_ status\_code _:int_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.ResponseCannotBeDecodedError.status_code "Link to this definition")weaviate.exceptions.ResponseCannotBeDecodedException [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.ResponseCannotBeDecodedException "Link to this definition")

alias of [`ResponseCannotBeDecodedError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.ResponseCannotBeDecodedError "weaviate.exceptions.ResponseCannotBeDecodedError")

_exception_ weaviate.exceptions.ObjectAlreadyExistsError( _message=''_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#ObjectAlreadyExistsError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.ObjectAlreadyExistsError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Object Already Exists Exception.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

weaviate.exceptions.ObjectAlreadyExistsException [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.ObjectAlreadyExistsException "Link to this definition")

alias of [`ObjectAlreadyExistsError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.ObjectAlreadyExistsError "weaviate.exceptions.ObjectAlreadyExistsError")

_exception_ weaviate.exceptions.AuthenticationFailedError( _message=''_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#AuthenticationFailedError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.AuthenticationFailedError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Authentication Failed Exception.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

weaviate.exceptions.AuthenticationFailedException [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.AuthenticationFailedException "Link to this definition")

alias of [`AuthenticationFailedError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.AuthenticationFailedError "weaviate.exceptions.AuthenticationFailedError")

_exception_ weaviate.exceptions.SchemaValidationError( _message=''_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#SchemaValidationError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.SchemaValidationError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Schema Validation Exception.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

weaviate.exceptions.SchemaValidationException [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.SchemaValidationException "Link to this definition")

alias of [`SchemaValidationError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.SchemaValidationError "weaviate.exceptions.SchemaValidationError")

_exception_ weaviate.exceptions.BackupFailedError( _message=''_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#BackupFailedError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.BackupFailedError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Backup Failed Exception.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

weaviate.exceptions.BackupFailedException [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.BackupFailedException "Link to this definition")

alias of [`BackupFailedError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.BackupFailedError "weaviate.exceptions.BackupFailedError")

_exception_ weaviate.exceptions.BackupCanceledError( _message=''_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#BackupCanceledError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.BackupCanceledError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Backup canceled Exception.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

_exception_ weaviate.exceptions.EmptyResponseError( _message=''_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#EmptyResponseError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.EmptyResponseError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Occurs when an HTTP request unexpectedly returns an empty response.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

weaviate.exceptions.EmptyResponseException [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.EmptyResponseException "Link to this definition")

alias of [`EmptyResponseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.EmptyResponseError "weaviate.exceptions.EmptyResponseError")

_exception_ weaviate.exceptions.MissingScopeError( _message=''_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#MissingScopeError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.MissingScopeError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Scope was not provided with client credential flow.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

weaviate.exceptions.MissingScopeException [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.MissingScopeException "Link to this definition")

alias of [`MissingScopeError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.MissingScopeError "weaviate.exceptions.MissingScopeError")

_exception_ weaviate.exceptions.AdditionalPropertiesError( _additional\_dict_, _additional\_dataclass_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#AdditionalPropertiesError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.AdditionalPropertiesError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Additional properties were provided multiple times.

Weaviate base exception initializer.

Parameters:

- **message** ( _str_) – An error message specific to the context in which the error occurred.

- **additional\_dict** ( _str_)

- **additional\_dataclass** ( _str_)


weaviate.exceptions.AdditionalPropertiesException [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.AdditionalPropertiesException "Link to this definition")

alias of [`AdditionalPropertiesError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.AdditionalPropertiesError "weaviate.exceptions.AdditionalPropertiesError")

_exception_ weaviate.exceptions.InvalidDataModelError( _type\__) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#InvalidDataModelError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.InvalidDataModelError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Is raised when the user provides a generic that is not supported.

Weaviate base exception initializer.

Parameters:

- **message** ( _str_) – An error message specific to the context in which the error occurred.

- **type\_** ( _str_)


Return type:

None

weaviate.exceptions.InvalidDataModelException [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.InvalidDataModelException "Link to this definition")

alias of [`InvalidDataModelError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.InvalidDataModelError "weaviate.exceptions.InvalidDataModelError")

_exception_ weaviate.exceptions.WeaviateStartUpError( _message=''_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateStartUpError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateStartUpError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Is raised if weaviate is not available on the given url+port.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

_exception_ weaviate.exceptions.WeaviateEmbeddedInvalidVersionError( _url_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateEmbeddedInvalidVersionError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateEmbeddedInvalidVersionError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Invalid version provided to Weaviate embedded.

Weaviate base exception initializer.

Parameters:

- **message** ( _str_) – An error message specific to the context in which the error occurred.

- **url** ( _str_)


weaviate.exceptions.WeaviateEmbeddedInvalidVersionException [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateEmbeddedInvalidVersionException "Link to this definition")

alias of [`WeaviateEmbeddedInvalidVersionError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateEmbeddedInvalidVersionError "weaviate.exceptions.WeaviateEmbeddedInvalidVersionError")

_exception_ weaviate.exceptions.WeaviateInvalidInputError( _message_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateInvalidInputError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateInvalidInputError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Is raised if the input to a function is invalid.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

weaviate.exceptions.WeaviateInvalidInputException [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateInvalidInputException "Link to this definition")

alias of [`WeaviateInvalidInputError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateInvalidInputError "weaviate.exceptions.WeaviateInvalidInputError")

_exception_ weaviate.exceptions.WeaviateQueryError( _message_, _protocol\_type_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateQueryError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateQueryError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Is raised if a query (either gRPC or GraphQL) to Weaviate fails in any way.

Weaviate base exception initializer.

Parameters:

- **message** ( _str_) – An error message specific to the context in which the error occurred.

- **protocol\_type** ( _str_)


_property_ error _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateQueryError.error "Link to this definition")weaviate.exceptions.WeaviateQueryException [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateQueryException "Link to this definition")

alias of [`WeaviateQueryError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateQueryError "weaviate.exceptions.WeaviateQueryError")

_exception_ weaviate.exceptions.WeaviateBatchError( _message_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateBatchError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBatchError "Link to this definition")

Bases: [`WeaviateQueryError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateQueryError "weaviate.exceptions.WeaviateQueryError")

Is raised if a gRPC batch query to Weaviate fails in any way.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

_exception_ weaviate.exceptions.WeaviateDeleteManyError( _message_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateDeleteManyError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateDeleteManyError "Link to this definition")

Bases: [`WeaviateQueryError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateQueryError "weaviate.exceptions.WeaviateQueryError")

Is raised if a gRPC delete many request to Weaviate fails in any way.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

_exception_ weaviate.exceptions.WeaviateTenantGetError( _message_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateTenantGetError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateTenantGetError "Link to this definition")

Bases: [`WeaviateQueryError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateQueryError "weaviate.exceptions.WeaviateQueryError")

Is raised if a gRPC tenant get request to Weaviate fails in any way.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

_exception_ weaviate.exceptions.WeaviateAddInvalidPropertyError( _message_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateAddInvalidPropertyError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateAddInvalidPropertyError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Is raised when adding an invalid new property.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

_exception_ weaviate.exceptions.WeaviateBatchValidationError( _message_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateBatchValidationError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBatchValidationError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Is raised when a batch validation error occurs.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

_exception_ weaviate.exceptions.WeaviateInsertInvalidPropertyError( _data_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateInsertInvalidPropertyError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateInsertInvalidPropertyError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Is raised when inserting an invalid property.

Weaviate base exception initializer.

Parameters:

- **message** ( _str_) – An error message specific to the context in which the error occurred.

- **data** ( _dict_)


_exception_ weaviate.exceptions.WeaviateGRPCUnavailableError( _weaviate\_version=''_, _grpc\_address=('notprovided',0)_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateGRPCUnavailableError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateGRPCUnavailableError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Is raised when a gRPC-backed query is made with no gRPC connection present.

Weaviate base exception initializer.

Parameters:

- **message** ( _str_) – An error message specific to the context in which the error occurred.

- **weaviate\_version** ( _str_)

- **grpc\_address** ( _Tuple_ _\[_ _str_ _,_ _int_ _\]_)


Return type:

None

weaviate.exceptions.WeaviateGrpcUnavailable [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateGrpcUnavailable "Link to this definition")

alias of [`WeaviateGRPCUnavailableError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateGRPCUnavailableError "weaviate.exceptions.WeaviateGRPCUnavailableError")

_exception_ weaviate.exceptions.WeaviateInsertManyAllFailedError( _message=''_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateInsertManyAllFailedError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateInsertManyAllFailedError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Is raised when all objects fail to be inserted.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

Return type:

None

_exception_ weaviate.exceptions.WeaviateClosedClientError [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateClosedClientError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateClosedClientError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Is raised when a client is closed and a method is called on it.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

Return type:

None

_exception_ weaviate.exceptions.WeaviateConnectionError( _message=''_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateConnectionError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateConnectionError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Is raised when the connection to Weaviate fails.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

Return type:

None

_exception_ weaviate.exceptions.WeaviateUnsupportedFeatureError( _feature_, _current_, _minimum_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateUnsupportedFeatureError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateUnsupportedFeatureError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Is raised when a client method tries to use a new feature with an old Weaviate version.

Weaviate base exception initializer.

Parameters:

- **message** ( _str_) – An error message specific to the context in which the error occurred.

- **feature** ( _str_)

- **current** ( _str_)

- **minimum** ( _str_)


Return type:

None

_exception_ weaviate.exceptions.WeaviateTimeoutError( _message=''_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateTimeoutError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateTimeoutError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Is raised when a request to Weaviate times out.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

Return type:

None

_exception_ weaviate.exceptions.WeaviateRetryError( _message_, _count_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateRetryError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateRetryError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Is raised when a request to Weaviate fails and is retried multiple times.

Weaviate base exception initializer.

Parameters:

- **message** ( _str_) – An error message specific to the context in which the error occurred.

- **count** ( _int_)


Return type:

None

_exception_ weaviate.exceptions.InsufficientPermissionsError( _res_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#InsufficientPermissionsError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.InsufficientPermissionsError "Link to this definition")

Bases: [`UnexpectedStatusCodeError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError")

Is raised when a request to Weaviate fails due to insufficient permissions.

Is raised in case the status code returned from Weaviate is not handled in the client implementation and suggests an error.

Custom code can act on the attributes:
\- status\_code
\- json

Parameters:

- **message** – An error message specific to the context, in which the error occurred.

- **response** – The request response of which the status code was unexpected.

- **res** ( _Response_ _\|_ _AioRpcError_ _\|_ _Call_)


Return type:

None

_exception_ weaviate.exceptions.WeaviateAgentsNotInstalledError [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateAgentsNotInstalledError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateAgentsNotInstalledError "Link to this definition")

Bases: [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError")

Error raised when trying to use Weaviate Agents without the required dependencies.

Weaviate base exception initializer.

Parameters:

**message** ( _str_) – An error message specific to the context in which the error occurred.

Return type:

None

_exception_ weaviate.exceptions.WeaviateProtobufIncompatibility( _pb_, _grpc_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/exceptions.html#WeaviateProtobufIncompatibility) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateProtobufIncompatibility "Link to this definition")

Bases: `Exception`

Parameters:

- **pb** ( _Version_)

- **grpc** ( _Version_)


Return type:

None

Versions[latest](https://weaviate-python-client.readthedocs.io/en/latest/weaviate.exceptions.html)**[stable](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html)**[v4.16.10](https://weaviate-python-client.readthedocs.io/en/v4.16.10/weaviate.exceptions.html)[v4.16.9](https://weaviate-python-client.readthedocs.io/en/v4.16.9/weaviate.exceptions.html)[v4.16.8](https://weaviate-python-client.readthedocs.io/en/v4.16.8/weaviate.exceptions.html)[v4.16.7](https://weaviate-python-client.readthedocs.io/en/v4.16.7/weaviate.exceptions.html)[v4.16.6](https://weaviate-python-client.readthedocs.io/en/v4.16.6/weaviate.exceptions.html)[v4.16.5](https://weaviate-python-client.readthedocs.io/en/v4.16.5/weaviate.exceptions.html)[v4.16.4](https://weaviate-python-client.readthedocs.io/en/v4.16.4/weaviate.exceptions.html)[v4.16.3](https://weaviate-python-client.readthedocs.io/en/v4.16.3/weaviate.exceptions.html)[v4.16.2](https://weaviate-python-client.readthedocs.io/en/v4.16.2/weaviate.exceptions.html)[v4.16.1](https://weaviate-python-client.readthedocs.io/en/v4.16.1/weaviate.exceptions.html)[v4.16.0](https://weaviate-python-client.readthedocs.io/en/v4.16.0/weaviate.exceptions.html)[v4.15.4](https://weaviate-python-client.readthedocs.io/en/v4.15.4/weaviate.exceptions.html)[v4.15.3](https://weaviate-python-client.readthedocs.io/en/v4.15.3/weaviate.exceptions.html)[v4.15.2](https://weaviate-python-client.readthedocs.io/en/v4.15.2/weaviate.exceptions.html)[v4.15.1](https://weaviate-python-client.readthedocs.io/en/v4.15.1/weaviate.exceptions.html)[v4.15.0](https://weaviate-python-client.readthedocs.io/en/v4.15.0/weaviate.exceptions.html)[v4.14.4](https://weaviate-python-client.readthedocs.io/en/v4.14.4/weaviate.exceptions.html)[v4.14.3](https://weaviate-python-client.readthedocs.io/en/v4.14.3/weaviate.exceptions.html)[v4.14.2](https://weaviate-python-client.readthedocs.io/en/v4.14.2/weaviate.exceptions.html)[v4.14.1](https://weaviate-python-client.readthedocs.io/en/v4.14.1/weaviate.exceptions.html)[v4.14.0](https://weaviate-python-client.readthedocs.io/en/v4.14.0/weaviate.exceptions.html)[v4.13.2](https://weaviate-python-client.readthedocs.io/en/v4.13.2/weaviate.exceptions.html)[v4.13.1](https://weaviate-python-client.readthedocs.io/en/v4.13.1/weaviate.exceptions.html)[v4.13.0](https://weaviate-python-client.readthedocs.io/en/v4.13.0/weaviate.exceptions.html)[v4.12.1](https://weaviate-python-client.readthedocs.io/en/v4.12.1/weaviate.exceptions.html)[v4.12.0](https://weaviate-python-client.readthedocs.io/en/v4.12.0/weaviate.exceptions.html)[v4.11.3](https://weaviate-python-client.readthedocs.io/en/v4.11.3/weaviate.exceptions.html)[v4.11.2](https://weaviate-python-client.readthedocs.io/en/v4.11.2/weaviate.exceptions.html)[v4.11.1](https://weaviate-python-client.readthedocs.io/en/v4.11.1/weaviate.exceptions.html)[v4.11.0](https://weaviate-python-client.readthedocs.io/en/v4.11.0/weaviate.exceptions.html)[v4.10.4](https://weaviate-python-client.readthedocs.io/en/v4.10.4/weaviate.exceptions.html)[v4.10.3](https://weaviate-python-client.readthedocs.io/en/v4.10.3/weaviate.exceptions.html)[v4.10.2](https://weaviate-python-client.readthedocs.io/en/v4.10.2/weaviate.exceptions.html)[v4.10.0](https://weaviate-python-client.readthedocs.io/en/v4.10.0/weaviate.exceptions.html)[v4.9.6](https://weaviate-python-client.readthedocs.io/en/v4.9.6/weaviate.exceptions.html)[v4.9.5](https://weaviate-python-client.readthedocs.io/en/v4.9.5/weaviate.exceptions.html)[v4.9.4](https://weaviate-python-client.readthedocs.io/en/v4.9.4/weaviate.exceptions.html)[v4.9.3](https://weaviate-python-client.readthedocs.io/en/v4.9.3/weaviate.exceptions.html)[v4.9.2](https://weaviate-python-client.readthedocs.io/en/v4.9.2/weaviate.exceptions.html)[v4.9.1](https://weaviate-python-client.readthedocs.io/en/v4.9.1/weaviate.exceptions.html)[v4.9.0](https://weaviate-python-client.readthedocs.io/en/v4.9.0/weaviate.exceptions.html)[v4.8.1](https://weaviate-python-client.readthedocs.io/en/v4.8.1/weaviate.exceptions.html)[v4.8.0](https://weaviate-python-client.readthedocs.io/en/v4.8.0/weaviate.exceptions.html)[v4.7.1](https://weaviate-python-client.readthedocs.io/en/v4.7.1/weaviate.exceptions.html)[v4.7.0](https://weaviate-python-client.readthedocs.io/en/v4.7.0/weaviate.exceptions.html)[v4.6.7](https://weaviate-python-client.readthedocs.io/en/v4.6.7/weaviate.exceptions.html)[v4.6.6](https://weaviate-python-client.readthedocs.io/en/v4.6.6/weaviate.exceptions.html)[v4.6.5](https://weaviate-python-client.readthedocs.io/en/v4.6.5/weaviate.exceptions.html)[v4.6.4](https://weaviate-python-client.readthedocs.io/en/v4.6.4/weaviate.exceptions.html)[v4.6.3](https://weaviate-python-client.readthedocs.io/en/v4.6.3/weaviate.exceptions.html)[v4.6.2](https://weaviate-python-client.readthedocs.io/en/v4.6.2/weaviate.exceptions.html)[v4.6.1](https://weaviate-python-client.readthedocs.io/en/v4.6.1/weaviate.exceptions.html)[v4.6.0](https://weaviate-python-client.readthedocs.io/en/v4.6.0/weaviate.exceptions.html)[v4.5.7](https://weaviate-python-client.readthedocs.io/en/v4.5.7/weaviate.exceptions.html)[v4.5.6](https://weaviate-python-client.readthedocs.io/en/v4.5.6/weaviate.exceptions.html)[v4.5.5](https://weaviate-python-client.readthedocs.io/en/v4.5.5/weaviate.exceptions.html)[v4.5.4](https://weaviate-python-client.readthedocs.io/en/v4.5.4/weaviate.exceptions.html)[v4.5.3](https://weaviate-python-client.readthedocs.io/en/v4.5.3/weaviate.exceptions.html)[v4.5.2](https://weaviate-python-client.readthedocs.io/en/v4.5.2/weaviate.exceptions.html)[v4.5.1](https://weaviate-python-client.readthedocs.io/en/v4.5.1/weaviate.exceptions.html)[v4.5.0](https://weaviate-python-client.readthedocs.io/en/v4.5.0/weaviate.exceptions.html)[v4.4.4](https://weaviate-python-client.readthedocs.io/en/v4.4.4/weaviate.exceptions.html)[v4.4.3](https://weaviate-python-client.readthedocs.io/en/v4.4.3/weaviate.exceptions.html)[v4.4.2](https://weaviate-python-client.readthedocs.io/en/v4.4.2/weaviate.exceptions.html)[v4.4.1](https://weaviate-python-client.readthedocs.io/en/v4.4.1/weaviate.exceptions.html)[v4.4.0](https://weaviate-python-client.readthedocs.io/en/v4.4.0/weaviate.exceptions.html)[v3.26.2](https://weaviate-python-client.readthedocs.io/en/v3.26.2/weaviate.exceptions.html)[v3.26.1](https://weaviate-python-client.readthedocs.io/en/v3.26.1/weaviate.exceptions.html)[v3.26.0](https://weaviate-python-client.readthedocs.io/en/v3.26.0/weaviate.exceptions.html)[v3.25.3](https://weaviate-python-client.readthedocs.io/en/v3.25.3/weaviate.exceptions.html)[v3.25.2](https://weaviate-python-client.readthedocs.io/en/v3.25.2/weaviate.exceptions.html)[v3.23.0](https://weaviate-python-client.readthedocs.io/en/v3.23.0/weaviate.exceptions.html)[v3.22.1](https://weaviate-python-client.readthedocs.io/en/v3.22.1/weaviate.exceptions.html)[v3.22.0](https://weaviate-python-client.readthedocs.io/en/v3.22.0/weaviate.exceptions.html)[v3.21.0](https://weaviate-python-client.readthedocs.io/en/v3.21.0/weaviate.exceptions.html)[v3.20.1](https://weaviate-python-client.readthedocs.io/en/v3.20.1/weaviate.exceptions.html)[v3.20.0](https://weaviate-python-client.readthedocs.io/en/v3.20.0/weaviate.exceptions.html)[v3.19.2](https://weaviate-python-client.readthedocs.io/en/v3.19.2/weaviate.exceptions.html)[v3.19.1](https://weaviate-python-client.readthedocs.io/en/v3.19.1/weaviate.exceptions.html)[v3.19.0](https://weaviate-python-client.readthedocs.io/en/v3.19.0/weaviate.exceptions.html)[v3.18.0](https://weaviate-python-client.readthedocs.io/en/v3.18.0/weaviate.exceptions.html)[v3.15.6](https://weaviate-python-client.readthedocs.io/en/v3.15.6/weaviate.exceptions.html)[v3.15.5](https://weaviate-python-client.readthedocs.io/en/v3.15.5/weaviate.exceptions.html)[v3.15.4](https://weaviate-python-client.readthedocs.io/en/v3.15.4/weaviate.exceptions.html)[v3.15.3](https://weaviate-python-client.readthedocs.io/en/v3.15.3/weaviate.exceptions.html)[v3.15.2](https://weaviate-python-client.readthedocs.io/en/v3.15.2/weaviate.exceptions.html)[v3.15.1](https://weaviate-python-client.readthedocs.io/en/v3.15.1/weaviate.exceptions.html)[v3.15.0](https://weaviate-python-client.readthedocs.io/en/v3.15.0/weaviate.exceptions.html)[v3.14.0](https://weaviate-python-client.readthedocs.io/en/v3.14.0/weaviate.exceptions.html)[v3.13.0](https://weaviate-python-client.readthedocs.io/en/v3.13.0/weaviate.exceptions.html)[v3.12.0\_a](https://weaviate-python-client.readthedocs.io/en/v3.12.0_a/weaviate.exceptions.html)[v3.11.0](https://weaviate-python-client.readthedocs.io/en/v3.11.0/weaviate.exceptions.html)[v3.10.0](https://weaviate-python-client.readthedocs.io/en/v3.10.0/weaviate.exceptions.html)[v3.9.0](https://weaviate-python-client.readthedocs.io/en/v3.9.0/weaviate.exceptions.html)[v3.8.0](https://weaviate-python-client.readthedocs.io/en/v3.8.0/weaviate.exceptions.html)[v3.7.0](https://weaviate-python-client.readthedocs.io/en/v3.7.0/weaviate.exceptions.html)[v3.6.0](https://weaviate-python-client.readthedocs.io/en/v3.6.0/weaviate.exceptions.html)[v3.5.1](https://weaviate-python-client.readthedocs.io/en/v3.5.1/weaviate.exceptions.html)[v3.5.0](https://weaviate-python-client.readthedocs.io/en/v3.5.0/weaviate.exceptions.html)[v3.4.1](https://weaviate-python-client.readthedocs.io/en/v3.4.1/weaviate.exceptions.html)[v3.4.0](https://weaviate-python-client.readthedocs.io/en/v3.4.0/weaviate.exceptions.html)[v3.3.3](https://weaviate-python-client.readthedocs.io/en/v3.3.3/weaviate.exceptions.html)[v3.3.2](https://weaviate-python-client.readthedocs.io/en/v3.3.2/weaviate.exceptions.html)[v3.3.1](https://weaviate-python-client.readthedocs.io/en/v3.3.1/weaviate.exceptions.html)[v3.3.0](https://weaviate-python-client.readthedocs.io/en/v3.3.0/weaviate.exceptions.html)[v3.2.5](https://weaviate-python-client.readthedocs.io/en/v3.2.5/weaviate.exceptions.html)[v3.2.4](https://weaviate-python-client.readthedocs.io/en/v3.2.4/weaviate.exceptions.html)[v3.2.3](https://weaviate-python-client.readthedocs.io/en/v3.2.3/weaviate.exceptions.html)[v3.2.2](https://weaviate-python-client.readthedocs.io/en/v3.2.2/weaviate.exceptions.html)[v3.2.1](https://weaviate-python-client.readthedocs.io/en/v3.2.1/weaviate.exceptions.html)[v3.2.0](https://weaviate-python-client.readthedocs.io/en/v3.2.0/weaviate.exceptions.html)[v3.1.1](https://weaviate-python-client.readthedocs.io/en/v3.1.1/weaviate.exceptions.html)[v3.1.0](https://weaviate-python-client.readthedocs.io/en/v3.1.0/weaviate.exceptions.html)[v3.0.0](https://weaviate-python-client.readthedocs.io/en/v3.0.0/weaviate.exceptions.html)On Read the Docs[Project Home](https://app.readthedocs.org/projects/weaviate-python-client/?utm_source=weaviate-python-client&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/weaviate-python-client/builds/?utm_source=weaviate-python-client&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=weaviate-python-client&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=weaviate-python-client&utm_content=flyout)