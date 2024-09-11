# -*- coding: utf-8 -*-

"""
This script automatically setup a newly created GitHub repository with
codecov.io and readthedocs.org.

You have to follow this guide
https://dev-exp-share.readthedocs.io/en/latest/search.html?q=store-token-on-local-laptop&check_keywords=yes&area=default
to store your access token in the proper location on your laptop.

Requirements::

    pip install "requests>=2.29.0,<3.0.0"
    pip install "PyGithub>=2.1.1,<3.0.0"
"""

from pathlib import Path

import requests
from github import Github

dir_home = Path.home()

endpoint = "https://api.codecov.io/api/v2"


CODECOV_GITHUB_SERVICE_NAME = "github"


def get_codecov_token_file(
    service: str,
    owner_username: str,
    token_name: str,
) -> Path:
    """
    Ref: https://dev-exp-share.readthedocs.io/en/latest/search.html?q=store-token-on-local-laptop&check_keywords=yes&area=default
    """
    return dir_home / ".codecov" / service / owner_username / f"{token_name}.txt"


def get_github_token_file(
    owner_username: str,
    token_name: str,
) -> Path:
    """
    Ref: https://dev-exp-share.readthedocs.io/en/latest/search.html?q=store-token-on-local-laptop&check_keywords=yes&area=default
    """
    return dir_home / ".github" / "pac" / owner_username / f"{token_name}.txt"


def get_readthedocs_token_file(
    owner_username: str,
    token_name: str,
) -> Path:
    """
    Ref: https://dev-exp-share.readthedocs.io/en/latest/search.html?q=store-token-on-local-laptop&check_keywords=yes&area=default
    """
    return dir_home / ".readthedocs" / owner_username / f"{token_name}.txt"


def raise_http_response_error(response: requests.Response):
    print(f"{response.text = }")
    print(f"{response.status_code = }")
    raise Exception("Failed to get repository information. See error details above.")


def get_codecov_io_upload_token(
    codecov_token: str,
    service: str,
    github_owner_username: str,
    repo_name: str,
) -> str:
    """
     Get the upload token for codecov io for your GitHub repo.

    Ref:

    - https://docs.codecov.com/reference/repos_retrieve
    - https://docs.codecov.com/reference/repos_config_retrieve
    """
    print("Getting codecov.io upload token...")
    url = f"https://app.codecov.io/gh/{github_owner_username}/{repo_name}/settings"
    print(f"  preview at {url}")
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {codecov_token}",
    }

    url = f"{endpoint}/{service}/{github_owner_username}/repos/{repo_name}/"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise_http_response_error(response)

    data = response.json()
    is_private = data["private"]
    if is_private is True:
        raise ValueError("You cannot use codecov.io for private repositories.")

    url = f"{endpoint}/{service}/{github_owner_username}/repos/{repo_name}/config/"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise_http_response_error(response)

    upload_token = response.json()["upload_token"]
    return upload_token


def setup_codecov_upload_token_on_github(
    codecov_upload_token: str,
    github_token: str,
    github_owner_username: str,
    repo_name: str,
):
    """
    Apply the codecov upload token to GitHub Action secrets in your GitHub repository.

    Ref:

    - https://pygithub.readthedocs.io/en/latest/examples/Repository.html
    """
    print("Setting up codecov.io upload token on GitHub...")
    url = f"https://github.com/{github_owner_username}/{repo_name}/settings/secrets/actions"
    print(f"  preview at {url}")
    gh = Github(github_token)
    repo = gh.get_repo(f"{github_owner_username}/{repo_name}")
    repo.create_secret(
        secret_name="CODECOV_TOKEN",
        unencrypted_value=codecov_upload_token,
        secret_type="actions",
    )


