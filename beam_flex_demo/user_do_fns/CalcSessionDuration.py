import apache_beam as beam
from datetime import datetime

class CalcSessionDuration(beam.DoFn):
    def process(self, element):
        """
        :param element:
        :return: List[str] --> ip, SessionDuration
        """
        dt_format = "%Y-%m-%dT%H:%M:%S"
        session_duration_secs = (datetime.strptime(element[2],dt_format) - datetime.strptime(element[1],dt_format)).total_seconds()

        yield[element[0], session_duration_secs]