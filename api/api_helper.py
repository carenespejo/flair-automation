"""
============================================================
 api_helper.py
============================================================

FLAIR-ALIGNED API HELPER (READ-ONLY)

WHAT THIS FILE IS FOR
---------------------
- Read-only verification of sourcing data created via FLAIR UI
- Used ONLY when backend/API access is available
- Supports QA validation without bypassing security

WHAT THIS FILE IS NOT
---------------------
- NOT used to create data
- NOT used to trigger SAP
- NOT required for UI-only testing

IMPORTANT
---------
- If API access is unavailable, methods will safely return None / False
  instead of failing tests.
"""

from __future__ import annotations

import os
import requests
from typing import Any, Dict, Optional


class ItemSourcingAPI:
    """
    Read-only helper for verifying Item Sourcing data in FLAIR.

    This helper assumes:
    - Backend access MAY or MAY NOT be available
    - QA should never bypass authentication
    """

    def __init__(self):
        # Backend URL (optional)
        self.base_url: Optional[str] = os.getenv("https://test.techignitebusiness.com:7012")

        # Optional auth token (read-only)
        self.auth_token: Optional[str] = os.getenv("FLAIR_API_TOKEN")

        self.headers = {
            "Content-Type": "application/json",
        }

        if self.auth_token:
            self.headers["Authorization"] = f"Bearer {self.auth_token}"

    # -------------------------------------------------
    # INTERNAL SAFETY CHECK
    # -------------------------------------------------
    def _api_available(self) -> bool:
        return bool(self.base_url)

    # -------------------------------------------------
    # GENERIC GET WRAPPER (READ-ONLY)
    # -------------------------------------------------
    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        if not self._api_available():
            return None

        try:
            response = requests.get(
                f"{self.base_url.rstrip('/')}{path}",
                headers=self.headers,
                params=params,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            # QA-safe: do not crash UI tests
            return None

    # -------------------------------------------------
    # FLAIR-SPECIFIC METHODS
    # -------------------------------------------------
    def get_item_sourcing_list(
        self,
        page_size: int = 200,
        page: int = 1,
    ) -> Optional[list[Dict[str, Any]]]:
        """
        Fetch sourcing records from FLAIR backend (if accessible).
        """
        response = self._get(
            "/api/item-sourcing",
            params={"pageSize": page_size, "page": page},
        )
        if not response:
            return None

        return response.get("data", [])

    def find_sourcing_by_supplier_name(self, supplier_name: str) -> Optional[Dict[str, Any]]:
        """
        Find a sourcing record by supplier name.
        """
        records = self.get_item_sourcing_list()
        if not records:
            return None

        for record in records:
            if record.get("supplierName") == supplier_name:
                return record

        return None

    def find_item_in_sourcing(
        self,
        sourcing_record: Dict[str, Any],
        item_name: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Find an item inside a sourcing record.
        """
        for item in sourcing_record.get("items", []):
            if item.get("itemName") == item_name:
                return item
        return None

    # -------------------------------------------------
    # QA VERIFICATION METHODS (SAFE)
    # -------------------------------------------------
    def verify_supplier_exists(self, supplier_name: str) -> bool:
        """
        Verify supplier exists (API available).
        Returns False if API is unavailable.
        """
        return self.find_sourcing_by_supplier_name(supplier_name) is not None

    def verify_item_exists_under_supplier(
        self,
        supplier_name: str,
        item_name: str,
    ) -> bool:
        """
        Verify item exists under supplier (API available).
        """
        sourcing = self.find_sourcing_by_supplier_name(supplier_name)
        if not sourcing:
            return False

        return self.find_item_in_sourcing(sourcing, item_name) is not None
