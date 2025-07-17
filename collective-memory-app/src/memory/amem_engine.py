"""
A-Mem Inspired Memory Engine for Collective Memory v3.0
Dynamic memory creation and automatic linking system
"""

import json
import logging
import threading
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import re
import hashlib
import networkx as nx
from collections import defaultdict, deque
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemoryNodeType(Enum):
    """Types of memory nodes in the A-Mem system."""

    ATOMIC = "atomic"  # Single fact or piece of information
    COMPOSITE = "composite"  # Collection of related atomic memories
    PATTERN = "pattern"  # Recurring patterns or templates
    INSIGHT = "insight"  # High-level understanding or conclusions
    LINK = "link"  # Connection between memories


class LinkType(Enum):
    """Types of links between memories."""

    SEMANTIC = "semantic"  # Semantic similarity
    CAUSAL = "causal"  # Cause-effect relationship
    TEMPORAL = "temporal"  # Time-based relationship
    SPATIAL = "spatial"  # Location-based relationship
    HIERARCHICAL = "hierarchical"  # Parent-child relationship
    CONTRADICTORY = "contradictory"  # Conflicting information
    SUPPORTIVE = "supportive"  # Supporting evidence


@dataclass
class MemoryNode:
    """Represents a memory node in the A-Mem system."""

    id: str
    content: str
    node_type: MemoryNodeType
    importance: float
    created_at: datetime
    last_accessed: datetime
    access_count: int
    tags: Set[str]
    context: Dict
    metadata: Dict

    def __post_init__(self):
        """Post-initialization processing."""
        if isinstance(self.tags, list):
            self.tags = set(self.tags)
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)
        if isinstance(self.last_accessed, str):
            self.last_accessed = datetime.fromisoformat(self.last_accessed)


@dataclass
class MemoryLink:
    """Represents a link between memory nodes."""

    id: str
    source_id: str
    target_id: str
    link_type: LinkType
    strength: float
    confidence: float
    created_at: datetime
    context: Dict
    metadata: Dict


