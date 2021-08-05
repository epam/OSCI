"""Copyright since 2020, EPAM Systems

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
from osci.datalake.reports.general.company_contributors_repository_commits import CompaniesContributorsRepository
from osci.datalake.schemas.bq import BigQueryCompaniesContributorsRepositoriesCommitsColumns
from google.cloud import bigquery
from osci.datalake import DataLake
import datetime
import logging

log = logging.getLogger(__name__)


def load_companies_contrib_repos_to_bq(date: datetime.datetime) -> bigquery.table.Table:
    """Load companies contributors repositories to BigQuery for a given day"""
    df = CompaniesContributorsRepository(date).read().rename(
        columns=BigQueryCompaniesContributorsRepositoriesCommitsColumns.mapping)
    df[BigQueryCompaniesContributorsRepositoriesCommitsColumns.Columns.date] = date.date()
    return DataLake().big_query.load_dataframe(df=df,
                                               table_id=BigQueryCompaniesContributorsRepositoriesCommitsColumns.table_id,
                                               schema=BigQueryCompaniesContributorsRepositoriesCommitsColumns.schema)
