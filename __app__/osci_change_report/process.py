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
from __app__.datalake import DataLake
from datetime import datetime, timedelta
from __app__.osci_change_report.change_report import get_osci_ranking_change_report


def __get_previous_date(date: datetime):
    if date.month == 1:
        return datetime(year=date.year, month=date.month, day=1)
    return datetime(year=date.year, month=date.month, day=1) - timedelta(days=1)


def get_change_report(date: datetime):
    report_name = 'OSCI_ranking_YTD'
    rank_field = 'Position'
    change_suffix = 'Change'
    output_report_name = 'OSCI_change_ranking'
    previous_date = __get_previous_date(date=date)
    report_schema = DataLake().public.schemas.company_contributors_ranking
    new_report = DataLake().public.get_report(report_name=report_name, date=date).reset_index().\
        rename(columns={'index': rank_field})
    old_report = DataLake().public.get_report(report_name=report_name, date=previous_date).reset_index().\
        rename(columns={'index': rank_field})
    change_report = get_osci_ranking_change_report(old_report=old_report,
                                                   new_report=new_report,
                                                   company_field=report_schema.company,
                                                   active_contributors_field=report_schema.active,
                                                   total_community_field=report_schema.total,
                                                   rank_field=rank_field,
                                                   change_suffix=change_suffix)
    DataLake().public.save_report(report_df=change_report, report_name=output_report_name, date=date)
    DataLake().public.save_solutions_hub_osci_change_report_view(change_report=change_report,
                                                                 report_dir_name='SolutionsHub_' + output_report_name,
                                                                 old_date=previous_date,
                                                                 new_date=date)