class AMemEngine:
    """
    A-Mem Inspired Memory Engine

    Core concepts from A-Mem:
    1. Notes (memories) as atomic units
    2. Automatic linking based on content analysis
    3. Bidirectional connections
    4. Importance propagation through network
    5. Emergent organization
    """

    def __init__(self, database_manager=None):
        """Initialize A-Mem engine."""
        self.database = database_manager
        self.memory_graph = nx.DiGraph()
        self.memory_nodes = {}
        self.memory_links = {}

        # Linking parameters
        self.linking_threshold = 0.6
        self.max_links_per_memory = 10
        self.link_decay_rate = 0.1

        # Pattern detection
        self.pattern_detector = PatternDetector()
        self.insight_generator = InsightGenerator()

        # Thread safety
        self.lock = threading.RLock()

        # Statistics
        self.stats = {
            "total_memories": 0,
            "total_links": 0,
            "avg_connections": 0.0,
            "patterns_detected": 0,
            "insights_generated": 0,
        }

        logger.info("A-Mem engine initialized")

    def create_memory_node(
        self,
        content: str,
        node_type: MemoryNodeType = MemoryNodeType.ATOMIC,
        importance: float = None,
        tags: Set[str] = None,
        context: Dict = None,
        metadata: Dict = None,
    ) -> MemoryNode:
        """Create a new memory node."""

        with self.lock:
            # Generate unique ID
            node_id = self._generate_memory_id(content)

            # Calculate importance if not provided
            if importance is None:
                importance = self._calculate_node_importance(content, context or {})

            # Create memory node
            node = MemoryNode(
                id=node_id,
                content=content,
                node_type=node_type,
                importance=importance,
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                access_count=1,
                tags=tags or set(),
                context=context or {},
                metadata=metadata or {},
            )

            # Store in memory
            self.memory_nodes[node_id] = node

            # Add to graph
            self.memory_graph.add_node(node_id, **asdict(node))

            # Auto-link to existing memories
            self._auto_link_memory(node)

            # Update statistics
            self.stats["total_memories"] += 1
            self._update_network_stats()

            # Check for patterns
            self._detect_patterns(node)

            # Store in database if available
            if self.database:
                self._store_in_database(node)

            logger.info(
                f"Created memory node: {node_id[:8]}... (importance: {importance:.3f})"
            )
            return node

    def _generate_memory_id(self, content: str) -> str:
        """Generate unique memory ID."""
        timestamp = datetime.now().isoformat()
        combined = f"{content}{timestamp}"
        return hashlib.sha256(combined.encode()).hexdigest()

    def _calculate_node_importance(self, content: str, context: Dict) -> float:
        """Calculate importance score for a memory node."""
        importance = 0.5  # Base importance

        # Content length factor
        length_factor = min(len(content) / 1000, 0.3)
        importance += length_factor

        # Keyword importance
        important_keywords = [
            "critical",
            "important",
            "key",
            "main",
            "core",
            "essential",
        ]
        for keyword in important_keywords:
            if keyword in content.lower():
                importance += 0.1

        # Context importance
        if context.get("project_path"):
            importance += 0.05
        if context.get("cursor_session_id"):
            importance += 0.05

        # Code complexity (if it's code)
        if "```" in content or "def " in content or "class " in content:
            importance += 0.1

        return min(1.0, importance)

    def _auto_link_memory(self, new_node: MemoryNode):
        """Automatically create links to existing memories."""

        # Find candidate memories for linking
        candidates = self._find_linking_candidates(new_node)

        for candidate_id, similarity in candidates:
            if similarity >= self.linking_threshold:
                # Determine link type
                link_type = self._determine_link_type(
                    new_node, self.memory_nodes[candidate_id]
                )

                # Create bidirectional link
                self._create_memory_link(
                    new_node.id,
                    candidate_id,
                    link_type,
                    strength=similarity,
                    confidence=0.8,
                )

    def _find_linking_candidates(self, node: MemoryNode) -> List[Tuple[str, float]]:
        """Find candidates for linking with similarity scores."""
        candidates = []

        # Extract features from the node
        node_features = self._extract_features(node.content)

        # Compare with existing memories
        for existing_id, existing_node in self.memory_nodes.items():
            if existing_id != node.id:
                # Calculate similarity
                similarity = self._calculate_similarity(
                    node_features, existing_node.content
                )

                if similarity > 0.3:  # Minimum similarity threshold
                    candidates.append((existing_id, similarity))

        # Sort by similarity
        candidates.sort(key=lambda x: x[1], reverse=True)

        # Return top candidates
        return candidates[: self.max_links_per_memory]

    def _extract_features(self, content: str) -> Dict:
        """Extract features from content for similarity calculation."""
        features = {
            "words": set(re.findall(r"\b\w+\b", content.lower())),
            "entities": self._extract_entities(content),
            "concepts": self._extract_concepts(content),
            "code_elements": self._extract_code_elements(content),
            "length": len(content),
            "has_code": "```" in content or "def " in content,
            "has_question": "?" in content,
            "has_command": any(
                word in content.lower() for word in ["create", "build", "fix", "update"]
            ),
        }
        return features

    def _extract_entities(self, content: str) -> Set[str]:
        """Extract entities from content."""
        entities = set()

        # File paths
        file_patterns = [
            r"[a-zA-Z]:[\\/][\w\\/.-]+\.\w+",  # Windows paths
            r"[/~][\w/.-]+\.\w+",  # Unix paths
            r"[\w.-]+\.py|[\w.-]+\.js|[\w.-]+\.html",  # Common file extensions
        ]

        for pattern in file_patterns:
            matches = re.findall(pattern, content)
            entities.update(matches)

        # Function names
        function_pattern = r"\b[a-zA-Z_][a-zA-Z0-9_]*\("
        functions = re.findall(function_pattern, content)
        entities.update([f[:-1] for f in functions])  # Remove the '('

        # Class names (CamelCase)
        class_pattern = r"\b[A-Z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*\b"
        classes = re.findall(class_pattern, content)
        entities.update(classes)

        return entities

    def _extract_concepts(self, content: str) -> Set[str]:
        """Extract conceptual terms from content."""
        concepts = set()

        # Technical concepts
        tech_concepts = [
            "algorithm",
            "architecture",
            "design",
            "pattern",
            "framework",
            "library",
            "api",
            "database",
            "server",
            "client",
            "security",
            "performance",
            "optimization",
            "testing",
            "deployment",
        ]

        for concept in tech_concepts:
            if concept in content.lower():
                concepts.add(concept)

        # Programming concepts
        prog_concepts = [
            "function",
            "class",
            "method",
            "variable",
            "constant",
            "loop",
            "condition",
            "exception",
            "inheritance",
            "polymorphism",
        ]

        for concept in prog_concepts:
            if concept in content.lower():
                concepts.add(concept)

        return concepts

    def _extract_code_elements(self, content: str) -> Set[str]:
        """Extract code elements from content."""
        elements = set()

        # Keywords
        keywords = [
            "def",
            "class",
            "import",
            "from",
            "if",
            "else",
            "elif",
            "for",
            "while",
            "try",
            "except",
            "finally",
            "return",
            "yield",
            "async",
            "await",
            "lambda",
        ]

        for keyword in keywords:
            if f" {keyword} " in content or f"{keyword} " in content:
                elements.add(keyword)

        return elements

    def _calculate_similarity(self, features1: Dict, content2: str) -> float:
        """Calculate similarity between two pieces of content."""
        # Extract features from second content
        features2 = self._extract_features(content2)

        # Calculate different types of similarity

        # Word overlap
        words1 = features1["words"]
        words2 = features2["words"]
        word_similarity = (
            len(words1 & words2) / len(words1 | words2) if words1 | words2 else 0
        )

        # Entity overlap
        entities1 = features1["entities"]
        entities2 = features2["entities"]
        entity_similarity = (
            len(entities1 & entities2) / len(entities1 | entities2)
            if entities1 | entities2
            else 0
        )

        # Concept overlap
        concepts1 = features1["concepts"]
        concepts2 = features2["concepts"]
        concept_similarity = (
            len(concepts1 & concepts2) / len(concepts1 | concepts2)
            if concepts1 | concepts2
            else 0
        )

        # Code element overlap
        code1 = features1["code_elements"]
        code2 = features2["code_elements"]
        code_similarity = (
            len(code1 & code2) / len(code1 | code2) if code1 | code2 else 0
        )

        # Structural similarity
        structural_similarity = 0.0
        if features1["has_code"] and features2["has_code"]:
            structural_similarity += 0.2
        if features1["has_question"] and features2["has_question"]:
            structural_similarity += 0.1
        if features1["has_command"] and features2["has_command"]:
            structural_similarity += 0.1

        # Combine similarities with weights
        total_similarity = (
            word_similarity * 0.3
            + entity_similarity * 0.25
            + concept_similarity * 0.25
            + code_similarity * 0.15
            + structural_similarity * 0.05
        )

        return total_similarity

    def _determine_link_type(self, node1: MemoryNode, node2: MemoryNode) -> LinkType:
        """Determine the type of link between two nodes."""

        content1 = node1.content.lower()
        content2 = node2.content.lower()

        # Check for causal relationship
        if any(
            word in content1 for word in ["because", "since", "due to", "caused by"]
        ):
            return LinkType.CAUSAL

        # Check for contradictory relationship
        if any(
            word in content1 for word in ["not", "no", "never", "opposite", "contrary"]
        ):
            return LinkType.CONTRADICTORY

        # Check for supportive relationship
        if any(
            word in content1
            for word in ["also", "additionally", "furthermore", "supports"]
        ):
            return LinkType.SUPPORTIVE

        # Check for hierarchical relationship
        if any(
            word in content1
            for word in ["part of", "component", "includes", "contains"]
        ):
            return LinkType.HIERARCHICAL

        # Check for temporal relationship
        if any(
            word in content1 for word in ["after", "before", "then", "next", "previous"]
        ):
            return LinkType.TEMPORAL

        # Default to semantic
        return LinkType.SEMANTIC

    def _create_memory_link(
        self,
        source_id: str,
        target_id: str,
        link_type: LinkType,
        strength: float,
        confidence: float,
    ) -> MemoryLink:
        """Create a link between two memory nodes."""

        # Generate link ID
        link_id = f"{source_id[:8]}_{target_id[:8]}_{link_type.value}"

        # Create link object
        link = MemoryLink(
            id=link_id,
            source_id=source_id,
            target_id=target_id,
            link_type=link_type,
            strength=strength,
            confidence=confidence,
            created_at=datetime.now(),
            context={},
            metadata={},
        )

        # Store link
        self.memory_links[link_id] = link

        # Add to graph
        self.memory_graph.add_edge(
            source_id,
            target_id,
            link_type=link_type.value,
            strength=strength,
            confidence=confidence,
        )

        # Create reverse link for bidirectional connection
        reverse_link_id = f"{target_id[:8]}_{source_id[:8]}_{link_type.value}_rev"
        reverse_link = MemoryLink(
            id=reverse_link_id,
            source_id=target_id,
            target_id=source_id,
            link_type=link_type,
            strength=strength,
            confidence=confidence,
            created_at=datetime.now(),
            context={},
            metadata={},
        )

        self.memory_links[reverse_link_id] = reverse_link
        self.memory_graph.add_edge(
            target_id,
            source_id,
            link_type=link_type.value,
            strength=strength,
            confidence=confidence,
        )

        # Update statistics
        self.stats["total_links"] += 2  # Bidirectional

        return link

    def _detect_patterns(self, node: MemoryNode):
        """Detect patterns in the memory network."""
        patterns = self.pattern_detector.detect_patterns(node, self.memory_graph)

        for pattern in patterns:
            # Create pattern node
            pattern_node = self.create_memory_node(
                content=pattern["description"],
                node_type=MemoryNodeType.PATTERN,
                importance=pattern["importance"],
                tags={"pattern"},
                context=pattern["context"],
            )

            self.stats["patterns_detected"] += 1

    def _store_in_database(self, node: MemoryNode):
        """Store memory node in database."""
        if self.database:
            try:
                self.database.store_memory(
                    content=node.content,
                    context=json.dumps(node.context),
                    memory_type=node.node_type.value,
                    importance_score=node.importance,
                    metadata=node.metadata,
                )
            except Exception as e:
                logger.error(f"Error storing memory in database: {e}")

    def _update_network_stats(self):
        """Update network statistics."""
        if self.stats["total_memories"] > 0:
            self.stats["avg_connections"] = (
                self.stats["total_links"] / 2
            ) / self.stats["total_memories"]

    def get_memory_network(self, center_node_id: str, depth: int = 2) -> Dict:
        """Get the memory network around a specific node."""

        if center_node_id not in self.memory_nodes:
            return {}

        # Get subgraph
        subgraph_nodes = set([center_node_id])
        current_level = {center_node_id}

        for _ in range(depth):
            next_level = set()
            for node_id in current_level:
                neighbors = set(self.memory_graph.neighbors(node_id))
                next_level.update(neighbors)

            subgraph_nodes.update(next_level)
            current_level = next_level

        # Create subgraph
        subgraph = self.memory_graph.subgraph(subgraph_nodes)

        # Format for output
        network = {"center_node": center_node_id, "nodes": {}, "links": []}

        # Add nodes
        for node_id in subgraph.nodes():
            if node_id in self.memory_nodes:
                node = self.memory_nodes[node_id]
                network["nodes"][node_id] = {
                    "id": node.id,
                    "content": (
                        node.content[:100] + "..."
                        if len(node.content) > 100
                        else node.content
                    ),
                    "type": node.node_type.value,
                    "importance": node.importance,
                    "tags": list(node.tags),
                }

        # Add links
        for edge in subgraph.edges(data=True):
            source, target, data = edge
            network["links"].append(
                {
                    "source": source,
                    "target": target,
                    "type": data.get("link_type", "semantic"),
                    "strength": data.get("strength", 0.5),
                    "confidence": data.get("confidence", 0.5),
                }
            )

        return network

    def search_memories(self, query: str, max_results: int = 10) -> List[MemoryNode]:
        """Search memories using A-Mem network traversal."""

        results = []
        query_features = self._extract_features(query)

        # Calculate similarity with all memories
        similarities = []
        for node_id, node in self.memory_nodes.items():
            similarity = self._calculate_similarity(query_features, node.content)
            similarities.append((node_id, similarity))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Network-based ranking enhancement
        enhanced_results = []
        for node_id, similarity in similarities[: max_results * 2]:
            node = self.memory_nodes[node_id]

            # Calculate network importance
            network_importance = self._calculate_network_importance(node_id)

            # Combined score
            combined_score = similarity * 0.7 + network_importance * 0.3

            enhanced_results.append((node, combined_score))

        # Sort by combined score
        enhanced_results.sort(key=lambda x: x[1], reverse=True)

        # Return top results
        return [result[0] for result in enhanced_results[:max_results]]

    def _calculate_network_importance(self, node_id: str) -> float:
        """Calculate importance based on network position."""
        if node_id not in self.memory_graph:
            return 0.0

        # Degree centrality
        degree = self.memory_graph.degree(node_id)
        degree_centrality = (
            degree / (len(self.memory_graph) - 1) if len(self.memory_graph) > 1 else 0
        )

        # PageRank
        try:
            pagerank = nx.pagerank(self.memory_graph).get(node_id, 0)
        except:
            pagerank = 0

        # Betweenness centrality (for smaller graphs)
        if len(self.memory_graph) < 1000:
            try:
                betweenness = nx.betweenness_centrality(self.memory_graph).get(
                    node_id, 0
                )
            except:
                betweenness = 0
        else:
            betweenness = 0

        # Combine measures
        network_importance = (
            degree_centrality * 0.4 + pagerank * 0.4 + betweenness * 0.2
        )

        return network_importance

    def get_statistics(self) -> Dict:
        """Get engine statistics."""
        return {
            **self.stats,
            "network_density": nx.density(self.memory_graph),
            "connected_components": nx.number_connected_components(
                self.memory_graph.to_undirected()
            ),
            "clustering_coefficient": (
                nx.average_clustering(self.memory_graph.to_undirected())
                if len(self.memory_graph) > 0
                else 0
            ),
        }


