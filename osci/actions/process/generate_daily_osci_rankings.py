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
from osci.datalake import DatePeriodType

from osci.jobs.osci_ranking import OSCIRankingJob
from osci.jobs.osci_licenses import OSCILicensesJob
from osci.jobs.osci_commits_ranking import OSCICommitsRankingJob
from osci.jobs.company_contributors_repository_commits import CompanyContributorsRepositoryCommitsJob
from osci.jobs.osci_languages import OSCILanguagesJob
from osci.jobs.osci_contributors_ranking import OSCIContributorsRankingJob

from datetime import datetime


class DailyOSCIRankingsAction(Action):
    """Daily Main ETL"""
    params = (
        ActionParam(name='to_day', type=datetime, required=True, short_name='td'),
    )

    @classmethod
    def help_text(cls) -> str:
        return "Transform, filter and save data for the subsequent creating report"

    @classmethod
    def name(cls):
        return 'daily-osci-rankings'

    def _execute(self, to_day: datetime):
        for date_period in [DatePeriodType.YTD, DatePeriodType.MTD]:
            osci_ranking_job = OSCIRankingJob(date_period_type=date_period)
            osci_commits_ranking_job = OSCICommitsRankingJob(date_period_type=date_period)

            commits = osci_ranking_job.extract(to_date=to_day).cache()

            osci_ranking_job.load(df=osci_ranking_job.transform(commits), date=to_day)
            osci_commits_ranking_job.load(df=osci_commits_ranking_job.transform(commits), date=to_day)

            if date_period == DatePeriodType.YTD:
                company_contributors_repos = CompanyContributorsRepositoryCommitsJob(date_period_type=date_period)
                company_contributors_repos.load(company_contributors_repos.transform(commits, date=to_day), date=to_day)

                osci_contributors_ranking_job = OSCIContributorsRankingJob(date_period_type=date_period)
                osci_contributors_ranking_job.load(osci_contributors_ranking_job.transform(commits), date=to_day)
                osci_language_job = OSCILanguagesJob(date_period_type=date_period)
                osci_language_job.load(osci_language_job.transform(commits), date=to_day)

                osci_licenses_ytd = OSCILicensesJob(date_period_type=date_period)
                osci_licenses_ytd.load(osci_licenses_ytd.transform(df=commits), date=to_day)
