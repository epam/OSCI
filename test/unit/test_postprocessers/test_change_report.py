from datetime import datetime

import pandas as pd
import numpy as np

from osci.postprocess.osci_change_report import get_osci_ranking_change_report, \
    get_contributors_ranking_mbm_change_report


def test_get_osci_ranking_change_report():
    company_field = 'Company'
    change_field = 'Change'
    active_contributors_field = 'Active Contributors'
    active_contributors_change_field = f'{active_contributors_field} {change_field}'
    total_community_field = 'Total Community'
    total_community_change_field = f'{total_community_field} {change_field}'
    rank_field = '#'
    rank_change_field = f'Position {change_field}'

    old_report = pd.DataFrame([
        {rank_field: 1, company_field: 'Google', active_contributors_field: 100, total_community_field: 200},
        {rank_field: 2, company_field: 'Microsoft', active_contributors_field: 80, total_community_field: 180},
        {rank_field: 3, company_field: 'EPAM', active_contributors_field: 70, total_community_field: 100},
    ])
    new_report = pd.DataFrame([
        {rank_field: 2, company_field: 'Google', active_contributors_field: 90, total_community_field: 250},
        {rank_field: 1, company_field: 'Microsoft', active_contributors_field: 100, total_community_field: 130},
        {rank_field: 3, company_field: 'Tutanota', active_contributors_field: 73, total_community_field: 80},
    ])

    reference = pd.DataFrame([{rank_field: 1,
                               rank_change_field: -1.0,
                               company_field: 'Microsoft',
                               active_contributors_field: 100.0,
                               active_contributors_change_field: 20.0,
                               total_community_field: 130.0,
                               total_community_change_field: -50.0},
                              {rank_field: 2,
                               rank_change_field: 1.0,
                               company_field: 'Google',
                               active_contributors_field: 90.0,
                               active_contributors_change_field: -10.0,
                               total_community_field: 250.0,
                               total_community_change_field: 50.0},
                              {rank_field: 3,
                               rank_change_field: np.nan,
                               company_field: 'Tutanota',
                               active_contributors_field: 73.0,
                               active_contributors_change_field: np.nan,
                               total_community_field: 80.0,
                               total_community_change_field: np.nan}])

    df = get_osci_ranking_change_report(old_report=old_report,
                                        new_report=new_report,

                                        company_field=company_field,

                                        active_contributors_field=active_contributors_field,
                                        active_contributors_change_field=active_contributors_change_field,

                                        total_community_field=total_community_field,
                                        total_community_change_field=total_community_change_field,

                                        rank_field=rank_field,
                                        rank_change_field=rank_change_field)

    pd.testing.assert_frame_equal(reference.set_index(rank_field), df)


def test_get_contributors_ranking_mbm_change_report():
    contributor_field = 'Contributor'
    commits_amount_field = 'Commits'
    jan, feb, dec = datetime(year=2020, month=1, day=1), \
                    datetime(year=2020, month=2, day=1), \
                    datetime(year=2020, month=12, day=1)
    reports = [
        (jan, pd.DataFrame([{contributor_field: 'User1', commits_amount_field: 3},
                            {contributor_field: 'User2', commits_amount_field: 4}])),
        (feb, pd.DataFrame([{contributor_field: 'User2', commits_amount_field: 1},
                            {contributor_field: 'User3', commits_amount_field: 2}])),
        (dec, pd.DataFrame([{contributor_field: 'User1', commits_amount_field: 3},
                            {contributor_field: 'User3', commits_amount_field: 1},
                            {contributor_field: 'User4', commits_amount_field: 1}])),
    ]

    reference = pd.DataFrame([
        {contributor_field: 'User1', jan.strftime('%b'): 3, feb.strftime('%b'): 0, dec.strftime('%b'): 3, 'Total': 6},
        {contributor_field: 'User2', jan.strftime('%b'): 4, feb.strftime('%b'): 1, dec.strftime('%b'): 0, 'Total': 5},
        {contributor_field: 'User3', jan.strftime('%b'): 0, feb.strftime('%b'): 2, dec.strftime('%b'): 1, 'Total': 3},
        {contributor_field: 'User4', jan.strftime('%b'): 0, feb.strftime('%b'): 0, dec.strftime('%b'): 1, 'Total': 1},
    ])

    df = get_contributors_ranking_mbm_change_report(reports,
                                                    contributor_field=contributor_field,
                                                    commits_amount_field=commits_amount_field)

    pd.testing.assert_frame_equal(reference, df)
