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
import pandas as pd
from typing import Dict, List, Any, Mapping
from datetime import datetime
from .base import base_map_generator
from osci.datalake.schemas.public import (OSCIContributorsRankingSchema,
                                             OSCILicensesReportSchema,
                                             OSCILanguagesReportSchema,
                                             CompanyContributorsRankingReportSchema as OSCISchema)

Mapper = Mapping[str, List[Dict[str, Any]]]


def generate_company_to_contributors_map(company_contributors_df: pd.DataFrame) -> Mapper:
    return base_map_generator(company_contributors_df, group_by_column=OSCIContributorsRankingSchema.company,
                              nested_columns=[OSCIContributorsRankingSchema.author,
                                              OSCIContributorsRankingSchema.commits])


def generate_company_to_licenses_map(company_licenses_df: pd.DataFrame) -> Mapper:
    return base_map_generator(company_licenses_df, group_by_column=OSCIContributorsRankingSchema.company,
                              nested_columns=[OSCILicensesReportSchema.license,
                                              OSCILicensesReportSchema.commits],
                              rename_columns={OSCILicensesReportSchema.license: 'name',
                                              OSCILicensesReportSchema.commits: 'amount'})


def generate_company_to_languages_map(company_languages_df: pd.DataFrame) -> Mapper:
    return base_map_generator(company_languages_df, group_by_column=OSCIContributorsRankingSchema.company,
                              nested_columns=[OSCILanguagesReportSchema.language,
                                              OSCILanguagesReportSchema.commits],
                              rename_columns={OSCILanguagesReportSchema.language: 'name',
                                              OSCILanguagesReportSchema.commits: 'amount'})


def generate_company_to_active_contributors_map(osci_ranking: pd.DataFrame) -> Mapping[str, int]:
    return {company: active
            for company, active in osci_ranking[[OSCISchema.company, OSCISchema.active]].fillna(0).values}
