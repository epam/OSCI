from osci.helper import (generate_company_to_contributors_map, generate_company_to_languages_map,
                            generate_company_to_licenses_map)


def test_company_to_contributors_map(company_contributors_df, expected_generate_company_to_contributors_map):
    result = generate_company_to_contributors_map(company_contributors_df)
    assert result == expected_generate_company_to_contributors_map


def test_company_to_licenses_map(company_licenses_df, expected_generate_company_to_licenses_map):
    result = generate_company_to_licenses_map(company_licenses_df)
    assert result == expected_generate_company_to_licenses_map


def test_company_to_languages_map(company_languages_df, expected_generate_company_to_languages_map):
    result = generate_company_to_languages_map(company_languages_df)
    assert result == expected_generate_company_to_languages_map
