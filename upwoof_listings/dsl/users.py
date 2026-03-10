from typing import Any, Dict, List, Optional, Union
from .. import resources

class UsersDSL:
    def get_users(self) -> List[resources.User]:
        return resources.User.parse(self.request('get', 'users/'))

    def get_user_me(self) -> resources.User:
        return resources.User.parse(self.request('get', 'users/me'))

    def get_user(self, *, id: str) -> resources.User:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.User.parse(self.request('get', f"users/{id}"))

    def create_user(self, *, params: Dict[str, Any]) -> resources.User:
        return resources.User.parse(self.request('post', 'users/', query=params))

    def update_user(self, *, id: str, params: Dict[str, Any]) -> resources.User:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.User.parse(self.request('put', f"users/{id}", query=params))

    def patch_user(self, *, id: str, params: Dict[str, Any]) -> resources.User:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.User.parse(self.request('patch', f"users/{id}", query=params))

    def delete_user(self, *, id: str) -> bool:
        if not id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"users/{id}").status_code == 204
