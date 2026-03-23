from typing import Any, Dict, List, Optional
from .. import resources

class UwListingCmsAppsDSL:
    def get_uw_listing_cms_apps(self, params: Optional[Dict[str, Any]] = None) -> List[resources.UwListingCmsApp]:
        return resources.UwListingCmsApp.parse(self.request('get', 'uw_listing_cms_apps/', query=params))

    def get_uw_listing_cms_app(self, *, resource_id: str) -> resources.UwListingCmsApp:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.UwListingCmsApp.parse(self.request('get', f"uw_listing_cms_apps/{resource_id}"))

    def create_uw_listing_cms_app(self, *, params: Dict[str, Any]) -> resources.UwListingCmsApp:
        return resources.UwListingCmsApp.parse(self.request('post', 'uw_listing_cms_apps/', query=params))

    def update_uw_listing_cms_app(self, *, resource_id: str, params: Dict[str, Any]) -> resources.UwListingCmsApp:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.UwListingCmsApp.parse(self.request('put', f"uw_listing_cms_apps/{resource_id}", query=params))

    def patch_uw_listing_cms_app(self, *, resource_id: str, params: Dict[str, Any]) -> resources.UwListingCmsApp:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.UwListingCmsApp.parse(self.request('patch', f"uw_listing_cms_apps/{resource_id}", query=params))

    def delete_uw_listing_cms_app(self, *, resource_id: str) -> bool:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"uw_listing_cms_apps/{resource_id}").status_code == 204
