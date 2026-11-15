"""Old page-view addresses and the name each answers as (split out of serve.py)."""


# A theme's board page answers at /_board/<theme>-board, named as its theme is (JL 261007: "make them
# the same to the theme name"). The names two had before (task-board, paper) answered as them until 261012,
# when they were dropped (JL: "yes, this one should be droped"): nothing links them any more.
# One Page Task's views were a route each (the old Page workbench, one page per tab); they are the
# frame's Task Spaces now (JL 261007: "why not merge them into the base"), served by the frame route
# as `/_board/workbench?view=<view>`. A GET or HEAD of an old address answers as that; its POST twin
# (the tab contract's write) keeps its address.
PAGE_VIEW_ROUTES = {"/_board/folderstat": "folder", "/_board/draft": "draft", "/_board/outline": "draft",
                    "/_board/value": "value", "/_board/evidence": "evidence", "/_board/delivery": "delivery",
                    "/_board/runs": "runs", "/_board/pageruns": "pageruns"}


def new_route_name(path: str, method: str = "GET") -> str:
    """On a GET or HEAD, `/_board/runs?x` -> `/_board/workbench?view=runs&x`; any other path as it is."""
    head, sep, query = path.partition("?")
    view = PAGE_VIEW_ROUTES.get(head) if method in ("GET", "HEAD") else None
    if view:
        return "/_board/workbench?view=" + view + ("&" + query if query else "")
    return head + sep + query
