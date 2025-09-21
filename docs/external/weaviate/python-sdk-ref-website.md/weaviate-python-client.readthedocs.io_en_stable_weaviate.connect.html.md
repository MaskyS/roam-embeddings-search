---
url: "https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html"
title: "weaviate.connect — Weaviate Python Client 4.16.10 documentation"
---

- [Home](https://weaviate-python-client.readthedocs.io/en/stable/index.html)
- [Weaviate Library](https://weaviate-python-client.readthedocs.io/en/stable/modules.html)
- [weaviate](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html)
- weaviate.connect
- [View page source](https://weaviate-python-client.readthedocs.io/en/stable/_sources/weaviate.connect.rst.txt)

* * *

# weaviate.connect [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html\#module-weaviate.connect "Link to this heading")

Module communication to a Weaviate instance. Used to connect to Weaviate and run REST requests.

weaviate.connect.ConnectionV4 [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ConnectionV4 "Link to this definition")

alias of `ConnectionAsync`

_pydanticmodel_ weaviate.connect.ConnectionParams [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/base.html#ConnectionParams) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ConnectionParams "Link to this definition")

Bases: `BaseModel`

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ grpc _: [ProtocolParams](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ProtocolParams "weaviate.connect.base.ProtocolParams")_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ConnectionParams.grpc "Link to this definition")Validated by:

- `_check_port_collision`


_field_ http _: [ProtocolParams](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ProtocolParams "weaviate.connect.base.ProtocolParams")_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ConnectionParams.http "Link to this definition")Validated by:

- `_check_port_collision`


_classmethod_ from\_params( _http\_host_, _http\_port_, _http\_secure_, _grpc\_host_, _grpc\_port_, _grpc\_secure_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/base.html#ConnectionParams.from_params) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ConnectionParams.from_params "Link to this definition")Parameters:

- **http\_host** ( _str_)

- **http\_port** ( _int_)

- **http\_secure** ( _bool_)

- **grpc\_host** ( _str_)

- **grpc\_port** ( _int_)

- **grpc\_secure** ( _bool_)


Return type:

[_ConnectionParams_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ConnectionParams "weaviate.connect.base.ConnectionParams")

_classmethod_ from\_url( _url_, _grpc\_port_, _grpc\_secure=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/base.html#ConnectionParams.from_url) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ConnectionParams.from_url "Link to this definition")Parameters:

- **url** ( _str_)

- **grpc\_port** ( _int_)

- **grpc\_secure** ( _bool_)


Return type:

[_ConnectionParams_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ConnectionParams "weaviate.connect.base.ConnectionParams")

_pydanticmodel_ weaviate.connect.ProtocolParams [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/connect/base.html#ProtocolParams) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ProtocolParams "Link to this definition")

Bases: `BaseModel`

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ host _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ProtocolParams.host "Link to this definition")Validated by:

- `_check_host`


_field_ port _:int_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ProtocolParams.port "Link to this definition")Validated by:

- `_check_port`


_field_ secure _:bool_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html#weaviate.connect.ProtocolParams.secure "Link to this definition")

Versions[latest](https://weaviate-python-client.readthedocs.io/en/latest/weaviate.connect.html)**[stable](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.connect.html)**[v4.16.10](https://weaviate-python-client.readthedocs.io/en/v4.16.10/weaviate.connect.html)[v4.16.9](https://weaviate-python-client.readthedocs.io/en/v4.16.9/weaviate.connect.html)[v4.16.8](https://weaviate-python-client.readthedocs.io/en/v4.16.8/weaviate.connect.html)[v4.16.7](https://weaviate-python-client.readthedocs.io/en/v4.16.7/weaviate.connect.html)[v4.16.6](https://weaviate-python-client.readthedocs.io/en/v4.16.6/weaviate.connect.html)[v4.16.5](https://weaviate-python-client.readthedocs.io/en/v4.16.5/weaviate.connect.html)[v4.16.4](https://weaviate-python-client.readthedocs.io/en/v4.16.4/weaviate.connect.html)[v4.16.3](https://weaviate-python-client.readthedocs.io/en/v4.16.3/weaviate.connect.html)[v4.16.2](https://weaviate-python-client.readthedocs.io/en/v4.16.2/weaviate.connect.html)[v4.16.1](https://weaviate-python-client.readthedocs.io/en/v4.16.1/weaviate.connect.html)[v4.16.0](https://weaviate-python-client.readthedocs.io/en/v4.16.0/weaviate.connect.html)[v4.15.4](https://weaviate-python-client.readthedocs.io/en/v4.15.4/weaviate.connect.html)[v4.15.3](https://weaviate-python-client.readthedocs.io/en/v4.15.3/weaviate.connect.html)[v4.15.2](https://weaviate-python-client.readthedocs.io/en/v4.15.2/weaviate.connect.html)[v4.15.1](https://weaviate-python-client.readthedocs.io/en/v4.15.1/weaviate.connect.html)[v4.15.0](https://weaviate-python-client.readthedocs.io/en/v4.15.0/weaviate.connect.html)[v4.14.4](https://weaviate-python-client.readthedocs.io/en/v4.14.4/weaviate.connect.html)[v4.14.3](https://weaviate-python-client.readthedocs.io/en/v4.14.3/weaviate.connect.html)[v4.14.2](https://weaviate-python-client.readthedocs.io/en/v4.14.2/weaviate.connect.html)[v4.14.1](https://weaviate-python-client.readthedocs.io/en/v4.14.1/weaviate.connect.html)[v4.14.0](https://weaviate-python-client.readthedocs.io/en/v4.14.0/weaviate.connect.html)[v4.13.2](https://weaviate-python-client.readthedocs.io/en/v4.13.2/weaviate.connect.html)[v4.13.1](https://weaviate-python-client.readthedocs.io/en/v4.13.1/weaviate.connect.html)[v4.13.0](https://weaviate-python-client.readthedocs.io/en/v4.13.0/weaviate.connect.html)[v4.12.1](https://weaviate-python-client.readthedocs.io/en/v4.12.1/weaviate.connect.html)[v4.12.0](https://weaviate-python-client.readthedocs.io/en/v4.12.0/weaviate.connect.html)[v4.11.3](https://weaviate-python-client.readthedocs.io/en/v4.11.3/weaviate.connect.html)[v4.11.2](https://weaviate-python-client.readthedocs.io/en/v4.11.2/weaviate.connect.html)[v4.11.1](https://weaviate-python-client.readthedocs.io/en/v4.11.1/weaviate.connect.html)[v4.11.0](https://weaviate-python-client.readthedocs.io/en/v4.11.0/weaviate.connect.html)[v4.10.4](https://weaviate-python-client.readthedocs.io/en/v4.10.4/weaviate.connect.html)[v4.10.3](https://weaviate-python-client.readthedocs.io/en/v4.10.3/weaviate.connect.html)[v4.10.2](https://weaviate-python-client.readthedocs.io/en/v4.10.2/weaviate.connect.html)[v4.10.0](https://weaviate-python-client.readthedocs.io/en/v4.10.0/weaviate.connect.html)[v4.9.6](https://weaviate-python-client.readthedocs.io/en/v4.9.6/weaviate.connect.html)[v4.9.5](https://weaviate-python-client.readthedocs.io/en/v4.9.5/weaviate.connect.html)[v4.9.4](https://weaviate-python-client.readthedocs.io/en/v4.9.4/weaviate.connect.html)[v4.9.3](https://weaviate-python-client.readthedocs.io/en/v4.9.3/weaviate.connect.html)[v4.9.2](https://weaviate-python-client.readthedocs.io/en/v4.9.2/weaviate.connect.html)[v4.9.1](https://weaviate-python-client.readthedocs.io/en/v4.9.1/weaviate.connect.html)[v4.9.0](https://weaviate-python-client.readthedocs.io/en/v4.9.0/weaviate.connect.html)[v4.8.1](https://weaviate-python-client.readthedocs.io/en/v4.8.1/weaviate.connect.html)[v4.8.0](https://weaviate-python-client.readthedocs.io/en/v4.8.0/weaviate.connect.html)[v4.7.1](https://weaviate-python-client.readthedocs.io/en/v4.7.1/weaviate.connect.html)[v4.7.0](https://weaviate-python-client.readthedocs.io/en/v4.7.0/weaviate.connect.html)[v4.6.7](https://weaviate-python-client.readthedocs.io/en/v4.6.7/weaviate.connect.html)[v4.6.6](https://weaviate-python-client.readthedocs.io/en/v4.6.6/weaviate.connect.html)[v4.6.5](https://weaviate-python-client.readthedocs.io/en/v4.6.5/weaviate.connect.html)[v4.6.4](https://weaviate-python-client.readthedocs.io/en/v4.6.4/weaviate.connect.html)[v4.6.3](https://weaviate-python-client.readthedocs.io/en/v4.6.3/weaviate.connect.html)[v4.6.2](https://weaviate-python-client.readthedocs.io/en/v4.6.2/weaviate.connect.html)[v4.6.1](https://weaviate-python-client.readthedocs.io/en/v4.6.1/weaviate.connect.html)[v4.6.0](https://weaviate-python-client.readthedocs.io/en/v4.6.0/weaviate.connect.html)[v4.5.7](https://weaviate-python-client.readthedocs.io/en/v4.5.7/weaviate.connect.html)[v4.5.6](https://weaviate-python-client.readthedocs.io/en/v4.5.6/weaviate.connect.html)[v4.5.5](https://weaviate-python-client.readthedocs.io/en/v4.5.5/weaviate.connect.html)[v4.5.4](https://weaviate-python-client.readthedocs.io/en/v4.5.4/weaviate.connect.html)[v4.5.3](https://weaviate-python-client.readthedocs.io/en/v4.5.3/weaviate.connect.html)[v4.5.2](https://weaviate-python-client.readthedocs.io/en/v4.5.2/weaviate.connect.html)[v4.5.1](https://weaviate-python-client.readthedocs.io/en/v4.5.1/weaviate.connect.html)[v4.5.0](https://weaviate-python-client.readthedocs.io/en/v4.5.0/weaviate.connect.html)[v4.4.4](https://weaviate-python-client.readthedocs.io/en/v4.4.4/weaviate.connect.html)[v4.4.3](https://weaviate-python-client.readthedocs.io/en/v4.4.3/weaviate.connect.html)[v4.4.2](https://weaviate-python-client.readthedocs.io/en/v4.4.2/weaviate.connect.html)[v4.4.1](https://weaviate-python-client.readthedocs.io/en/v4.4.1/weaviate.connect.html)[v4.4.0](https://weaviate-python-client.readthedocs.io/en/v4.4.0/weaviate.connect.html)[v3.26.2](https://weaviate-python-client.readthedocs.io/en/v3.26.2/weaviate.connect.html)[v3.26.1](https://weaviate-python-client.readthedocs.io/en/v3.26.1/weaviate.connect.html)[v3.26.0](https://weaviate-python-client.readthedocs.io/en/v3.26.0/weaviate.connect.html)[v3.25.3](https://weaviate-python-client.readthedocs.io/en/v3.25.3/weaviate.connect.html)[v3.25.2](https://weaviate-python-client.readthedocs.io/en/v3.25.2/weaviate.connect.html)[v3.23.0](https://weaviate-python-client.readthedocs.io/en/v3.23.0/weaviate.connect.html)[v3.22.1](https://weaviate-python-client.readthedocs.io/en/v3.22.1/weaviate.connect.html)[v3.22.0](https://weaviate-python-client.readthedocs.io/en/v3.22.0/weaviate.connect.html)[v3.21.0](https://weaviate-python-client.readthedocs.io/en/v3.21.0/weaviate.connect.html)[v3.20.1](https://weaviate-python-client.readthedocs.io/en/v3.20.1/weaviate.connect.html)[v3.20.0](https://weaviate-python-client.readthedocs.io/en/v3.20.0/weaviate.connect.html)[v3.19.2](https://weaviate-python-client.readthedocs.io/en/v3.19.2/weaviate.connect.html)[v3.19.1](https://weaviate-python-client.readthedocs.io/en/v3.19.1/weaviate.connect.html)[v3.19.0](https://weaviate-python-client.readthedocs.io/en/v3.19.0/weaviate.connect.html)[v3.18.0](https://weaviate-python-client.readthedocs.io/en/v3.18.0/weaviate.connect.html)[v3.15.6](https://weaviate-python-client.readthedocs.io/en/v3.15.6/weaviate.connect.html)[v3.15.5](https://weaviate-python-client.readthedocs.io/en/v3.15.5/weaviate.connect.html)[v3.15.4](https://weaviate-python-client.readthedocs.io/en/v3.15.4/weaviate.connect.html)[v3.15.3](https://weaviate-python-client.readthedocs.io/en/v3.15.3/weaviate.connect.html)[v3.15.2](https://weaviate-python-client.readthedocs.io/en/v3.15.2/weaviate.connect.html)[v3.15.1](https://weaviate-python-client.readthedocs.io/en/v3.15.1/weaviate.connect.html)[v3.15.0](https://weaviate-python-client.readthedocs.io/en/v3.15.0/weaviate.connect.html)[v3.14.0](https://weaviate-python-client.readthedocs.io/en/v3.14.0/weaviate.connect.html)[v3.13.0](https://weaviate-python-client.readthedocs.io/en/v3.13.0/weaviate.connect.html)[v3.12.0\_a](https://weaviate-python-client.readthedocs.io/en/v3.12.0_a/weaviate.connect.html)[v3.11.0](https://weaviate-python-client.readthedocs.io/en/v3.11.0/weaviate.connect.html)[v3.10.0](https://weaviate-python-client.readthedocs.io/en/v3.10.0/weaviate.connect.html)[v3.9.0](https://weaviate-python-client.readthedocs.io/en/v3.9.0/weaviate.connect.html)[v3.8.0](https://weaviate-python-client.readthedocs.io/en/v3.8.0/weaviate.connect.html)[v3.7.0](https://weaviate-python-client.readthedocs.io/en/v3.7.0/weaviate.connect.html)[v3.6.0](https://weaviate-python-client.readthedocs.io/en/v3.6.0/weaviate.connect.html)[v3.5.1](https://weaviate-python-client.readthedocs.io/en/v3.5.1/weaviate.connect.html)[v3.5.0](https://weaviate-python-client.readthedocs.io/en/v3.5.0/weaviate.connect.html)[v3.4.1](https://weaviate-python-client.readthedocs.io/en/v3.4.1/weaviate.connect.html)[v3.4.0](https://weaviate-python-client.readthedocs.io/en/v3.4.0/weaviate.connect.html)[v3.3.3](https://weaviate-python-client.readthedocs.io/en/v3.3.3/weaviate.connect.html)[v3.3.2](https://weaviate-python-client.readthedocs.io/en/v3.3.2/weaviate.connect.html)[v3.3.1](https://weaviate-python-client.readthedocs.io/en/v3.3.1/weaviate.connect.html)[v3.3.0](https://weaviate-python-client.readthedocs.io/en/v3.3.0/weaviate.connect.html)[v3.2.5](https://weaviate-python-client.readthedocs.io/en/v3.2.5/weaviate.connect.html)[v3.2.4](https://weaviate-python-client.readthedocs.io/en/v3.2.4/weaviate.connect.html)[v3.2.3](https://weaviate-python-client.readthedocs.io/en/v3.2.3/weaviate.connect.html)[v3.2.2](https://weaviate-python-client.readthedocs.io/en/v3.2.2/weaviate.connect.html)[v3.2.1](https://weaviate-python-client.readthedocs.io/en/v3.2.1/weaviate.connect.html)[v3.2.0](https://weaviate-python-client.readthedocs.io/en/v3.2.0/weaviate.connect.html)[v3.1.1](https://weaviate-python-client.readthedocs.io/en/v3.1.1/weaviate.connect.html)[v3.1.0](https://weaviate-python-client.readthedocs.io/en/v3.1.0/weaviate.connect.html)[v3.0.0](https://weaviate-python-client.readthedocs.io/en/v3.0.0/weaviate.connect.html)On Read the Docs[Project Home](https://app.readthedocs.org/projects/weaviate-python-client/?utm_source=weaviate-python-client&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/weaviate-python-client/builds/?utm_source=weaviate-python-client&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=weaviate-python-client&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=weaviate-python-client&utm_content=flyout)