---
url: "https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html"
title: "weaviate.outputs — Weaviate Python Client 4.16.10 documentation"
---

- [Home](https://weaviate-python-client.readthedocs.io/en/stable/index.html)
- [Weaviate Library](https://weaviate-python-client.readthedocs.io/en/stable/modules.html)
- [weaviate](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html)
- weaviate.outputs
- [View page source](https://weaviate-python-client.readthedocs.io/en/stable/_sources/weaviate.outputs.rst.txt)

* * *

# weaviate.outputs [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html\#module-weaviate.outputs "Link to this heading")

## weaviate.outputs.aggregate [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html\#module-weaviate.outputs.aggregate "Link to this heading")

_class_ weaviate.outputs.aggregate.AggregateBoolean( _count_, _percentage\_false_, _percentage\_true_, _total\_false_, _total\_true_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#AggregateBoolean) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateBoolean "Link to this definition")

Bases: `object`

The aggregation result for a boolean property.

Parameters:

- **count** ( _int_ _\|_ _None_)

- **percentage\_false** ( _float_ _\|_ _None_)

- **percentage\_true** ( _float_ _\|_ _None_)

- **total\_false** ( _int_ _\|_ _None_)

- **total\_true** ( _int_ _\|_ _None_)


count _:int\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateBoolean.count "Link to this definition")percentage\_false _:float\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateBoolean.percentage_false "Link to this definition")percentage\_true _:float\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateBoolean.percentage_true "Link to this definition")total\_false _:int\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateBoolean.total_false "Link to this definition")total\_true _:int\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateBoolean.total_true "Link to this definition")_class_ weaviate.outputs.aggregate.AggregateDate( _count_, _maximum_, _median_, _minimum_, _mode_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#AggregateDate) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateDate "Link to this definition")

Bases: `object`

The aggregation result for a date property.

Parameters:

- **count** ( _int_ _\|_ _None_)

- **maximum** ( _str_ _\|_ _None_)

- **median** ( _str_ _\|_ _None_)

- **minimum** ( _str_ _\|_ _None_)

- **mode** ( _str_ _\|_ _None_)


count _:int\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateDate.count "Link to this definition")maximum _:str\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateDate.maximum "Link to this definition")median _:str\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateDate.median "Link to this definition")minimum _:str\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateDate.minimum "Link to this definition")mode _:str\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateDate.mode "Link to this definition")_class_ weaviate.outputs.aggregate.AggregateGroup( _grouped\_by_, _properties_, _total\_count_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#AggregateGroup) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateGroup "Link to this definition")

Bases: `object`

The aggregation result for a collection grouped by a property.

Parameters:

- **grouped\_by** ( [_GroupedBy_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.GroupedBy "weaviate.collections.classes.aggregate.GroupedBy"))

- **properties** ( _Dict_ _\[_ _str_ _,_ [_AggregateInteger_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateInteger "weaviate.collections.classes.aggregate.AggregateInteger") _\|_ [_AggregateNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateNumber "weaviate.collections.classes.aggregate.AggregateNumber") _\|_ [_AggregateText_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateText "weaviate.collections.classes.aggregate.AggregateText") _\|_ [_AggregateBoolean_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateBoolean "weaviate.collections.classes.aggregate.AggregateBoolean") _\|_ [_AggregateDate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateDate "weaviate.collections.classes.aggregate.AggregateDate") _\|_ [_AggregateReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateReference "weaviate.collections.classes.aggregate.AggregateReference") _\]_)

- **total\_count** ( _int_ _\|_ _None_)


grouped\_by _: [GroupedBy](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.GroupedBy "weaviate.collections.classes.aggregate.GroupedBy")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateGroup.grouped_by "Link to this definition")properties _:Dict\[str, [AggregateInteger](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateInteger "weaviate.collections.classes.aggregate.AggregateInteger") \| [AggregateNumber](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateNumber "weaviate.collections.classes.aggregate.AggregateNumber") \| [AggregateText](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateText "weaviate.collections.classes.aggregate.AggregateText") \| [AggregateBoolean](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateBoolean "weaviate.collections.classes.aggregate.AggregateBoolean") \| [AggregateDate](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateDate "weaviate.collections.classes.aggregate.AggregateDate") \| [AggregateReference](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateReference "weaviate.collections.classes.aggregate.AggregateReference")\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateGroup.properties "Link to this definition")total\_count _:int\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateGroup.total_count "Link to this definition")_class_ weaviate.outputs.aggregate.AggregateGroupByReturn( _groups_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#AggregateGroupByReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateGroupByReturn "Link to this definition")

Bases: `object`

The aggregation results for a collection grouped by a property.

Parameters:

**groups** ( _List_ _\[_ [_AggregateGroup_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateGroup "weaviate.collections.classes.aggregate.AggregateGroup") _\]_)

groups _:List\[ [AggregateGroup](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateGroup "weaviate.collections.classes.aggregate.AggregateGroup")\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateGroupByReturn.groups "Link to this definition")_class_ weaviate.outputs.aggregate.AggregateInteger( _count_, _maximum_, _mean_, _median_, _minimum_, _mode_, _sum\__) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#AggregateInteger) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateInteger "Link to this definition")

Bases: `object`

The aggregation result for an int property.

Parameters:

- **count** ( _int_ _\|_ _None_)

- **maximum** ( _int_ _\|_ _None_)

- **mean** ( _float_ _\|_ _None_)

- **median** ( _float_ _\|_ _None_)

- **minimum** ( _int_ _\|_ _None_)

- **mode** ( _int_ _\|_ _None_)

- **sum\_** ( _int_ _\|_ _None_)


count _:int\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateInteger.count "Link to this definition")maximum _:int\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateInteger.maximum "Link to this definition")mean _:float\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateInteger.mean "Link to this definition")median _:float\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateInteger.median "Link to this definition")minimum _:int\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateInteger.minimum "Link to this definition")mode _:int\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateInteger.mode "Link to this definition")sum\_ _:int\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateInteger.sum_ "Link to this definition")_class_ weaviate.outputs.aggregate.AggregateNumber( _count_, _maximum_, _mean_, _median_, _minimum_, _mode_, _sum\__) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#AggregateNumber) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateNumber "Link to this definition")

Bases: `object`

The aggregation result for a number property.

Parameters:

- **count** ( _int_ _\|_ _None_)

- **maximum** ( _float_ _\|_ _None_)

- **mean** ( _float_ _\|_ _None_)

- **median** ( _float_ _\|_ _None_)

- **minimum** ( _float_ _\|_ _None_)

- **mode** ( _float_ _\|_ _None_)

- **sum\_** ( _float_ _\|_ _None_)


count _:int\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateNumber.count "Link to this definition")maximum _:float\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateNumber.maximum "Link to this definition")mean _:float\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateNumber.mean "Link to this definition")median _:float\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateNumber.median "Link to this definition")minimum _:float\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateNumber.minimum "Link to this definition")mode _:float\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateNumber.mode "Link to this definition")sum\_ _:float\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateNumber.sum_ "Link to this definition")_class_ weaviate.outputs.aggregate.AggregateReturn( _properties_, _total\_count_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#AggregateReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateReturn "Link to this definition")

Bases: `object`

The aggregation result for a collection.

Parameters:

- **properties** ( _Dict_ _\[_ _str_ _,_ [_AggregateInteger_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateInteger "weaviate.collections.classes.aggregate.AggregateInteger") _\|_ [_AggregateNumber_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateNumber "weaviate.collections.classes.aggregate.AggregateNumber") _\|_ [_AggregateText_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateText "weaviate.collections.classes.aggregate.AggregateText") _\|_ [_AggregateBoolean_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateBoolean "weaviate.collections.classes.aggregate.AggregateBoolean") _\|_ [_AggregateDate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateDate "weaviate.collections.classes.aggregate.AggregateDate") _\|_ [_AggregateReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateReference "weaviate.collections.classes.aggregate.AggregateReference") _\]_)

- **total\_count** ( _int_ _\|_ _None_)


properties _:Dict\[str, [AggregateInteger](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateInteger "weaviate.collections.classes.aggregate.AggregateInteger") \| [AggregateNumber](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateNumber "weaviate.collections.classes.aggregate.AggregateNumber") \| [AggregateText](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateText "weaviate.collections.classes.aggregate.AggregateText") \| [AggregateBoolean](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateBoolean "weaviate.collections.classes.aggregate.AggregateBoolean") \| [AggregateDate](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateDate "weaviate.collections.classes.aggregate.AggregateDate") \| [AggregateReference](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.AggregateReference "weaviate.collections.classes.aggregate.AggregateReference")\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateReturn.properties "Link to this definition")total\_count _:int\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateReturn.total_count "Link to this definition")_class_ weaviate.outputs.aggregate.AggregateText( _count_, _top\_occurrences_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#AggregateText) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateText "Link to this definition")

Bases: `object`

The aggregation result for a text property.

Parameters:

- **count** ( _int_ _\|_ _None_)

- **top\_occurrences** ( _List_ _\[_ [_TopOccurrence_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.TopOccurrence "weaviate.collections.classes.aggregate.TopOccurrence") _\]_)


count _:int\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateText.count "Link to this definition")top\_occurrences _:List\[ [TopOccurrence](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.aggregate.TopOccurrence "weaviate.collections.classes.aggregate.TopOccurrence")\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.AggregateText.top_occurrences "Link to this definition")_class_ weaviate.outputs.aggregate.GroupedBy( _prop_, _value_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/aggregate.html#GroupedBy) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.GroupedBy "Link to this definition")

Bases: `object`

The property that the collection was grouped by.

Parameters:

- **prop** ( _str_)

- **value** ( _str_ _\|_ _int_ _\|_ _float_ _\|_ _bool_ _\|_ _List_ _\[_ _str_ _\]_ _\|_ _List_ _\[_ _int_ _\]_ _\|_ _List_ _\[_ _float_ _\]_ _\|_ _List_ _\[_ _bool_ _\]_ _\|_ [_GeoCoordinate_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.GeoCoordinate "weaviate.collections.classes.types.GeoCoordinate") _\|_ _None_)


prop _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.GroupedBy.prop "Link to this definition")value _:str\|int\|float\|bool\|List\[str\]\|List\[int\]\|List\[float\]\|List\[bool\]\| [GeoCoordinate](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.GeoCoordinate "weaviate.collections.classes.types.GeoCoordinate") \|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.aggregate.GroupedBy.value "Link to this definition")

## weaviate.outputs.backup [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html\#module-weaviate.outputs.backup "Link to this heading")

_class_ weaviate.outputs.backup.BackupStatus( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupStatus) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStatus "Link to this definition")

Bases: `str`, `Enum`

The status of a backup.

