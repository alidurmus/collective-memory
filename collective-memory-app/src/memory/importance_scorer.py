"""
Importance Scoring System for Collective Memory v3.0
A-Mem + Mem0 inspired memory importance calculation
"""

import re
import math
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """Memory types with base importance scores."""

    FACT = 0.5
    PATTERN = 0.6
    PREFERENCE = 0.4
    CODE = 0.7
    DECISION = 0.9
    ERROR = 0.8
    SOLUTION = 0.9
    INSIGHT = 0.8
    RELATIONSHIP = 0.6


class ContentCategory(Enum):
    """Content categories for scoring."""

    TECHNICAL = 1.0
    BUSINESS = 0.8
    PERSONAL = 0.6
    GENERAL = 0.4


@dataclass
class ScoringFactors:
    """Factors that influence importance scoring."""

    recency: float = 0.0
    frequency: float = 0.0
    context_relevance: float = 0.0
    content_quality: float = 0.0
    user_interaction: float = 0.0
    code_complexity: float = 0.0
    error_criticality: float = 0.0
    decision_impact: float = 0.0


class ImportanceScorer:
    """
    Advanced importance scoring system for memories

    Scoring factors:
    1. Content intrinsic value (type, quality, complexity)
    2. Temporal factors (recency, frequency)
    3. Context relevance (project, session)
    4. User interaction patterns
    5. Network effects (connections to other memories)
    """

    def __init__(self):
        self.weights = {
            "base_type": 0.2,
            "content_quality": 0.15,
            "recency": 0.15,
            "frequency": 0.1,
            "context_relevance": 0.15,
            "user_interaction": 0.1,
            "code_complexity": 0.1,
            "network_centrality": 0.05,
        }

        # Keywords that increase importance
        self.important_keywords = {
            "critical": 0.3,
            "important": 0.2,
            "urgent": 0.25,
            "bug": 0.2,
            "error": 0.15,
            "fix": 0.15,
            "solution": 0.2,
            "decided": 0.25,
            "chosen": 0.2,
            "will use": 0.2,
            "architecture": 0.15,
            "design": 0.1,
            "pattern": 0.1,
            "best practice": 0.15,
            "performance": 0.1,
            "security": 0.2,
            "optimization": 0.1,
        }

        # Code complexity indicators
        self.complexity_indicators = {
            "class": 0.1,
            "function": 0.05,
            "import": 0.02,
            "if": 0.01,
            "for": 0.02,
            "while": 0.02,
            "try": 0.03,
            "except": 0.03,
            "async": 0.05,
            "await": 0.05,
            "lambda": 0.03,
            "decorator": 0.04,
        }

    def calculate_importance(
        self, content: str, memory_type: str, context: str = None, metadata: Dict = None
    ) -> float:
        """Calculate importance score for a memory."""

        factors = ScoringFactors()

        # 1. Base type score
        base_score = self._get_base_type_score(memory_type)

        # 2. Content quality score
        factors.content_quality = self._calculate_content_quality(content)

        # 3. Context relevance score
        factors.context_relevance = self._calculate_context_relevance(content, context)

        # 4. Recency score (if metadata available)
        if metadata and "created_at" in metadata:
            factors.recency = self._calculate_recency_score(metadata["created_at"])

        # 5. Frequency score (if metadata available)
        if metadata and "access_count" in metadata:
            factors.frequency = self._calculate_frequency_score(
                metadata["access_count"]
            )

        # 6. User interaction score
        factors.user_interaction = self._calculate_user_interaction_score(
            content, metadata
        )

        # 7. Code complexity score (if it's code)
        if memory_type == "code":
            factors.code_complexity = self._calculate_code_complexity(content)

        # 8. Error criticality score (if it's an error)
        if memory_type == "error":
            factors.error_criticality = self._calculate_error_criticality(content)

        # 9. Decision impact score (if it's a decision)
        if memory_type == "decision":
            factors.decision_impact = self._calculate_decision_impact(content)

        # Calculate weighted final score
        final_score = (
            base_score * self.weights["base_type"]
            + factors.content_quality * self.weights["content_quality"]
            + factors.recency * self.weights["recency"]
            + factors.frequency * self.weights["frequency"]
            + factors.context_relevance * self.weights["context_relevance"]
            + factors.user_interaction * self.weights["user_interaction"]
            + factors.code_complexity * self.weights["code_complexity"]
        )

        # Apply keyword bonuses
        keyword_bonus = self._calculate_keyword_bonus(content)
        final_score += keyword_bonus

        # Normalize to 0-1 range
        final_score = max(0.0, min(1.0, final_score))

        logger.debug(
            f"Importance score calculated: {final_score:.3f} for type: {memory_type}"
        )
        return final_score

    def _get_base_type_score(self, memory_type: str) -> float:
        """Get base importance score for memory type."""
        try:
            return MemoryType[memory_type.upper()].value
        except KeyError:
            return MemoryType.FACT.value

    def _calculate_content_quality(self, content: str) -> float:
        """Calculate content quality score."""
        if not content:
            return 0.0

        quality_score = 0.0

        # Length factor (not too short, not too long)
        length = len(content)
        if length < 10:
            quality_score += 0.0
        elif length < 50:
            quality_score += 0.3
        elif length < 200:
            quality_score += 0.6
        elif length < 500:
            quality_score += 0.8
        elif length < 1000:
            quality_score += 0.9
        else:
            quality_score += 0.7  # Very long content might be less focused

        # Structure indicators
        if "\n" in content:
            quality_score += 0.1  # Multi-line content

        if "```" in content:
            quality_score += 0.2  # Code blocks

        if re.search(r"\d+\.|\*|\-", content):
            quality_score += 0.1  # Lists or numbered items

        # Technical depth indicators
        technical_patterns = [
            r"[a-zA-Z_][a-zA-Z0-9_]*\([^)]*\)",  # Function calls
            r"[a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*",  # Method calls
            r"[A-Z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*",  # CamelCase
            r"[a-z_]+[A-Z][a-zA-Z0-9]*",  # mixedCase
            r"[A-Z_]{2,}",  # CONSTANTS
            r"\/[^\/\s]+\/[gimuy]*",  # Regex
            r"https?:\/\/[^\s]+",  # URLs
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  # Email
        ]

        for pattern in technical_patterns:
            if re.search(pattern, content):
                quality_score += 0.05

        return min(1.0, quality_score)

    def _calculate_context_relevance(self, content: str, context: str) -> float:
        """Calculate context relevance score."""
        if not context:
            return 0.5  # Neutral if no context

        relevance_score = 0.0

        # Keyword overlap between content and context
        content_words = set(re.findall(r"\b\w+\b", content.lower()))
        context_words = set(re.findall(r"\b\w+\b", context.lower()))

        if content_words and context_words:
            overlap = len(content_words & context_words)
            total_unique = len(content_words | context_words)
            relevance_score = overlap / total_unique if total_unique > 0 else 0.0

        # Project-specific relevance
        if any(term in context.lower() for term in ["project", "repo", "codebase"]):
            relevance_score += 0.1

        # Session-specific relevance
        if any(term in context.lower() for term in ["session", "conversation", "chat"]):
            relevance_score += 0.05

        return min(1.0, relevance_score)

    def _calculate_recency_score(self, created_at: str) -> float:
        """Calculate recency score with exponential decay."""
        try:
            if isinstance(created_at, str):
                created_time = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            else:
                created_time = created_at

            # Calculate age in days
            age_days = (datetime.now() - created_time).days

            # Exponential decay: score = e^(-age/30) where 30 is half-life in days
            decay_factor = 30.0
            recency_score = math.exp(-age_days / decay_factor)

            return recency_score

        except Exception as e:
            logger.debug(f"Error calculating recency score: {e}")
            return 0.5

    def _calculate_frequency_score(self, access_count: int) -> float:
        """Calculate frequency score based on access count."""
        if access_count <= 0:
            return 0.0

        # Logarithmic scaling to prevent dominance of very frequent items
        frequency_score = math.log(access_count + 1) / math.log(
            100 + 1
        )  # Normalize to log(100)

        return min(1.0, frequency_score)

    def _calculate_user_interaction_score(self, content: str, metadata: Dict) -> float:
        """Calculate user interaction score."""
        interaction_score = 0.0

        # Question indicators (user seeking help)
        if "?" in content:
            interaction_score += 0.2

        # User commands/requests
        command_patterns = [
            r"\b(create|make|build|add|fix|change|update|remove|delete)\b",
            r"\b(how|what|why|when|where|which)\b",
            r"\b(please|can you|could you|would you)\b",
        ]

        for pattern in command_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                interaction_score += 0.1

        # User feedback indicators
        feedback_patterns = [
            r"\b(good|great|perfect|excellent|thanks|thank you)\b",
            r"\b(wrong|incorrect|not right|doesn\'t work|error)\b",
        ]

        for pattern in feedback_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                interaction_score += 0.05

        # Manual marking by user (if available in metadata)
        if metadata and metadata.get("user_marked_important"):
            interaction_score += 0.3

        return min(1.0, interaction_score)

    def _calculate_code_complexity(self, content: str) -> float:
        """Calculate code complexity score."""
        complexity_score = 0.0

        # Count complexity indicators
        for indicator, weight in self.complexity_indicators.items():
            count = len(re.findall(rf"\b{indicator}\b", content, re.IGNORECASE))
            complexity_score += count * weight

        # Nesting level (approximate)
        nesting_indicators = ["{", "(", "["]
        max_nesting = 0
        current_nesting = 0

        for char in content:
            if char in nesting_indicators:
                current_nesting += 1
                max_nesting = max(max_nesting, current_nesting)
            elif char in ["}", ")", "]"]:
                current_nesting = max(0, current_nesting - 1)

        complexity_score += max_nesting * 0.05

        # Line count
        lines = content.count("\n") + 1
        complexity_score += min(lines / 100, 0.2)  # Cap at 0.2 for line count

        return min(1.0, complexity_score)

    def _calculate_error_criticality(self, content: str) -> float:
        """Calculate error criticality score."""
        criticality_score = 0.0

        # Error severity indicators
        severity_patterns = {
            r"\b(fatal|critical|severe)\b": 0.4,
            r"\b(error|exception|fail)\b": 0.3,
            r"\b(warning|warn)\b": 0.2,
            r"\b(info|debug)\b": 0.1,
        }

        for pattern, weight in severity_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                criticality_score += weight

        # System impact indicators
        impact_patterns = {
            r"\b(crash|hang|freeze|deadlock)\b": 0.3,
            r"\b(memory|leak|overflow|corruption)\b": 0.25,
            r"\b(security|vulnerability|breach)\b": 0.35,
            r"\b(data|loss|corruption)\b": 0.3,
            r"\b(performance|slow|timeout)\b": 0.2,
        }

        for pattern, weight in impact_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                criticality_score += weight

        # Stack trace presence
        if re.search(r"Traceback|Stack trace|at \w+\.\w+", content):
            criticality_score += 0.2

        return min(1.0, criticality_score)

    def _calculate_decision_impact(self, content: str) -> float:
        """Calculate decision impact score."""
        impact_score = 0.0

        # Decision strength indicators
        decision_patterns = {
            r"\b(decided|chosen|selected|will use|adopted)\b": 0.3,
            r"\b(prefer|recommend|suggest)\b": 0.2,
            r"\b(might|could|maybe|perhaps)\b": 0.1,
        }

        for pattern, weight in decision_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                impact_score += weight

        # Scope indicators
        scope_patterns = {
            r"\b(architecture|design|framework|library)\b": 0.3,
            r"\b(project|team|company|organization)\b": 0.25,
            r"\b(feature|module|component)\b": 0.2,
            r"\b(function|method|variable)\b": 0.1,
        }

        for pattern, weight in scope_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                impact_score += weight

        # Timeline indicators
        timeline_patterns = {
            r"\b(permanent|forever|always)\b": 0.3,
            r"\b(long.term|strategic)\b": 0.25,
            r"\b(short.term|temporary|quick)\b": 0.1,
        }

        for pattern, weight in timeline_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                impact_score += weight

        return min(1.0, impact_score)

    def _calculate_keyword_bonus(self, content: str) -> float:
        """Calculate bonus score based on important keywords."""
        bonus_score = 0.0

        for keyword, weight in self.important_keywords.items():
            if keyword in content.lower():
                bonus_score += weight

        # Cap the bonus to prevent over-weighting
        return min(0.2, bonus_score)

    def calculate_network_centrality(
        self, memory_id: int, memory_links: List[Dict]
    ) -> float:
        """Calculate network centrality score based on memory connections."""
        if not memory_links:
            return 0.0

        # Count connections
        connection_count = len(memory_links)

        # Weight by connection strength
        total_strength = sum(link.get("strength", 0.5) for link in memory_links)
        avg_strength = (
            total_strength / connection_count if connection_count > 0 else 0.0
        )

        # Centrality score based on connections and strength
        centrality_score = (
            min(connection_count / 10, 0.5)  # Connection count (max 0.5)
            + avg_strength * 0.5  # Average strength (max 0.5)
        )

        return min(1.0, centrality_score)

    def update_importance_based_on_usage(
        self, current_score: float, access_count: int, time_since_access: int
    ) -> float:
        """Update importance score based on usage patterns."""

        # Boost frequently accessed memories
        frequency_boost = min(0.1, access_count * 0.01)

        # Decay based on time since last access
        if time_since_access > 0:
            decay_factor = math.exp(-time_since_access / 30.0)  # 30-day half-life
            current_score *= decay_factor

        # Apply frequency boost
        new_score = current_score + frequency_boost

        return min(1.0, max(0.0, new_score))

    def batch_score_memories(self, memories: List[Dict]) -> List[Tuple[int, float]]:
        """Calculate importance scores for multiple memories."""
        scored_memories = []

        for memory in memories:
            score = self.calculate_importance(
                content=memory.get("content", ""),
                memory_type=memory.get("memory_type", "fact"),
                context=memory.get("context", ""),
                metadata=memory,
            )

            scored_memories.append((memory["id"], score))

        return scored_memories

    def get_scoring_explanation(
        self, content: str, memory_type: str, context: str = None, metadata: Dict = None
    ) -> Dict:
        """Get detailed explanation of scoring factors."""

        explanation = {
            "base_type_score": self._get_base_type_score(memory_type),
            "content_quality_score": self._calculate_content_quality(content),
            "context_relevance_score": self._calculate_context_relevance(
                content, context
            ),
            "keyword_bonus": self._calculate_keyword_bonus(content),
            "weights": self.weights,
            "final_score": self.calculate_importance(
                content, memory_type, context, metadata
            ),
        }

        if metadata and "created_at" in metadata:
            explanation["recency_score"] = self._calculate_recency_score(
                metadata["created_at"]
            )

        if metadata and "access_count" in metadata:
            explanation["frequency_score"] = self._calculate_frequency_score(
                metadata["access_count"]
            )

        if memory_type == "code":
            explanation["code_complexity_score"] = self._calculate_code_complexity(
                content
            )

        if memory_type == "error":
            explanation["error_criticality_score"] = self._calculate_error_criticality(
                content
            )

        if memory_type == "decision":
            explanation["decision_impact_score"] = self._calculate_decision_impact(
                content
            )

        return explanation


