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
from osci.actions import Action, ActionParam
from osci.config import Config
from osci.datalake.reports.company.contributors import ContributorsRankingMTD
from osci.datalake.reports.company.month_by_month_contributors import ContributorsRankingMBM
from osci.datalake.schemas.public import ContributorsRankingReportSchema
from osci.notify.get_contributors_ranking_mbm_report import get_contributors_ranking_mbm_change_report

from datetime import datetime


class ContributorsRankingMbmReportAction(Action):
    """Generate report for sending via email"""

    params = Action.params + (
        ActionParam(name='company', short_name='c', type=str, required=True),
    )

    @classmethod
    def name(cls):
        return 'get-contributors-ranking-mbm-report'

    @classmethod
    def help_text(cls) -> str:
        return "Prepared Contributors month by month report"

    def _execute(self, date: datetime, company: str):
        contributors_report = ContributorsRankingMTD(date=date, company=company)
        contributors_mbm_report = ContributorsRankingMBM(date=date, company=company)

        df = get_contributors_ranking_mbm_change_report(
            reports=contributors_report.read_all(),
            contributor_field=ContributorsRankingReportSchema.author,
            commits_amount_field=ContributorsRankingReportSchema.commits
        )
        contributors_mbm_report.save(df=df)
        return dict(out_df=str(df))