STARTED _='STARTED'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStatus.STARTED "Link to this definition")TRANSFERRING _='TRANSFERRING'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStatus.TRANSFERRING "Link to this definition")TRANSFERRED _='TRANSFERRED'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStatus.TRANSFERRED "Link to this definition")SUCCESS _='SUCCESS'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStatus.SUCCESS "Link to this definition")FAILED _='FAILED'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStatus.FAILED "Link to this definition")CANCELED _='CANCELED'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStatus.CANCELED "Link to this definition")_pydanticmodel_ weaviate.outputs.backup.BackupStatusReturn [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupStatusReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStatusReturn "Link to this definition")

Bases: `BaseModel`

Return type of the backup status methods.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ backup\_id _:str_ _\[Required\]_ _(alias'id')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStatusReturn.backup_id "Link to this definition")_field_ error _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStatusReturn.error "Link to this definition")_field_ path _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStatusReturn.path "Link to this definition")_field_ status _: [BackupStatus](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatus "weaviate.backup.backup.BackupStatus")_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStatusReturn.status "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStatusReturn._abc_impl "Link to this definition")_class_ weaviate.outputs.backup.BackupStorage( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupStorage) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStorage "Link to this definition")

Bases: `str`, `Enum`

Which backend should be used to write the backup to.

FILESYSTEM _='filesystem'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStorage.FILESYSTEM "Link to this definition")S3 _='s3'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStorage.S3 "Link to this definition")GCS _='gcs'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStorage.GCS "Link to this definition")AZURE _='azure'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStorage.AZURE "Link to this definition")_pydanticmodel_ weaviate.outputs.backup.BackupReturn [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupReturn "Link to this definition")

Bases: [`BackupStatusReturn`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatusReturn "weaviate.backup.backup.BackupStatusReturn")

Return type of the backup creation and restore methods.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ backup\_id _:str_ _\[Required\]_ _(alias'id')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupReturn.backup_id "Link to this definition")_field_ collections _:List\[str\]_ _\[Optional\]_ _(alias'classes')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupReturn.collections "Link to this definition")_field_ error _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupReturn.error "Link to this definition")_field_ path _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupReturn.path "Link to this definition")_field_ status _: [BackupStatus](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupStatus "weaviate.outputs.backup.BackupStatus")_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupReturn.status "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.backup.BackupReturn._abc_impl "Link to this definition")

## weaviate.outputs.batch [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html\#module-weaviate.outputs.batch "Link to this heading")

_class_ weaviate.outputs.batch.BatchObjectReturn( _\_all\_responses=<factory>_, _elapsed\_seconds=0.0_, _errors=<factory>_, _uuids=<factory>_, _has\_errors=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/batch.html#BatchObjectReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.BatchObjectReturn "Link to this definition")

Bases: `object`

This class contains the results of a batch insert\_many operation.

Since the individual objects within the batch can error for differing reasons, the data is split up within this class for ease use when performing error checking, handling, and data revalidation.

Note

Due to concerns over memory usage, this object will only ever store the last MAX\_STORED\_RESULTS uuids in the uuids dictionary and MAX\_STORED\_RESULTS in the all\_responses list.
If more than MAX\_STORED\_RESULTS uuids are added to the dictionary, the oldest uuids will be removed. If the number of objects inserted in this batch exceeds MAX\_STORED\_RESULTS, the all\_responses list will only contain the last MAX\_STORED\_RESULTS objects.
The keys of the errors and uuids dictionaries will always be equivalent to the original\_index of the objects as you added them to the batching loop but won’t necessarily be the same as the indices in the all\_responses list because of this.

Parameters:

- **\_all\_responses** ( _List_ _\[_ _UUID_ _\|_ [_ErrorObject_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.batch.ErrorObject "weaviate.collections.classes.batch.ErrorObject") _\]_)

- **elapsed\_seconds** ( _float_)

- **errors** ( _Dict_ _\[_ _int_ _,_ [_ErrorObject_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.batch.ErrorObject "weaviate.collections.classes.batch.ErrorObject") _\]_)

- **uuids** ( _Dict_ _\[_ _int_ _,_ _UUID_ _\]_)

- **has\_errors** ( _bool_)


elapsed\_seconds [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.BatchObjectReturn.elapsed_seconds "Link to this definition")

The time taken to perform the batch operation.

Type:

float

errors [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.BatchObjectReturn.errors "Link to this definition")

A dictionary of all the failed responses from the batch operation. The keys are the indices of the objects in the batch, and the values are the Error objects.

Type:

Dict\[int, [weaviate.collections.classes.batch.ErrorObject](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.batch.ErrorObject "weaviate.collections.classes.batch.ErrorObject")\]

uuids [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.BatchObjectReturn.uuids "Link to this definition")

A dictionary of all the successful responses from the batch operation. The keys are the indices of the objects in the batch, and the values are the uuid\_package.UUID objects.

Type:

Dict\[int, uuid.UUID\]

has\_errors [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.BatchObjectReturn.has_errors "Link to this definition")

A boolean indicating whether or not any of the objects in the batch failed to be inserted. If this is True, then the errors dictionary will contain at least one entry.

Type:

bool

_property_ all\_responses _:List\[UUID\| [ErrorObject](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.batch.ErrorObject "weaviate.collections.classes.batch.ErrorObject")\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.BatchObjectReturn.all_responses "Link to this definition")

A list of all the responses from the batch operation. Each response is either a uuid\_package.UUID object or an Error object.

WARNING: This only stores the last MAX\_STORED\_RESULTS objects. If more than MAX\_STORED\_RESULTS objects are added to the batch, the oldest objects will be removed from this list.

Type:

@deprecated

elapsed\_seconds _:float_ _=0.0_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id0 "Link to this definition")has\_errors _:bool_ _=False_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id1 "Link to this definition")\_all\_responses _:List\[UUID\| [ErrorObject](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.batch.ErrorObject "weaviate.collections.classes.batch.ErrorObject")\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.BatchObjectReturn._all_responses "Link to this definition")errors _:Dict\[int, [ErrorObject](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.batch.ErrorObject "weaviate.collections.classes.batch.ErrorObject")\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id2 "Link to this definition")uuids _:Dict\[int,UUID\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id3 "Link to this definition")_class_ weaviate.outputs.batch.BatchReferenceReturn( _elapsed\_seconds=0.0_, _errors=<factory>_, _has\_errors=False_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/batch.html#BatchReferenceReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.BatchReferenceReturn "Link to this definition")

Bases: `object`

This class contains the results of a batch insert\_many\_references operation.

Since the individual references within the batch can error for differing reasons, the data is split up within this class for ease use when performing error checking, handling, and data revalidation.

Parameters:

- **elapsed\_seconds** ( _float_)

- **errors** ( _Dict_ _\[_ _int_ _,_ [_ErrorReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.batch.ErrorReference "weaviate.collections.classes.batch.ErrorReference") _\]_)

- **has\_errors** ( _bool_)


elapsed\_seconds [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.BatchReferenceReturn.elapsed_seconds "Link to this definition")

The time taken to perform the batch operation.

Type:

float

errors [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.BatchReferenceReturn.errors "Link to this definition")

A dictionary of all the failed responses from the batch operation. The keys are the indices of the references in the batch, and the values are the Error objects.

Type:

Dict\[int, [weaviate.collections.classes.batch.ErrorReference](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.batch.ErrorReference "weaviate.collections.classes.batch.ErrorReference")\]

has\_errors [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.BatchReferenceReturn.has_errors "Link to this definition")

A boolean indicating whether or not any of the references in the batch failed to be inserted. If this is True, then the errors dictionary will contain at least one entry.

Type:

bool

elapsed\_seconds _:float_ _=0.0_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id4 "Link to this definition")has\_errors _:bool_ _=False_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id5 "Link to this definition")errors _:Dict\[int, [ErrorReference](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.batch.ErrorReference "weaviate.collections.classes.batch.ErrorReference")\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id6 "Link to this definition")_class_ weaviate.outputs.batch.BatchResult [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/batch.html#BatchResult) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.BatchResult "Link to this definition")

Bases: `object`

This class contains the results of a batch operation.

Since the individual objects and references within the batch can error for differing reasons, the data is split up
within this class for ease use when performing error checking, handling, and data revalidation.

objs [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.BatchResult.objs "Link to this definition")

The results of the batch object operation.

refs [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.BatchResult.refs "Link to this definition")

The results of the batch reference operation.

_class_ weaviate.outputs.batch.ErrorObject( _message_, _object\__, _original\_uuid=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/batch.html#ErrorObject) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.ErrorObject "Link to this definition")

Bases: `object`

This class contains the error information for a single object in a batch operation.

Parameters:

- **message** ( _str_)

- **object\_** ( [_BatchObject_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.batch.BatchObject "weaviate.collections.classes.batch.BatchObject"))

- **original\_uuid** ( _str_ _\|_ _UUID_ _\|_ _None_)


original\_uuid _:str\|UUID\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.ErrorObject.original_uuid "Link to this definition")message _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.ErrorObject.message "Link to this definition")object\_ _: [BatchObject](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.batch.BatchObject "weaviate.collections.classes.batch.BatchObject")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.ErrorObject.object_ "Link to this definition")_class_ weaviate.outputs.batch.ErrorReference( _message_, _reference_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/batch.html#ErrorReference) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.ErrorReference "Link to this definition")

Bases: `object`

This class contains the error information for a single reference in a batch operation.

Parameters:

- **message** ( _str_)

- **reference** ( [_BatchReference_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.batch.BatchReference "weaviate.collections.classes.batch.BatchReference"))


message _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.ErrorReference.message "Link to this definition")reference _: [BatchReference](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.batch.BatchReference "weaviate.collections.classes.batch.BatchReference")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.batch.ErrorReference.reference "Link to this definition")

## weaviate.outputs.cluster [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html\#module-weaviate.outputs.cluster "Link to this heading")

