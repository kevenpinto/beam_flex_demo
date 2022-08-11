import argparse
import logging

# Beam Related Imports
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import WriteToText

# Local Imports
from beam_flex_demo.utils.common_functions import split_element
from beam_flex_demo.utils.pipeline_funcs import combine_datasets
from beam_flex_demo.user_do_fns.CalcSessionDuration import CalcSessionDuration
from beam_flex_demo.user_do_fns.GetCountryName import GetCountryName


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output',
        required=True,
        help='The file path for the input text to process.')

    args, beam_args = parser.parse_known_args()
    beam_options = PipelineOptions(beam_args)

    with beam.Pipeline(options=beam_options) as pipeline:
        data = (pipeline
                | "Read Data" >> beam.Create([
                    "per,2022-09-15T16:30:15,2022-09-15T16:32:55",
                    "per,2022-09-15T17:30:15,2022-09-15T17:32:55",
                    "per,2022-09-15T15:30:15,2022-09-15T15:32:55",
                    "mex,2022-09-15T18:34:28,2022-09-15T18:38:32",
                    "mex,2022-09-15T20:39:24,2022-09-15T20:41:34",
                    "mex,2022-09-15T09:55:12,2022-09-15T09:57:11",
                    "arg,2022-09-15T09:56:00,2022-09-15T09:56:37",
                    "per,2022-09-15T09:56:35,2022-09-15T09:58:03",
                    "bra,2022-09-15T14:33:40,2022-09-15T14:35:08",
                    "bra,2022-09-15T14:36:55,2022-09-15T15:38:12",
                    "mex,2022-09-15T15:30:15,2022-09-15T15:32:55",
                    "arg,2022-09-15T14:37:49,2022-09-15T14:38:19",
                    "bra,2022-09-15T14:47:42,2022-09-15T14:56:31",
                    "arg,2022-09-15T15:34:02,2022-09-15T15:38:57",
                    "bra,2022-09-15T16:38:31,2022-09-15T16:39:48"
                ])
                | "Parse Elements" >> beam.Map(split_element)
                )

        session_dataset = data | "CalcSessionDuration" >> beam.ParDo(CalcSessionDuration())
        country_dataset = data | "GetCountryName" >> beam.ParDo(GetCountryName())

        merged_data = (session_dataset
                       | "Merge with Country Data -- Using a Side Input" >> beam.Map(combine_datasets,
                                                                                     dataset2=beam.pvalue.AsDict(
                                                                                         country_dataset))
                       | "Average" >> beam.CombinePerKey(beam.combiners.MeanCombineFn())
                       | "Write to File" >> WriteToText(args.output)
                       )


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.WARNING)
    run()
