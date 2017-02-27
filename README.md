# QUBS Climate Data API

A web API for accessing live data from the Queen's University Biological Station Climate Data network. The data
retrieved from this API is provided **completely as-is**. It should be made known that there is no quality assurance
or proofreading done to data stored hear and thus readings may be inaccurate.

## Contents

* [Requirements and Technologies](#requirements-and-technologies)
* [Accessing API Data](#accessing-api-data)
    * [`GET /messages/`](#get-messages)
    * [`GET /messages/latest/`](#get-messageslatest)
    * [`GET /messages/[id]/`](#get-messagesid-where-id-is-the-numeric-id-of-a-message)
    * [`GET /readings/`](#get-readings)
    * [`GET /readings/[id]/`](#get-readingsid-where-id-is-the-numeric-id-of-a-reading)
    * [`GET /sensors/`](#get-sensors)
    * [`GET /sensors/[id]/`](#get-sensorsid-where-id-is-the-numeric-id-of-a-sensor)
    * [`GET /stations/`](#get-stations)
    * [`GET /stations/[id]/`](#get-stationsid-where-id-is-the-numeric-id-of-a-station)
* [Object Types](#object-types)
    * [Message](#message)
    * [Reading](#reading)
    * [Sensor](#sensor)
    * [Station](#station)

## Requirements and Technologies

Requirements are listed programmatically in the `requirements.txt` file. The API is built on the
[Django Rest Framework](http://www.django-rest-framework.org/) and uses [PostgreSQL](https://www.postgresql.org/) for
a database.

## Installation

### Database

Make sure PostgreSQL 9.5 or later is installed on your web server.

### API Server

1. Download the latest release from the [releases page](https://github.com/qubs/climate-data-api/releases) of the
repository.

2. Unzip it to a directory not directly accessible from the web.

3. Enter the directory and create a virtual environment for the API server withg the command `virtualenv env`.

4. Source the virtual environment with `source env/bin/activate`.

5. Download the dependencies with `pip3 install -r requirements.txt`.

### Apache HTTPD

**BE CAREFUL!** The version of `mod_wsgi` shipped with Ubuntu Server 14.04 does not work with the version of Python 3
provided by the OS. It is necessary to [install a newer version](http://askubuntu.com/questions/569550/assertionerror-using-apache2-and-libapache2-mod-wsgi-py3-on-ubuntu-14-04-python/569551#569551)
of `mod_wsgi`.

`WSGIPassAuthorization On`

### NGINX

TODO

## Accessing API Data

The API is hosted at [http://api.climate.qubs.ca](http://api.climate.qubs.ca). Listed below are request paths based
on this URL for fetching data programmatically.

### `GET /messages/`

Lists all messages from the past 7 days sent from the stations.

#### Parameters

`start`: TODO

`start_exclusive`: TODO

`end`: TODO

#### Example Request

TODO

### `GET /messages/latest/`

#### Parameters

None.

#### Example Request

```
GET /messages/latest/
Host: api.climate.qubs.ca
```

```json
[
    {
        "id": 25088,
        "created": "2017-02-26T22:35:04.007139Z",
        "updated": "2017-02-26T22:35:04.007224Z",
        "goes_id": "C7A867A4",
        "goes_channel": 19,
        "goes_spacecraft": "E",
        "arrival_time": "2017-02-26T22:20:11Z",
        "failure_code": "G",
        "signal_strength": 38,
        "frequency_offset": "+0",
        "modulation_index": "N",
        "data_quality": "N",
        "data_source": "UP",
        "recorded_message_length": 198,
        "values": [],
        "message_text": "...",
        "station": 6
    },
    {
        "id": 25090,
        "created": "2017-02-26T23:20:05.087461Z",
        "updated": "2017-02-26T23:20:05.087565Z",
        "goes_id": "C7A02008",
        "goes_channel": 19,
        "goes_spacecraft": "E",
        "arrival_time": "2017-02-26T23:19:21Z",
        "failure_code": "G",
        "signal_strength": 41,
        "frequency_offset": "+0",
        "modulation_index": "N",
        "data_quality": "N",
        "data_source": "UB",
        "recorded_message_length": 114,
        "values": [],
        "message_text": "...",
        "station": 2
    }
]
```

(Response truncated, message and values removed for conciseness)

### `GET /messages/[id]/` (where `[id]` is the numeric ID of a message)

Shows a single message object.

#### Example request

```
GET /messages/2/
Host: api.climate.qubs.ca
```

```json
{
    "id": 2,
    "created": "2016-08-13T23:07:30.336944Z",
    "updated": "2016-08-13T23:07:30.336979Z",
    "goes_id": "C7A01592",
    "goes_channel": 19,
    "goes_spacecraft": "E",
    "arrival_time": "2016-08-13T22:19:11Z",
    "failure_code": "G",
    "signal_strength": 39,
    "frequency_offset": "+0",
    "modulation_index": "N",
    "data_quality": "N",
    "data_source": "UB",
    "recorded_message_length": 114,
    "values": [],
    "message_text":"...",
    "station": 8
}
```

(Message and values removed for conciseness)

### `GET /readings/`

#### Parameters

`start`: TODO

`start_exclusive`: TODO

`end`: TODO

`sensors`: TODO

#### Example Request

TODO

### `GET /readings/[id]/` (where `[id]` is the numeric ID of a reading)

#### Parameters

None.

#### Example Request

TODO

### `GET /sensors/`

#### Parameters

None.

#### Example Request

TODO

### `GET /sensors/[id]/` (where `[id]` is the numeric ID of a sensor)

#### Parameters

None.

#### Example Request

TODO

### `GET /stations/`

#### Parameters

`goes_id`: TODO

#### Example Request

```
GET /stations/
Host: api.climate.qubs.ca
```

```json
[
    {
        "id": 1,
        "created": "2016-08-16T13:13:50.932622Z",
        "updated": "2016-08-16T13:13:50.932680Z",
        "name": "Elbow Lake",
        "goes_id": "C7A0337E",
        "sensors": [1, 2, 3, 4, 5, 6, 9, 10, 12]
    },
    {
        "id": 2,
        "created": "2016-08-16T13:17:52.584038Z",
        "updated": "2016-08-16T13:17:52.584123Z",
        "name": "Hill Island",
        "goes_id": "C7A02008",
        "sensors": [1, 2, 5, 6, 7, 8, 9, 10, 11]
    }
]
```

(Response truncated for conciseness)

### `GET /stations/[id]/` (where `[id]` is the numeric ID of a station)

#### Parameters

None.

#### Example Request

TODO

## Object Types

### Message

#### Format

```json
{
    "id": 2,
    "created": "2016-08-13T23:07:30.336944Z",
    "updated": "2016-08-13T23:07:30.336979Z",
    "goes_id": "C7A01592",
    "goes_channel": 19,
    "goes_spacecraft": "E",
    "arrival_time": "2016-08-13T22:19:11Z",
    "failure_code": "G",
    "signal_strength": 39,
    "frequency_offset": "+0",
    "modulation_index": "N",
    "data_quality": "N",
    "data_source": "UB",
    "recorded_message_length": 114,
    "values": [],
    "message_text": "...",
    "station": 8
}
```

(Message and values removed for conciseness)

#### Fields

`id`: A unique numerical ID representing the message.

`created`: A timestamp when the message was created (not when it arrived, but when it was added to the database).

`updated`: A timestamp of when the message in the database was last changed.

`goes_id`: The GOES self-timed identifier / address, unique to a station. Made up of 4 2-hexadecimal digit numbers.

`goes_channel`:

`goes_spacecraft`: Which GOES satellite was used to transmit the message. Possible values are `E` for east and `W` for
west. All QUBS climate stations communicate with the `E`ast satellite.

`arrival_time`: The time of arrival of the message to the ground station.

`failure_code`: Indicates a possible issue with the message or an error generated by the NOAA's Data Collection System
(DCS) Data Auto-Processing System (DAPS). Possible values are listed
[here](http://eddn.usgs.gov/dcpformat.html#failure).

`signal_strength`: A 2-digit number indicating the signal strength
([EIRP](https://en.wikipedia.org/wiki/Equivalent_isotropically_radiated_power)) with an assumption that the pilot is a
+47 dBm reference.

`frequency_offset`: Indicating if the Data Collection Platform is transmititng above or below the centre channel
frequency. The first character will always be a `+` or `-`, and the second character can be `0` through `9` or an `A`.
Offset can be calculated by multiplying the value by 50 Hz. If the second character is `A`, the frequency offset is
`+` or `-` `500`.

`modulation_index`: Can be one of 3 values: `N`ormal, `L`ow, or `H`igh.

`data_quality`: Can be one of 3 values: `N`ormal, `F`air, or `P`oor.

`data_source`: A 2-character code indicating a receiving location. A lookup table can be found
[here](http://eddn.usgs.gov/dataSourceCodes.html).

`recorded_message_length`: The length of the message excluding all above metadata.

`values`: An **ordered** list of values, which are measurements taken by the station (before decimal point insertion).

`message_text`: The transmitted message in its original form.

`station`: The API ID of the station which transmitted the message.

### Reading

#### Format

```json
{
    "id": 187337,
    "created": "2016-08-23T01:59:48.078269Z",
    "updated": "2016-08-23T01:59:48.078298Z",
    "read_time": "2016-07-23T01:15:00Z",
    "data_source": "G",
    "value": 2870,
    "qc_processed": false,
    "invalid": false,
    "sensor": 1,
    "station": 1,
    "message": 4132
}
```

#### Fields

`id`: A unique numerical ID representing the reading.

`created`: A timestamp when the reading was created (not when it was taken, but when the data object was added to the
database).

`updated`: A timestamp of when the data object representing the reading in the database was last changed.

`read_time`: When the reading was taken (in UTC time).

`data_source`: Where the reading is sourced from. `G` means the value was downloaded from the **G**OES satellite, and
`L` means it was taken from the device data **L**og.

`value`: The value of the reading, raw from the message. Takes on a `null` value if the reading could not be parsed or
was deemed completely invalid by the auto-downloader. Does not include a decimal point (which can be located in the
details of the reading's sensor).

`qc_processed`: Whether or not a quality control system has processed and made a decision about the validity of this
reading.

`invalid`: Whether or not this point is invalid desplite posessing a non-`null` `value`.

`sensor`: The API ID of the sensor which took the reading.

`station`: The API ID of the station which transmitted the message and is linked with the aforementioned sensor.

`message`: The API Id of the GOES message which this reading was sourced from, if applicable.

### Sensor

#### Format

```json
{
    "id": 1,
    "created": "2016-08-15T14:57:16.130683Z",
    "updated": "2016-08-15T14:57:16.130716Z",
    "name": "lufft_ws_502umb_temp",
    "data_id": "air_temp",
    "decimals": 2
}
```

#### Fields

`id`: A unique numerical ID representing the sensor.

`created`: A timestamp when the sensor was created (not when it was installed, but when the data object was added to the
database).

`updated`: A timestamp of when the data object representing the sensor in the database was last changed.

`name`: A human- and machine-readable name representing the sensor. Preferably underscore-separated and all lowercase.

`data_id`: A generalized human- and machine-readable ID for displaying at the top of generated spreadsheets, etc.

`decimals`: How many decimal places a reading from the sensor has (as the climate stations only transmit whole numbers).

### Station

#### Format

```json
{
    "id": 1,
    "created": "2016-08-16T13:13:50.932622Z",
    "updated": "2016-08-16T13:13:50.932680Z",
    "name": "Elbow Lake",
    "goes_id": "C7A0337E",
    "sensors": [1, 2, 3, 4, 5, 6, 9, 10, 12]
}
```

#### Fields

`id`: A unique numerical ID representing the station.

`created`: A timestamp when the station was created (not when it was installed, but when the data object was added to
the database).

`updated`: A timestamp of when the data object representing the station in the database was last changed.

`name`: A human-readable name for the station.

`goes_id`: The GOES self-timed identifier / address, unique to the station. Made up of 4 2-hexadecimal digit numbers.

`sensors`: An **unordered** list of links to data object representations of the sensors on the station.