# Example usage and testing
if __name__ == "__main__":
    scorer = ImportanceScorer()

    # Test different memory types
    test_memories = [
        {
            "content": "We decided to use React for the frontend framework because it has better performance.",
            "memory_type": "decision",
            "context": "Frontend architecture discussion",
        },
        {
            "content": "def calculate_importance(self, content, memory_type): return 0.5",
            "memory_type": "code",
            "context": "Memory system implementation",
        },
        {
            "content": 'Error: NoneType object has no attribute "split"',
            "memory_type": "error",
            "context": "String processing bug",
        },
        {
            "content": "The user prefers dark mode themes.",
            "memory_type": "preference",
            "context": "UI preferences",
        },
    ]

    for memory in test_memories:
        score = scorer.calculate_importance(
            memory["content"], memory["memory_type"], memory["context"]
        )
        print(f"Memory: {memory['content'][:50]}...")
        print(f"Type: {memory['memory_type']}")
        print(f"Score: {score:.3f}")
        print("---")

    # Test scoring explanation
    explanation = scorer.get_scoring_explanation(
        "We decided to use React for the frontend framework because it has better performance.",
        "decision",
        "Frontend architecture discussion",
    )

    print("\nScoring Explanation:")
    for key, value in explanation.items():
        print(f"{key}: {value}")
