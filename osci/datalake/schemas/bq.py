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
from google.cloud import bigquery
from .public import PublicSchemas


class BaseBigQueryOSCIRankingReport:
    table_id = ''

    class Columns:
        total = 'Total_community'
        active = 'Active_contributors'
        company = 'Company'
        date = 'Date'
        position = 'Position'

    schema = [
        bigquery.SchemaField(Columns.position, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.company, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.active, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.total, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.date, bigquery.enums.SqlTypeNames.DATE),
    ]

    mapping = {
        PublicSchemas.company_contributors_ranking.company: Columns.company,
        PublicSchemas.company_contributors_ranking.active: Columns.active,
        PublicSchemas.company_contributors_ranking.total: Columns.total,
    }


class BigQueryOSCIRankingReport(BaseBigQueryOSCIRankingReport):
    table_id = 'OSCI.OSCI_Ranking'


class BigQueryOSCIRankingReportMTD(BaseBigQueryOSCIRankingReport):
    table_id = 'OSCI.OSCI_Ranking_MTD'


class BaseBigQueryChangeOSCIRankingReport:
    """OSCI Contributors and Community change DTD"""
    table_id = ''
    class Columns:
        position = 'Position'
        position_change = 'Position_change'
        company = 'Company'
        active = 'Active_contributors'
        active_change = 'Active_contributors_change'
        total = 'Total_community'
        total_change = 'Total_community_change'
        date = 'Date'

    schema = [
        bigquery.SchemaField(Columns.position, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.position_change, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.company, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.active, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.active_change, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.total, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.total_change, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.date, bigquery.enums.SqlTypeNames.DATE),
    ]

    mapping = {
        PublicSchemas.osci_ranking_schema.company: Columns.company,
        PublicSchemas.osci_ranking_schema.active: Columns.active,
        PublicSchemas.osci_ranking_schema.total: Columns.total,
        PublicSchemas.osci_ranking_schema.position: Columns.position,
        PublicSchemas.osci_ranking_schema.position_change: Columns.position_change,
        PublicSchemas.osci_ranking_schema.active_change: Columns.active_change,
        PublicSchemas.osci_ranking_schema.total_change: Columns.total_change,
    }


class BigQueryOSCIDailyChangeRankingReport(BaseBigQueryChangeOSCIRankingReport):
    table_id = 'OSCI.OSCI_Change_ranking_DTD'


class BaseBigQueryOSCICommitsRankingReport:
    table_id = ''

    class Columns:
        commits = 'Commits'
        company = 'Company'
        date = 'Date'
        position = 'Position'

    schema = [
        bigquery.SchemaField(Columns.position, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.company, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.commits, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.date, bigquery.enums.SqlTypeNames.DATE),
    ]

    mapping = {
        PublicSchemas.company_commits_ranking.company: Columns.company,
        PublicSchemas.company_commits_ranking.commits: Columns.commits
    }


class BigQueryOSCICommitsRankingReport(BaseBigQueryOSCICommitsRankingReport):
    table_id = 'OSCI.OSCI_Commits_Ranking'


class BigQueryOSCICommitsRankingReportMTD(BaseBigQueryOSCICommitsRankingReport):
    table_id = 'OSCI.OSCI_Commits_Ranking_MTD'


class BigQueryPushEventsCommitsColumns:
    table_id = 'OSCI.PushEventsCommits'

    class Columns:
        event_id = 'event_id'
        event_created_at = 'event_created_at'
        repo_name = 'repo_name'
        org_name = 'org_name'
        actor_login = 'actor_login'
        sha = 'sha'
        author_name = 'author_name'
        author_email = 'author_email'
        company = 'company'

    schema = [
        bigquery.SchemaField(Columns.event_id, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.event_created_at, bigquery.enums.SqlTypeNames.TIMESTAMP),
        bigquery.SchemaField(Columns.repo_name, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.org_name, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.actor_login, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.sha, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.author_name, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.author_email, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.company, bigquery.enums.SqlTypeNames.STRING),
    ]


class BigQueryLicensedRepository:
    """BigQuery OSCI Licensed Repositories"""
    table_id = 'OSCI.LicensedRepositories'

    class Columns:
        name = 'name'
        language = 'language'
        license = 'license'
        downloaded_at = 'downloaded_at'

    schema = [
        bigquery.SchemaField(Columns.name, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.language, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.license, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.downloaded_at, bigquery.enums.SqlTypeNames.DATE),
    ]


class BigQueryCompaniesContributorsRepositoriesCommitsColumns:
    table_id = 'OSCI.CompaniesContributorsRepositoriesCommits'

    class Columns:
        author_name = 'Author'
        author_email = 'Email'
        company = 'Company'
        repository = 'Repository'
        language = 'Language'
        license = 'License'
        commits = 'Commits'
        date = 'Date'

    schema = [
        bigquery.SchemaField(Columns.author_name, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.author_email, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.company, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.repository, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.language, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.license, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.commits, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.date, bigquery.enums.SqlTypeNames.DATE),
    ]

    mapping = {
        PublicSchemas.company_contributors_repository_commits.author_name: Columns.author_name,
        PublicSchemas.company_contributors_repository_commits.author_email: Columns.author_email,
        PublicSchemas.company_contributors_repository_commits.company: Columns.company,
        PublicSchemas.company_contributors_repository_commits.repository: Columns.repository,
        PublicSchemas.company_contributors_repository_commits.language: Columns.language,
        PublicSchemas.company_contributors_repository_commits.license: Columns.license,
        PublicSchemas.company_contributors_repository_commits.commits: Columns.commits,
        PublicSchemas.company_contributors_repository_commits.date: Columns.date,
    }


