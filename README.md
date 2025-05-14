# Simple Data Counter

A command-line tool to count records in InfluxDB for either vital data or device status data.

## Requirements

- Python 3.7+
- influxdb-client (install with `pip install influxdb-client`)

## Usage

```bash
python counter.py --config <config_file> --type <vital|device_status> [other options]
```

### Parameters

- `--config` (required): Path to InfluxDB config file
- `--type` (required): Type of data to query: `vital` or `device_status`
- `--start` (required): Start time (e.g. 2025-05-13T00:30:00Z)
- `--end` (required): End time (e.g. 2025-05-13T18:30:59Z)
- `--id`: Device user ID (required for `vital`)
- `--device-type`: Device type (required for `device_status`)
- `--device-id`: Device ID (required for `device_status`)

### Examples

#### Count vital records

```bash
python counter.py --config influxdb_config.ini --type vital --id 1f0111bf-f975-6e37-adc5-dd4e03a22082 --start 2025-05-13T00:30:00Z --end 2025-05-13T18:30:59Z
```

#### Count device status records

```bash
python counter.py --config influxdb_config.ini --type device_status --device-type 2 --device-id 1000200 --start 2025-05-13T00:30:00Z --end 2025-05-13T18:30:59Z
```

## Output

The program prints the count result to the console:

```bash
<number>
```
