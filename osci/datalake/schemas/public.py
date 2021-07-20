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
from .staging import PushEventsCommitsSchema, RepositoriesSchema


class MonthlyEmployeesAmountReportSchema:
    employees_amount = 'Employees'
    month = 'Month'


class MonthByMonthCommitsReportSchema:
    commits_amount = 'Commits'
    month = 'Month'


class OSCILanguagesReportSchema:
    company = "Company"
    language = "Language"
    commits = "Commits"


class OSCILicensesReportSchema:
    company = "Company"
    license = "License"
    commits = "Commits"


class CompanyEmployeesAmountReportSchema:
    employees = 'Employees'
    company = 'Company'


class CompanyContributorsRankingReportSchema:
    total = 'Total community'
    active = 'Active contributors'
    company = 'Company'

    position = 'Position'

    required = [company, active, total]


class CompanyCommitsRankingReportSchema:
    commits = 'Commits'
    company = 'Company'

    required = [company, commits]


class ContributorsRankingReportSchema:
    commits = 'Commits'
    author = 'Contributor'
    author_email = 'Contributor\'s email'


class ContributorsRankingMBMReportSchema:
    contributor = 'Contributor'
    total = 'Total'
    jan = 'Jan'
    feb = 'Feb'
    march = 'Mar'
    april = 'Apr'
    may = 'May'
    june = 'Jun'
    july = 'Jul'
    aug = 'Aug'
    sep = 'Sep'
    oct = 'Oct'
    nov = 'Nov'
    dec = 'Dec'
    required = [contributor, jan, feb, march, april, may, june, july, aug, sep, oct, nov, dec, total]


class ReposCommitsRankingReportSchema:
    commits = 'Commits'
    repo = 'Repository'


class ContributorsReposCommitsRankingReportSchema:
    commits = 'Commits'
    repo = 'Repository'
    author = 'Contributor'
    author_email = 'Contributor\'s email'


class NewContributorsSchema:
    author = ContributorsReposCommitsRankingReportSchema.author


class NewReposSchema:
    repo = ContributorsReposCommitsRankingReportSchema.repo


class OSCIChangeRankingSchema:
    company = CompanyContributorsRankingReportSchema.company
    total = CompanyContributorsRankingReportSchema.total
    active = CompanyContributorsRankingReportSchema.active

    change_suffix = 'Change'
    position = CompanyContributorsRankingReportSchema.position

    position_change = f'{position} {change_suffix}'
    total_change = f'{total} {change_suffix}'
    active_change = f'{active} {change_suffix}'


class OSCIChangeRankingExcelSchema(OSCIChangeRankingSchema):
    position = '#'

    total_change = OSCIChangeRankingSchema.change_suffix
    active_change = OSCIChangeRankingSchema.change_suffix


class ProjectsActivitySchema:
    project = 'Project'
    description = 'Description'
    commits = 'Commits'
    total = 'Total_%'


class CompaniesContributorsRepositoryCommits:
    author_name = PushEventsCommitsSchema().author_name
    author_email = PushEventsCommitsSchema().author_email
    company = PushEventsCommitsSchema().company
    repository = PushEventsCommitsSchema().repo_name

    language = PushEventsCommitsSchema().language
    license = PushEventsCommitsSchema().license

    commits = 'commits'
    date = 'date'


class NumberRepositoryPerCompaniesSchema:
    company = 'Company'
    repository = 'Repositories'


class NumberOfCompaniesCommitsInRepositories:
    company = 'Company'
    repository = 'Repositories'
    commits = 'Commits'


class OSCIContributorsRankingSchema:
    company = 'Company'
    author = 'Contributor'
    author_email = 'Contributor\'s email'
    commits = 'Commits'


class PublicSchemas:
    employees_amount_monthly = MonthlyEmployeesAmountReportSchema
    company_employees_amount = CompanyEmployeesAmountReportSchema
    company_contributors_ranking = CompanyContributorsRankingReportSchema
    contributors_ranking = ContributorsRankingReportSchema
    company_commits_ranking = CompanyCommitsRankingReportSchema
    month_by_month_commits = MonthByMonthCommitsReportSchema
    repo_commits_ranking = ReposCommitsRankingReportSchema
    contributors_repo_commits_ranking = ContributorsReposCommitsRankingReportSchema
    new_contributors = NewContributorsSchema
    new_repos = NewReposSchema
    company_contributors_repository_commits = CompaniesContributorsRepositoryCommits
    osci_contributors_ranking = OSCIContributorsRankingSchema
    num_rep_per_company = NumberRepositoryPerCompaniesSchema