_class_ weaviate.outputs.cluster.Node( _git\_hash_, _name_, _shards_, _stats_, _status_, _version_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/cluster.html#Node) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Node "Link to this definition")

Bases: `Generic`\[ `Sh`, `St`\]

The properties of a single node in the cluster.

Parameters:

- **git\_hash** ( _str_)

- **name** ( _str_)

- **shards** ( _Sh_)

- **stats** ( _St_)

- **status** ( _str_)

- **version** ( _str_)


git\_hash _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Node.git_hash "Link to this definition")name _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Node.name "Link to this definition")shards _:Sh_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Node.shards "Link to this definition")stats _:St_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Node.stats "Link to this definition")status _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Node.status "Link to this definition")version _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Node.version "Link to this definition")_class_ weaviate.outputs.cluster.Shard( _collection_, _name_, _node_, _object\_count_, _vector\_indexing\_status_, _vector\_queue\_length_, _compressed_, _loaded_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/cluster.html#Shard) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Shard "Link to this definition")

Bases: `object`

The properties of a single shard of a collection.

Parameters:

- **collection** ( _str_)

- **name** ( _str_)

- **node** ( _str_)

- **object\_count** ( _int_)

- **vector\_indexing\_status** ( _Literal_ _\[_ _'READONLY'_ _,_ _'INDEXING'_ _,_ _'READY'_ _\]_)

- **vector\_queue\_length** ( _int_)

- **compressed** ( _bool_)

- **loaded** ( _bool_ _\|_ _None_)


collection _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Shard.collection "Link to this definition")name _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Shard.name "Link to this definition")node _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Shard.node "Link to this definition")object\_count _:int_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Shard.object_count "Link to this definition")vector\_indexing\_status _:Literal\['READONLY','INDEXING','READY'\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Shard.vector_indexing_status "Link to this definition")vector\_queue\_length _:int_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Shard.vector_queue_length "Link to this definition")compressed _:bool_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Shard.compressed "Link to this definition")loaded _:bool\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Shard.loaded "Link to this definition")_class_ weaviate.outputs.cluster.Stats( _object\_count_, _shard\_count_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/cluster.html#Stats) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Stats "Link to this definition")

Bases: `object`

The statistics of a collection.

Parameters:

- **object\_count** ( _int_)

- **shard\_count** ( _int_)


object\_count _:int_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Stats.object_count "Link to this definition")shard\_count _:int_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.Stats.shard_count "Link to this definition")_class_ weaviate.outputs.cluster.ShardingState( _collection_, _shards_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/cluster/models.html#ShardingState) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.ShardingState "Link to this definition")

Bases: `object`

Class representing the sharding state of a collection.

Parameters:

- **collection** ( _str_)

- **shards** ( _List_ _\[_ [_ShardReplicas_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.ShardReplicas "weaviate.cluster.models.ShardReplicas") _\]_)


_static_\_from\_weaviate( _data_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/cluster/models.html#ShardingState._from_weaviate) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.ShardingState._from_weaviate "Link to this definition")Parameters:

**data** ( _\_ReplicationShardingStateResponse_)

collection _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.ShardingState.collection "Link to this definition")shards _:List\[ [ShardReplicas](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.ShardReplicas "weaviate.cluster.models.ShardReplicas")\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.ShardingState.shards "Link to this definition")_class_ weaviate.outputs.cluster.ShardReplicas( _name_, _replicas_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/cluster/models.html#ShardReplicas) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.ShardReplicas "Link to this definition")

Bases: `object`

Class representing a shard replica.

Parameters:

- **name** ( _str_)

- **replicas** ( _List_ _\[_ _str_ _\]_)


_static_\_from\_weaviate( _data_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/cluster/models.html#ShardReplicas._from_weaviate) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.ShardReplicas._from_weaviate "Link to this definition")Parameters:

**data** ( _\_ReplicationShardReplicas_)

name _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.ShardReplicas.name "Link to this definition")replicas _:List\[str\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.cluster.ShardReplicas.replicas "Link to this definition")

## weaviate.outputs.config [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html\#module-weaviate.outputs.config "Link to this heading")

weaviate.outputs.config.BM25Config [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.BM25Config "Link to this definition")

alias of [`_BM25Config`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._BM25Config "weaviate.collections.classes.config._BM25Config")

weaviate.outputs.config.CollectionConfig [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.CollectionConfig "Link to this definition")

alias of [`_CollectionConfig`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._CollectionConfig "weaviate.collections.classes.config._CollectionConfig")

weaviate.outputs.config.CollectionConfigSimple [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.CollectionConfigSimple "Link to this definition")

alias of [`_CollectionConfigSimple`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._CollectionConfigSimple "weaviate.collections.classes.config._CollectionConfigSimple")

weaviate.outputs.config.GenerativeConfig [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.GenerativeConfig "Link to this definition")

alias of [`_GenerativeConfig`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._GenerativeConfig "weaviate.collections.classes.config._GenerativeConfig")

_class_ weaviate.outputs.config.GenerativeSearches( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#GenerativeSearches) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.GenerativeSearches "Link to this definition")

Bases: `str`, `BaseEnum`

The available generative search modules in Weaviate.

These modules generate text from text-based inputs.
See the [docs](https://weaviate.io/developers/weaviate/modules/reader-generator-modules) for more details.

AWS [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.GenerativeSearches.AWS "Link to this definition")

Weaviate module backed by AWS Bedrock generative models.

ANTHROPIC [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.GenerativeSearches.ANTHROPIC "Link to this definition")

Weaviate module backed by Anthropic generative models.

ANYSCALE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.GenerativeSearches.ANYSCALE "Link to this definition")

Weaviate module backed by Anyscale generative models.

COHERE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.GenerativeSearches.COHERE "Link to this definition")

Weaviate module backed by Cohere generative models.

DATABRICKS [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.GenerativeSearches.DATABRICKS "Link to this definition")

Weaviate module backed by Databricks generative models.

FRIENDLIAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.GenerativeSearches.FRIENDLIAI "Link to this definition")

Weaviate module backed by FriendliAI generative models.

MISTRAL [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.GenerativeSearches.MISTRAL "Link to this definition")

Weaviate module backed by Mistral generative models.

NVIDIA [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.GenerativeSearches.NVIDIA "Link to this definition")

Weaviate module backed by NVIDIA generative models.

OLLAMA [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.GenerativeSearches.OLLAMA "Link to this definition")

Weaviate module backed by generative models deployed on Ollama infrastructure.

OPENAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.GenerativeSearches.OPENAI "Link to this definition")

Weaviate module backed by OpenAI and Azure-OpenAI generative models.

PALM [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.GenerativeSearches.PALM "Link to this definition")

Weaviate module backed by PaLM generative models.

AWS _='generative-aws'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id7 "Link to this definition")ANTHROPIC _='generative-anthropic'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id8 "Link to this definition")ANYSCALE _='generative-anyscale'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id9 "Link to this definition")COHERE _='generative-cohere'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id10 "Link to this definition")DATABRICKS _='generative-databricks'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id11 "Link to this definition")DUMMY _='generative-dummy'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.GenerativeSearches.DUMMY "Link to this definition")FRIENDLIAI _='generative-friendliai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id12 "Link to this definition")MISTRAL _='generative-mistral'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id13 "Link to this definition")NVIDIA _='generative-nvidia'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id14 "Link to this definition")OLLAMA _='generative-ollama'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id15 "Link to this definition")OPENAI _='generative-openai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id16 "Link to this definition")PALM _='generative-palm'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id17 "Link to this definition")XAI _='generative-xai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.GenerativeSearches.XAI "Link to this definition")weaviate.outputs.config.InvertedIndexConfig [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.InvertedIndexConfig "Link to this definition")

alias of [`_InvertedIndexConfig`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._InvertedIndexConfig "weaviate.collections.classes.config._InvertedIndexConfig")

weaviate.outputs.config.MultiTenancyConfig [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.MultiTenancyConfig "Link to this definition")

alias of [`_MultiTenancyConfig`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._MultiTenancyConfig "weaviate.collections.classes.config._MultiTenancyConfig")

_class_ weaviate.outputs.config.ReplicationDeletionStrategy( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#ReplicationDeletionStrategy) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.ReplicationDeletionStrategy "Link to this definition")

Bases: `str`, `BaseEnum`

How object deletions in multi node environments should be resolved.

PERMANENT\_DELETION [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.ReplicationDeletionStrategy.PERMANENT_DELETION "Link to this definition")

Once an object has been deleted on one node it will be deleted on all nodes in case of conflicts.

NO\_AUTOMATED\_RESOLUTION [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.ReplicationDeletionStrategy.NO_AUTOMATED_RESOLUTION "Link to this definition")

No deletion resolution.

DELETE\_ON\_CONFLICT _='DeleteOnConflict'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.ReplicationDeletionStrategy.DELETE_ON_CONFLICT "Link to this definition")NO\_AUTOMATED\_RESOLUTION _='NoAutomatedResolution'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id18 "Link to this definition")TIME\_BASED\_RESOLUTION _='TimeBasedResolution'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.ReplicationDeletionStrategy.TIME_BASED_RESOLUTION "Link to this definition")weaviate.outputs.config.PQConfig [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.PQConfig "Link to this definition")

alias of [`_PQConfig`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._PQConfig "weaviate.collections.classes.config._PQConfig")

weaviate.outputs.config.PQEncoderConfig [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.PQEncoderConfig "Link to this definition")

alias of [`_PQEncoderConfig`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._PQEncoderConfig "weaviate.collections.classes.config._PQEncoderConfig")

_class_ weaviate.outputs.config.PQEncoderDistribution( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config_vector_index.html#PQEncoderDistribution) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.PQEncoderDistribution "Link to this definition")

Bases: `str`, `BaseEnum`

Distribution of the PQ encoder.

LOG\_NORMAL [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.PQEncoderDistribution.LOG_NORMAL "Link to this definition")

Log-normal distribution.

NORMAL [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.PQEncoderDistribution.NORMAL "Link to this definition")

Normal distribution.

LOG\_NORMAL _='log-normal'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id19 "Link to this definition")NORMAL _='normal'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id20 "Link to this definition")_class_ weaviate.outputs.config.PQEncoderType( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config_vector_index.html#PQEncoderType) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.PQEncoderType "Link to this definition")

Bases: `str`, `BaseEnum`

Type of the PQ encoder.

KMEANS [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.PQEncoderType.KMEANS "Link to this definition")

K-means encoder.

TILE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.PQEncoderType.TILE "Link to this definition")

Tile encoder.

KMEANS _='kmeans'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id21 "Link to this definition")TILE _='tile'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id22 "Link to this definition")weaviate.outputs.config.PropertyConfig [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.PropertyConfig "Link to this definition")

alias of [`_Property`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._Property "weaviate.collections.classes.config._Property")

weaviate.outputs.config.ReferencePropertyConfig [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.ReferencePropertyConfig "Link to this definition")

alias of [`_ReferenceProperty`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._ReferenceProperty "weaviate.collections.classes.config._ReferenceProperty")

weaviate.outputs.config.ReplicationConfig [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.ReplicationConfig "Link to this definition")

alias of [`_ReplicationConfig`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._ReplicationConfig "weaviate.collections.classes.config._ReplicationConfig")

_class_ weaviate.outputs.config.Rerankers( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config.html#Rerankers) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Rerankers "Link to this definition")

Bases: `str`, `BaseEnum`

The available reranker modules in Weaviate.

These modules rerank the results of a search query.
See the [docs](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules#re-ranking) for more details.

NONE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Rerankers.NONE "Link to this definition")

No reranker.

COHERE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Rerankers.COHERE "Link to this definition")

Weaviate module backed by Cohere reranking models.

TRANSFORMERS [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Rerankers.TRANSFORMERS "Link to this definition")

Weaviate module backed by Transformers reranking models.

VOYAGEAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Rerankers.VOYAGEAI "Link to this definition")

Weaviate module backed by VoyageAI reranking models.

JINAAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Rerankers.JINAAI "Link to this definition")

Weaviate module backed by JinaAI reranking models.

NVIDIA [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Rerankers.NVIDIA "Link to this definition")

Weaviate module backed by NVIDIA reranking models.