def setup_readthedocs_project(
    readthedocs_token: str,
    github_owner_username: str,
    repo_name: str,
    readthedocs_project_name: str,
):
    """
    Create an project on readthedocs.org.

    Ref:

    - https://docs.readthedocs.io/en/stable/api/v3.html#get--api-v3-projects-(string-project_slug)-
    - https://docs.readthedocs.io/en/stable/api/v3.html#post--api-v3-projects-
    """
    print("Setting up readthedocs project...")
    readthedocs_project_name_slug = readthedocs_project_name.replace("_", "-")
    url = f"https://readthedocs.org/dashboard/{readthedocs_project_name_slug}/edit/"
    print(f"  preview at {url}")
    headers = {
        "accept": "application/json",
        "Authorization": f"Token {readthedocs_token}",
    }
    endpoint = "https://readthedocs.org/api/v3"

    url = f"{endpoint}/projects/{readthedocs_project_name_slug}/"
    response = requests.get(url, headers=headers)
    if response.status_code != 200 and response.status_code != 404:
        raise_http_response_error(response)

    if response.status_code != 404:
        url = f"https://readthedocs.org/projects/{readthedocs_project_name_slug}/"
        raise ValueError(
            f"Project already exists on readthedocs.org, please check it out at: {url}"
        )

    url = f"{endpoint}/projects/"
    github_repo_url = f"https://github.com/{github_owner_username}/{repo_name}"
    data = {
        "name": readthedocs_project_name,
        "repository": {"url": github_repo_url, "type": "git"},
        "homepage": f"http://{readthedocs_project_name_slug}.readthedocs.io/",
        "programming_language": "py",
        "language": "en",
        "privacy_level": "public",
        "external_builds_privacy_level": "public",
        "versioning_scheme": "multiple_versions_with_translations",
        "tags": [],
    }
    response = requests.post(
        url,
        json=data,
        headers=headers,
    )
    if response.status_code != 204:
        raise_http_response_error(response)


# ------------------------------------------------------------------------------
# Don't touch code above
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # --------------------------------------------------------------------------
    # **User input, update values below according to your setting**
    # --------------------------------------------------------------------------
    service = "github"
    repo_name = "compress-project"
    codecov_owner_username = "MacHu-GWU"
    codecov_token_name = "sanhe-dev"
    github_owner_username = "MacHu-GWU"
    github_token_name = "sanhe-dev"
    readthedocs_owner_username = "machugwu"
    readthedocs_token_name = "sanhe-dev"
    readthedocs_project_name = "compress"

    # --------------------------------------------------------------------------
    # Don't touch code below
    # --------------------------------------------------------------------------
    user_input = input(
        "Are you sure you want to setup codecov.io and readthedocs.org for your GitHub repository?\n"
        "You should wait for at least 30 seconds after you create your GitHub repository before running this.\n"
        "Type 'Y' to continue: "
    )
    if user_input.strip() != "Y":
        raise ValueError("User aborted.")

    path_codecov_token = get_codecov_token_file(
        service=service,
        owner_username=codecov_owner_username,
        token_name=codecov_token_name,
    )
    codecov_token = path_codecov_token.read_text().strip()
    path_github_token = get_github_token_file(
        owner_username=github_owner_username,
        token_name=github_token_name,
    )
    github_token = path_github_token.read_text().strip()
    path_readthedocs_token = get_readthedocs_token_file(
        owner_username=readthedocs_owner_username,
        token_name=readthedocs_token_name,
    )
    readthedocs_token = path_readthedocs_token.read_text().strip()

    if service != "github":
        raise ValueError("Only support github service.")

    codecov_upload_token = get_codecov_io_upload_token(
        codecov_token=codecov_token,
        service=service,
        github_owner_username=github_owner_username,
        repo_name=repo_name,
    )

    setup_codecov_upload_token_on_github(
        codecov_upload_token=codecov_upload_token,
        github_token=github_token,
        github_owner_username=github_owner_username,
        repo_name=repo_name,
    )

    setup_readthedocs_project(
        readthedocs_token=readthedocs_token,
        github_owner_username=github_owner_username,
        repo_name=repo_name,
        readthedocs_project_name=readthedocs_project_name,
    )
