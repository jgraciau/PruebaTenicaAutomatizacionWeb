import re
from collections import Counter
from typing import Any

from agents.architect.models.finding import Finding
from agents.architect.models.recommendation import Recommendation


def relationships(maps: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    dependency_map = maps.get("dependency-map", {})
    items = dependency_map.get("relationships")
    if isinstance(items, list):
        return [item for item in items if isinstance(item, dict)]

    relationship_map = maps.get("relationship-map", {})
    items = relationship_map.get("relationships", [])
    return [item for item in items if isinstance(item, dict)]


def graph_edges(maps: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    graph = maps.get("dependency-graph", {})
    edges = graph.get("edges", [])
    if isinstance(edges, list) and edges:
        return [edge for edge in edges if isinstance(edge, dict)]
    return relationships(maps)


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


def dependency_metrics(
    maps: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    graph = maps.get("dependency-graph", {})
    nodes = graph.get("nodes", [])
    node_ids = {
        node["id"]
        for node in nodes
        if isinstance(nodes, list)
        and isinstance(node, dict)
        and isinstance(node.get("id"), str)
    } if isinstance(nodes, list) else set()
    fan_in = {node_id: 0 for node_id in node_ids}
    fan_out = {node_id: 0 for node_id in node_ids}
    edges = graph_edges(maps)
    for edge in edges:
        source_id = edge.get("source_id")
        target_id = edge.get("target_id")
        if not isinstance(source_id, str) or not isinstance(target_id, str):
            continue
        fan_out[source_id] = fan_out.get(source_id, 0) + 1
        fan_in[target_id] = fan_in.get(target_id, 0) + 1
        fan_in.setdefault(source_id, 0)
        fan_out.setdefault(target_id, 0)
    degrees = {
        node_id: fan_in[node_id] + fan_out[node_id]
        for node_id in fan_in
    }
    node_count = max(len(node_ids), len(degrees))
    return {
        "node_count": node_count,
        "edge_count": len(edges),
        "fan_in": fan_in,
        "fan_out": fan_out,
        "degree": degrees,
        "max_fan_out": max(fan_out.values(), default=0),
        "max_degree": max(degrees.values(), default=0),
        "average_degree": (
            sum(degrees.values()) / len(degrees) if degrees else 0.0
        ),
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
    return Finding(identifier, title, description, evidence, severity).to_dict()


def recommendation(
    category: str,
    title: str,
    action: str,
    evidence: str,
    severity: str = "medium",
) -> dict[str, str]:
    return Recommendation(category, title, action, evidence, severity).to_dict()


def duplicate_components(
    architecture: dict[str, Any],
    categories: tuple[str, ...],
) -> dict[str, list[dict[str, Any]]]:
    duplicates: dict[str, list[dict[str, Any]]] = {}
    for category in categories:
        by_name: dict[str, list[dict[str, Any]]] = {}
        for component in components(architecture, category):
            name = component.get("name")
            if isinstance(name, str) and name.strip():
                normalized_name = re.sub(r"\W+", "", name.casefold())
                by_name.setdefault(normalized_name, []).append(component)
        for normalized_name, matches in by_name.items():
            if len(matches) > 1:
                duplicates[f"{category}:{normalized_name}"] = matches
    return duplicates
