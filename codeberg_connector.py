"""
Codeberg API Connector for AI Agents

A Python client for the Codeberg (Gitea) API.
Supports repositories, issues, pull requests, user/org data, and Git operations.

Usage:
    from codeberg_connector import CodebergClient
    
    client = CodebergClient(token="your_personal_access_token")
    
    # List your repositories
    repos = client.list_repos()
    
    # Create a new repository
    client.create_repo("my-new-repo", private=False)
    
    # List issues for a repo
    issues = client.list_issues("username/repo-name")

API Documentation:
    https://codeberg.org/api/swagger
    https://gitea.com/api/swagger (Codeberg uses Gitea API)
"""

import asyncio
import os
from dataclasses import dataclass
from typing import Any, Optional, Union
from urllib.parse import urljoin

import aiohttp
from aiohttp import ClientSession, ClientResponseError


# Base API URL for Codeberg
CODEBERG_API_URL = "https://codeberg.org/api/v1"


@dataclass
class Repo:
    """Repository data class."""
    id: int
    name: str
    full_name: str
    description: Optional[str] = None
    private: bool = False
    fork: bool = False
    html_url: Optional[str] = None
    ssh_url: Optional[str] = None
    clone_url: Optional[str] = None
    default_branch: Optional[str] = None
    owner: Optional[dict] = None
    permissions: Optional[dict] = None


@dataclass
class Issue:
    """Issue data class."""
    id: int
    number: int
    title: str
    body: Optional[str] = None
    state: str = "open"  # open, closed
    html_url: Optional[str] = None
    user: Optional[dict] = None
    labels: Optional[list] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class PullRequest:
    """Pull Request data class."""
    id: int
    number: int
    title: str
    body: Optional[str] = None
    state: str = "open"  # open, closed, merged
    html_url: Optional[str] = None
    user: Optional[dict] = None
    base: Optional[dict] = None
    head: Optional[dict] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class User:
    """User data class."""
    id: int
    login: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    html_url: Optional[str] = None
    type: Optional[str] = None  # user, organization


class CodebergError(Exception):
    """Base exception for Codeberg API errors."""
    pass


class AuthenticationError(CodebergError):
    """Raised when authentication fails."""
    pass


class NotFoundError(CodebergError):
    """Raised when a resource is not found."""
    pass


