import sys
from .counter import InfluxDBVitalCounter, InfluxDBDeviceStatusCounter

from .file_parser import parse_output_file
from .core_api import get_device_user


def main():
    # Support reading output file from stdin (pipeline) or as a file
    if not sys.stdin.isatty():
        # Read from stdin and write to a temp file
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            tmp.write(sys.stdin.read())
            tmp.flush()
            output_file = tmp.name
    else:
        output_file = "output.txt"

    # Parse output file to get parameters
    result = parse_output_file(output_file)

    device_type = result.deviceType
    device_id = result.deviceId
    # Get device user ID from core API
    device_user_id = get_device_user(device_type, device_id).id
    print(f"Device user ID: {device_user_id}")

    vital_counter = InfluxDBVitalCounter("influxdb_config.ini")
    vital_count = vital_counter.get(
        id=device_user_id,
        start=result.start.isoformat(),
        end=result.end.isoformat(),
    )
    print(f"File count: {result.vital_request_count}, Query count: {vital_count}")

    device_counter = InfluxDBDeviceStatusCounter("influxdb_config.ini")
    device_count = device_counter.get(
        id=(device_type, device_id),
        start=result.start.isoformat(),
        end=result.end.isoformat(),
    )

    print(
        f"File count: {result.device_status_request_count}, Query count: {device_count}"
    )

    print(f"Vital count match: {result.vital_request_count == vital_count}")
    print(
        f"Device status count match: {result.device_status_request_count == device_count}"
    )


if __name__ == "__main__":
    main()
