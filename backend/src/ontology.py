"""Simple in-memory ontology layer for pivot concepts."""

from __future__ import annotations

from typing import List, Tuple


class Ontology:
    """Stores lightweight triples describing pivot concepts."""

    def __init__(self) -> None:
        self._triples: List[Tuple[str, str, str]] = []

    def add(self, subject: str, predicate: str, obj: str) -> None:
        self._triples.append((subject, predicate, obj))

    def find(
        self,
        subject: str | None = None,
        predicate: str | None = None,
        obj: str | None = None,
    ) -> List[Tuple[str, str, str]]:
        def match(t: Tuple[str, str, str]) -> bool:
            s, p, o = t
            return (
                (subject is None or s == subject)
                and (predicate is None or p == predicate)
                and (obj is None or o == obj)
            )

        return [t for t in self._triples if match(t)]


# Prepopulate base classes
ontology = Ontology()
ontology.add("PivotPoint", "isa", "PivotFamily")
ontology.add("PivotFamily", "isa", "Archetype")
ontology.add("Scale", "related", "Metric")
