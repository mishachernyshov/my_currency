# MyCurrency

## Overview
MyCurrency is a web platform that allows users to calculate currency exchange rates.

## Installation
### Prerequisites
Required:
- [Docker](https://docs.docker.com/engine/install/)
- [Make](https://www.gnu.org/software/make/)

Development:
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Project set up
To allow [CurrencyBeacon](https://currencybeacon.com/) provider usage, set your
CurrencyBeacon API key value for `CURRENCY_BEACON_API_KEY` variable in 
*envs/local/web.env*.

To build and run the project, run

```shell
make build
```

By default, the service will be accessible at `http://localhost:8000/`.
