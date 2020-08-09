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


class MonthlyEmployeesAmountReportSchema:
    employees_amount = 'Employees'
    month = 'Month'


class MonthByMonthCommitsReportSchema:
    commits_amount = 'Commits'
    month = 'Month'


class CompanyEmployeesAmountReportSchema:
    employees = 'Employees'
    company = 'Company'


class CompanyContributorsRankingReportSchema:
    total = 'Total community'
    active = 'Active contributors'
    company = 'Company'

    required = [company, active, total]


class CompanyCommitsRankingReportSchema:
    commits = 'Commits'
    company = 'Company'


class ContributorsRankingReportSchema:
    commits = 'Commits'
    author = 'Contributor'
    author_email = 'Contributor\'s email'


class ReposCommitsRankingReportSchema:
    commits = 'Commits'
    repo = 'Repository'


class ContributorsReposCommitsRankingReportSchema:
    commits = 'Commits'
    repo = 'Repository'
    author = 'Contributor'
    author_email = 'Contributor\'s email'


class PublicSchemas:
    employees_amount_monthly = MonthlyEmployeesAmountReportSchema
    company_employees_amount = CompanyEmployeesAmountReportSchema
    company_contributors_ranking = CompanyContributorsRankingReportSchema
    contributors_ranking = ContributorsRankingReportSchema
    company_commits_ranking = CompanyCommitsRankingReportSchema
    month_by_month_commits = MonthByMonthCommitsReportSchema
    repo_commits_ranking = ReposCommitsRankingReportSchema
    contributors_repo_commits_ranking = ContributorsReposCommitsRankingReportSchema
