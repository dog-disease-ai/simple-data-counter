from dataclasses import dataclass
import re
from datetime import datetime, timezone


@dataclass
class OutputParseResult:
    """
    Dataclass to hold the parsed output file data.
    Attributes:
        start (datetime): Start time of the emulator.
        end (datetime): End time of the emulator.
        deviceType (str): Type of the device.
        deviceId (str): ID of the device.
        vital_request_count (int): Count of successful sensor data requests sent.
        device_status_request_count (int): Count of successful sync data requests sent.
    """

    start: datetime
    end: datetime
    deviceType: str
    deviceId: str
    vital_request_count: int
    device_status_request_count: int


def parse_output_file(filepath: str) -> OutputParseResult:
    """
    Parse the output.txt file to extract:
    - start time
    - end time
    - success sensor data requests sent (as vital_request_count)
    - success sync data requests sent (as device_status_request_count)
    Returns an OutputParseResult dataclass instance.
    """
    with open(filepath, "r") as f:
        content = f.read()

    start_time = re.search(r"Emulator Start Timestamp\s*:\s*(.*)", content)
    end_time = re.search(r"Emualtor End Timestamp\s*:\s*(.*)", content)
    device_type = re.search(r"Device Type\s*:\s*(.*)", content)
    device_id = re.search(r"Device ID\s*:\s*(.*)", content)
    if not (device_type and device_id):
        device_type = "2"  # use default device type
        device_id = "1000200"  # use default device id
    else:
        device_type = device_type.group(1).strip()
        device_id = device_id.group(1).strip()
    sensor_success = re.search(r"Success Sensor Data Requests Sent:\s*(\d+)", content)
    sync_success = re.search(r"Success Sync Data Requests Sent:\s*(\d+)", content)
    if not (sensor_success and sync_success):
        raise ValueError("Could not parse all required fields from the file.")
    else:
        sensor_success = sensor_success.group(1).strip()
        sync_success = sync_success.group(1).strip()

    if not (start_time and end_time and sensor_success and sync_success):
        raise ValueError("Could not parse all required fields from the file.")
    # Floor start to the beginning of the second, ceil end to the end of the second
    start_dt = datetime.strptime(
        start_time.group(1).strip(), "%Y-%m-%d %H:%M:%S.%f"
    ).astimezone(tz=timezone.utc)
    end_dt = datetime.strptime(
        end_time.group(1).strip(), "%Y-%m-%d %H:%M:%S.%f"
    ).astimezone(tz=timezone.utc)
    # Floor start (remove microseconds)
    start_dt = start_dt.replace(microsecond=0)
    # Ceil end (if microsecond > 0, add 1 second)
    if end_dt.microsecond > 0:
        from datetime import timedelta

        end_dt = end_dt.replace(microsecond=0) + timedelta(seconds=1)
    else:
        end_dt = end_dt.replace(microsecond=0)

    return OutputParseResult(
        start=start_dt,
        end=end_dt,
        deviceType=device_type,
        deviceId=device_id,
        vital_request_count=int(sensor_success),
        device_status_request_count=int(sync_success),
    )


if __name__ == "__main__":
    result = parse_output_file("output.txt")
    print(result)
