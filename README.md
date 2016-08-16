# QUBS Climate Data API

A web API for accessing live data from the Queen's University Biological Station Climate Data network. The data
retrieved from this API is provided **completely as-is**. It should be made known that there is no quality assurance
or proofreading done to data stored hear and thus readings may be inaccurate.

## Requirements and Technologies

Requirements are listed programmatically in the `requirements.txt` file. The API is built on the
[Django Rest Framework](http://www.django-rest-framework.org/) and uses [PostgreSQL](https://www.postgresql.org/) for
a database.

## Accessing Data

The API is hosted at [http://climate.qubs.ca/api/](http://climate.qubs.ca/api/). Listed below are request paths based
on this URL for fetching data programmatically.

### `GET /messages/`

Lists all messages from the past 7 days sent from the stations.

#### Parameters

TODO

#### Example Request

TODO

### `GET /messages/[id]/` (where `[id]` is the numeric id of a message)

Shows a single message object.

#### Example request

```
GET /messages/2/
Host: climate.qubs.ca
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
    "values": [18600, 15200, 15500, 14500, 102, 101, 176, 246,2383,2341,2310,2316,2385,2360,2345,2350,2265,2182,2130,2118,9490,9570,9589,9598,94840,94840,94840,94840,2395,2404,2413,2400,1559,1559,1559,1559],
    "message_text":"C7A0159216226221911G39+0NN019EUB00114bB1DDbhCm`CrLCbd@Af@Ae@Bp@Cv@eO@de@dF@dL@eQ@dx@di@dn@cY@bF@aR@aFBTRBUbBUuBU~WIxWIxWIxWIx@e[@ed@em@e`@XW@XW@XW@XWI",
    "station": 8
}
```

### `GET /readings/`

#### Parameters

TODO

#### Example Request

TODO

### `GET /sensors/`

#### Parameters

TODO

#### Example Request

TODO

### `GET /stations/`

#### Parameters

TODO

#### Example Request

```
GET /stations/
Host: climate.qubs.ca
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
    },
    .
    .
    .
]
```

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
    "values": [18600, 15200, 15500, 14500, 102, 101, 176, 246, 2383, 2341, 2310, 2316, 2385, 2360, 2345, 2350, 2265,
        2182, 2130, 2118, 9490, 9570, 9589, 9598, 94840, 94840, 94840, 94840, 2395, 2404, 2413, 2400, 1559,
        1559, 1559, 1559],
    "message_text": "C7A0159216226221911G39+0NN019EUB00114bB1DDbhCm`CrLCbd@Af@Ae@Bp@Cv@eO@de@dF@dL@eQ@dx@di@dn@cY@bF@aR@aFBTRBUbBUuBU~WIxWIxWIxWIx@e[@ed@em@e`@XW@XW@XW@XWI",
    "station": null
}
```

### Reading

#### Format

TODO

#### Fields

TODO

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
