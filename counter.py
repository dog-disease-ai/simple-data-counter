#!/usr/bin/env python3
import argparse
import influxdb_client
from datetime import datetime


class SimpleCounter:
    """
    Get count of records in Datasource.
    """

    def get(self, id: any, start: datetime, end: datetime) -> int:
        """
        Get count of records on giben time range in Datasource.
        :return: The count of records.
        """
        pass


class InfluxDBVitalCounter(SimpleCounter):
    """
    Get count of vital records in InfluxDB.
    """

    def __init__(self, config_file: str):
        self.client = influxdb_client.InfluxDBClient.from_config_file(
            config_file, debug=False
        )

    def __delattr__(self, name):
        self.client.close()

    def get(self, id: str, start: datetime, end: datetime) -> int:
        """
        Validate the count of records in InfluxDB.
        :param count: The expected count of records.
        :return: Whether count of records is matched with datasource.
        """
        query = self._build_query(
            bucket="cotons_vet",
            start=start,
            stop=end,
            measurement="vital",
            field="status",
            device_user_id=id,
        )
        print(f"Query: {query}")
        query_result = self.client.query_api().query(query)

        if len(query_result) == 0:
            print("No data found in the given time range.")
            return False
        result = query_result.to_values(["_value"])
        return result.pop().pop()

    def _build_query(
        self,
        bucket: str,
        start: str,
        stop: str,
        measurement: str,
        field: str,
        device_user_id: str,
    ) -> str:
        """
        Build the Flux query to count records.

        :param bucket: The name of the bucket.
        :param start: The start time of the range. should be in 2025-05-13T18:30:59Z format.
        :param stop: The stop time of the range. should be in 2025-05-13T18:30:59Z format.
        :param measurement: The measurement name.
        :param field: The field name.
        :param device user ID: The device user ID.
        :return: The Flux query string.
        """
        return f"""
                from(bucket: "{bucket}")
                |> range(start: {start}, stop: {stop})
                |> filter(fn: (r) => r["_measurement"] == "{measurement}")
                |> filter(fn: (r) => r["_field"] == "{field}")
                |> filter(fn: (r) => r["device_user_id"] == "{device_user_id}")
                |> count()
            """


class InfluxDBDeviceStatusCounter(SimpleCounter):
    """
    Get count of device status records in InfluxDB.
    """

    class Device:
        """
        Device class to hold device information.
        """

        deviceType: str
        deviceId: str

    def __init__(self, config_file: str):
        self.client = influxdb_client.InfluxDBClient.from_config_file(
            config_file, debug=False
        )

    def __delattr__(self, name):
        self.client.close()

    def get(self, id: Device, start: datetime, end: datetime) -> int:
        """
        Validate the count of records in InfluxDB.
        :param count: The expected count of records.
        :return: Whether count of records is matched with datasource.
        """
        query = self._build_query(
            bucket="cotons_vet",
            start=start,
            stop=end,
            measurement="device_status",
            field="battery",
            device_type=id.deviceType,
            device_id=id.deviceId,
        )
        print(f"Query: {query}")
        query_result = self.client.query_api().query(query)

        if len(query_result) == 0:
            print("No data found in the given time range.")
            return 0
        result = query_result.to_values(["_value"])
        return result.pop().pop()

    def _build_query(
        self,
        bucket: str,
        start: str,
        stop: str,
        measurement: str,
        field: str,
        device_type: str,
        device_id: str,
    ) -> str:
        """
        Build the Flux query to count records.

        :param bucket: The name of the bucket.
        :param start: The start time of the range. should be in 2025-05-13T18:30:59Z format.
        :param stop: The stop time of the range. should be in 2025-05-13T18:30:59Z format.
        :param measurement: The measurement name.
        :param field: The field name.
        :param device_type: The device type.
        :param device_id: The device ID.
        :return: The Flux query string.
        """
        return f"""
                from(bucket: "{bucket}")
                |> range(start: {start}, stop: {stop})
                |> filter(fn: (r) => r["_measurement"] == "{measurement}")
                |> filter(fn: (r) => r["_field"] == "{field}")
                |> filter(fn: (r) => r["device_type"] == "{device_type}")
                |> filter(fn: (r) => r["device_id"] == "{device_id}")
                |> count()
            """


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count records in InfluxDB.")
    parser.add_argument("--config", required=True, help="Path to InfluxDB config file")
    parser.add_argument(
        "--type",
        required=True,
        choices=["vital", "device_status"],
        help="Type of data to query: 'vital' or 'device_status'",
    )
    parser.add_argument(
        "--start", required=True, help="Start time (e.g. 2025-05-13T00:30:00Z)"
    )
    parser.add_argument(
        "--end", required=True, help="End time (e.g. 2025-05-13T18:30:59Z)"
    )
    parser.add_argument("--id", help="Device user ID (for vital)")
    parser.add_argument("--device-type", help="Device type (for device_status)")
    parser.add_argument("--device-id", help="Device ID (for device_status)")

    args = parser.parse_args()

    if args.type == "vital":
        if not args.id:
            parser.error("--id is required when --type is 'vital'")
        influxdb_counter = InfluxDBVitalCounter(args.config)
        result = influxdb_counter.get(args.id, start=args.start, end=args.end)
    elif args.type == "device_status":
        if not args.device_type or not args.device_id:
            parser.error(
                "--device-type and --device-id are required when --type is 'device_status'"
            )
        device = InfluxDBDeviceStatusCounter.Device()
        device.deviceType = args.device_type
        device.deviceId = args.device_id
        influxdb_counter = InfluxDBDeviceStatusCounter(args.config)
        result = influxdb_counter.get(device, start=args.start, end=args.end)
    else:
        parser.error("Invalid type specified.")

    print(f"{result}")
