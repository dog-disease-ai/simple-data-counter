import sys
from file_parser import parse_output_file
import subprocess
import re

if __name__ == "__main__":
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
    # Call counter.py for vital
    vital_cmd = [
        "python3",
        "counter.py",
        "--config",
        "influxdb_config.ini",
        "--type",
        "vital",
        "--id",
        "1f0111bf-f975-6e37-adc5-dd4e03a22082",
        "--start",
        result.start.isoformat(),
        "--end",
        result.end.isoformat(),
    ]
    print("Running vital count:")
    vital_proc = subprocess.run(vital_cmd, capture_output=True, text=True)
    # Extract the last integer from the output (robust for pipeline usage)
    vital_query_count = None
    for line in vital_proc.stdout.splitlines():
        match = re.search(r"(\d+)$", line.strip())
        if match:
            vital_query_count = int(match.group(1))
    if vital_query_count is None:
        print("Failed to parse vital query count from output:", vital_proc.stdout)
    print(f"File count: {result.vital_request_count}, Query count: {vital_query_count}")
    if vital_query_count is not None:
        print(
            "Match!" if result.vital_request_count == vital_query_count else "Mismatch!"
        )

    # Call counter.py for device_status
    device_status_cmd = [
        "python3",
        "counter.py",
        "--config",
        "influxdb_config.ini",
        "--type",
        "device_status",
        "--device-type",
        "2",
        "--device-id",
        "1000200",
        "--start",
        result.start.isoformat(),
        "--end",
        result.end.isoformat(),
    ]
    print("Running device status count:")
    device_proc = subprocess.run(device_status_cmd, capture_output=True, text=True)
    device_query_count = None
    for line in device_proc.stdout.splitlines():
        match = re.search(r"(\d+)$", line.strip())
        if match:
            device_query_count = int(match.group(1))
    if device_query_count is None:
        print(
            "Failed to parse device status query count from output:", device_proc.stdout
        )
    print(
        f"File count: {result.device_status_request_count}, Query count: {device_query_count}"
    )
    if device_query_count is not None:
        print(
            "Match!"
            if result.device_status_request_count == device_query_count
            else "Mismatch!"
        )