NONE _='none'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id24 "Link to this definition")COHERE _='reranker-cohere'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id25 "Link to this definition")TRANSFORMERS _='reranker-transformers'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id26 "Link to this definition")VOYAGEAI _='reranker-voyageai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id27 "Link to this definition")JINAAI _='reranker-jinaai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id28 "Link to this definition")NVIDIA _='reranker-nvidia'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id29 "Link to this definition")weaviate.outputs.config.RerankerConfig [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.RerankerConfig "Link to this definition")

alias of [`_RerankerConfig`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._RerankerConfig "weaviate.collections.classes.config._RerankerConfig")

weaviate.outputs.config.ShardingConfig [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.ShardingConfig "Link to this definition")

alias of [`_ShardingConfig`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._ShardingConfig "weaviate.collections.classes.config._ShardingConfig")

weaviate.outputs.config.ShardStatus [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.ShardStatus "Link to this definition")

alias of [`_ShardStatus`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._ShardStatus "weaviate.collections.classes.config._ShardStatus")

_class_ weaviate.outputs.config.VectorDistances( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config_vectorizers.html#VectorDistances) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.VectorDistances "Link to this definition")

Bases: `str`, `Enum`

Vector similarity distance metric to be used in the VectorIndexConfig class.

To ensure optimal search results, we recommend reviewing whether your model provider advises a
specific distance metric and following their advice.

COSINE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.VectorDistances.COSINE "Link to this definition")

Cosine distance: [reference](https://en.wikipedia.org/wiki/Cosine_similarity)

DOT [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.VectorDistances.DOT "Link to this definition")

Dot distance: [reference](https://en.wikipedia.org/wiki/Dot_product)

L2\_SQUARED [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.VectorDistances.L2_SQUARED "Link to this definition")

L2 squared distance: [reference](https://en.wikipedia.org/wiki/Euclidean_distance)

HAMMING [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.VectorDistances.HAMMING "Link to this definition")

Hamming distance: [reference](https://en.wikipedia.org/wiki/Hamming_distance)

MANHATTAN [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.VectorDistances.MANHATTAN "Link to this definition")

Manhattan distance: [reference](https://en.wikipedia.org/wiki/Taxicab_geometry)

COSINE _='cosine'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id34 "Link to this definition")DOT _='dot'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id35 "Link to this definition")L2\_SQUARED _='l2-squared'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id36 "Link to this definition")HAMMING _='hamming'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id37 "Link to this definition")MANHATTAN _='manhattan'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id38 "Link to this definition")weaviate.outputs.config.VectorIndexConfigHNSW [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.VectorIndexConfigHNSW "Link to this definition")

alias of [`_VectorIndexConfigHNSW`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._VectorIndexConfigHNSW "weaviate.collections.classes.config._VectorIndexConfigHNSW")

weaviate.outputs.config.VectorIndexConfigFlat [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.VectorIndexConfigFlat "Link to this definition")

alias of [`_VectorIndexConfigFlat`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._VectorIndexConfigFlat "weaviate.collections.classes.config._VectorIndexConfigFlat")

_class_ weaviate.outputs.config.VectorIndexType( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config_vector_index.html#VectorIndexType) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.VectorIndexType "Link to this definition")

Bases: `str`, `Enum`

The available vector index types in Weaviate.

HNSW [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.VectorIndexType.HNSW "Link to this definition")

Hierarchical Navigable Small World (HNSW) index.

FLAT [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.VectorIndexType.FLAT "Link to this definition")

Flat index.

HNSW _='hnsw'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id39 "Link to this definition")FLAT _='flat'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id40 "Link to this definition")DYNAMIC _='dynamic'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.VectorIndexType.DYNAMIC "Link to this definition")_class_ weaviate.outputs.config.Vectorizers( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/config_vectorizers.html#Vectorizers) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers "Link to this definition")

Bases: `str`, `Enum`

The available vectorization modules in Weaviate.

These modules encode binary data into lists of floats called vectors.
See the [docs](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules) for more details.

NONE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.NONE "Link to this definition")

No vectorizer.

TEXT2VEC\_AWS [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_AWS "Link to this definition")

Weaviate module backed by AWS text-based embedding models.

TEXT2VEC\_COHERE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_COHERE "Link to this definition")

Weaviate module backed by Cohere text-based embedding models.

TEXT2VEC\_CONTEXTIONARY [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_CONTEXTIONARY "Link to this definition")

Weaviate module backed by Contextionary text-based embedding models.

TEXT2VEC\_GPT4ALL [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_GPT4ALL "Link to this definition")

Weaviate module backed by GPT-4-All text-based embedding models.

TEXT2VEC\_HUGGINGFACE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_HUGGINGFACE "Link to this definition")

Weaviate module backed by HuggingFace text-based embedding models.

TEXT2VEC\_OPENAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_OPENAI "Link to this definition")

Weaviate module backed by OpenAI and Azure-OpenAI text-based embedding models.

TEXT2VEC\_PALM [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_PALM "Link to this definition")

Weaviate module backed by PaLM text-based embedding models.

TEXT2VEC\_TRANSFORMERS [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_TRANSFORMERS "Link to this definition")

Weaviate module backed by Transformers text-based embedding models.

TEXT2VEC\_JINAAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_JINAAI "Link to this definition")

Weaviate module backed by Jina AI text-based embedding models.

TEXT2VEC\_VOYAGEAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_VOYAGEAI "Link to this definition")

Weaviate module backed by Voyage AI text-based embedding models.

TEXT2VEC\_NVIDIA [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_NVIDIA "Link to this definition")

Weaviate module backed by NVIDIA text-based embedding models.

TEXT2VEC\_WEAVIATE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_WEAVIATE "Link to this definition")

Weaviate module backed by Weaviate’s self-hosted text-based embedding models.

IMG2VEC\_NEURAL [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.IMG2VEC_NEURAL "Link to this definition")

Weaviate module backed by a ResNet-50 neural network for images.

MULTI2VEC\_CLIP [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.MULTI2VEC_CLIP "Link to this definition")

Weaviate module backed by a Sentence-BERT CLIP model for images and text.

MULTI2VEC\_PALM [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.MULTI2VEC_PALM "Link to this definition")

Weaviate module backed by a palm model for images and text.

MULTI2VEC\_BIND [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.MULTI2VEC_BIND "Link to this definition")

Weaviate module backed by the ImageBind model for images, text, audio, depth, IMU, thermal, and video.

MULTI2VEC\_VOYAGEAI [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.MULTI2VEC_VOYAGEAI "Link to this definition")

Weaviate module backed by a Voyage AI multimodal embedding models.

MULTI2VEC\_NVIDIA [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.MULTI2VEC_NVIDIA "Link to this definition")

Weaviate module backed by NVIDIA multimodal embedding models.

REF2VEC\_CENTROID [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.REF2VEC_CENTROID "Link to this definition")

Weaviate module backed by a centroid-based model that calculates an object’s vectors from its referenced vectors.

NONE _='none'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id42 "Link to this definition")TEXT2COLBERT\_JINAAI _='text2colbert-jinaai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2COLBERT_JINAAI "Link to this definition")TEXT2VEC\_AWS _='text2vec-aws'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id43 "Link to this definition")TEXT2VEC\_COHERE _='text2vec-cohere'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id44 "Link to this definition")TEXT2VEC\_CONTEXTIONARY _='text2vec-contextionary'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id45 "Link to this definition")TEXT2VEC\_DATABRICKS _='text2vec-databricks'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_DATABRICKS "Link to this definition")TEXT2VEC\_GPT4ALL _='text2vec-gpt4all'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id46 "Link to this definition")TEXT2VEC\_HUGGINGFACE _='text2vec-huggingface'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id47 "Link to this definition")TEXT2VEC\_MISTRAL _='text2vec-mistral'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_MISTRAL "Link to this definition")TEXT2VEC\_MORPH _='text2vec-morph'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_MORPH "Link to this definition")TEXT2VEC\_MODEL2VEC _='text2vec-model2vec'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_MODEL2VEC "Link to this definition")TEXT2VEC\_NVIDIA _='text2vec-nvidia'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id48 "Link to this definition")TEXT2VEC\_OLLAMA _='text2vec-ollama'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.TEXT2VEC_OLLAMA "Link to this definition")TEXT2VEC\_OPENAI _='text2vec-openai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id49 "Link to this definition")TEXT2VEC\_PALM _='text2vec-palm'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id50 "Link to this definition")TEXT2VEC\_TRANSFORMERS _='text2vec-transformers'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id51 "Link to this definition")TEXT2VEC\_JINAAI _='text2vec-jinaai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id52 "Link to this definition")TEXT2VEC\_VOYAGEAI _='text2vec-voyageai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id53 "Link to this definition")TEXT2VEC\_WEAVIATE _='text2vec-weaviate'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id54 "Link to this definition")IMG2VEC\_NEURAL _='img2vec-neural'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id55 "Link to this definition")MULTI2VEC\_AWS _='multi2vec-aws'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.MULTI2VEC_AWS "Link to this definition")MULTI2VEC\_CLIP _='multi2vec-clip'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id56 "Link to this definition")MULTI2VEC\_COHERE _='multi2vec-cohere'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.MULTI2VEC_COHERE "Link to this definition")MULTI2VEC\_JINAAI _='multi2vec-jinaai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.MULTI2VEC_JINAAI "Link to this definition")MULTI2MULTI\_JINAAI _='multi2multivec-jinaai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.Vectorizers.MULTI2MULTI_JINAAI "Link to this definition")MULTI2VEC\_BIND _='multi2vec-bind'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id57 "Link to this definition")MULTI2VEC\_PALM _='multi2vec-palm'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id58 "Link to this definition")MULTI2VEC\_VOYAGEAI _='multi2vec-voyageai'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id59 "Link to this definition")MULTI2VEC\_NVIDIA _='multi2vec-nvidia'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id60 "Link to this definition")REF2VEC\_CENTROID _='ref2vec-centroid'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id61 "Link to this definition")weaviate.outputs.config.VectorizerConfig [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.config.VectorizerConfig "Link to this definition")

alias of [`_VectorizerConfig`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.config._VectorizerConfig "weaviate.collections.classes.config._VectorizerConfig")

## weaviate.outputs.data [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html\#module-weaviate.outputs.data "Link to this heading")

