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

### `messages/`

Lists all messages from the past 7 days sent from the stations.

#### Parameters

TODO

### `messages/[id]/` (where `[id]` is the numeric id of a message)

Shows a single message object.

#### Example Response

### `readings/`

#### Parameters

TODO

### `sensors/`

#### Parameters

TODO

### `stations/`

#### Parameters

TODO

## Object Types

### Message

#### Format

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
                   1559, 1559, 1559
                  ],
        "message_text": "C7A0159216226221911G39+0NN019EUB00114bB1DDbhCm`CrLCbd@Af@Ae@Bp@Cv@eO@de@dF@dL@eQ@dx@di@dn@cY@bF@aR@aFBTRBUbBUuBU~WIxWIxWIxWIx@e[@ed@em@e`@XW@XW@XW@XWI",
        "station": null
    }

### Reading

#### Format

TODO

### Sensor

#### Format

    {
        "id": 1,
        "created": "2016-08-15T14:57:16.130683Z",
        "updated": "2016-08-15T14:57:16.130716Z",
        "name": "lufft_ws_502umb_temp",
        "data_id": "air_temp",
        "decimals": 2
    }

### Station

#### Format

    {
        "id": 1,
        "created": "2016-08-16T13:13:50.932622Z",
        "updated": "2016-08-16T13:13:50.932680Z",
        "name": "Elbow Lake",
        "goes_id": "C7A0337E",
        "sensors": [1, 2, 3, 4, 5, 6, 9, 10, 12]
    }
