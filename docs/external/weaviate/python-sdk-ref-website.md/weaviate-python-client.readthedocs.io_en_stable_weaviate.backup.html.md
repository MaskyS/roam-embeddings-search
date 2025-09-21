---
url: "https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html"
title: "weaviate.backup — Weaviate Python Client 4.16.10 documentation"
---

- [Home](https://weaviate-python-client.readthedocs.io/en/stable/index.html)
- [Weaviate Library](https://weaviate-python-client.readthedocs.io/en/stable/modules.html)
- [weaviate](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html)
- weaviate.backup
- [View page source](https://weaviate-python-client.readthedocs.io/en/stable/_sources/weaviate.backup.rst.txt)

* * *

# weaviate.backup [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html\#module-weaviate.backup "Link to this heading")

Module for backup/restore operations.

_class_ weaviate.backup.BackupStorage( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupStorage) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.BackupStorage "Link to this definition")

Bases: `str`, `Enum`

Which backend should be used to write the backup to.

FILESYSTEM _='filesystem'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.BackupStorage.FILESYSTEM "Link to this definition")S3 _='s3'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.BackupStorage.S3 "Link to this definition")GCS _='gcs'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.BackupStorage.GCS "Link to this definition")AZURE _='azure'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.BackupStorage.AZURE "Link to this definition")_class_ weaviate.backup.\_BackupAsync( _connection_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/async_.html#_BackupAsync) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup._BackupAsync "Link to this definition")

Bases: `_BackupExecutor`\[ `ConnectionAsync`\]

Parameters:

**connection** ( _ConnectionSync_ _\|_ _ConnectionAsync_)

_class_ weaviate.backup.\_Backup( _connection_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/sync.html#_Backup) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup._Backup "Link to this definition")

Bases: `_BackupExecutor`\[ `ConnectionSync`\]

Parameters:

**connection** ( _ConnectionSync_ _\|_ _ConnectionAsync_)

## weaviate.backup.backup [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html\#module-weaviate.backup.backup "Link to this heading")

_class_ weaviate.backup.backup.BackupCompressionLevel( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupCompressionLevel) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupCompressionLevel "Link to this definition")

Bases: `str`, `Enum`

Which compression level should be used to compress the backup.

DEFAULT _='DefaultCompression'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupCompressionLevel.DEFAULT "Link to this definition")BEST\_SPEED _='BestSpeed'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupCompressionLevel.BEST_SPEED "Link to this definition")BEST\_COMPRESSION _='BestCompression'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupCompressionLevel.BEST_COMPRESSION "Link to this definition")_class_ weaviate.backup.backup.BackupStorage( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupStorage) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStorage "Link to this definition")

Bases: `str`, `Enum`

Which backend should be used to write the backup to.

FILESYSTEM _='filesystem'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStorage.FILESYSTEM "Link to this definition")S3 _='s3'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStorage.S3 "Link to this definition")GCS _='gcs'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStorage.GCS "Link to this definition")AZURE _='azure'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStorage.AZURE "Link to this definition")_class_ weaviate.backup.backup.BackupStatus( _\*values_) [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupStatus) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatus "Link to this definition")

Bases: `str`, `Enum`

The status of a backup.

STARTED _='STARTED'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatus.STARTED "Link to this definition")TRANSFERRING _='TRANSFERRING'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatus.TRANSFERRING "Link to this definition")TRANSFERRED _='TRANSFERRED'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatus.TRANSFERRED "Link to this definition")SUCCESS _='SUCCESS'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatus.SUCCESS "Link to this definition")FAILED _='FAILED'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatus.FAILED "Link to this definition")CANCELED _='CANCELED'_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatus.CANCELED "Link to this definition")_pydanticmodel_ weaviate.backup.backup.\_BackupConfigBase [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#_BackupConfigBase) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup._BackupConfigBase "Link to this definition")

Bases: `BaseModel`

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ CPUPercentage _:int\|None_ _=None_ _(alias'cpu\_percentage')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup._BackupConfigBase.CPUPercentage "Link to this definition")\_to\_dict() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#_BackupConfigBase._to_dict) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup._BackupConfigBase._to_dict "Link to this definition")Return type:

