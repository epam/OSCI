import pytest
from datetime import datetime
import pandas as pd
from unittest.mock import patch
from osci.postprocess.osci_general_report.osci_general_report import generate_general_report, ReportTransformation
from osci.datalake.schemas.public import (
    OSCIChangeRankingSchema,
    CompanyContributorsRankingReportSchema,
    CompanyCommitsRankingReportSchema,
    OSCIGrowthSpeedSchema,
    OSCIGeneralRankingSchema,
)
from pandas.testing import assert_frame_equal
from osci.datalake import DatePeriodType
from osci.datalake.reports.general import (
    OSCIChangeRanking,
    OSCIChangeRankingDTD,
    OSCICommitsRankingFactory,
    OSCIRankingFactory,
    OSCIGrowthSpeed,
    OSCIRankingMTD,
    OSCICommitsRankingYTD,
    OSCICommitsRankingMTD,
)


@pytest.fixture()
def date_input():
    return datetime.strptime('2021-01-01', '%Y-%m-%d')


def osci_change_ranking_dtd_df():
    return pd.DataFrame([
        {
            OSCIChangeRankingSchema.company: "Company",
            OSCIChangeRankingSchema.total: 10,
            OSCIChangeRankingSchema.active: 5,
            OSCIChangeRankingSchema.position: 4,
            OSCIChangeRankingSchema.position_change: 2,
            OSCIChangeRankingSchema.total_change: 7,
            OSCIChangeRankingSchema.active_change: 3,
        }])


def osci_change_ranking_ytd_df():
    return pd.DataFrame([
        {
            OSCIChangeRankingSchema.company: "Company",
            OSCIChangeRankingSchema.total: 100,
            OSCIChangeRankingSchema.active: 50,
            OSCIChangeRankingSchema.position: 40,
            OSCIChangeRankingSchema.position_change: 20,
            OSCIChangeRankingSchema.total_change: 70,
            OSCIChangeRankingSchema.active_change: 30,
        }])


def osci_ranking_mtd_df():
    return pd.DataFrame([
        {
            CompanyContributorsRankingReportSchema.company: "Company",
            CompanyContributorsRankingReportSchema.total: 20,
            CompanyContributorsRankingReportSchema.active: 10,
            CompanyContributorsRankingReportSchema.position: 8,
        }])


def osci_commits_ranking_mtd_df():
    return pd.DataFrame([
        {
            CompanyCommitsRankingReportSchema.commits: 500,
            CompanyCommitsRankingReportSchema.company: "Company",
        }])


def osci_commits_ranking_ytd_df():
    return pd.DataFrame([
        {
            CompanyCommitsRankingReportSchema.commits: 1000,
            CompanyCommitsRankingReportSchema.company: "Company",
        }])


def osci_growth_report_df():
    return pd.DataFrame([
        {
            OSCIGrowthSpeedSchema.company: 'Company',
            OSCIGrowthSpeedSchema.position_growth: 0.05,
            OSCIGrowthSpeedSchema.total_growth: 0.01,
            OSCIGrowthSpeedSchema.active_growth: 0.04,
        }])


def fake_extract(self):
    df = None
    if isinstance(self.report, OSCIChangeRankingDTD):
        df = osci_change_ranking_dtd_df()
    elif isinstance(self.report, OSCIChangeRanking):
        df = osci_change_ranking_ytd_df()
    elif isinstance(self.report, OSCIRankingMTD):
        df = osci_ranking_mtd_df()
    elif isinstance(self.report, OSCICommitsRankingYTD):
        df = osci_commits_ranking_ytd_df()
    elif isinstance(self.report, OSCICommitsRankingMTD):
        df = osci_commits_ranking_mtd_df()
    elif isinstance(self.report, OSCIGrowthSpeed):
        df = osci_growth_report_df()
    return df


@pytest.fixture()
def expected_final_report():
    return pd.DataFrame([{
        OSCIGeneralRankingSchema.position: 4,
        OSCIGeneralRankingSchema.position_change_ytd: 20,
        OSCIGeneralRankingSchema.position_change_dtd: 2,
        OSCIGeneralRankingSchema.position_growth_speed: 0.05,
        OSCIGeneralRankingSchema.commits_ytd: 1000,
        OSCIGeneralRankingSchema.commits_mtd: 500,
        OSCIGeneralRankingSchema.total_ytd: 100,
        OSCIGeneralRankingSchema.total_mtd: 20,
        OSCIGeneralRankingSchema.total_dtd: 10,
        OSCIGeneralRankingSchema.total_change_ytd: 70,
        OSCIGeneralRankingSchema.total_change_dtd: 7,
        OSCIGeneralRankingSchema.total_growth_speed: 0.01,
        OSCIGeneralRankingSchema.active_ytd: 50,
        OSCIGeneralRankingSchema.active_mtd: 10,
        OSCIGeneralRankingSchema.active_dtd: 5,
        OSCIGeneralRankingSchema.active_change_ytd: 30,
        OSCIGeneralRankingSchema.active_change_dtd: 3,
        OSCIGeneralRankingSchema.active_growth_speed: 0.04,
        OSCIGeneralRankingSchema.company: "Company",
    }]).sort_index(axis=1)


def test_generating_general_report(mocker, date_input, expected_final_report):
    mocker.patch.object(ReportTransformation, "extract", new=fake_extract)
    df = generate_general_report(date=date_input).sort_index(axis=1)
    assert_frame_equal(df,
                       expected_final_report, check_names=True)
