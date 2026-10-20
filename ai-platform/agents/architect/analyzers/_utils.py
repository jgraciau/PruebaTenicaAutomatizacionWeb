import re
from collections import Counter
from typing import Any


def relationships(maps: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    dependency_map = maps.get("dependency-map", {})
    items = dependency_map.get("relationships")
    if isinstance(items, list):
        return [item for item in items if isinstance(item, dict)]

    relationship_map = maps.get("relationship-map", {})
    items = relationship_map.get("relationships", [])
    return [item for item in items if isinstance(item, dict)]


def components(
    architecture: dict[str, Any],
    *names: str,
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for name in names:
        values = architecture.get(name, [])
        if isinstance(values, list):
            result.extend(item for item in values if isinstance(item, dict))
    return result


def isolated_components(
    maps: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    architecture = maps.get("architecture-map", {})
    edges = relationships(maps)
    connected_ids = {
        edge.get(endpoint)
        for edge in edges
        for endpoint in ("source_id", "target_id")
        if isinstance(edge.get(endpoint), str)
    }
    return {
        name: [
            item
            for item in components(architecture, name)
            if isinstance(item.get("id"), str)
            and item["id"] not in connected_ids
        ]
        for name in ("tasks", "questions", "interactions", "targets", "models")
    }


def cycle_affected_count(maps: dict[str, dict[str, Any]]) -> int:
    graph_data = maps.get("dependency-graph", {})
    architecture = maps.get("architecture-map", {})
    nodes = graph_data.get("nodes", [])
    node_ids: set[str] = set()
    if isinstance(nodes, list):
        node_ids = {
            node["id"]
            for node in nodes
            if isinstance(node, dict) and isinstance(node.get("id"), str)
        }
    if not node_ids:
        categories = (
            "features",
            "scenarios",
            "step_definitions",
            "actors",
            "tasks",
            "questions",
            "interactions",
            "targets",
            "models",
        )
        for component in components(architecture, *categories):
            identifier = component.get("id")
            if isinstance(identifier, str):
                node_ids.add(identifier)
    adjacency: dict[str, list[str]] = {node_id: [] for node_id in node_ids}
    for edge in relationships(maps):
        source_id = edge.get("source_id")
        target_id = edge.get("target_id")
        if isinstance(source_id, str) and isinstance(target_id, str):
            adjacency.setdefault(source_id, []).append(target_id)
            adjacency.setdefault(target_id, [])

    indegree = {node_id: 0 for node_id in adjacency}
    for targets in adjacency.values():
        for target_id in targets:
            indegree[target_id] += 1
    ready = [
        node_id for node_id, degree in indegree.items() if degree == 0
    ]
    visited_count = 0
    while ready:
        node_id = ready.pop()
        visited_count += 1
        for target_id in adjacency[node_id]:
            indegree[target_id] -= 1
            if indegree[target_id] == 0:
                ready.append(target_id)
    declared = graph_data.get("cycles", [])
    declared_count = len(declared) if isinstance(declared, list) else 0
    return max(len(adjacency) - visited_count, declared_count)


def repeated_scenario_signatures(
    architecture: dict[str, Any],
) -> Counter[tuple[str, ...]]:
    scenarios = components(architecture, "scenarios")
    if not scenarios:
        features = components(architecture, "features")
        scenarios = [
            scenario
            for feature in features
            for scenario in feature.get("scenarios", [])
            if isinstance(scenario, dict)
        ]
    return Counter(
        tuple(
            re.sub(r'"[^"]*"', '"{value}"', str(step).casefold())
            for step in scenario.get("steps", [])
        )
        for scenario in scenarios
        if isinstance(scenario.get("steps"), list) and scenario["steps"]
    )


def finding(
    identifier: str,
    title: str,
    description: str,
    evidence: str,
    severity: str = "medium",
) -> dict[str, str]:
    return {
        "id": identifier,
        "title": title,
        "description": description,
        "evidence": evidence,
        "severity": severity,
    }


def recommendation(
    category: str,
    title: str,
    action: str,
    evidence: str,
    severity: str = "medium",
) -> dict[str, str]:
    return {
        "category": category,
        "title": title,
        "action": action,
        "evidence": evidence,
        "severity": severity,
    }
