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
import pandas as pd
from datetime import datetime
from osci.datalake import CompaniesContributorsRepository
from osci.datalake.schemas.public import NumberOfCompaniesCommitsInRepositories


def get_num_companies_commit_per_repository(date: datetime) -> pd.DataFrame:
    """Get number of companies commits in repositories"""
    report_schema = NumberOfCompaniesCommitsInRepositories
    schema = CompaniesContributorsRepository.schema
    rep_per_comp_df = CompaniesContributorsRepository(date=date).read()
    return rep_per_comp_df[[schema.company, schema.repository, schema.commits]] \
        .groupby([schema.company, schema.repository]) \
        .sum() \
        .reset_index() \
        .rename(columns={schema.repository: report_schema.repository,
                         schema.company: report_schema.company,
                         schema.commits: report_schema.commits})
