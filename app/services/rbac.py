ROLE_PERMISSIONS: dict[str, list[str]] = {
    "Admin": ["*"] ,
    "Financial Analyst": [
        "documents:upload",
        "documents:edit",
        "documents:view",
        "rag:index",
        "rag:search",
    ],
    "Auditor": ["documents:view", "documents:review", "rag:search"],
    "Client": ["documents:view_company", "rag:search_company"],
}


def get_permissions_for_roles(role_names: list[str]) -> set[str]:
    permissions: set[str] = set()
    for role_name in role_names:
        permissions.update(ROLE_PERMISSIONS.get(role_name, []))
    return permissions
