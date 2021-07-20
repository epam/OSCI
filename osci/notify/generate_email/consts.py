from typing import Dict, Type

from osci.datalake.reports.company import *
from osci.datalake.reports.general import *

COMPANY_REPORTS_URLS: Dict[str, Type[CompanyReport]] = {'new_repositories': NewRepos,
                                                        'new_contributors': NewContributors,
                                                        'contributors_ranking_ytd': ContributorsRankingYTD,
                                                        'contributors_ranking_mtd': ContributorsRankingMTD,
                                                        'contributors_ranking_mbm': ContributorsRankingMBM,
                                                        'repos_ranking_mtd': ReposRankingMTD,
                                                        'contributors_repos_ranking_ytd': ContributorsReposYTD,
                                                        'contributors_repos_ranking_mtd': ContributorsReposMTD,
                                                        'projects_activity_mtd': ProjectsActivityMTD,
                                                        'month_by_month_commits_ytd': MBMCommitsYTD}

OSCI_REPORTS_URLS: Dict[str, Type[Report]] = {'osci_ranking_ytd': OSCIRankingYTD,
                                              'osci_ranking_mtd': OSCIRankingMTD,
                                              'osci_change_ranking': OSCIChangeRanking,
                                              'osci_commits_ranking_ytd': OSCICommitsRankingYTD,
                                              'osci_commits_ranking_mtd': OSCICommitsRankingMTD}
