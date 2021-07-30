"""Copyright since 2021, EPAM Systems

   This file is part of OSCI.

   OSCI is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   OSCI is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with OSCI.  If not, see <http://www.gnu.org/licenses/>."""
from datetime import datetime
import pandas as pd
from osci.datalake.reports.general import (
    OSCIChangeRanking,
    OSCIChangeRankingDTD,
    OSCIGrowthSpeed,
    OSCIRankingMTD,
    OSCICommitsRankingMTD,
    OSCICommitsRankingYTD,
)
from osci.datalake.schemas.public import OSCIGeneralRankingSchema
from typing import Type, Iterable, FrozenSet
from osci.datalake.reports.general.base import Report
import logging

log = logging.getLogger(__name__)


class ReportTransformation:

    def __init__(self, report_cls: Type[Report], date: datetime):
        self.date = date
        self.date_period_type = report_cls.date_period
        self.report = report_cls(date=date)

    def extract(self):
        return self.report.read()

    def _rename_columns(self, df: pd.DataFrame, general_fields: FrozenSet[str]):
        suffix = self.date_period_type
        rename_dict = {col: f"{col}_{suffix}" for col in df.columns
                       if f"{col}_{suffix}" in general_fields}
        return df.rename(columns=rename_dict)

    def transform(self, df: pd.DataFrame, general_fields: FrozenSet[str]):
        if self.date_period_type:
            df = self._rename_columns(df, general_fields=general_fields)
        return df

    def load(self, general_report_fields: FrozenSet[str]):
        df = self.extract()
        return self.transform(df, general_report_fields)


class OSCIChangeRankingYTDTransformation(ReportTransformation):
    def _rename_columns(self, df: pd.DataFrame, *args, **kwargs):
        df = df.reset_index().rename(columns={'index': OSCIChangeRanking(date=self.date).schema.position})
        return super()._rename_columns(df, *args, **kwargs)


def _get_reports(date: datetime) -> Iterable[ReportTransformation]:
    """Retrieve all reports for joining into one final general report"""
    return (
        ReportTransformation(report_cls=OSCIChangeRankingDTD, date=date),
        OSCIChangeRankingYTDTransformation(report_cls=OSCIChangeRanking, date=date),
        ReportTransformation(report_cls=OSCIRankingMTD, date=date),
        ReportTransformation(report_cls=OSCICommitsRankingMTD, date=date),
        ReportTransformation(report_cls=OSCICommitsRankingYTD, date=date),
        ReportTransformation(report_cls=OSCIGrowthSpeed, date=date),
    )


def _join_reports(reports: Iterable[ReportTransformation]) -> pd.DataFrame:
    """Join reports to one general report"""
    df = pd.DataFrame(columns=[OSCIGeneralRankingSchema.company])
    for report in reports:
        df = pd.merge(left=df, right=report.load(general_report_fields=OSCIGeneralRankingSchema.required),
                      on=[OSCIGeneralRankingSchema.company],
                      how='outer',
                      suffixes=('', '_drop'))
    return df[OSCIGeneralRankingSchema.required]


def generate_general_report(date: datetime) -> pd.DataFrame:
    """Concat reports to one general report"""
    reports = _get_reports(date=date)
    return _join_reports(reports=reports)
