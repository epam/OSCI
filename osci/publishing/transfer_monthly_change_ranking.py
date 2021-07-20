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
from osci.datalake.reports.general import (OSCIChangeRanking,
                                              OSCIRankingYTD,
                                              OSCILanguagesYTD,
                                              OSCILicensesYTD,
                                              OSCIContributorsRankingYTD)
from osci.datalake.schemas.web import WebOSCIChangeRankingData, WebOSCIChangeRanking
from osci.datalake import DataLake
from osci.helper.mappers import (generate_company_to_active_contributors_map,
                                    generate_company_to_contributors_map,
                                    generate_company_to_languages_map,
                                    generate_company_to_licenses_map)
from osci.utils import get_compared_date

from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Iterable

import logging

log = logging.getLogger(__name__)


def generate_web_osci_change_ranking(date: datetime) -> dict:
    log.info(f'Load OSCI change ranking {date:%Y-%m-%d}')
    ranking_df = OSCIChangeRanking(date=date).read()
    ranking_df[OSCIChangeRanking.schema.position] = range(1, len(ranking_df)+1)
    ranking_df = ranking_df.rename(columns=WebOSCIChangeRankingData.mapping).fillna(0)
    last_year = date - relativedelta(years=1)
    before_last_year = date - relativedelta(years=2)
    log.info(f'Load previous OSCI change ranking {last_year:%Y-%m-%d}')
    last_year_contributors = generate_company_to_active_contributors_map(OSCIRankingYTD(date=last_year).read())
    log.info(f'Load previous OSCI change ranking {before_last_year:%Y-%m-%d}')
    before_last_year_contributors = generate_company_to_active_contributors_map(
        OSCIRankingYTD(date=before_last_year).read()
    )
    log.info(f'Load OSCI Contributors ranking {date:%Y-%m-%d}')
    contributors_map = generate_company_to_contributors_map(OSCIContributorsRankingYTD(date=date).read().dropna())
    log.info(f'Load OSCI Languages ranking {date:%Y-%m-%d}')
    languages_map = generate_company_to_languages_map(OSCILanguagesYTD(date=date).read().dropna())
    log.info(f'Load OSCI Licenses ranking {date:%Y-%m-%d}')
    licenses_map = generate_company_to_licenses_map(OSCILicensesYTD(date=date).read().dropna())

    def _data_field_value_generator(rows: Iterable[dict]):
        for row in rows:
            yield {
                **row,
                WebOSCIChangeRankingData.Columns.year_of_year: [
                    dict(date=before_last_year,
                         active=before_last_year_contributors.get(row[WebOSCIChangeRankingData.Columns.company], [])),
                    dict(date=last_year,
                         active=last_year_contributors.get(row[WebOSCIChangeRankingData.Columns.company], []))
                ],
                WebOSCIChangeRankingData.Columns.contributors:
                    contributors_map.get(row[WebOSCIChangeRankingData.Columns.company]),
                WebOSCIChangeRankingData.Columns.languages:
                    languages_map.get(row[WebOSCIChangeRankingData.Columns.company]),
                WebOSCIChangeRankingData.Columns.licenses:
                    licenses_map.get(row[WebOSCIChangeRankingData.Columns.company]),
            }

    return {
        WebOSCIChangeRanking.Columns.date: date,
        WebOSCIChangeRanking.Columns.compared_date: get_compared_date(date),
        WebOSCIChangeRanking.Columns.data: list(
            _data_field_value_generator(ranking_df.to_dict(orient='records'))
        )
    }


def transfer_monthly_change_ranking(date: datetime) -> dict:
    web_ranking = generate_web_osci_change_ranking(date)
    DataLake().web.save_monthly_osci_ranking(ranking=web_ranking, date=date)
    return web_ranking