# Simple Data Counter

A command-line tool to count records in InfluxDB for either vital data or device status data, and to compare these counts with those found in an output log file.

## Requirements

- Python 3.7+
- influxdb-client (install with `pip install influxdb-client`)

## Usage

### 1. Count Directly from InfluxDB

```bash
python counter.py --config <config_file> --type <vital|device_status> [other options]
```

#### Parameters

- `--config` (required): Path to InfluxDB config file
- `--type` (required): Type of data to query: `vital` or `device_status`
- `--start` (required): Start time (e.g. 2025-05-13T00:30:00Z)
- `--end` (required): End time (e.g. 2025-05-13T18:30:59Z)
- `--id`: Device user ID (required for `vital`)
- `--device-type`: Device type (required for `device_status`)
- `--device-id`: Device ID (required for `device_status`)

#### Examples

Count vital records:

```bash
python counter.py --config influxdb_config.ini --type vital --id 1f0111bf-f975-6e37-adc5-dd4e03a22082 --start 2025-05-13T00:30:00Z --end 2025-05-13T18:30:59Z
```

Count device status records:

```bash
python counter.py --config influxdb_config.ini --type device_status --device-type 2 --device-id 1000200 --start 2025-05-13T00:30:00Z --end 2025-05-13T18:30:59Z
```

#### Example Output

When you run the command, you might see output similar to:

```bash
18118
```

Or for device status:

```bash
1079
```

### 2. Compare Output Log File with InfluxDB Query

You can use `main.py` to parse an output log (such as `output.txt`), extract the relevant time range and request counts, and compare them with the counts queried from InfluxDB.

#### How to Use with Output Log

- Using a file:

  ```bash
  python main.py
  ```

  (This will use `output.txt` in the current directory.)

- Using a pipeline:

  ```bash
  cat output.txt | python main.py
  ```

#### Output

The program prints the file count, query count, and whether they match for both vital and device status:

```bash
Running vital count:
File count: 2, Query count: 2
Match!
Running device status count:
File count: 1, Query count: 1
Match!
```

## Configuration

Copy `influxdb_config.ini.template` to `influxdb_config.ini` and fill in your InfluxDB credentials.