class CodebergClient:
    """
    Async client for the Codeberg API.
    
    Args:
        token: Personal access token for authentication.
               Can also be set via CODEBERG_TOKEN environment variable.
        base_url: Base API URL (default: https://codeberg.org/api/v1).
        session: Optional aiohttp ClientSession for reuse.
    """
    
    def __init__(
        self,
        token: Optional[str] = None,
        base_url: str = CODEBERG_API_URL,
        session: Optional[ClientSession] = None
    ):
        self.token = token or os.getenv("CODEBERG_TOKEN")
        self.base_url = base_url.rstrip("/")
        self._session = session
        self._owns_session = False
        
    async def __aenter__(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._owns_session = True
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._owns_session and self._session:
            await self._session.close()
            self._session = None
            self._owns_session = False
    
    def _get_headers(self) -> dict:
        """Get headers with authentication if token is available."""
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        return urljoin(f"{self.base_url}/", endpoint.lstrip("/"))
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        json: Optional[dict] = None
    ) -> dict:
        """
        Make an HTTP request to the Codeberg API.
        """
        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._owns_session = True
        
        url = self._build_url(endpoint)
        headers = self._get_headers()
        
        try:
            async with self._session.request(
                method,
                url,
                headers=headers,
                params=params,
                data=data,
                json=json
            ) as response:
                if response.status == 403:
                    rate_limit_reset = response.headers.get("X-RateLimit-Reset")
                    raise CodebergError(f"Rate limit exceeded. Reset at: {rate_limit_reset}")
                
                if response.status == 401:
                    raise AuthenticationError("Authentication failed. Check your token.")
                
                if response.status == 404:
                    raise NotFoundError(f"Resource not found: {endpoint}")
                
                if response.status >= 400:
                    try:
                        error_data = await response.json()
                        error_msg = error_data.get("message", response.reason)
                    except:
                        error_msg = response.reason
                    raise CodebergError(f"API error: {error_msg}")
                
                try:
                    return await response.json()
                except:
                    return {"status": response.status, "text": await response.text()}
                    
        except aiohttp.ClientError as e:
            raise CodebergError(f"Network error: {str(e)}")
    
    # Repository Operations
    
    async def list_repos(
        self,
        user: Optional[str] = None,
        org: Optional[str] = None,
        limit: int = 30,
        page: int = 1
    ) -> list:
        """List repositories."""
        if org:
            endpoint = f"org/{org}/repos"
        elif user:
            endpoint = f"users/{user}/repos"
        else:
            endpoint = "user/repos"
        
        params = {"limit": limit, "page": page}
        data = await self._request("GET", endpoint, params=params)
        
        repos = []
        for repo_data in data:
            repos.append(Repo(
                id=repo_data.get("id"),
                name=repo_data.get("name"),
                full_name=repo_data.get("full_name"),
                description=repo_data.get("description"),
                private=repo_data.get("private", False),
                fork=repo_data.get("fork", False),
                html_url=repo_data.get("html_url"),
                ssh_url=repo_data.get("ssh_url"),
                clone_url=repo_data.get("clone_url"),
                default_branch=repo_data.get("default_branch"),
                owner=repo_data.get("owner"),
                permissions=repo_data.get("permissions")
            ))
        return repos
    
    async def get_repo(self, repo_full_name: str):
        """Get a single repository by full name."""
        data = await self._request("GET", f"repos/{repo_full_name}")
        return Repo(
            id=data.get("id"),
            name=data.get("name"),
            full_name=data.get("full_name"),
            description=data.get("description"),
            private=data.get("private", False),
            fork=data.get("fork", False),
            html_url=data.get("html_url"),
            ssh_url=data.get("ssh_url"),
            clone_url=data.get("clone_url"),
            default_branch=data.get("default_branch"),
            owner=data.get("owner"),
            permissions=data.get("permissions")
        )
    
    async def create_repo(
        self,
        name: str,
        description: Optional[str] = None,
        private: bool = False,
        auto_init: bool = False,
        gitignores: Optional[str] = None,
        license: Optional[str] = None,
        readme: Optional[str] = None
    ):
        """Create a new repository."""
        data = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": auto_init,
            "gitignores": gitignores,
            "license": license,
            "readme": readme
        }
        data = {k: v for k, v in data.items() if v is not None}
        response = await self._request("POST", "user/repos", json=data)
        return Repo(
            id=response.get("id"),
            name=response.get("name"),
            full_name=response.get("full_name"),
            description=response.get("description"),
            private=response.get("private", False),
            fork=response.get("fork", False),
            html_url=response.get("html_url"),
            ssh_url=response.get("ssh_url"),
            clone_url=response.get("clone_url"),
            default_branch=response.get("default_branch"),
            owner=response.get("owner"),
            permissions=response.get("permissions")
        )
    
    async def delete_repo(self, repo_full_name: str) -> bool:
        """Delete a repository."""
        await self._request("DELETE", f"repos/{repo_full_name}")
        return True
    
    # Issue Operations
    
    async def list_issues(
        self,
        repo_full_name: str,
        state: str = "open",
        labels: Optional[str] = None,
        milestone: Optional[int] = None,
        limit: int = 30,
        page: int = 1
    ):
        """List issues for a repository."""
        params = {"state": state, "labels": labels, "milestone": milestone, "limit": limit, "page": page}
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._request("GET", f"repos/{repo_full_name}/issues", params=params)
        
        issues = []
        for issue_data in data:
            issues.append(Issue(
                id=issue_data.get("id"),
                number=issue_data.get("number"),
                title=issue_data.get("title"),
                body=issue_data.get("body"),
                state=issue_data.get("state", "open"),
                html_url=issue_data.get("html_url"),
                user=issue_data.get("user"),
                labels=issue_data.get("labels"),
                created_at=issue_data.get("created_at"),
                updated_at=issue_data.get("updated_at")
            ))
        return issues
    
    async def get_issue(self, repo_full_name: str, issue_number: int):
        """Get a single issue."""
        data = await self._request("GET", f"repos/{repo_full_name}/issues/{issue_number}")
        return Issue(
            id=data.get("id"),
            number=data.get("number"),
            title=data.get("title"),
            body=data.get("body"),
            state=data.get("state", "open"),
            html_url=data.get("html_url"),
            user=data.get("user"),
            labels=data.get("labels"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    async def create_issue(
        self,
        repo_full_name: str,
        title: str,
        body: Optional[str] = None,
        labels: Optional[list] = None,
        milestone: Optional[int] = None
    ):
        """Create a new issue."""
        data = {"title": title, "body": body, "labels": labels, "milestone": milestone}
        data = {k: v for k, v in data.items() if v is not None}
        response = await self._request("POST", f"repos/{repo_full_name}/issues", json=data)
        return Issue(
            id=response.get("id"),
            number=response.get("number"),
            title=response.get("title"),
            body=response.get("body"),
            state=response.get("state", "open"),
            html_url=response.get("html_url"),
            user=response.get("user"),
            labels=response.get("labels"),
            created_at=response.get("created_at"),
            updated_at=response.get("updated_at")
        )
    
    async def add_issue_comment(self, repo_full_name: str, issue_number: int, body: str):
        """Add a comment to an issue."""
        return await self._request(
            "POST", f"repos/{repo_full_name}/issues/{issue_number}/comments", json={"body": body}
        )
    
    # Pull Request Operations
    
    async def list_pull_requests(self, repo_full_name: str, state: str = "open", limit: int = 30, page: int = 1):
        """List pull requests for a repository."""
        params = {"state": state, "limit": limit, "page": page}
        data = await self._request("GET", f"repos/{repo_full_name}/pulls", params=params)
        pulls = []
        for pr_data in data:
            pulls.append(PullRequest(
                id=pr_data.get("id"),
                number=pr_data.get("number"),
                title=pr_data.get("title"),
                body=pr_data.get("body"),
                state=pr_data.get("state", "open"),
                html_url=pr_data.get("html_url"),
                user=pr_data.get("user"),
                base=pr_data.get("base"),
                head=pr_data.get("head"),
                created_at=pr_data.get("created_at"),
                updated_at=pr_data.get("updated_at")
            ))
        return pulls
    
    async def get_pull_request(self, repo_full_name: str, pr_number: int):
        """Get a single pull request."""
        data = await self._request("GET", f"repos/{repo_full_name}/pulls/{pr_number}")
        return PullRequest(
            id=data.get("id"),
            number=data.get("number"),
            title=data.get("title"),
            body=data.get("body"),
            state=data.get("state", "open"),
            html_url=data.get("html_url"),
            user=data.get("user"),
            base=data.get("base"),
            head=data.get("head"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    async def create_pull_request(
        self, repo_full_name: str, title: str, head: str, base: str, body: Optional[str] = None
    ):
        """Create a new pull request."""
        data = {"title": title, "head": head, "base": base, "body": body}
        data = {k: v for k, v in data.items() if v is not None}
        response = await self._request("POST", f"repos/{repo_full_name}/pulls", json=data)
        return PullRequest(
            id=response.get("id"),
            number=response.get("number"),
            title=response.get("title"),
            body=response.get("body"),
            state=response.get("state", "open"),
            html_url=response.get("html_url"),
            user=response.get("user"),
            base=response.get("base"),
            head=response.get("head"),
            created_at=response.get("created_at"),
            updated_at=response.get("updated_at")
        )
    
    # User/Organization Operations
    
    async def get_user(self, username: str):
        """Get user information."""
        data = await self._request("GET", f"users/{username}")
        return User(
            id=data.get("id"),
            login=data.get("login"),
            full_name=data.get("full_name"),
            email=data.get("email"),
            avatar_url=data.get("avatar_url"),
            html_url=data.get("html_url"),
            type=data.get("type")
        )
    
    async def get_authenticated_user(self):
        """Get information about the authenticated user."""
        data = await self._request("GET", "user")
        return User(
            id=data.get("id"),
            login=data.get("login"),
            full_name=data.get("full_name"),
            email=data.get("email"),
            avatar_url=data.get("avatar_url"),
            html_url=data.get("html_url"),
            type=data.get("type")
        )
    
    async def list_orgs(self):
        """List organizations the authenticated user belongs to."""
        data = await self._request("GET", "user/orgs")
        orgs = []
        for org_data in data:
            orgs.append(User(
                id=org_data.get("id"),
                login=org_data.get("login"),
                full_name=org_data.get("full_name"),
                email=org_data.get("email"),
                avatar_url=org_data.get("avatar_url"),
                html_url=org_data.get("html_url"),
                type=org_data.get("type")
            ))
        return orgs
    
    async def get_org(self, org_name: str):
        """Get organization information."""
        data = await self._request("GET", f"orgs/{org_name}")
        return User(
            id=data.get("id"),
            login=data.get("login"),
            full_name=data.get("full_name"),
            email=data.get("email"),
            avatar_url=data.get("avatar_url"),
            html_url=data.get("html_url"),
            type=data.get("type")
        )
    
    # Git Operations
    
    def get_repo_clone_url(self, repo_full_name: str, protocol: str = "https") -> str:
        """Get the clone URL for a repository."""
        if protocol == "https":
            return f"https://codeberg.org/{repo_full_name}.git"
        elif protocol == "ssh":
            return f"git@codeberg.org:{repo_full_name}.git"
        elif protocol == "git":
            return f"git://codeberg.org/{repo_full_name}.git"
        else:
            raise ValueError(f"Unsupported protocol: {protocol}")


# Synchronous Wrapper

class SyncCodebergClient:
    """Synchronous wrapper for the Codeberg API."""
    
    def __init__(self, token: Optional[str] = None, base_url: str = CODEBERG_API_URL):
        self.token = token or os.getenv("CODEBERG_TOKEN")
        self.base_url = base_url.rstrip("/")
        self._loop = None
    
    def _get_loop(self):
        if self._loop is None:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        return self._loop
    
    def _run_async(self, coro):
        loop = self._get_loop()
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            return future.result()
        else:
            return loop.run_until_complete(coro)
    
    def list_repos(self, **kwargs):
        async def _list():
            async with CodebergClient(self.token, self.base_url) as client:
                return await client.list_repos(**kwargs)
        return self._run_async(_list())
    
    def get_repo(self, repo_full_name: str):
        async def _get():
            async with CodebergClient(self.token, self.base_url) as client:
                return await client.get_repo(repo_full_name)
        return self._run_async(_get())
    
    def create_repo(self, **kwargs):
        async def _create():
            async with CodebergClient(self.token, self.base_url) as client:
                return await client.create_repo(**kwargs)
        return self._run_async(_create())
    
    def list_issues(self, repo_full_name: str, **kwargs):
        async def _list():
            async with CodebergClient(self.token, self.base_url) as client:
                return await client.list_issues(repo_full_name, **kwargs)
        return self._run_async(_list())
    
    def get_issue(self, repo_full_name: str, issue_number: int):
        async def _get():
            async with CodebergClient(self.token, self.base_url) as client:
                return await client.get_issue(repo_full_name, issue_number)
        return self._run_async(_get())
    
    def create_issue(self, repo_full_name: str, **kwargs):
        async def _create():
            async with CodebergClient(self.token, self.base_url) as client:
                return await client.create_issue(repo_full_name, **kwargs)
        return self._run_async(_create())
    
    def list_pull_requests(self, repo_full_name: str, **kwargs):
        async def _list():
            async with CodebergClient(self.token, self.base_url) as client:
                return await client.list_pull_requests(repo_full_name, **kwargs)
        return self._run_async(_list())
    
    def get_pull_request(self, repo_full_name: str, pr_number: int):
        async def _get():
            async with CodebergClient(self.token, self.base_url) as client:
                return await client.get_pull_request(repo_full_name, pr_number)
        return self._run_async(_get())
    
    def create_pull_request(self, repo_full_name: str, **kwargs):
        async def _create():
            async with CodebergClient(self.token, self.base_url) as client:
                return await client.create_pull_request(repo_full_name, **kwargs)
        return self._run_async(_create())
    
    def get_user(self, username: str):
        async def _get():
            async with CodebergClient(self.token, self.base_url) as client:
                return await client.get_user(username)
        return self._run_async(_get())
    
    def get_authenticated_user(self):
        async def _get():
            async with CodebergClient(self.token, self.base_url) as client:
                return await client.get_authenticated_user()
        return self._run_async(_get())
    
    def list_orgs(self):
        async def _list():
            async with CodebergClient(self.token, self.base_url) as client:
                return await client.list_orgs()
        return self._run_async(_list())
    
    def get_org(self, org_name: str):
        async def _get():
            async with CodebergClient(self.token, self.base_url) as client:
                return await client.get_org(org_name)
        return self._run_async(_get())
    
    def get_repo_clone_url(self, repo_full_name: str, protocol: str = "https") -> str:
        return CodebergClient.get_repo_clone_url(self, repo_full_name, protocol)


if __name__ == "__main__":
    import asyncio
    
    async def demo():
        async with CodebergClient() as client:
            print("=== Listing repos ===")
            repos = await client.list_repos(user="codeberg")
            for repo in repos[:5]:
                print(f"  {repo.full_name} - {repo.description or 'No description'}")
            
            if client.token:
                print("\n=== Authenticated User ===")
                user = await client.get_authenticated_user()
                print(f"  {user.login} ({user.full_name or 'No full name'})")
    
    asyncio.run(demo())
