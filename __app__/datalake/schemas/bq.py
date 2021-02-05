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
