"""Copyright since 2019, EPAM Systems

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

from datetime import datetime, timedelta

from __app__.osci_change_report.change_report import get_osci_ranking_change_report
from __app__.datalake.reports.general.change_ranking import OSCIChangeRanking
from __app__.datalake.reports.general.osci_ranking import OSCIRankingYTD
from __app__.datalake.reports.excel import OSCIChangeRankingExcel


def get_previous_date(date: datetime):
    if date.month == 1:
        return datetime(year=date.year, month=date.month, day=1)
    return datetime(year=date.year, month=date.month, day=1) - timedelta(days=1)


def get_change_report(date: datetime):
    previous_date = get_previous_date(date=date)

    ranking = OSCIRankingYTD(date=date)
    ranking_df = ranking.read().reset_index().rename(columns={'index': ranking.schema.position})

    old_ranking = OSCIRankingYTD(date=previous_date)
    old_ranking_df = old_ranking.read().reset_index().rename(columns={'index': old_ranking.schema.position})

    report = OSCIChangeRanking(date=date)
    change_report = get_osci_ranking_change_report(old_report=old_ranking_df,
                                                   new_report=ranking_df,

                                                   company_field=ranking.schema.company,

                                                   active_contributors_field=ranking.schema.active,
                                                   active_contributors_change_field=report.schema.active_change,

                                                   total_community_field=ranking.schema.total,
                                                   total_community_change_field=report.schema.total_change,

                                                   rank_field=ranking.schema.position,
                                                   rank_change_field=report.schema.position_change)

    report.save(df=change_report)

    excel_report = OSCIChangeRankingExcel(from_date=previous_date, to_date=date)
    excel_report.save(df=change_report)
