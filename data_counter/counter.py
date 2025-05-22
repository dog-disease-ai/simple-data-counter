import influxdb_client
from datetime import datetime, timezone


class SimpleCounter:
    """
    Get count of records in Datasource.
    """

    def get(self, id: any, start: datetime, end: datetime) -> int:
        """
        Get count of records on given time range in Datasource.
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

    def __delattr__(self):
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

        def __init__(self, deviceType: str, deviceId: str):
            self.deviceType = deviceType
            self.deviceId = deviceId

    def __init__(self, config_file: str):
        self.client = influxdb_client.InfluxDBClient.from_config_file(
            config_file, debug=False
        )

    def __delattr__(self):
        self.client.close()

    def get(self, id: tuple, start: datetime, end: datetime) -> int:
        """
        Validate the count of records in InfluxDB.
        :param count: The expected count of records.
        :return: Whether count of records is matched with datasource.
        """
        device = self.Device(id[0], id[1])
        query = self._build_query(
            bucket="cotons_vet",
            start=start,
            stop=end,
            measurement="device_status",
            field="battery",
            device_type=device.deviceType,
            device_id=device.deviceId,
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
    result = InfluxDBVitalCounter("influxdb_config.ini").get(
        "1f036d44-fd73-6fe0-8bb9-67a9de0b011a",
        datetime(2025, 5, 13, 9, 30, 59, tzinfo=timezone.utc).isoformat(),
        datetime(2025, 5, 13, 9, 31, 59, tzinfo=timezone.utc).isoformat(),
    )
    print(f"Count: {result}")

    print(f"{result}")
