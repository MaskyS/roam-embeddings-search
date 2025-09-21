When [creating a property](https://docs.weaviate.io/weaviate/manage-collections/collection-operations#add-a-property), you must specify a data type. Weaviate accepts the following types.

## Available data types [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#available-data-types "Direct link to Available data types")

Array types

Arrays of a data type are specified by adding `[]` to the type (e.g. `text` ➡ `text[]`). Note that not all data types support arrays.

| Name | Exact type | Formatting | Array ( `[]`) available (example) | Note |
| --- | --- | --- | --- | --- |
| [text](https://docs.weaviate.io/weaviate/config-refs/datatypes#text) | string | `string` | ✅ `["string one", "string two"]` |  |
| [boolean](https://docs.weaviate.io/weaviate/config-refs/datatypes#boolean--int--number) | boolean | `true`/ `false` | ✅ `[true, false]` |  |
| [int](https://docs.weaviate.io/weaviate/config-refs/datatypes#boolean--int--number) | int64 (see [notes](https://docs.weaviate.io/weaviate/config-refs/datatypes#note-graphql-and-int64)) | `123` | ✅ `[123, -456]` |  |
| [number](https://docs.weaviate.io/weaviate/config-refs/datatypes#boolean--int--number) | float64 | `0.0` | ✅ `[0.0, 1.1]` |  |
| [date](https://docs.weaviate.io/weaviate/config-refs/datatypes#date) | string | [more info](https://docs.weaviate.io/weaviate/config-refs/datatypes#date) | ✅ |  |
| [uuid](https://docs.weaviate.io/weaviate/config-refs/datatypes#uuid) | string | `"c8f8176c-6f9b-5461-8ab3-f3c7ce8c2f5c"` | ✅ `["c8f8176c-6f9b-5461-8ab3-f3c7ce8c2f5c", "36ddd591-2dee-4e7e-a3cc-eb86d30a4303"]` |  |
| [geoCoordinates](https://docs.weaviate.io/weaviate/config-refs/datatypes#geocoordinates) | string | [more info](https://docs.weaviate.io/weaviate/config-refs/datatypes#geocoordinates) | ❌ |  |
| [phoneNumber](https://docs.weaviate.io/weaviate/config-refs/datatypes#phonenumber) | string | [more info](https://docs.weaviate.io/weaviate/config-refs/datatypes#phonenumber) | ❌ |  |
| [blob](https://docs.weaviate.io/weaviate/config-refs/datatypes#blob) | base64 encoded string | [more info](https://docs.weaviate.io/weaviate/config-refs/datatypes#blob) | ❌ |  |
| [object](https://docs.weaviate.io/weaviate/config-refs/datatypes#object) | object | `{"child": "I'm nested!"}` | ✅ `[{"child": "I'm nested!"}, {"child": "I'm nested too!"}` | Available from `1.22` |\
| [_cross reference_](https://docs.weaviate.io/weaviate/config-refs/datatypes#cross-reference) | string | [more info](https://docs.weaviate.io/weaviate/config-refs/datatypes#cross-reference) | ❌ |  |\
\
Deprecated types\
\
| Name | Exact type | Formatting | Array available (example) | Deprecated from |\
| --- | --- | --- | --- | --- |\
| string | string | `"string"` | ✅ `["string", "second string"]` | `v1.19` |\
\
Further details on each data type are provided below.\
\
## `text` [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#text "Direct link to text")\
\
Use this type for any text data.\
\
- Properties with the `text` type is used for vectorization and keyword search unless specified otherwise [in the property settings](https://docs.weaviate.io/weaviate/manage-collections/vector-config#property-level-settings).\
- If using [named vectors](https://docs.weaviate.io/weaviate/concepts/data#multiple-vector-embeddings-named-vectors), the property vectorization is defined in the [named vector definition](https://docs.weaviate.io/weaviate/manage-collections/vector-config#define-named-vectors).\
- Text properties are tokenized prior to being indexed for keyword/BM25 searches. See [collection definition: tokenization](https://docs.weaviate.io/weaviate/config-refs/collections#tokenization) for more information.\
\
`string` is deprecated\
\
Prior to `v1.19`, Weaviate supported an additional datatype `string`, which was differentiated by tokenization behavior to `text`. As of `v1.19`, this type is deprecated and will be removed in a future release.\
\
Use `text` instead of `string`. `text` supports the tokenization options that are available through `string`.\
\
### Examples [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#examples "Direct link to Examples")\
\
#### Property definition [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#property-definition "Direct link to Property definition")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
from weaviate.classes.config import Property, DataType, Configure, Tokenization\
\
# Create collection\
my_collection = client.collections.create(\
    name="Movie",\
    properties=[\
        Property(\
            name="title", data_type=DataType.TEXT, tokenization=Tokenization.LOWERCASE\
        ),\
        Property(\
            name="movie_id", data_type=DataType.TEXT, tokenization=Tokenization.FIELD\
        ),\
        Property(\
            name="genres", data_type=DataType.TEXT_ARRAY, tokenization=Tokenization.WORD\
        ),\
    ],\
    # Other properties are omitted for brevity\
)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
#### Object insertion [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#object-insertion "Direct link to Object insertion")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
# Create an object\
example_object = {\
    "title": "Rogue One",\
    "movie_id": "ro123456",\
    "genres": ["Action", "Adventure", "Sci-Fi"],\
}\
\
obj_uuid = my_collection.data.insert(example_object)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
## `boolean` / `int` / `number` [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#boolean--int--number "Direct link to boolean--int--number")\
\
The `boolean`, `int`, and `number` types are used for storing boolean, integer, and floating-point numbers, respectively.\
\
### Examples [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#examples-1 "Direct link to Examples")\
\
#### Property definition [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#property-definition-1 "Direct link to Property definition")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
from weaviate.classes.config import Property, DataType\
\
# Create collection\
my_collection = client.collections.create(\
    name="Product",\
    properties=[\
        Property(name="name", data_type=DataType.TEXT),\
        Property(name="price", data_type=DataType.NUMBER),\
        Property(name="stock_quantity", data_type=DataType.INT),\
        Property(name="is_on_sale", data_type=DataType.BOOL),\
        Property(name="customer_ratings", data_type=DataType.NUMBER_ARRAY),\
    ],\
    # Other properties are omitted for brevity\
)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
#### Object insertion [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#object-insertion-1 "Direct link to Object insertion")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
# Create an object\
example_object = {\
    "name": "Wireless Headphones",\
    "price": 95.50,\
    "stock_quantity": 100,\
    "is_on_sale": True,\
    "customer_ratings": [4.5, 4.8, 4.2],\
}\
\
obj_uuid = my_collection.data.insert(example_object)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
### Note: GraphQL and `int64` [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#note-graphql-and-int64 "Direct link to note-graphql-and-int64")\
\
Although Weaviate supports `int64`, GraphQL currently only supports `int32`, and does not support `int64`. This means that currently _integer_ data fields in Weaviate with integer values larger than `int32`, will not be returned using GraphQL queries. We are working on solving this [issue](https://github.com/weaviate/weaviate/issues/1563). As current workaround is to use a `string` instead.\
\
## `date` [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#date "Direct link to date")\
\
A `date` in Weaviate is represented by an [RFC 3339](https://datatracker.ietf.org/doc/rfc3339/) timestamp in the `date-time` format. The timestamp includes the time and an offset.\
\
For example:\
\
- `"1985-04-12T23:20:50.52Z"`\
- `"1996-12-19T16:39:57-08:00"`\
- `"1937-01-01T12:00:27.87+00:20"`\
\
To add a list of dates as a single entity, use an array of `date-time` formatted strings. For example: `["1985-04-12T23:20:50.52Z", "1937-01-01T12:00:27.87+00:20"]`\
\
In specific client libraries, you may be able to use the native date object as shown in the following examples.\
\
### Examples [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#examples-2 "Direct link to Examples")\
\
#### Property definition [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#property-definition-2 "Direct link to Property definition")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
from weaviate.classes.config import Property, DataType\
from datetime import datetime, timezone\
\
# Create collection\
my_collection = client.collections.create(\
    name="ConcertTour",\
    properties=[\
        Property(name="artist", data_type=DataType.TEXT),\
        Property(name="tour_name", data_type=DataType.TEXT),\
        Property(name="tour_start", data_type=DataType.DATE),\
        Property(name="tour_dates", data_type=DataType.DATE_ARRAY),\
    ],\
    # Other properties are omitted for brevity\
)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
#### Object insertion [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#object-insertion-2 "Direct link to Object insertion")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
# Create an object\
# In Python, you can use the RFC 3339 format or a datetime object (preferably with a timezone)\
example_object = {\
    "artist": "Taylor Swift",\
    "tour_name": "Eras Tour",\
    "tour_start": datetime(2023, 3, 17).replace(tzinfo=timezone.utc),\
    "tour_dates": [\
        # Use `datetime` objects with a timezone\
        datetime(2023, 3, 17).replace(tzinfo=timezone.utc),\
        datetime(2023, 3, 18).replace(tzinfo=timezone.utc),\
        # .. more dates\
        # Or use RFC 3339 format\
        "2024-12-07T00:00:00Z",\
        "2024-12-08T00:00:00Z",\
    ],\
}\
\
obj_uuid = my_collection.data.insert(example_object)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
## `uuid` [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#uuid "Direct link to uuid")\
\
The dedicated `uuid` and `uuid[]` data types efficiently store [UUIDs](https://en.wikipedia.org/wiki/Universally_unique_identifier).\
\
- Each `uuid` is a 128-bit (16-byte) number.\
- The filterable index uses roaring bitmaps.\
\
Aggregate/sort currently not possible\
\
It is currently not possible to aggregate or sort by `uuid` or `uuid[]` types.\
\
### Examples [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#examples-3 "Direct link to Examples")\
\
#### Property definition [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#property-definition-3 "Direct link to Property definition")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
from weaviate.classes.config import Property, DataType\
from weaviate.util import generate_uuid5\
\
# Create collection\
my_collection = client.collections.create(\
    name="Movie",\
    properties=[\
        Property(name="title", data_type=DataType.TEXT),\
        Property(name="movie_uuid", data_type=DataType.UUID),\
        Property(name="related_movie_uuids", data_type=DataType.UUID_ARRAY),\
    ],\
    # Other properties are omitted for brevity\
)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
#### Object insertion [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#object-insertion-3 "Direct link to Object insertion")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
# Create an object\
example_object = {\
    "title": "The Matrix",\
    "movie_uuid": generate_uuid5("The Matrix"),\
    "related_movie_uuids": [\
        generate_uuid5("The Matrix Reloaded"),\
        generate_uuid5("The Matrix Revolutions"),\
        generate_uuid5("Matrix Resurrections"),\
    ],\
}\
\
obj_uuid = my_collection.data.insert(example_object)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
## `geoCoordinates` [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#geocoordinates "Direct link to geocoordinates")\
\
Geo coordinates can be used to find objects in a radius around a query location. A geo coordinate value stored as a float, and is processed as [decimal degree](https://en.wikipedia.org/wiki/Decimal_degrees) according to the [ISO standard](https://www.iso.org/standard/39242.html#:~:text=For%20computer%20data%20interchange%20of,minutes%2C%20seconds%20and%20decimal%20seconds).\
\
To supply a `geoCoordinates` property, specify the `latitude` and `longitude` as floating point decimal degrees.\
\
### Examples [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#examples-4 "Direct link to Examples")\
\
#### Property definition [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#property-definition-4 "Direct link to Property definition")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
from weaviate.classes.config import Property, DataType\
from weaviate.classes.data import GeoCoordinate\
\
# Create collection\
my_collection = client.collections.create(\
    name="City",\
    properties=[\
        Property(name="name", data_type=DataType.TEXT),\
        Property(name="location", data_type=DataType.GEO_COORDINATES),\
    ],\
    # Other properties are omitted for brevity\
)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
#### Object insertion [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#object-insertion-4 "Direct link to Object insertion")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
# Create an object\
example_object = {\
    "name": "Sydney",\
    "location": GeoCoordinate(latitude=-33.8688, longitude=151.2093),\
}\
\
obj_uuid = my_collection.data.insert(example_object)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
Limitations\
\
Currently, geo-coordinate filtering is limited to the nearest 800 results from the source location, which will be further reduced by any other filter conditions and search parameters.\
\
If you plan on a densely populated dataset, consider using another strategy such as geo-hashing into a `text` datatype, and filtering further, such as with a `ContainsAny` filter.\
\
## `phoneNumber` [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#phonenumber "Direct link to phonenumber")\
\
A `phoneNumber` input will be normalized and validated, unlike the single fields as `number` and `string`. The data field is an object with multiple fields.\
\
```codeBlockLines_e6Vv\
{\
  "phoneNumber": {\
    "input": "020 1234567",                       // Required. Raw input in string format\
    "defaultCountry": "nl",                       // Required if only a national number is provided, ISO 3166-1 alpha-2 country code. Only set if explicitly set by the user.\
    "internationalFormatted": "+31 20 1234567",   // Read-only string\
    "countryCode": 31,                            // Read-only unsigned integer, numerical country code\
    "national": 201234567,                        // Read-only unsigned integer, numerical representation of the national number\
    "nationalFormatted": "020 1234567",           // Read-only string\
    "valid": true                                 // Read-only boolean. Whether the parser recognized the phone number as valid\
  }\
}\
\
```\
\
There are two fields that accept input. `input` must always be set, while `defaultCountry` must only be set in specific situations. There are two scenarios possible:\
\
- When you enter an international number (e.g. `"+31 20 1234567"`) to the `input` field, no `defaultCountry` needs to be entered. The underlying parser will automatically recognize the number's country.\
- When you enter a national number (e.g. `"020 1234567"`), you need to specify the country in `defaultCountry` (in this case, `"nl"`), so that the parse can correctly convert the number into all formats. The string in `defaultCountry` should be an [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) country code.\
\
Weaviate will also add further read-only fields such as `internationalFormatted`, `countryCode`, `national`, `nationalFormatted` and `valid` when reading back a field of type `phoneNumber`.\
\
### Examples [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#examples-5 "Direct link to Examples")\
\
#### Property definition [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#property-definition-5 "Direct link to Property definition")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
from weaviate.classes.config import Property, DataType\
from weaviate.classes.data import PhoneNumber\
\
# Create collection\
my_collection = client.collections.create(\
    name="Person",\
    properties=[\
        Property(name="name", data_type=DataType.TEXT),\
        Property(name="phone", data_type=DataType.PHONE_NUMBER),\
    ],\
    # Other properties are omitted for brevity\
)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
#### Object insertion [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#object-insertion-5 "Direct link to Object insertion")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
# Create an object\
example_object = {\
    "name": "Ray Stantz",\
    "phone": PhoneNumber(number="212 555 2368", default_country="us"),\
}\
\
obj_uuid = my_collection.data.insert(example_object)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
## `blob` [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#blob "Direct link to blob")\
\
The datatype blob accepts any binary data. The data should be `base64` encoded, and passed as a `string`. Characteristics:\
\
- Weaviate doesn't make assumptions about the type of data that is encoded. A module (e.g. `img2vec`) can investigate file headers as it wishes, but Weaviate itself does not do this.\
- When storing, the data is `base64` decoded (so Weaviate stores it more efficiently).\
- When serving, the data is `base64` encoded (so it is safe to serve as `json`).\
- There is no max file size limit.\
- This `blob` field is always skipped in the inverted index, regardless of setting. This mean you can not search by this `blob` field in a Weaviate GraphQL `where` filter, and there is no `valueBlob` field accordingly. Depending on the module, this field can be used in module-specific filters (e.g. `nearImage` in the `img2vec-neural` filter).\
\
To obtain the base64-encoded value of an image, you can run the following command - or use the helper methods in the Weaviate clients - to do so:\
\
```codeBlockLines_e6Vv\
cat my_image.png | base64\
\
```\
\
### Examples [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#examples-6 "Direct link to Examples")\
\
#### Property definition [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#property-definition-6 "Direct link to Property definition")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
from weaviate.classes.config import Property, DataType\
\
# Create collection\
my_collection = client.collections.create(\
    name="Poster",\
    properties=[\
        Property(name="title", data_type=DataType.TEXT),\
        Property(name="image", data_type=DataType.BLOB),\
    ],\
    # Other properties are omitted for brevity\
)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
#### Object insertion [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#object-insertion-6 "Direct link to Object insertion")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
# Create an object\
example_object = {\
    "title": "The Matrix",\
    "image": blob_string\
}\
\
obj_uuid = my_collection.data.insert(example_object)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
## `object` [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#object "Direct link to object")\
\
Added in `v1.22`\
\
The `object` type allows you to store nested data as a JSON object that can be nested to any depth.\
\
For example, a `Person` collection could have an `address` property as an object. It could in turn include nested properties such as `street` and `city`:\
\
Limitations\
\
Currently, `object` and `object[]` datatype properties are not indexed and not vectorized.\
\
Future plans include the ability to index nested properties, for example to allow for filtering on nested properties and vectorization options.\
\
### Examples [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#examples-7 "Direct link to Examples")\
\
#### Property definition [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#property-definition-7 "Direct link to Property definition")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
from weaviate.classes.config import Property, DataType\
\
# Create collection\
my_collection = client.collections.create(\
    name="Person",\
    properties=[\
        Property(name="name", data_type=DataType.TEXT),\
        Property(\
            name="home_address",\
            data_type=DataType.OBJECT,\
            nested_properties=[\
                Property(\
                    name="street",\
                    data_type=DataType.OBJECT,\
                    nested_properties=[\
                        Property(name="number", data_type=DataType.INT),\
                        Property(name="name", data_type=DataType.TEXT),\
                    ],\
                ),\
                Property(name="city", data_type=DataType.TEXT),\
            ],\
        ),\
        Property(\
            name="office_addresses",\
            data_type=DataType.OBJECT_ARRAY,\
            nested_properties=[\
                Property(name="office_name", data_type=DataType.TEXT),\
                Property(\
                    name="street",\
                    data_type=DataType.OBJECT,\
                    nested_properties=[\
                        Property(name="name", data_type=DataType.TEXT),\
                        Property(name="number", data_type=DataType.INT),\
                    ],\
                ),\
            ],\
        ),\
    ],\
    # Other properties are omitted for brevity\
)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
#### Object insertion [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#object-insertion-7 "Direct link to Object insertion")\
\
- Python Client v4\
- JS/TS Client v3\
\
```codeBlockLines_e6Vv\
# Create an object\
example_object = {\
    "name": "John Smith",\
    "home_address": {\
        "street": {\
            "number": 123,\
            "name": "Main Street",\
        },\
        "city": "London",\
    },\
    "office_addresses": [\
        {\
            "office_name": "London HQ",\
            "street": {"number": 456, "name": "Oxford Street"},\
        },\
        {\
            "office_name": "Manchester Branch",\
            "street": {"number": 789, "name": "Piccadilly Gardens"},\
        },\
    ],\
}\
\
obj_uuid = my_collection.data.insert(example_object)\
\
```\
\
[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")\
\
## `cross-reference` [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#cross-reference "Direct link to cross-reference")\
\
Cross-references and query performance\
\
Queries involving cross-references can be slower than queries that do not involve cross-references, especially at scale such as for multiple objects or complex queries.\
\
At the first instance, we strongly encourage you to consider whether you can avoid using cross-references in your data schema. As a scalable AI-native database, Weaviate is well-placed to perform complex queries with vector, keyword and hybrid searches involving filters. You may benefit from rethinking your data schema to avoid cross-references where possible.\
\
For example, instead of creating separate "Author" and "Book" collections with cross-references, consider embedding author information directly in Book objects and using searches and filters to find books by author characteristics.\
\
The `cross-reference` type allows a link to be created from one object to another. This is useful for creating relationships between collections, such as linking a `Person` collection to a `Company` collection.\
\
The `cross-reference` type objects are `arrays` by default. This allows you to link to any number of instances of a given collection (including zero).\
\
For more information on cross-references, see the [cross-references](https://docs.weaviate.io/weaviate/concepts/data#cross-references). To see how to work with cross-references, see [how to manage data: cross-references](https://docs.weaviate.io/weaviate/manage-collections/cross-references).\
\
## Notes [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#notes "Direct link to Notes")\
\
#### Formatting in payloads [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#formatting-in-payloads "Direct link to Formatting in payloads")\
\
In raw payloads (e.g. JSON payloads for REST), data types are specified as an array (e.g. `["text"]`, or `["text[]"]`), as it is required for some cross-reference specifications.\
\
## Further resources [​](https://docs.weaviate.io/weaviate/config-refs/datatypes\#further-resources "Direct link to Further resources")\
\
- [How-to: Manage collections](https://docs.weaviate.io/weaviate/manage-collections)\
- [Concepts: Data structure](https://docs.weaviate.io/weaviate/concepts/data)\
- [References: REST API: Schema](https://docs.weaviate.io/weaviate/api/rest#tag/schema)\
\
