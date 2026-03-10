from typing import Any, Dict, List
from .. import resources

class UsersDSL:
    def get_users(self) -> List[resources.User]:
        return resources.User.parse(self.request('get', 'users/'))

    def get_user_me(self) -> resources.User:
        return resources.User.parse(self.request('get', 'users/me'))

    def get_user(self, *, resource_id: str) -> resources.User:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.User.parse(self.request('get', f"users/{resource_id}"))

    def create_user(self, *, params: Dict[str, Any]) -> resources.User:
        return resources.User.parse(self.request('post', 'users/', query=params))

    def update_user(self, *, resource_id: str, params: Dict[str, Any]) -> resources.User:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.User.parse(self.request('put', f"users/{resource_id}", query=params))

    def patch_user(self, *, resource_id: str, params: Dict[str, Any]) -> resources.User:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.User.parse(self.request('patch', f"users/{resource_id}", query=params))

    def delete_user(self, *, resource_id: str) -> bool:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"users/{resource_id}").status_code == 204
