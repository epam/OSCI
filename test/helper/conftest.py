import pytest
import pandas as pd

from osci.datalake.schemas.public import OSCIContributorsRankingSchema, OSCILanguagesReportSchema, \
    OSCILicensesReportSchema


@pytest.fixture()
def company_contributors_df():
    return pd.DataFrame([
        {OSCIContributorsRankingSchema.company: 'Google', OSCIContributorsRankingSchema.author: 'Lorem',
         OSCIContributorsRankingSchema.author_email: 'lorem@google.com', OSCIContributorsRankingSchema.commits: 50},
        {OSCIContributorsRankingSchema.company: 'Google', OSCIContributorsRankingSchema.author: 'Ipsum',
         OSCIContributorsRankingSchema.author_email: 'ipsum@google.com', OSCIContributorsRankingSchema.commits: 30},
        {OSCIContributorsRankingSchema.company: 'Google', OSCIContributorsRankingSchema.author: 'Dolor',
         OSCIContributorsRankingSchema.author_email: 'dolor@google.com', OSCIContributorsRankingSchema.commits: 20},

        {OSCIContributorsRankingSchema.company: 'Microsoft', OSCIContributorsRankingSchema.author: 'Sit',
         OSCIContributorsRankingSchema.author_email: 'sit@microsoft.com', OSCIContributorsRankingSchema.commits: 40},
        {OSCIContributorsRankingSchema.company: 'Microsoft', OSCIContributorsRankingSchema.author: 'Amet',
         OSCIContributorsRankingSchema.author_email: 'amet@microsoft.com', OSCIContributorsRankingSchema.commits: 20},
        {OSCIContributorsRankingSchema.company: 'Microsoft', OSCIContributorsRankingSchema.author: 'Consectetur',
         OSCIContributorsRankingSchema.author_email: 'consectetur@microsoft.com',
         OSCIContributorsRankingSchema.commits: 10},

    ])


@pytest.fixture()
def expected_generate_company_to_contributors_map():
    return {
        'Google': [
            {OSCIContributorsRankingSchema.author: 'Lorem', OSCIContributorsRankingSchema.commits: 50},
            {OSCIContributorsRankingSchema.author: 'Ipsum', OSCIContributorsRankingSchema.commits: 30},
            {OSCIContributorsRankingSchema.author: 'Dolor', OSCIContributorsRankingSchema.commits: 20},
        ],
        'Microsoft': [
            {OSCIContributorsRankingSchema.author: 'Sit', OSCIContributorsRankingSchema.commits: 40},
            {OSCIContributorsRankingSchema.author: 'Amet', OSCIContributorsRankingSchema.commits: 20},
            {OSCIContributorsRankingSchema.author: 'Consectetur', OSCIContributorsRankingSchema.commits: 10},
        ]
    }


@pytest.fixture()
def company_licenses_df():
    return pd.DataFrame(
        [{OSCILicensesReportSchema.company: 'Google', OSCILicensesReportSchema.license: 'apache-2.0',
          OSCILicensesReportSchema.commits: 50},
         {OSCILicensesReportSchema.company: 'Google', OSCILicensesReportSchema.license: 'mit',
          OSCILicensesReportSchema.commits: 30},

         {OSCILicensesReportSchema.company: 'Microsoft', OSCILicensesReportSchema.license: 'gpl-3.0',
          OSCILicensesReportSchema.commits: 40},
         {OSCILicensesReportSchema.company: 'Microsoft', OSCILicensesReportSchema.license: 'lgpl-2.1',
          OSCILicensesReportSchema.commits: 20},
         ]
    )


@pytest.fixture()
def expected_generate_company_to_licenses_map():
    return {
        'Google': [
            {'name': 'apache-2.0', 'amount': 50},
            {'name': 'mit', 'amount': 30},
        ],
        'Microsoft': [
            {'name': 'gpl-3.0', 'amount': 40},
            {'name': 'lgpl-2.1', 'amount': 20}
        ]
    }


@pytest.fixture()
def company_languages_df():
    return pd.DataFrame([
        {OSCILanguagesReportSchema.company: 'Google', OSCILanguagesReportSchema.language: 'python',
         OSCILanguagesReportSchema.commits: 50},
        {OSCILanguagesReportSchema.company: 'Google', OSCILanguagesReportSchema.language: 'go',
         OSCILanguagesReportSchema.commits: 30},

        {OSCILanguagesReportSchema.company: 'Microsoft', OSCILanguagesReportSchema.language: 'typescript',
         OSCILanguagesReportSchema.commits: 40},
        {OSCILanguagesReportSchema.company: 'Microsoft', OSCILanguagesReportSchema.language: 'powershell',
         OSCILanguagesReportSchema.commits: 20},

    ])


@pytest.fixture()
def expected_generate_company_to_languages_map():
    return {
        'Google': [
            {'name': 'python', 'amount': 50},
            {'name': 'go', 'amount': 30},
        ],
        'Microsoft': [
            {'name': 'typescript', 'amount': 40},
            {'name': 'powershell', 'amount': 20}
        ]
    }