_class_ weaviate.outputs.data.DeleteManyObject( _uuid_, _successful_, _error=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/batch.html#DeleteManyObject) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.data.DeleteManyObject "Link to this definition")

Bases: `object`

This class contains the objects of a delete\_many operation.

Parameters:

- **uuid** ( _UUID_)

- **successful** ( _bool_)

- **error** ( _str_ _\|_ _None_)


error _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.data.DeleteManyObject.error "Link to this definition")uuid _:UUID_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.data.DeleteManyObject.uuid "Link to this definition")successful _:bool_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.data.DeleteManyObject.successful "Link to this definition")_class_ weaviate.outputs.data.DeleteManyReturn( _failed_, _matches_, _objects_, _successful_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/batch.html#DeleteManyReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.data.DeleteManyReturn "Link to this definition")

Bases: `Generic`\[ `T`\]

This class contains the results of a delete\_many operation..

Parameters:

- **failed** ( _int_)

- **matches** ( _int_)

- **objects** ( _T_)

- **successful** ( _int_)


failed _:int_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.data.DeleteManyReturn.failed "Link to this definition")matches _:int_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.data.DeleteManyReturn.matches "Link to this definition")objects _:T_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.data.DeleteManyReturn.objects "Link to this definition")successful _:int_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.data.DeleteManyReturn.successful "Link to this definition")_class_ weaviate.outputs.data.Error( _message_, _code=None_, _original\_uuid=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/data.html#Error) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.data.Error "Link to this definition")

Bases: `object`

This class represents an error that occurred when attempting to insert an object within a batch.

Parameters:

- **message** ( _str_)

- **code** ( _int_ _\|_ _None_)

- **original\_uuid** ( _str_ _\|_ _UUID_ _\|_ _None_)


code _:int\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.data.Error.code "Link to this definition")original\_uuid _:str\|UUID\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.data.Error.original_uuid "Link to this definition")message _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.data.Error.message "Link to this definition")_class_ weaviate.outputs.data.RefError( _message_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/data.html#RefError) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.data.RefError "Link to this definition")

Bases: `object`

This class represents an error that occurred when attempting to insert a reference between objects within a batch.

Parameters:

**message** ( _str_)

message _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.data.RefError.message "Link to this definition")

## weaviate.outputs.query [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html\#module-weaviate.outputs.query "Link to this heading")

weaviate.outputs.query.FilterByCreationTime [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.FilterByCreationTime "Link to this definition")

alias of [`_FilterByCreationTime`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._FilterByCreationTime "weaviate.collections.classes.filters._FilterByCreationTime")

weaviate.outputs.query.FilterById [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.FilterById "Link to this definition")

alias of [`_FilterById`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._FilterById "weaviate.collections.classes.filters._FilterById")

weaviate.outputs.query.FilterByProperty [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.FilterByProperty "Link to this definition")

alias of [`_FilterByProperty`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._FilterByProperty "weaviate.collections.classes.filters._FilterByProperty")

weaviate.outputs.query.FilterByRef [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.FilterByRef "Link to this definition")

alias of [`_FilterByRef`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._FilterByRef "weaviate.collections.classes.filters._FilterByRef")

weaviate.outputs.query.FilterByUpdateTime [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.FilterByUpdateTime "Link to this definition")

alias of [`_FilterByUpdateTime`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._FilterByUpdateTime "weaviate.collections.classes.filters._FilterByUpdateTime")

weaviate.outputs.query.FilterReturn [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.FilterReturn "Link to this definition")

alias of [`_Filters`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.filters._Filters "weaviate.collections.classes.filters._Filters")

_pydanticmodel_ weaviate.outputs.query.GeoCoordinate [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/types.html#GeoCoordinate) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GeoCoordinate "Link to this definition")

Bases: [`_WeaviateInput`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._WeaviateInput "weaviate.collections.classes.types._WeaviateInput")

Input for the geo-coordinate datatype.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ latitude _:float_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GeoCoordinate.latitude "Link to this definition")Constraints:

- **ge** = -90

- **le** = 90


_field_ longitude _:float_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GeoCoordinate.longitude "Link to this definition")Constraints:

- **ge** = -180

- **le** = 180


\_to\_dict() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/types.html#GeoCoordinate._to_dict) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GeoCoordinate._to_dict "Link to this definition")Return type:

_Dict_\[str, float\]

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GeoCoordinate._abc_impl "Link to this definition")_class_ weaviate.outputs.query.BM25OperatorAnd [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#BM25OperatorAnd) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.BM25OperatorAnd "Link to this definition")

Bases: [`BM25OperatorOptions`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.BM25OperatorOptions "weaviate.collections.classes.grpc.BM25OperatorOptions")

Define the ‘And’ operator for keyword queries.

operator _:ClassVar\[Any\]_ _=2_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.BM25OperatorAnd.operator "Link to this definition")_class_ weaviate.outputs.query.BM25OperatorOr( _minimum\_should\_match_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/grpc.html#BM25OperatorOr) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.BM25OperatorOr "Link to this definition")

Bases: [`BM25OperatorOptions`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc.BM25OperatorOptions "weaviate.collections.classes.grpc.BM25OperatorOptions")

Define the ‘Or’ operator for keyword queries.

Parameters:

**minimum\_should\_match** ( _int_)

operator _:ClassVar\[Any\]_ _=1_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.BM25OperatorOr.operator "Link to this definition")minimum\_should\_match _:int_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.BM25OperatorOr.minimum_should_match "Link to this definition")weaviate.outputs.query.ListOfVectorsQuery [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.ListOfVectorsQuery "Link to this definition")