_Dict_\[str, _Any_\]

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup._BackupConfigBase._abc_impl "Link to this definition")_pydanticmodel_ weaviate.backup.backup.BackupConfigCreate [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupConfigCreate) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupConfigCreate "Link to this definition")

Bases: [`_BackupConfigBase`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup._BackupConfigBase "weaviate.backup.backup._BackupConfigBase")

Options to configure the backup when creating a backup.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ ChunkSize _:int\|None_ _=None_ _(alias'chunk\_size')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupConfigCreate.ChunkSize "Link to this definition")_field_ CompressionLevel _: [BackupCompressionLevel](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupCompressionLevel "weaviate.backup.backup.BackupCompressionLevel") \|None_ _=None_ _(alias'compression\_level')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupConfigCreate.CompressionLevel "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupConfigCreate._abc_impl "Link to this definition")_pydanticmodel_ weaviate.backup.backup.BackupConfigRestore [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupConfigRestore) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupConfigRestore "Link to this definition")

Bases: [`_BackupConfigBase`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup._BackupConfigBase "weaviate.backup.backup._BackupConfigBase")

Options to configure the backup when restoring a backup.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupConfigRestore._abc_impl "Link to this definition")_pydanticmodel_ weaviate.backup.backup.BackupStatusReturn [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupStatusReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatusReturn "Link to this definition")

Bases: `BaseModel`

Return type of the backup status methods.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ backup\_id _:str_ _\[Required\]_ _(alias'id')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatusReturn.backup_id "Link to this definition")_field_ error _:str\|None_ _=None_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatusReturn.error "Link to this definition")_field_ path _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatusReturn.path "Link to this definition")_field_ status _: [BackupStatus](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatus "weaviate.backup.backup.BackupStatus")_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatusReturn.status "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatusReturn._abc_impl "Link to this definition")_pydanticmodel_ weaviate.backup.backup.BackupReturn [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupReturn "Link to this definition")

Bases: [`BackupStatusReturn`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatusReturn "weaviate.backup.backup.BackupStatusReturn")

Return type of the backup creation and restore methods.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ collections _:List\[str\]_ _\[Optional\]_ _(alias'classes')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupReturn.collections "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupReturn._abc_impl "Link to this definition")_pydanticmodel_ weaviate.backup.backup.BackupListReturn [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup.html#BackupListReturn) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupListReturn "Link to this definition")

Bases: `BaseModel`

Return type of the backup list method.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ backup\_id _:str_ _\[Required\]_ _(alias'id')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupListReturn.backup_id "Link to this definition")_field_ collections _:List\[str\]_ _\[Optional\]_ _(alias'classes')_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupListReturn.collections "Link to this definition")_field_ status _: [BackupStatus](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupStatus "weaviate.backup.backup.BackupStatus")_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupListReturn.status "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup.BackupListReturn._abc_impl "Link to this definition")

## weaviate.backup.backup\_location [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html\#module-weaviate.backup.backup_location "Link to this heading")

_pydanticmodel_ weaviate.backup.backup\_location.\_BackupLocationConfig [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup_location.html#_BackupLocationConfig) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationConfig "Link to this definition")

Bases: `BaseModel`

The dynamic location of a backup.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

\_to\_dict() [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup_location.html#_BackupLocationConfig._to_dict) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationConfig._to_dict "Link to this definition")Return type:

_Dict_\[str, _Any_\]

\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationConfig._abc_impl "Link to this definition")_pydanticmodel_ weaviate.backup.backup\_location.\_BackupLocationFilesystem [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup_location.html#_BackupLocationFilesystem) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationFilesystem "Link to this definition")

Bases: [`_BackupLocationConfig`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationConfig "weaviate.backup.backup_location._BackupLocationConfig")

The dynamic location of a backup for filesystem.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ path _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationFilesystem.path "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationFilesystem._abc_impl "Link to this definition")_pydanticmodel_ weaviate.backup.backup\_location.\_BackupLocationS3 [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup_location.html#_BackupLocationS3) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationS3 "Link to this definition")

Bases: [`_BackupLocationConfig`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationConfig "weaviate.backup.backup_location._BackupLocationConfig")

The dynamic location of a backup for S3.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ bucket _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationS3.bucket "Link to this definition")_field_ path _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationS3.path "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationS3._abc_impl "Link to this definition")_pydanticmodel_ weaviate.backup.backup\_location.\_BackupLocationGCP [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup_location.html#_BackupLocationGCP) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationGCP "Link to this definition")

Bases: [`_BackupLocationConfig`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationConfig "weaviate.backup.backup_location._BackupLocationConfig")

The dynamic location of a backup for GCP.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ bucket _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationGCP.bucket "Link to this definition")_field_ path _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationGCP.path "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationGCP._abc_impl "Link to this definition")_pydanticmodel_ weaviate.backup.backup\_location.\_BackupLocationAzure [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup_location.html#_BackupLocationAzure) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationAzure "Link to this definition")

