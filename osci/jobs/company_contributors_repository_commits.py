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
from pyspark.sql import DataFrame

from osci.transformers.company_contributors_repository_commits import get_company_contributors_repository_commits
from osci.datalake.reports.general.company_contributors_repository_commits import (
    CompanyContributorsRepositoryCommitsFactory
)
from osci.datalake.schemas.public import CompaniesContributorsRepositoryCommits
from osci.datalake.schemas.staging import PushEventsCommitsSchema

from .base import PushCommitsRankingJob

from datetime import datetime, timedelta


class CompanyContributorsRepositoryCommitsJob(PushCommitsRankingJob):
    """Job that generates company contributors repository commits"""
    REPORT_FACTORY = CompanyContributorsRepositoryCommitsFactory

    def transform(self, df: DataFrame, date: datetime = None, **kwargs) -> DataFrame:
        schema: CompaniesContributorsRepositoryCommits = self.report_cls.schema
        day = (datetime.now()-timedelta(days=1) if date is None else date).date()
        return get_company_contributors_repository_commits(df=df,
                                                           author_email_field=schema.author_name,
                                                           author_name_field=schema.author_email,
                                                           repo_name_field=schema.repository,
                                                           language_field=schema.language,
                                                           license_field=schema.license,
                                                           company_field=schema.company,
                                                           commits_id_field=PushEventsCommitsSchema().sha,
                                                           datetime_field=PushEventsCommitsSchema().event_created_at,
                                                           day=day,
                                                           result_field=schema.commits)