class PatternDetector:
    """Detects patterns in memory networks."""

    def detect_patterns(self, node: MemoryNode, graph: nx.DiGraph) -> List[Dict]:
        """Detect patterns involving the given node."""
        patterns = []

        # Detect clustering patterns
        clusters = self._detect_clusters(node, graph)
        patterns.extend(clusters)

        # Detect sequential patterns
        sequences = self._detect_sequences(node, graph)
        patterns.extend(sequences)

        # Detect hierarchical patterns
        hierarchies = self._detect_hierarchies(node, graph)
        patterns.extend(hierarchies)

        return patterns

    def _detect_clusters(self, node: MemoryNode, graph: nx.DiGraph) -> List[Dict]:
        """Detect clustering patterns."""
        # Implementation for cluster detection
        return []

    def _detect_sequences(self, node: MemoryNode, graph: nx.DiGraph) -> List[Dict]:
        """Detect sequential patterns."""
        # Implementation for sequence detection
        return []

    def _detect_hierarchies(self, node: MemoryNode, graph: nx.DiGraph) -> List[Dict]:
        """Detect hierarchical patterns."""
        # Implementation for hierarchy detection
        return []


class InsightGenerator:
    """Generates insights from memory patterns."""

    def generate_insights(self, patterns: List[Dict]) -> List[Dict]:
        """Generate insights from detected patterns."""
        insights = []

        for pattern in patterns:
            # Analyze pattern significance
            insight = self._analyze_pattern_significance(pattern)
            if insight:
                insights.append(insight)

        return insights

    def _analyze_pattern_significance(self, pattern: Dict) -> Optional[Dict]:
        """Analyze the significance of a pattern."""
        # Implementation for insight generation
        return None


# Example usage
if __name__ == "__main__":
    # Create A-Mem engine
    engine = AMemEngine()

    # Create test memories
    memories = [
        "We decided to use React for the frontend framework because it has better performance.",
        "The React components should be functional components with hooks.",
        "useState hook is used for state management in React functional components.",
        "useEffect hook handles side effects in React components.",
        "React Router is used for client-side routing in our application.",
    ]

    # Create memory nodes
    nodes = []
    for content in memories:
        node = engine.create_memory_node(content, tags={"react", "frontend"})
        nodes.append(node)

    # Search memories
    search_results = engine.search_memories("React hooks", max_results=3)

    print(f"Search results for 'React hooks':")
    for i, node in enumerate(search_results, 1):
        print(f"{i}. {node.content[:50]}... (importance: {node.importance:.3f})")

    # Get network around first node
    if nodes:
        network = engine.get_memory_network(nodes[0].id, depth=2)
        print(
            f"\nNetwork around first node: {len(network['nodes'])} nodes, {len(network['links'])} links"
        )

    # Get statistics
    stats = engine.get_statistics()
    print(f"\nEngine statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
