# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ProjectListParams"]


class ProjectListParams(TypedDict, total=False):
    user_id: Optional[str]

    x_organization_id: Annotated[str, PropertyInfo(alias="X-Organization-ID")]
