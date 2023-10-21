from __future__ import annotations
import lib.secrets as secrets

import lib.commons.Platform as Platform
import lib.commons.Credentials as Credentials
import lib.commons.Repository as Repository

import requests

class Gitea(Platform):
    @staticmethod
    def from_env(key: str) -> Gitea:
        Gitea(secrets.get_env_or_raise("%s_GITEA_URL" %s key))

    def __init__(self, instance: str):
        super().__init__(instance)

    def get_repositories_of_user(self, user: User, credentials: Credentials) -> list[Repository]:
        auth = (credentials.get_username(),
                credentials.get_token())
        headers = {
            "accept": "application/json"
        }
        username = user.get_username()
        response = requests.get("%s/api/v1/users/%s/repos" % (self.get_url(),
                                                              username),
                                headers=headers, auth=auth)
        return [Repository.from_json(_) for _ in response.json()]

    def _validate_migration_config(self, config: dict = None) -> dict:
        if config is None:
            config = {}
        if "mirror" not in config:
            config["mirror"] = False
        if "private" not in config:
            config["private"] = False
        if "wiki" not in config:
            config["wiki"] = True
        return config

    def migrate(self, repo: Repository, config: dict, credentials: Credentials) -> Repository:
        config = self._validate_migration_config(config)
        url = "%s/api/v1/repos/migrate" % self.get_url()
        auth = (credentials.get_username(),
                credentials.get_token())
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "auth_username": credentials.get_username(),
            "auth_password": credentials.get_token(),
            "clone_addr": repo.get_url(),
            "mirror": config["mirror"],
            "private": config["private"],
            "repo_name": "$REPO_NAME",
            "repo_owner": credentials.get_username(),
            "service": "git",
            "uid": 0,
            "wiki": config["wiki"]
        }
        response = requests.post(url, headers=headers, auth=auth, data=data)
        return Repository.from_json(response.json())
