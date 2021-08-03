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

    required = [company, total, active, position,
                position_change, total_change, active_change]


class OSCIGrowthSpeedSchema:
    company = OSCIChangeRankingSchema.company

    position_change = OSCIChangeRankingSchema.position_change
    active_change = OSCIChangeRankingSchema.active_change
    total_change = OSCIChangeRankingSchema.total_change

    _suffix = 'Growth Speed'

    position_growth = f'{OSCIChangeRankingSchema.position} {_suffix}'
    total_growth = f'{OSCIChangeRankingSchema.total} {_suffix}'
    active_growth = f'{OSCIChangeRankingSchema.active} {_suffix}'

    required = frozenset([company, position_growth, total_growth, active_growth])


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


class OSCIContributorsRankingSchema:
    company = 'Company'
    author = 'Contributor'
    author_email = 'Contributor\'s email'
    commits = 'Commits'


class OSCIGeneralRankingSchema:
    position = OSCIChangeRankingSchema.position

    __ytd = 'YTD'
    __dtd = 'DTD'
    __mtd = 'MTD'

    change_suffix = 'Change'
    position_change = f'{OSCIChangeRankingSchema.position_change}'
    position_change_ytd = f'{position_change}_{__ytd}'
    position_change_dtd = f'{position_change}_{__dtd}'

    position_growth_speed = OSCIGrowthSpeedSchema.position_growth
    commits = 'Commits'
    commits_ytd = f'{commits}_{__ytd}'
    commits_mtd = f'{commits}_{__mtd}'

    total = OSCIChangeRankingSchema.total
    total_ytd = f'{total}_{__ytd}'
    total_mtd = f'{total}_{__mtd}'
    total_dtd = f'{total}_{__dtd}'

    total_change = OSCIChangeRankingSchema.total_change
    total_change_ytd = f'{total_change}_{__ytd}'
    total_change_dtd = f'{total_change}_{__dtd}'
    total_growth_speed = OSCIGrowthSpeedSchema.total_growth

    active = OSCIChangeRankingSchema.active
    active_ytd = f'{active}_{__ytd}'
    active_mtd = f'{active}_{__mtd}'
    active_dtd = f'{active}_{__dtd}'

    active_change = OSCIChangeRankingSchema.active_change
    active_change_ytd = f'{active_change}_{__ytd}'
    active_change_dtd = f'{active_change}_{__dtd}'
    active_growth_speed = OSCIGrowthSpeedSchema.active_growth

    company = OSCIChangeRankingSchema.company
    required = frozenset(
        [position, position_change_ytd, position_change_dtd, position_growth_speed, commits_mtd, commits_ytd,
         total_ytd, total_mtd, total_dtd, total_change_ytd, total_change_dtd, total_growth_speed,
         active_ytd, active_mtd,
         active_dtd, active_change_ytd, active_change_dtd, active_growth_speed, company])


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
    osci_ranking_schema = OSCIChangeRankingSchema
    osci_general_report = OSCIGeneralRankingSchema