class BigQueryCompaniesContributorsRepositoriesCommitsColumns:
    table_id = 'OSCI.CompaniesContributorsRepositoriesCommits'

    class Columns:
        author_name = 'Author'
        author_email = 'Email'
        company = 'Company'
        repository = 'Repository'
        language = 'Language'
        license = 'License'
        commits = 'Commits'
        date = 'Date'

    schema = [
        bigquery.SchemaField(Columns.author_name, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.author_email, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.company, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.repository, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.language, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.license, bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField(Columns.commits, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.date, bigquery.enums.SqlTypeNames.DATE),
    ]

    mapping = {
        PublicSchemas.company_contributors_repository_commits.author_name: Columns.author_name,
        PublicSchemas.company_contributors_repository_commits.author_email: Columns.author_email,
        PublicSchemas.company_contributors_repository_commits.company: Columns.company,
        PublicSchemas.company_contributors_repository_commits.repository: Columns.repository,
        PublicSchemas.company_contributors_repository_commits.language: Columns.language,
        PublicSchemas.company_contributors_repository_commits.license: Columns.license,
        PublicSchemas.company_contributors_repository_commits.commits: Columns.commits,
        PublicSchemas.company_contributors_repository_commits.date: Columns.date,
    }


class BigQueryOSCIGeneralRankingReport:
    table_id = 'OSCI.OSCI_General_Ranking'

    class Columns:
        position = 'Position'
        position_change_ytd = 'Position_change_YTD'
        position_change_dtd = 'Position_change_DTD'
        position_growth_speed = 'Position_growth_speed'
        commits_ytd = 'Commits_YTD'
        commits_mtd = 'Commits_MTD'

        company = 'Company'
        active_ytd = 'Active_contributors_YTD'
        active_mtd = 'Active_contributors_MTD'
        active_dtd = 'Active_contributors_DTD'

        active_change_ytd = 'Active_contributors_change_YTD'
        active_change_dtd = 'Active_contributors_change_DTD'
        active_contrib_growth_speed = 'Active_contributors_growth_speed'

        total_ytd = 'Total_community_YTD'
        total_mtd = 'Total_community_MTD'
        total_dtd = 'Total_community_DTD'

        total_change_ytd = 'Total_community_change_YTD'
        total_change_dtd = 'Total_community_change_DTD'
        total_com_growth_speed = 'Total_community_growth_speed'
        date = 'Date'

    schema = [
        bigquery.SchemaField(Columns.position, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.position_change_ytd, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.position_change_dtd, bigquery.enums.SqlTypeNames.INTEGER),

        bigquery.SchemaField(Columns.position_growth_speed, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.commits_ytd, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.commits_mtd, bigquery.enums.SqlTypeNames.INTEGER),

        bigquery.SchemaField(Columns.company, bigquery.enums.SqlTypeNames.STRING),

        bigquery.SchemaField(Columns.active_ytd, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.active_mtd, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.active_dtd, bigquery.enums.SqlTypeNames.INTEGER),

        bigquery.SchemaField(Columns.active_change_ytd, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.active_change_dtd, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.active_contrib_growth_speed, bigquery.enums.SqlTypeNames.INTEGER),

        bigquery.SchemaField(Columns.total_ytd, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.total_mtd, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.total_dtd, bigquery.enums.SqlTypeNames.INTEGER),

        bigquery.SchemaField(Columns.total_change_ytd, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.total_change_dtd, bigquery.enums.SqlTypeNames.INTEGER),

        bigquery.SchemaField(Columns.total_com_growth_speed, bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField(Columns.date, bigquery.enums.SqlTypeNames.DATE),
    ]

    mapping = {
        PublicSchemas.osci_general_report.position: Columns.position,
        PublicSchemas.osci_general_report.position_change_ytd: Columns.position_change_ytd,
        PublicSchemas.osci_general_report.position_change_dtd: Columns.position_change_dtd,
        PublicSchemas.osci_general_report.position_growth_speed: Columns.position_growth_speed,
        PublicSchemas.osci_general_report.commits_ytd: Columns.commits_ytd,
        PublicSchemas.osci_general_report.commits_mtd: Columns.commits_mtd,
        PublicSchemas.osci_general_report.company: Columns.company,
        PublicSchemas.osci_general_report.active_ytd: Columns.active_ytd,
        PublicSchemas.osci_general_report.active_mtd: Columns.active_mtd,
        PublicSchemas.osci_general_report.active_dtd: Columns.active_dtd,
        PublicSchemas.osci_general_report.active_change_ytd: Columns.active_change_ytd,
        PublicSchemas.osci_general_report.active_change_dtd: Columns.active_change_dtd,
        PublicSchemas.osci_general_report.active_growth_speed: Columns.active_contrib_growth_speed,
        PublicSchemas.osci_general_report.total_ytd: Columns.total_ytd,
        PublicSchemas.osci_general_report.total_mtd: Columns.total_mtd,
        PublicSchemas.osci_general_report.total_dtd: Columns.total_dtd,
        PublicSchemas.osci_general_report.total_change_ytd: Columns.total_change_ytd,
        PublicSchemas.osci_general_report.total_change_dtd: Columns.total_change_dtd,
        PublicSchemas.osci_general_report.total_growth_speed: Columns.total_com_growth_speed,
    }
