from pandas.testing import assert_frame_equal

from osci.filter.filter_unlicensed import filter_and_adjunct_push_event_commit


def test_filter_and_adjunct_push_event_commit__right_join(raw_push_events_commit_df, staging_repository_df,
                                                          filter_columns, adjunct_columns, required_columns,
                                                          right_index, left_index,
                                                          staging_push_event_commit_df
                                                          ):
    """positive test on success adjunct `license`, `language`"""
    res = filter_and_adjunct_push_event_commit(raw_push_events_commit_df, staging_repository_df, filter_columns,
                                               adjunct_columns, required_columns,
                                               right_index=right_index, left_index=left_index)
    assert_frame_equal(res, staging_push_event_commit_df)


def test_filter_and_adjunct_push_event_commit__right_filter(no_match_license_raw_push_event_commit_df,
                                                            staging_repository_df, filter_columns,
                                                            adjunct_columns, required_columns,
                                                            right_index, left_index
                                                            ):
    """negative test on filter no license match raw push event"""
    res = filter_and_adjunct_push_event_commit(no_match_license_raw_push_event_commit_df, staging_repository_df,
                                               filter_columns, adjunct_columns, required_columns,
                                               right_index=right_index,
                                               left_index=left_index)
    assert res.empty


def test_filter_and_adjunct_push_event_commit__right_join_filter(unfiltered_raw_push_events_commit_df,
                                                                 abnormal_staging_repository_df,
                                                                 filter_columns, adjunct_columns,
                                                                 required_columns, right_index, left_index,
                                                                 staging_push_event_commit_df
                                                                 ):
    """positive test on filtering license and right join without abnormal repositories"""
    res = filter_and_adjunct_push_event_commit(unfiltered_raw_push_events_commit_df,
                                               abnormal_staging_repository_df,
                                               filter_columns, adjunct_columns, required_columns,
                                               right_index=right_index,
                                               left_index=left_index)
    assert_frame_equal(res, staging_push_event_commit_df)
