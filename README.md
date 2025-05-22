# Simple Data Counter

A command-line tool to count records in InfluxDB for either vital data or device status data, and to compare these counts with those found in an output log file. The tool can also fetch device user IDs from a core API.

## Requirements

- Python 3.7+
- influxdb-client (install with `pip install influxdb-client`)
- requests (install with `pip install requests`)

## Installation (as CLI)

1. Install the package in your environment:

   ```bash
   pip install .
   ```

2. This will provide the CLI command:

   ```bash
   simple-data-counter
   ```

## Usage

### 1. Count Directly from InfluxDB

You can use the counter module directly (for advanced use):

```bash
python -m data_counter.counter --config <config_file> --type <vital|device_status> [other options]
```

#### Parameters

- `--config` (required): Path to InfluxDB config file
- `--type` (required): Type of data to query: `vital` or `device_status`
- `--start` (required): Start time (e.g. 2025-05-13T00:30:00Z)
- `--end` (required): End time (e.g. 2025-05-13T18:30:59Z)
- `--id`: Device user ID (required for `vital`)
- `--device-type`: Device type (required for `device_status`)
- `--device-id`: Device ID (required for `device_status`)

#### Example

Count vital records:

```bash
python -m data_counter.counter --config influxdb_config.ini --type vital --id 1f0111bf-f975-6e37-adc5-dd4e03a22082 --start 2025-05-13T00:30:00Z --end 2025-05-13T18:30:59Z
```

Count device status records:

```bash
python -m data_counter.counter --config influxdb_config.ini --type device_status --device-type 2 --device-id 1000200 --start 2025-05-13T00:30:00Z --end 2025-05-13T18:30:59Z
```

### 2. Compare Output Log File with InfluxDB Query

The main CLI entry point is:

```bash
simple-data-counter
```

This will:

- Parse `output.txt` (or accept piped input)
- Extract the relevant time range, device type, device id, and request counts
- Fetch the device user ID from the core API
- Query InfluxDB for both vital and device status counts
- Print a comparison summary

#### How to Use

- Using a file:

  ```bash
  simple-data-counter
  ```

  (This will use `output.txt` in the current directory.)

- Using a pipeline:

  ```bash
  cat output.txt | simple-data-counter
  ```

#### Output

The program prints the file count, query count, and whether they match for both vital and device status:

```bash
Device user ID: 1f0111bf-f975-6e37-adc5-dd4e03a22082
File count: 2, Query count: 2
File count: 1, Query count: 1
Vital count match: True
Device status count match: True
```

## Configuration

- Copy `influxdb_config.ini.template` to `influxdb_config.ini` and fill in your InfluxDB credentials.
- Copy `core_api_config.ini.template` to `core_api_config.ini` and fill in your Core API credentials.