Bases: [`_BackupLocationConfig`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationConfig "weaviate.backup.backup_location._BackupLocationConfig")

The dynamic location of a backup for Azure.

Create a new model by parsing and validating input data from keyword arguments.

Raises \[ValidationError\]\[pydantic\_core.ValidationError\] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

_field_ bucket _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationAzure.bucket "Link to this definition")_field_ path _:str_ _\[Required\]_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationAzure.path "Link to this definition")\_abc\_impl _=<\_abc.\_abc\_dataobject>_ [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationAzure._abc_impl "Link to this definition")_class_ weaviate.backup.backup\_location.BackupLocation [\[source\]](https://weaviate-python-client.readthedocs.io/en/stable/_modules/weaviate/backup/backup_location.html#BackupLocation) [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location.BackupLocation "Link to this definition")

Bases: `object`

The dynamic path of a backup.

FileSystem [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location.BackupLocation.FileSystem "Link to this definition")

alias of [`_BackupLocationFilesystem`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationFilesystem "weaviate.backup.backup_location._BackupLocationFilesystem")

S3 [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location.BackupLocation.S3 "Link to this definition")

alias of [`_BackupLocationS3`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationS3 "weaviate.backup.backup_location._BackupLocationS3")

GCP [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location.BackupLocation.GCP "Link to this definition")

alias of [`_BackupLocationGCP`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationGCP "weaviate.backup.backup_location._BackupLocationGCP")

Azure [](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location.BackupLocation.Azure "Link to this definition")

alias of [`_BackupLocationAzure`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html#weaviate.backup.backup_location._BackupLocationAzure "weaviate.backup.backup_location._BackupLocationAzure")

Versions[latest](https://weaviate-python-client.readthedocs.io/en/latest/weaviate.backup.html)**[stable](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.backup.html)**[v4.16.10](https://weaviate-python-client.readthedocs.io/en/v4.16.10/weaviate.backup.html)[v4.16.9](https://weaviate-python-client.readthedocs.io/en/v4.16.9/weaviate.backup.html)[v4.16.8](https://weaviate-python-client.readthedocs.io/en/v4.16.8/weaviate.backup.html)[v4.16.7](https://weaviate-python-client.readthedocs.io/en/v4.16.7/weaviate.backup.html)[v4.16.6](https://weaviate-python-client.readthedocs.io/en/v4.16.6/weaviate.backup.html)[v4.16.5](https://weaviate-python-client.readthedocs.io/en/v4.16.5/weaviate.backup.html)[v4.16.4](https://weaviate-python-client.readthedocs.io/en/v4.16.4/weaviate.backup.html)[v4.16.3](https://weaviate-python-client.readthedocs.io/en/v4.16.3/weaviate.backup.html)[v4.16.2](https://weaviate-python-client.readthedocs.io/en/v4.16.2/weaviate.backup.html)[v4.16.1](https://weaviate-python-client.readthedocs.io/en/v4.16.1/weaviate.backup.html)[v4.16.0](https://weaviate-python-client.readthedocs.io/en/v4.16.0/weaviate.backup.html)[v4.15.4](https://weaviate-python-client.readthedocs.io/en/v4.15.4/weaviate.backup.html)[v4.15.3](https://weaviate-python-client.readthedocs.io/en/v4.15.3/weaviate.backup.html)[v4.15.2](https://weaviate-python-client.readthedocs.io/en/v4.15.2/weaviate.backup.html)[v4.15.1](https://weaviate-python-client.readthedocs.io/en/v4.15.1/weaviate.backup.html)[v4.15.0](https://weaviate-python-client.readthedocs.io/en/v4.15.0/weaviate.backup.html)[v4.14.4](https://weaviate-python-client.readthedocs.io/en/v4.14.4/weaviate.backup.html)[v4.14.3](https://weaviate-python-client.readthedocs.io/en/v4.14.3/weaviate.backup.html)[v4.14.2](https://weaviate-python-client.readthedocs.io/en/v4.14.2/weaviate.backup.html)[v4.14.1](https://weaviate-python-client.readthedocs.io/en/v4.14.1/weaviate.backup.html)[v4.14.0](https://weaviate-python-client.readthedocs.io/en/v4.14.0/weaviate.backup.html)[v4.13.2](https://weaviate-python-client.readthedocs.io/en/v4.13.2/weaviate.backup.html)[v4.13.1](https://weaviate-python-client.readthedocs.io/en/v4.13.1/weaviate.backup.html)[v4.13.0](https://weaviate-python-client.readthedocs.io/en/v4.13.0/weaviate.backup.html)[v4.12.1](https://weaviate-python-client.readthedocs.io/en/v4.12.1/weaviate.backup.html)[v4.12.0](https://weaviate-python-client.readthedocs.io/en/v4.12.0/weaviate.backup.html)[v4.11.3](https://weaviate-python-client.readthedocs.io/en/v4.11.3/weaviate.backup.html)[v4.11.2](https://weaviate-python-client.readthedocs.io/en/v4.11.2/weaviate.backup.html)[v4.11.1](https://weaviate-python-client.readthedocs.io/en/v4.11.1/weaviate.backup.html)[v4.11.0](https://weaviate-python-client.readthedocs.io/en/v4.11.0/weaviate.backup.html)[v4.10.4](https://weaviate-python-client.readthedocs.io/en/v4.10.4/weaviate.backup.html)[v4.10.3](https://weaviate-python-client.readthedocs.io/en/v4.10.3/weaviate.backup.html)[v4.10.2](https://weaviate-python-client.readthedocs.io/en/v4.10.2/weaviate.backup.html)[v4.10.0](https://weaviate-python-client.readthedocs.io/en/v4.10.0/weaviate.backup.html)[v4.9.6](https://weaviate-python-client.readthedocs.io/en/v4.9.6/weaviate.backup.html)[v4.9.5](https://weaviate-python-client.readthedocs.io/en/v4.9.5/weaviate.backup.html)[v4.9.4](https://weaviate-python-client.readthedocs.io/en/v4.9.4/weaviate.backup.html)[v4.9.3](https://weaviate-python-client.readthedocs.io/en/v4.9.3/weaviate.backup.html)[v4.9.2](https://weaviate-python-client.readthedocs.io/en/v4.9.2/weaviate.backup.html)[v4.9.1](https://weaviate-python-client.readthedocs.io/en/v4.9.1/weaviate.backup.html)[v4.9.0](https://weaviate-python-client.readthedocs.io/en/v4.9.0/weaviate.backup.html)[v4.8.1](https://weaviate-python-client.readthedocs.io/en/v4.8.1/weaviate.backup.html)[v4.8.0](https://weaviate-python-client.readthedocs.io/en/v4.8.0/weaviate.backup.html)[v4.7.1](https://weaviate-python-client.readthedocs.io/en/v4.7.1/weaviate.backup.html)[v4.7.0](https://weaviate-python-client.readthedocs.io/en/v4.7.0/weaviate.backup.html)[v4.6.7](https://weaviate-python-client.readthedocs.io/en/v4.6.7/weaviate.backup.html)[v4.6.6](https://weaviate-python-client.readthedocs.io/en/v4.6.6/weaviate.backup.html)[v4.6.5](https://weaviate-python-client.readthedocs.io/en/v4.6.5/weaviate.backup.html)[v4.6.4](https://weaviate-python-client.readthedocs.io/en/v4.6.4/weaviate.backup.html)[v4.6.3](https://weaviate-python-client.readthedocs.io/en/v4.6.3/weaviate.backup.html)[v4.6.2](https://weaviate-python-client.readthedocs.io/en/v4.6.2/weaviate.backup.html)[v4.6.1](https://weaviate-python-client.readthedocs.io/en/v4.6.1/weaviate.backup.html)[v4.6.0](https://weaviate-python-client.readthedocs.io/en/v4.6.0/weaviate.backup.html)[v4.5.7](https://weaviate-python-client.readthedocs.io/en/v4.5.7/weaviate.backup.html)[v4.5.6](https://weaviate-python-client.readthedocs.io/en/v4.5.6/weaviate.backup.html)[v4.5.5](https://weaviate-python-client.readthedocs.io/en/v4.5.5/weaviate.backup.html)[v4.5.4](https://weaviate-python-client.readthedocs.io/en/v4.5.4/weaviate.backup.html)[v4.5.3](https://weaviate-python-client.readthedocs.io/en/v4.5.3/weaviate.backup.html)[v4.5.2](https://weaviate-python-client.readthedocs.io/en/v4.5.2/weaviate.backup.html)[v4.5.1](https://weaviate-python-client.readthedocs.io/en/v4.5.1/weaviate.backup.html)[v4.5.0](https://weaviate-python-client.readthedocs.io/en/v4.5.0/weaviate.backup.html)[v4.4.4](https://weaviate-python-client.readthedocs.io/en/v4.4.4/weaviate.backup.html)[v4.4.3](https://weaviate-python-client.readthedocs.io/en/v4.4.3/weaviate.backup.html)[v4.4.2](https://weaviate-python-client.readthedocs.io/en/v4.4.2/weaviate.backup.html)[v4.4.1](https://weaviate-python-client.readthedocs.io/en/v4.4.1/weaviate.backup.html)[v4.4.0](https://weaviate-python-client.readthedocs.io/en/v4.4.0/weaviate.backup.html)[v3.26.2](https://weaviate-python-client.readthedocs.io/en/v3.26.2/weaviate.backup.html)[v3.26.1](https://weaviate-python-client.readthedocs.io/en/v3.26.1/weaviate.backup.html)[v3.26.0](https://weaviate-python-client.readthedocs.io/en/v3.26.0/weaviate.backup.html)[v3.25.3](https://weaviate-python-client.readthedocs.io/en/v3.25.3/weaviate.backup.html)[v3.25.2](https://weaviate-python-client.readthedocs.io/en/v3.25.2/weaviate.backup.html)[v3.23.0](https://weaviate-python-client.readthedocs.io/en/v3.23.0/weaviate.backup.html)[v3.22.1](https://weaviate-python-client.readthedocs.io/en/v3.22.1/weaviate.backup.html)[v3.22.0](https://weaviate-python-client.readthedocs.io/en/v3.22.0/weaviate.backup.html)[v3.21.0](https://weaviate-python-client.readthedocs.io/en/v3.21.0/weaviate.backup.html)[v3.20.1](https://weaviate-python-client.readthedocs.io/en/v3.20.1/weaviate.backup.html)[v3.20.0](https://weaviate-python-client.readthedocs.io/en/v3.20.0/weaviate.backup.html)[v3.19.2](https://weaviate-python-client.readthedocs.io/en/v3.19.2/weaviate.backup.html)[v3.19.1](https://weaviate-python-client.readthedocs.io/en/v3.19.1/weaviate.backup.html)[v3.19.0](https://weaviate-python-client.readthedocs.io/en/v3.19.0/weaviate.backup.html)[v3.18.0](https://weaviate-python-client.readthedocs.io/en/v3.18.0/weaviate.backup.html)[v3.15.6](https://weaviate-python-client.readthedocs.io/en/v3.15.6/weaviate.backup.html)[v3.15.5](https://weaviate-python-client.readthedocs.io/en/v3.15.5/weaviate.backup.html)[v3.15.4](https://weaviate-python-client.readthedocs.io/en/v3.15.4/weaviate.backup.html)[v3.15.3](https://weaviate-python-client.readthedocs.io/en/v3.15.3/weaviate.backup.html)[v3.15.2](https://weaviate-python-client.readthedocs.io/en/v3.15.2/weaviate.backup.html)[v3.15.1](https://weaviate-python-client.readthedocs.io/en/v3.15.1/weaviate.backup.html)[v3.15.0](https://weaviate-python-client.readthedocs.io/en/v3.15.0/weaviate.backup.html)[v3.14.0](https://weaviate-python-client.readthedocs.io/en/v3.14.0/weaviate.backup.html)[v3.13.0](https://weaviate-python-client.readthedocs.io/en/v3.13.0/weaviate.backup.html)[v3.12.0\_a](https://weaviate-python-client.readthedocs.io/en/v3.12.0_a/weaviate.backup.html)[v3.11.0](https://weaviate-python-client.readthedocs.io/en/v3.11.0/weaviate.backup.html)[v3.10.0](https://weaviate-python-client.readthedocs.io/en/v3.10.0/weaviate.backup.html)[v3.9.0](https://weaviate-python-client.readthedocs.io/en/v3.9.0/weaviate.backup.html)[v3.8.0](https://weaviate-python-client.readthedocs.io/en/v3.8.0/weaviate.backup.html)[v3.7.0](https://weaviate-python-client.readthedocs.io/en/v3.7.0/weaviate.backup.html)[v3.6.0](https://weaviate-python-client.readthedocs.io/en/v3.6.0/weaviate.backup.html)[v3.5.1](https://weaviate-python-client.readthedocs.io/en/v3.5.1/weaviate.backup.html)[v3.5.0](https://weaviate-python-client.readthedocs.io/en/v3.5.0/weaviate.backup.html)[v3.4.1](https://weaviate-python-client.readthedocs.io/en/v3.4.1/weaviate.backup.html)[v3.4.0](https://weaviate-python-client.readthedocs.io/en/v3.4.0/weaviate.backup.html)[v3.3.3](https://weaviate-python-client.readthedocs.io/en/v3.3.3/weaviate.backup.html)[v3.3.2](https://weaviate-python-client.readthedocs.io/en/v3.3.2/weaviate.backup.html)[v3.3.1](https://weaviate-python-client.readthedocs.io/en/v3.3.1/weaviate.backup.html)[v3.3.0](https://weaviate-python-client.readthedocs.io/en/v3.3.0/weaviate.backup.html)[v3.2.5](https://weaviate-python-client.readthedocs.io/en/v3.2.5/weaviate.backup.html)[v3.2.4](https://weaviate-python-client.readthedocs.io/en/v3.2.4/weaviate.backup.html)[v3.2.3](https://weaviate-python-client.readthedocs.io/en/v3.2.3/weaviate.backup.html)[v3.2.2](https://weaviate-python-client.readthedocs.io/en/v3.2.2/weaviate.backup.html)[v3.2.1](https://weaviate-python-client.readthedocs.io/en/v3.2.1/weaviate.backup.html)[v3.2.0](https://weaviate-python-client.readthedocs.io/en/v3.2.0/weaviate.backup.html)[v3.1.1](https://weaviate-python-client.readthedocs.io/en/v3.1.1/weaviate.backup.html)[v3.1.0](https://weaviate-python-client.readthedocs.io/en/v3.1.0/weaviate.backup.html)[v3.0.0](https://weaviate-python-client.readthedocs.io/en/v3.0.0/weaviate.backup.html)On Read the Docs[Project Home](https://app.readthedocs.org/projects/weaviate-python-client/?utm_source=weaviate-python-client&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/weaviate-python-client/builds/?utm_source=weaviate-python-client&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=weaviate-python-client&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=weaviate-python-client&utm_content=flyout)