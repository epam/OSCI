import os
import pytest
import yaml


def get_file_path():
    """
    Return the absolute path to the YAML file based on the relative location from this script.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_dir, "osci", "preprocess", "match_company", "company_domain_match_list.yaml")


def read_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def parse_yaml_content(content):
    return yaml.safe_load(content)


def has_tabs(content):
    """
    Check if the provided content contains any tab characters.
    Return a list of line numbers where tabs are found.
    """
    lines_with_tabs = []
    lines = content.splitlines()
    for index, line in enumerate(lines, start=1):
        if '\t' in line:
            lines_with_tabs.append(index)
    return lines_with_tabs


def test_yaml_no_tabs():
    """
    Ensure that the YAML file does not contain tabs.
    This function prints out the specific line numbers where tabs are found.
    """
    file_path = get_file_path()
    content = read_file_content(file_path)
    lines_with_tabs = has_tabs(content)
    assert not lines_with_tabs, f"The YAML file contains tabs at line(s): {', '.join(map(str, lines_with_tabs))}"


def test_industry_exists_and_not_empty():
    """
    Test if each company entry has a non-empty 'industry' field.
    """
    file_path = get_file_path()
    content = read_file_content(file_path)
    data = parse_yaml_content(content)
    companies_with_issues = [entry['company'] for entry in data if 'industry' not in entry or not entry['industry']]
    assert not companies_with_issues, f"Missing or empty 'industry' for company(ies): {', '.join(companies_with_issues)}"


def test_domains_exist_and_not_empty():
    """
    Test if each company entry has non-empty 'domains' field.
    """
    file_path = get_file_path()
    content = read_file_content(file_path)
    data = parse_yaml_content(content)
    companies_with_issues = [entry['company'] for entry in data if
                             'domains' not in entry or not entry['domains'] or not all(entry['domains'])]
    assert not companies_with_issues, f"Missing or empty 'domains' for company(ies): {', '.join(companies_with_issues)}"