alias of [`_ListOfVectorsQuery`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#id219 "weaviate.collections.classes.grpc._ListOfVectorsQuery")

_class_ weaviate.outputs.query.MetadataReturn( _creation\_time=None_, _last\_update\_time=None_, _distance=None_, _certainty=None_, _score=None_, _explain\_score=None_, _is\_consistent=None_, _rerank\_score=None_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/internal.html#MetadataReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.MetadataReturn "Link to this definition")

Bases: `object`

Metadata of an object returned by a query.

Parameters:

- **creation\_time** ( _datetime_ _\|_ _None_)

- **last\_update\_time** ( _datetime_ _\|_ _None_)

- **distance** ( _float_ _\|_ _None_)

- **certainty** ( _float_ _\|_ _None_)

- **score** ( _float_ _\|_ _None_)

- **explain\_score** ( _str_ _\|_ _None_)

- **is\_consistent** ( _bool_ _\|_ _None_)

- **rerank\_score** ( _float_ _\|_ _None_)


\_is\_empty() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/internal.html#MetadataReturn._is_empty) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.MetadataReturn._is_empty "Link to this definition")Return type:

bool

certainty _:float\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.MetadataReturn.certainty "Link to this definition")creation\_time _:datetime\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.MetadataReturn.creation_time "Link to this definition")distance _:float\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.MetadataReturn.distance "Link to this definition")explain\_score _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.MetadataReturn.explain_score "Link to this definition")is\_consistent _:bool\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.MetadataReturn.is_consistent "Link to this definition")last\_update\_time _:datetime\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.MetadataReturn.last_update_time "Link to this definition")rerank\_score _:float\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.MetadataReturn.rerank_score "Link to this definition")score _:float\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.MetadataReturn.score "Link to this definition")_class_ weaviate.outputs.query.MetadataSingleObjectReturn( _creation\_time_, _last\_update\_time_, _is\_consistent_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/internal.html#MetadataSingleObjectReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.MetadataSingleObjectReturn "Link to this definition")

Bases: `object`

Metadata of an object returned by the fetch\_object\_by\_id query.

Parameters:

- **creation\_time** ( _datetime_)

- **last\_update\_time** ( _datetime_)

- **is\_consistent** ( _bool_ _\|_ _None_)


creation\_time _:datetime_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.MetadataSingleObjectReturn.creation_time "Link to this definition")last\_update\_time _:datetime_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.MetadataSingleObjectReturn.last_update_time "Link to this definition")is\_consistent _:bool\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.MetadataSingleObjectReturn.is_consistent "Link to this definition")_class_ weaviate.outputs.query.Object( _uuid_, _metadata_, _properties_, _references_, _vector_, _collection_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/internal.html#Object) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.Object "Link to this definition")

Bases: `Generic`\[ [`P`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [`R`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\], [`_Object`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal._Object "weaviate.collections.classes.internal._Object")\[ [`P`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [`R`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R"), [`MetadataReturn`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.MetadataReturn "weaviate.collections.classes.internal.MetadataReturn")\]

A single Weaviate object returned by a query within the .query namespace of a collection.

Parameters:

- **uuid** ( _UUID_)

- **metadata** ( [_M_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.M "weaviate.collections.classes.types.M"))

- **properties** ( [_P_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"))

- **references** ( [_R_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R"))

- **vector** ( _Dict_ _\[_ _str_ _,_ _List_ _\[_ _float_ _\]_ _\|_ _List_ _\[_ _List_ _\[_ _float_ _\]_ _\]_ _\]_)

- **collection** ( _str_)


_class_ weaviate.outputs.query.ObjectSingleReturn( _uuid_, _metadata_, _properties_, _references_, _vector_, _collection_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/internal.html#ObjectSingleReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.ObjectSingleReturn "Link to this definition")

Bases: `Generic`\[ [`P`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [`R`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\], [`_Object`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal._Object "weaviate.collections.classes.internal._Object")\[ [`P`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [`R`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R"), [`MetadataSingleObjectReturn`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.MetadataSingleObjectReturn "weaviate.collections.classes.internal.MetadataSingleObjectReturn")\]

A single Weaviate object returned by the fetch\_object\_by\_id query.

Parameters:

- **uuid** ( _UUID_)

- **metadata** ( [_M_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.M "weaviate.collections.classes.types.M"))

- **properties** ( [_P_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"))

- **references** ( [_R_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R"))

- **vector** ( _Dict_ _\[_ _str_ _,_ _List_ _\[_ _float_ _\]_ _\|_ _List_ _\[_ _List_ _\[_ _float_ _\]_ _\]_ _\]_)

- **collection** ( _str_)


_class_ weaviate.outputs.query.GroupByObject( _uuid_, _metadata_, _properties_, _references_, _vector_, _collection_, _belongs\_to\_group_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/internal.html#GroupByObject) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GroupByObject "Link to this definition")

Bases: `Generic`\[ [`P`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [`R`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\], [`_Object`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal._Object "weaviate.collections.classes.internal._Object")\[ [`P`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [`R`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R"), [`GroupByMetadataReturn`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GroupByMetadataReturn "weaviate.collections.classes.internal.GroupByMetadataReturn")\]

A single Weaviate object returned by a query with the group\_by argument specified.

Parameters:

- **uuid** ( _UUID_)

- **metadata** ( [_M_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.M "weaviate.collections.classes.types.M"))

- **properties** ( [_P_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"))

- **references** ( [_R_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R"))

- **vector** ( _Dict_ _\[_ _str_ _,_ _List_ _\[_ _float_ _\]_ _\|_ _List_ _\[_ _List_ _\[_ _float_ _\]_ _\]_ _\]_)

- **collection** ( _str_)

- **belongs\_to\_group** ( _str_)


belongs\_to\_group _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GroupByObject.belongs_to_group "Link to this definition")uuid _:UUID_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GroupByObject.uuid "Link to this definition")metadata _: [M](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.M "weaviate.collections.classes.types.M")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GroupByObject.metadata "Link to this definition")properties _: [P](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GroupByObject.properties "Link to this definition")references _: [R](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GroupByObject.references "Link to this definition")vector _:Dict\[str,List\[float\]\|List\[List\[float\]\]\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GroupByObject.vector "Link to this definition")collection _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GroupByObject.collection "Link to this definition")_class_ weaviate.outputs.query.GroupByReturn( _objects_, _groups_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/internal.html#GroupByReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GroupByReturn "Link to this definition")

Bases: `Generic`\[ [`P`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [`R`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\]

The return type of a query within the .query namespace of a collection with the group\_by argument specified.

Parameters:

- **objects** ( _List_ _\[_ [_GroupByObject_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GroupByObject "weaviate.collections.classes.internal.GroupByObject") _\[_ [_P_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P") _,_ [_R_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R") _\]_ _\]_)

- **groups** ( _Dict_ _\[_ _str_ _,_ [_Group_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.Group "weaviate.collections.classes.internal.Group") _\[_ [_P_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P") _,_ [_R_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R") _\]_ _\]_)


objects _:List\[ [GroupByObject](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GroupByObject "weaviate.collections.classes.internal.GroupByObject")\[ [P](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [R](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\]\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GroupByReturn.objects "Link to this definition")groups _:Dict\[str, [Group](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.Group "weaviate.collections.classes.internal.Group")\[ [P](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [R](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\]\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GroupByReturn.groups "Link to this definition")_class_ weaviate.outputs.query.Group( _name_, _min\_distance_, _max\_distance_, _number\_of\_objects_, _objects_, _rerank\_score_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/internal.html#Group) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.Group "Link to this definition")

Bases: `Generic`\[ [`P`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [`R`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\]

A group of objects returned in a group by query.

Parameters:

- **name** ( _str_)

- **min\_distance** ( _float_)

- **max\_distance** ( _float_)

- **number\_of\_objects** ( _int_)

- **objects** ( _List_ _\[_ [_GroupByObject_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GroupByObject "weaviate.collections.classes.internal.GroupByObject") _\[_ [_P_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P") _,_ [_R_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R") _\]_ _\]_)

- **rerank\_score** ( _float_ _\|_ _None_)


name _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.Group.name "Link to this definition")min\_distance _:float_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.Group.min_distance "Link to this definition")max\_distance _:float_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.Group.max_distance "Link to this definition")number\_of\_objects _:int_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.Group.number_of_objects "Link to this definition")objects _:List\[ [GroupByObject](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GroupByObject "weaviate.collections.classes.internal.GroupByObject")\[ [P](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [R](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\]\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.Group.objects "Link to this definition")rerank\_score _:float\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.Group.rerank_score "Link to this definition")_class_ weaviate.outputs.query.GenerativeObject( _generated_, _generative_, _uuid_, _metadata_, _properties_, _references_, _vector_, _collection_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/internal.html#GenerativeObject) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeObject "Link to this definition")

Bases: `Generic`\[ [`P`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [`R`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\], [`Object`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.Object "weaviate.collections.classes.internal.Object")\[ [`P`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [`R`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\]

A single Weaviate object returned by a query within the generate namespace of a collection.

Parameters:

- **generated** ( _str_ _\|_ _None_)

- **generative** ( [_GenerativeSingle_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GenerativeSingle "weaviate.collections.classes.internal.GenerativeSingle") _\|_ _None_)

- **uuid** ( _UUID_)

- **metadata** ( [_M_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.M "weaviate.collections.classes.types.M"))

- **properties** ( [_P_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"))

- **references** ( [_R_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R"))

- **vector** ( _Dict_ _\[_ _str_ _,_ _List_ _\[_ _float_ _\]_ _\|_ _List_ _\[_ _List_ _\[_ _float_ _\]_ _\]_ _\]_)

- **collection** ( _str_)


_property_ generated _:str\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeObject.generated "Link to this definition")

The single generated text of the object.

\_\_generated _:str\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeObject.__generated "Link to this definition")generative _: [GenerativeSingle](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GenerativeSingle "weaviate.collections.classes.internal.GenerativeSingle") \|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeObject.generative "Link to this definition")uuid _:UUID_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeObject.uuid "Link to this definition")metadata _: [M](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.M "weaviate.collections.classes.types.M")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeObject.metadata "Link to this definition")properties _: [P](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeObject.properties "Link to this definition")references _: [R](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeObject.references "Link to this definition")vector _:Dict\[str,List\[float\]\|List\[List\[float\]\]\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeObject.vector "Link to this definition")collection _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeObject.collection "Link to this definition")_class_ weaviate.outputs.query.GenerativeReturn( _generated_, _objects_, _generative_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/internal.html#GenerativeReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeReturn "Link to this definition")

Bases: `Generic`\[ [`P`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [`R`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\]

The return type of a query within the generate namespace of a collection.

Parameters:

- **generated** ( _str_ _\|_ _None_)

- **objects** ( _List_ _\[_ [_GenerativeObject_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GenerativeObject "weaviate.collections.classes.internal.GenerativeObject") _\[_ [_P_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P") _,_ [_R_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R") _\]_ _\]_)

- **generative** ( [_GenerativeGrouped_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GenerativeGrouped "weaviate.collections.classes.internal.GenerativeGrouped") _\|_ _None_)


_property_ generated _:str\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeReturn.generated "Link to this definition")

The grouped generated text of the objects.

\_\_generated _:str\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeReturn.__generated "Link to this definition")objects _:List\[ [GenerativeObject](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GenerativeObject "weaviate.collections.classes.internal.GenerativeObject")\[ [P](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [R](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\]\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeReturn.objects "Link to this definition")generative _: [GenerativeGrouped](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GenerativeGrouped "weaviate.collections.classes.internal.GenerativeGrouped") \|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeReturn.generative "Link to this definition")_class_ weaviate.outputs.query.GenerativeGroupByReturn( _objects_, _groups_, _generated_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/internal.html#GenerativeGroupByReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeGroupByReturn "Link to this definition")

Bases: `Generic`\[ [`P`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [`R`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\]

The return type of a query within the .generate namespace of a collection with the group\_by argument specified.

Parameters:

- **objects** ( _List_ _\[_ [_GroupByObject_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GroupByObject "weaviate.collections.classes.internal.GroupByObject") _\[_ [_P_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P") _,_ [_R_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R") _\]_ _\]_)

- **groups** ( _Dict_ _\[_ _str_ _,_ [_GenerativeGroup_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GenerativeGroup "weaviate.collections.classes.internal.GenerativeGroup") _\[_ [_P_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P") _,_ [_R_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R") _\]_ _\]_)

- **generated** ( _str_ _\|_ _None_)


objects _:List\[ [GroupByObject](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GroupByObject "weaviate.collections.classes.internal.GroupByObject")\[ [P](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [R](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\]\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeGroupByReturn.objects "Link to this definition")groups _:Dict\[str, [GenerativeGroup](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GenerativeGroup "weaviate.collections.classes.internal.GenerativeGroup")\[ [P](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [R](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\]\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeGroupByReturn.groups "Link to this definition")generated _:str\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeGroupByReturn.generated "Link to this definition")_class_ weaviate.outputs.query.GenerativeGroup( _name_, _min\_distance_, _max\_distance_, _number\_of\_objects_, _objects_, _rerank\_score_, _generated_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/internal.html#GenerativeGroup) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeGroup "Link to this definition")

Bases: `Generic`\[ [`P`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [`R`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\], [`Group`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.Group "weaviate.collections.classes.internal.Group")\[ [`P`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [`R`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\]

A group of objects returned in a generative group by query.

Parameters:

- **name** ( _str_)

- **min\_distance** ( _float_)

- **max\_distance** ( _float_)

- **number\_of\_objects** ( _int_)

- **objects** ( _List_ _\[_ [_GroupByObject_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GroupByObject "weaviate.collections.classes.internal.GroupByObject") _\[_ [_P_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P") _,_ [_R_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R") _\]_ _\]_)

- **rerank\_score** ( _float_ _\|_ _None_)

- **generated** ( _str_ _\|_ _None_)


generated _:str\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeGroup.generated "Link to this definition")name _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeGroup.name "Link to this definition")min\_distance _:float_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeGroup.min_distance "Link to this definition")max\_distance _:float_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeGroup.max_distance "Link to this definition")number\_of\_objects _:int_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeGroup.number_of_objects "Link to this definition")objects _:List\[ [GroupByObject](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.GroupByObject "weaviate.collections.classes.internal.GroupByObject")\[ [P](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [R](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\]\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeGroup.objects "Link to this definition")rerank\_score _:float\|None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.GenerativeGroup.rerank_score "Link to this definition")weaviate.outputs.query.PhoneNumberType [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.PhoneNumberType "Link to this definition")

alias of [`_PhoneNumber`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types._PhoneNumber "weaviate.collections.classes.types._PhoneNumber")

_class_ weaviate.outputs.query.QueryReturn( _objects_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/internal.html#QueryReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.QueryReturn "Link to this definition")

Bases: `Generic`\[ [`P`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [`R`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\]

The return type of a query within the .query namespace of a collection.

Parameters:

**objects** ( _List_ _\[_ [_Object_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.Object "weaviate.collections.classes.internal.Object") _\[_ [_P_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P") _,_ [_R_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R") _\]_ _\]_)

objects _:List\[ [Object](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.internal.Object "weaviate.collections.classes.internal.Object")\[ [P](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.P "weaviate.collections.classes.types.P"), [R](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.types.R "weaviate.collections.classes.types.R")\]\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.QueryReturn.objects "Link to this definition")weaviate.outputs.query.Sorting [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.query.Sorting "Link to this definition")

alias of [`_Sorting`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.grpc._Sorting "weaviate.collections.classes.grpc._Sorting")

## weaviate.outputs.rbac [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html\#module-weaviate.outputs.rbac "Link to this heading")

_pydanticmodel_ weaviate.outputs.rbac.BackupsPermissionOutput [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#BackupsPermissionOutput) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.BackupsPermissionOutput "Link to this definition")

Bases: [`_BackupsPermission`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models._BackupsPermission "weaviate.rbac.models._BackupsPermission")

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.BackupsPermissionOutput._abc_impl "Link to this definition")_pydanticmodel_ weaviate.outputs.rbac.ClusterPermissionOutput [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#ClusterPermissionOutput) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.ClusterPermissionOutput "Link to this definition")

Bases: [`_ClusterPermission`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models._ClusterPermission "weaviate.rbac.models._ClusterPermission")

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.ClusterPermissionOutput._abc_impl "Link to this definition")_pydanticmodel_ weaviate.outputs.rbac.CollectionsPermissionOutput [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#CollectionsPermissionOutput) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.CollectionsPermissionOutput "Link to this definition")

Bases: [`_CollectionsPermission`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models._CollectionsPermission "weaviate.rbac.models._CollectionsPermission")

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.CollectionsPermissionOutput._abc_impl "Link to this definition")_pydanticmodel_ weaviate.outputs.rbac.DataPermissionOutput [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#DataPermissionOutput) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.DataPermissionOutput "Link to this definition")

Bases: [`_DataPermission`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models._DataPermission "weaviate.rbac.models._DataPermission")

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.DataPermissionOutput._abc_impl "Link to this definition")_pydanticmodel_ weaviate.outputs.rbac.NodesPermissionOutput [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#NodesPermissionOutput) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.NodesPermissionOutput "Link to this definition")

Bases: [`_NodesPermission`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models._NodesPermission "weaviate.rbac.models._NodesPermission")

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.NodesPermissionOutput._abc_impl "Link to this definition")_pydanticmodel_ weaviate.outputs.rbac.RolesPermissionOutput [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#RolesPermissionOutput) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.RolesPermissionOutput "Link to this definition")

Bases: [`_RolesPermission`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models._RolesPermission "weaviate.rbac.models._RolesPermission")

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.RolesPermissionOutput._abc_impl "Link to this definition")_class_ weaviate.outputs.rbac.RoleScope( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#RoleScope) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.RoleScope "Link to this definition")

Bases: `str`, `BaseEnum`

Scope of the role permission.

MATCH _='match'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.RoleScope.MATCH "Link to this definition")ALL _='all'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.RoleScope.ALL "Link to this definition")_pydanticmodel_ weaviate.outputs.rbac.UsersPermissionOutput [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#UsersPermissionOutput) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.UsersPermissionOutput "Link to this definition")

Bases: [`_UsersPermission`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models._UsersPermission "weaviate.rbac.models._UsersPermission")

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.UsersPermissionOutput._abc_impl "Link to this definition")_class_ weaviate.outputs.rbac.UserAssignment( _user\_id:str_, _user\_type:[weaviate.rbac.models.UserTypes](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.UserTypes "weaviate.rbac.models.UserTypes")_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#UserAssignment) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.UserAssignment "Link to this definition")

Bases: `object`

Parameters:

- **user\_id** ( _str_)

- **user\_type** ( [_UserTypes_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.UserTypes "weaviate.rbac.models.UserTypes"))


user\_id _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.UserAssignment.user_id "Link to this definition")user\_type _: [UserTypes](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.UserTypes "weaviate.rbac.models.UserTypes")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.UserAssignment.user_type "Link to this definition")_pydanticmodel_ weaviate.outputs.rbac.AliasPermissionOutput [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#AliasPermissionOutput) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.AliasPermissionOutput "Link to this definition")

Bases: [`_AliasPermission`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models._AliasPermission "weaviate.rbac.models._AliasPermission")

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.AliasPermissionOutput._abc_impl "Link to this definition")_pydanticmodel_ weaviate.outputs.rbac.ReplicatePermissionOutput [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#ReplicatePermissionOutput) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.ReplicatePermissionOutput "Link to this definition")

Bases: [`_ReplicatePermission`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models._ReplicatePermission "weaviate.rbac.models._ReplicatePermission")

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.ReplicatePermissionOutput._abc_impl "Link to this definition")_pydanticmodel_ weaviate.outputs.rbac.GroupsPermissionOutput [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#GroupsPermissionOutput) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.GroupsPermissionOutput "Link to this definition")

Bases: [`_GroupsPermission`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models._GroupsPermission "weaviate.rbac.models._GroupsPermission")

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.GroupsPermissionOutput._abc_impl "Link to this definition")_pydanticmodel_ weaviate.outputs.rbac.TenantsPermissionOutput [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#TenantsPermissionOutput) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.TenantsPermissionOutput "Link to this definition")

Bases: [`_TenantsPermission`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models._TenantsPermission "weaviate.rbac.models._TenantsPermission")

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.TenantsPermissionOutput._abc_impl "Link to this definition")_class_ weaviate.outputs.rbac.GroupAssignment( _group\_id:str_, _group\_type:[weaviate.rbac.models.GroupTypes](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.GroupTypes "weaviate.rbac.models.GroupTypes")_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/rbac/models.html#GroupAssignment) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.GroupAssignment "Link to this definition")

Bases: `object`

Parameters:

- **group\_id** ( _str_)

- **group\_type** ( [_GroupTypes_](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.GroupTypes "weaviate.rbac.models.GroupTypes"))


group\_id _:str_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.GroupAssignment.group_id "Link to this definition")group\_type _: [GroupTypes](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.rbac.html#weaviate.rbac.models.GroupTypes "weaviate.rbac.models.GroupTypes")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.rbac.GroupAssignment.group_type "Link to this definition")

## weaviate.outputs.tenants [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html\#module-weaviate.outputs.tenants "Link to this heading")

_pydanticmodel_ weaviate.outputs.tenants.Tenant [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/tenants.html#Tenant) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.Tenant "Link to this definition")

Bases: `BaseModel`

Tenant class used to describe a tenant in Weaviate.

name [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.Tenant.name "Link to this definition")

The name of the tenant.

activity\_status [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.Tenant.activity_status "Link to this definition")

TenantActivityStatus, default: “HOT”

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ activityStatus _: [\_TenantActivistatusServerValues](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.tenants._TenantActivistatusServerValues "weaviate.collections.classes.tenants._TenantActivistatusServerValues")_ _=\_TenantActivistatusServerValues.HOT_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.Tenant.activityStatus "Link to this definition")_field_ activityStatusInternal _: [TenantActivityStatus](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.tenants.TenantActivityStatus "weaviate.collections.classes.tenants.TenantActivityStatus")_ _=TenantActivityStatus.ACTIVE_ _(alias'activity\_status')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.Tenant.activityStatusInternal "Link to this definition")_field_ name _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id62 "Link to this definition")\_model\_post\_init( _user\_input_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/tenants.html#Tenant._model_post_init) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.Tenant._model_post_init "Link to this definition")Parameters:

**user\_input** ( _bool_)

Return type:

None

model\_post\_init( _\_Tenant\_\_context_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/tenants.html#Tenant.model_post_init) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.Tenant.model_post_init "Link to this definition")

Override this method to perform additional initialization after \_\_init\_\_ and model\_construct.
This is useful if you want to do some validation that requires the entire model to be initialized.

Parameters:

**\_Tenant\_\_context** ( _Any_)

Return type:

None

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.Tenant._abc_impl "Link to this definition")_property_ activity\_status _: [TenantActivityStatus](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.tenants.TenantActivityStatus "weaviate.collections.classes.tenants.TenantActivityStatus")_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id63 "Link to this definition")

Getter for the activity status of the tenant.

_class_ weaviate.outputs.tenants.TenantActivityStatus( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/collections/classes/tenants.html#TenantActivityStatus) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.TenantActivityStatus "Link to this definition")

Bases: `str`, `Enum`

TenantActivityStatus class used to describe the activity status of a tenant in Weaviate.

ACTIVE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.TenantActivityStatus.ACTIVE "Link to this definition")

The tenant is fully active and can be used.

INACTIVE [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.TenantActivityStatus.INACTIVE "Link to this definition")

The tenant is not active, files stored locally.

OFFLOADED [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.TenantActivityStatus.OFFLOADED "Link to this definition")

The tenant is not active, files stored on the cloud.

OFFLOADING [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.TenantActivityStatus.OFFLOADING "Link to this definition")

The tenant is in the process of being offloaded.

ONLOADING [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.TenantActivityStatus.ONLOADING "Link to this definition")

The tenant is in the process of being activated.

HOT [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.TenantActivityStatus.HOT "Link to this definition")

DEPRECATED, please use ACTIVE. The tenant is fully active and can be used.

COLD [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.TenantActivityStatus.COLD "Link to this definition")

DEPRECATED, please use INACTIVE. The tenant is not active, files stored locally.

FROZEN [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.TenantActivityStatus.FROZEN "Link to this definition")

DEPRECATED, please use OFFLOADED. The tenant is not active, files stored on the cloud.

ACTIVE _='ACTIVE'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id64 "Link to this definition")INACTIVE _='INACTIVE'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id65 "Link to this definition")OFFLOADED _='OFFLOADED'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id66 "Link to this definition")OFFLOADING _='OFFLOADING'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id67 "Link to this definition")ONLOADING _='ONLOADING'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id68 "Link to this definition")HOT _='HOT'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id69 "Link to this definition")COLD _='COLD'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id70 "Link to this definition")FROZEN _='FROZEN'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#id71 "Link to this definition")weaviate.outputs.tenants.TenantOutputType [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html#weaviate.outputs.tenants.TenantOutputType "Link to this definition")

alias of [`Tenant`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.collections.classes.html#weaviate.collections.classes.tenants.Tenant "weaviate.collections.classes.tenants.Tenant")

Versions[latest](https://weaviate-python-client.readthedocs.io/en/latest/weaviate.outputs.html)**[stable](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.outputs.html)**[v4.16.10](https://weaviate-python-client.readthedocs.io/en/v4.16.10/weaviate.outputs.html)[v4.16.9](https://weaviate-python-client.readthedocs.io/en/v4.16.9/weaviate.outputs.html)[v4.16.8](https://weaviate-python-client.readthedocs.io/en/v4.16.8/weaviate.outputs.html)[v4.16.7](https://weaviate-python-client.readthedocs.io/en/v4.16.7/weaviate.outputs.html)[v4.16.6](https://weaviate-python-client.readthedocs.io/en/v4.16.6/weaviate.outputs.html)[v4.16.5](https://weaviate-python-client.readthedocs.io/en/v4.16.5/weaviate.outputs.html)[v4.16.4](https://weaviate-python-client.readthedocs.io/en/v4.16.4/weaviate.outputs.html)[v4.16.3](https://weaviate-python-client.readthedocs.io/en/v4.16.3/weaviate.outputs.html)[v4.16.2](https://weaviate-python-client.readthedocs.io/en/v4.16.2/weaviate.outputs.html)[v4.16.1](https://weaviate-python-client.readthedocs.io/en/v4.16.1/weaviate.outputs.html)[v4.16.0](https://weaviate-python-client.readthedocs.io/en/v4.16.0/weaviate.outputs.html)[v4.15.4](https://weaviate-python-client.readthedocs.io/en/v4.15.4/weaviate.outputs.html)[v4.15.3](https://weaviate-python-client.readthedocs.io/en/v4.15.3/weaviate.outputs.html)[v4.15.2](https://weaviate-python-client.readthedocs.io/en/v4.15.2/weaviate.outputs.html)[v4.15.1](https://weaviate-python-client.readthedocs.io/en/v4.15.1/weaviate.outputs.html)[v4.15.0](https://weaviate-python-client.readthedocs.io/en/v4.15.0/weaviate.outputs.html)[v4.14.4](https://weaviate-python-client.readthedocs.io/en/v4.14.4/weaviate.outputs.html)[v4.14.3](https://weaviate-python-client.readthedocs.io/en/v4.14.3/weaviate.outputs.html)[v4.14.2](https://weaviate-python-client.readthedocs.io/en/v4.14.2/weaviate.outputs.html)[v4.14.1](https://weaviate-python-client.readthedocs.io/en/v4.14.1/weaviate.outputs.html)[v4.14.0](https://weaviate-python-client.readthedocs.io/en/v4.14.0/weaviate.outputs.html)[v4.13.2](https://weaviate-python-client.readthedocs.io/en/v4.13.2/weaviate.outputs.html)[v4.13.1](https://weaviate-python-client.readthedocs.io/en/v4.13.1/weaviate.outputs.html)[v4.13.0](https://weaviate-python-client.readthedocs.io/en/v4.13.0/weaviate.outputs.html)[v4.12.1](https://weaviate-python-client.readthedocs.io/en/v4.12.1/weaviate.outputs.html)[v4.12.0](https://weaviate-python-client.readthedocs.io/en/v4.12.0/weaviate.outputs.html)[v4.11.3](https://weaviate-python-client.readthedocs.io/en/v4.11.3/weaviate.outputs.html)[v4.11.2](https://weaviate-python-client.readthedocs.io/en/v4.11.2/weaviate.outputs.html)[v4.11.1](https://weaviate-python-client.readthedocs.io/en/v4.11.1/weaviate.outputs.html)[v4.11.0](https://weaviate-python-client.readthedocs.io/en/v4.11.0/weaviate.outputs.html)[v4.10.4](https://weaviate-python-client.readthedocs.io/en/v4.10.4/weaviate.outputs.html)[v4.10.3](https://weaviate-python-client.readthedocs.io/en/v4.10.3/weaviate.outputs.html)[v4.10.2](https://weaviate-python-client.readthedocs.io/en/v4.10.2/weaviate.outputs.html)[v4.10.0](https://weaviate-python-client.readthedocs.io/en/v4.10.0/weaviate.outputs.html)[v4.9.6](https://weaviate-python-client.readthedocs.io/en/v4.9.6/weaviate.outputs.html)[v4.9.5](https://weaviate-python-client.readthedocs.io/en/v4.9.5/weaviate.outputs.html)[v4.9.4](https://weaviate-python-client.readthedocs.io/en/v4.9.4/weaviate.outputs.html)[v4.9.3](https://weaviate-python-client.readthedocs.io/en/v4.9.3/weaviate.outputs.html)[v4.9.2](https://weaviate-python-client.readthedocs.io/en/v4.9.2/weaviate.outputs.html)[v4.9.1](https://weaviate-python-client.readthedocs.io/en/v4.9.1/weaviate.outputs.html)[v4.9.0](https://weaviate-python-client.readthedocs.io/en/v4.9.0/weaviate.outputs.html)[v4.8.1](https://weaviate-python-client.readthedocs.io/en/v4.8.1/weaviate.outputs.html)[v4.8.0](https://weaviate-python-client.readthedocs.io/en/v4.8.0/weaviate.outputs.html)[v4.7.1](https://weaviate-python-client.readthedocs.io/en/v4.7.1/weaviate.outputs.html)[v4.7.0](https://weaviate-python-client.readthedocs.io/en/v4.7.0/weaviate.outputs.html)[v4.6.7](https://weaviate-python-client.readthedocs.io/en/v4.6.7/weaviate.outputs.html)[v4.6.6](https://weaviate-python-client.readthedocs.io/en/v4.6.6/weaviate.outputs.html)[v4.6.5](https://weaviate-python-client.readthedocs.io/en/v4.6.5/weaviate.outputs.html)[v4.6.4](https://weaviate-python-client.readthedocs.io/en/v4.6.4/weaviate.outputs.html)[v4.6.3](https://weaviate-python-client.readthedocs.io/en/v4.6.3/weaviate.outputs.html)[v4.6.2](https://weaviate-python-client.readthedocs.io/en/v4.6.2/weaviate.outputs.html)[v4.6.1](https://weaviate-python-client.readthedocs.io/en/v4.6.1/weaviate.outputs.html)[v4.6.0](https://weaviate-python-client.readthedocs.io/en/v4.6.0/weaviate.outputs.html)[v4.5.7](https://weaviate-python-client.readthedocs.io/en/v4.5.7/weaviate.outputs.html)[v4.5.6](https://weaviate-python-client.readthedocs.io/en/v4.5.6/weaviate.outputs.html)[v4.5.5](https://weaviate-python-client.readthedocs.io/en/v4.5.5/weaviate.outputs.html)[v4.5.4](https://weaviate-python-client.readthedocs.io/en/v4.5.4/weaviate.outputs.html)[v4.5.3](https://weaviate-python-client.readthedocs.io/en/v4.5.3/weaviate.outputs.html)[v4.5.2](https://weaviate-python-client.readthedocs.io/en/v4.5.2/weaviate.outputs.html)[v4.5.1](https://weaviate-python-client.readthedocs.io/en/v4.5.1/weaviate.outputs.html)[v4.5.0](https://weaviate-python-client.readthedocs.io/en/v4.5.0/weaviate.outputs.html)[v4.4.4](https://weaviate-python-client.readthedocs.io/en/v4.4.4/weaviate.outputs.html)[v4.4.3](https://weaviate-python-client.readthedocs.io/en/v4.4.3/weaviate.outputs.html)[v4.4.2](https://weaviate-python-client.readthedocs.io/en/v4.4.2/weaviate.outputs.html)[v4.4.1](https://weaviate-python-client.readthedocs.io/en/v4.4.1/weaviate.outputs.html)[v4.4.0](https://weaviate-python-client.readthedocs.io/en/v4.4.0/weaviate.outputs.html)[v3.26.2](https://weaviate-python-client.readthedocs.io/en/v3.26.2/weaviate.outputs.html)[v3.26.1](https://weaviate-python-client.readthedocs.io/en/v3.26.1/weaviate.outputs.html)[v3.26.0](https://weaviate-python-client.readthedocs.io/en/v3.26.0/weaviate.outputs.html)[v3.25.3](https://weaviate-python-client.readthedocs.io/en/v3.25.3/weaviate.outputs.html)[v3.25.2](https://weaviate-python-client.readthedocs.io/en/v3.25.2/weaviate.outputs.html)[v3.23.0](https://weaviate-python-client.readthedocs.io/en/v3.23.0/weaviate.outputs.html)[v3.22.1](https://weaviate-python-client.readthedocs.io/en/v3.22.1/weaviate.outputs.html)[v3.22.0](https://weaviate-python-client.readthedocs.io/en/v3.22.0/weaviate.outputs.html)[v3.21.0](https://weaviate-python-client.readthedocs.io/en/v3.21.0/weaviate.outputs.html)[v3.20.1](https://weaviate-python-client.readthedocs.io/en/v3.20.1/weaviate.outputs.html)[v3.20.0](https://weaviate-python-client.readthedocs.io/en/v3.20.0/weaviate.outputs.html)[v3.19.2](https://weaviate-python-client.readthedocs.io/en/v3.19.2/weaviate.outputs.html)[v3.19.1](https://weaviate-python-client.readthedocs.io/en/v3.19.1/weaviate.outputs.html)[v3.19.0](https://weaviate-python-client.readthedocs.io/en/v3.19.0/weaviate.outputs.html)[v3.18.0](https://weaviate-python-client.readthedocs.io/en/v3.18.0/weaviate.outputs.html)[v3.15.6](https://weaviate-python-client.readthedocs.io/en/v3.15.6/weaviate.outputs.html)[v3.15.5](https://weaviate-python-client.readthedocs.io/en/v3.15.5/weaviate.outputs.html)[v3.15.4](https://weaviate-python-client.readthedocs.io/en/v3.15.4/weaviate.outputs.html)[v3.15.3](https://weaviate-python-client.readthedocs.io/en/v3.15.3/weaviate.outputs.html)[v3.15.2](https://weaviate-python-client.readthedocs.io/en/v3.15.2/weaviate.outputs.html)[v3.15.1](https://weaviate-python-client.readthedocs.io/en/v3.15.1/weaviate.outputs.html)[v3.15.0](https://weaviate-python-client.readthedocs.io/en/v3.15.0/weaviate.outputs.html)[v3.14.0](https://weaviate-python-client.readthedocs.io/en/v3.14.0/weaviate.outputs.html)[v3.13.0](https://weaviate-python-client.readthedocs.io/en/v3.13.0/weaviate.outputs.html)[v3.12.0\_a](https://weaviate-python-client.readthedocs.io/en/v3.12.0_a/weaviate.outputs.html)[v3.11.0](https://weaviate-python-client.readthedocs.io/en/v3.11.0/weaviate.outputs.html)[v3.10.0](https://weaviate-python-client.readthedocs.io/en/v3.10.0/weaviate.outputs.html)[v3.9.0](https://weaviate-python-client.readthedocs.io/en/v3.9.0/weaviate.outputs.html)[v3.8.0](https://weaviate-python-client.readthedocs.io/en/v3.8.0/weaviate.outputs.html)[v3.7.0](https://weaviate-python-client.readthedocs.io/en/v3.7.0/weaviate.outputs.html)[v3.6.0](https://weaviate-python-client.readthedocs.io/en/v3.6.0/weaviate.outputs.html)[v3.5.1](https://weaviate-python-client.readthedocs.io/en/v3.5.1/weaviate.outputs.html)[v3.5.0](https://weaviate-python-client.readthedocs.io/en/v3.5.0/weaviate.outputs.html)[v3.4.1](https://weaviate-python-client.readthedocs.io/en/v3.4.1/weaviate.outputs.html)[v3.4.0](https://weaviate-python-client.readthedocs.io/en/v3.4.0/weaviate.outputs.html)[v3.3.3](https://weaviate-python-client.readthedocs.io/en/v3.3.3/weaviate.outputs.html)[v3.3.2](https://weaviate-python-client.readthedocs.io/en/v3.3.2/weaviate.outputs.html)[v3.3.1](https://weaviate-python-client.readthedocs.io/en/v3.3.1/weaviate.outputs.html)[v3.3.0](https://weaviate-python-client.readthedocs.io/en/v3.3.0/weaviate.outputs.html)[v3.2.5](https://weaviate-python-client.readthedocs.io/en/v3.2.5/weaviate.outputs.html)[v3.2.4](https://weaviate-python-client.readthedocs.io/en/v3.2.4/weaviate.outputs.html)[v3.2.3](https://weaviate-python-client.readthedocs.io/en/v3.2.3/weaviate.outputs.html)[v3.2.2](https://weaviate-python-client.readthedocs.io/en/v3.2.2/weaviate.outputs.html)[v3.2.1](https://weaviate-python-client.readthedocs.io/en/v3.2.1/weaviate.outputs.html)[v3.2.0](https://weaviate-python-client.readthedocs.io/en/v3.2.0/weaviate.outputs.html)[v3.1.1](https://weaviate-python-client.readthedocs.io/en/v3.1.1/weaviate.outputs.html)[v3.1.0](https://weaviate-python-client.readthedocs.io/en/v3.1.0/weaviate.outputs.html)[v3.0.0](https://weaviate-python-client.readthedocs.io/en/v3.0.0/weaviate.outputs.html)On Read the Docs[Project Home](https://app.readthedocs.org/projects/weaviate-python-client/?utm_source=weaviate-python-client&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/weaviate-python-client/builds/?utm_source=weaviate-python-client&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=weaviate-python-client&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=weaviate-python-client&utm_content=flyout)