"""
Mem0 Inspired Memory Evolution Engine for Collective Memory v3.0
Dynamic memory evolution with ADD/UPDATE/DELETE/NOOP operations
"""

import json
import logging
import re
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import difflib
from collections import defaultdict
import spacy
from sentence_transformers import SentenceTransformer
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EvolutionAction(Enum):
    """Types of evolution actions."""
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    NOOP = "noop"

class FactType(Enum):
    """Types of facts that can be extracted."""
    PERSONAL_FACT = "personal_fact"
    TECHNICAL_FACT = "technical_fact"
    PREFERENCE = "preference"
    DECISION = "decision"
    ERROR = "error"
    SOLUTION = "solution"
    PATTERN = "pattern"
    INSIGHT = "insight"

@dataclass
class ExtractedFact:
    """Represents a fact extracted from conversation."""
    content: str
    fact_type: FactType
    confidence: float
    importance: float
    context: Dict
    entities: List[str]
    keywords: List[str]
    timestamp: datetime
    source: str
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)

@dataclass
class EvolutionDecision:
    """Represents a decision made by the evolution engine."""
    action: EvolutionAction
    fact: ExtractedFact
    existing_memory_id: Optional[int]
    confidence: float
    reasoning: str
    metadata: Dict

@dataclass
class EvolutionResult:
    """Result of memory evolution process."""
    facts_extracted: List[ExtractedFact]
    decisions_made: List[EvolutionDecision]
    actions_taken: List[Dict]
    statistics: Dict
    processing_time: float

class FactExtractor:
    """Extracts facts from user-AI interactions."""
    
    def __init__(self):
        """Initialize fact extractor."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy English model not found. Using basic extraction.")
            self.nlp = None
        
        # Fact patterns
        self.fact_patterns = {
            FactType.PERSONAL_FACT: [
                r"I am (.*)",
                r"My name is (.*)",
                r"I work (.*)",
                r"I prefer (.*)",
                r"I like (.*)",
                r"I don't like (.*)",
                r"I use (.*)",
                r"I have (.*)"
            ],
            FactType.TECHNICAL_FACT: [
                r"(.*) is a (.*)",
                r"(.*) uses (.*)",
                r"(.*) requires (.*)",
                r"(.*) supports (.*)",
                r"(.*) implements (.*)",
                r"(.*) extends (.*)",
                r"The (.*) does (.*)"
            ],
            FactType.PREFERENCE: [
                r"prefer (.*) over (.*)",
                r"better to use (.*)",
                r"recommend (.*)",
                r"should use (.*)",
                r"avoid (.*)",
                r"don't use (.*)"
            ],
            FactType.DECISION: [
                r"decided to (.*)",
                r"chose (.*)",
                r"selected (.*)",
                r"will use (.*)",
                r"going with (.*)",
                r"opted for (.*)"
            ],
            FactType.ERROR: [
                r"error: (.*)",
                r"exception: (.*)",
                r"failed to (.*)",
                r"bug in (.*)",
                r"issue with (.*)",
                r"problem with (.*)"
            ],
            FactType.SOLUTION: [
                r"solution: (.*)",
                r"fix: (.*)",
                r"resolved by (.*)",
                r"solved with (.*)",
                r"workaround: (.*)",
                r"to fix this (.*)"
            ]
        }
        
        # Importance indicators
        self.importance_indicators = {
            'critical': 0.9,
            'important': 0.8,
            'essential': 0.8,
            'key': 0.7,
            'main': 0.7,
            'primary': 0.7,
            'significant': 0.6,
            'notable': 0.5,
            'minor': 0.3,
            'trivial': 0.2
        }
    
    def extract_facts(self, user_input: str, ai_response: str, context: Dict) -> List[ExtractedFact]:
        """Extract facts from user-AI interaction."""
        facts = []
        
        # Extract from user input
        user_facts = self._extract_from_text(user_input, "user", context)
        facts.extend(user_facts)
        
        # Extract from AI response
        ai_facts = self._extract_from_text(ai_response, "assistant", context)
        facts.extend(ai_facts)
        
        # Post-process facts
        facts = self._post_process_facts(facts)
        
        return facts
    
    def _extract_from_text(self, text: str, source: str, context: Dict) -> List[ExtractedFact]:
        """Extract facts from a single text."""
        facts = []
        
        # Extract using patterns
        for fact_type, patterns in self.fact_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        content = ' '.join(match)
                    else:
                        content = match
                    
                    if len(content.strip()) > 3:  # Ignore very short matches
                        fact = ExtractedFact(
                            content=content.strip(),
                            fact_type=fact_type,
                            confidence=0.7,
                            importance=self._calculate_importance(content, context),
                            context=context,
                            entities=self._extract_entities(content),
                            keywords=self._extract_keywords(content),
                            timestamp=datetime.now(),
                            source=source
                        )
                        facts.append(fact)
        
        # Extract using NLP if available
        if self.nlp:
            nlp_facts = self._extract_using_nlp(text, source, context)
            facts.extend(nlp_facts)
        
        return facts
    
    def _extract_using_nlp(self, text: str, source: str, context: Dict) -> List[ExtractedFact]:
        """Extract facts using NLP."""
        facts = []
        
        try:
            doc = self.nlp(text)
            
            # Extract entities
            for ent in doc.ents:
                if ent.label_ in ['PERSON', 'ORG', 'PRODUCT', 'EVENT']:
                    fact = ExtractedFact(
                        content=f"{ent.text} is a {ent.label_}",
                        fact_type=FactType.TECHNICAL_FACT,
                        confidence=0.6,
                        importance=0.5,
                        context=context,
                        entities=[ent.text],
                        keywords=[ent.text.lower()],
                        timestamp=datetime.now(),
                        source=source
                    )
                    facts.append(fact)
            
            # Extract noun phrases
            for noun_phrase in doc.noun_chunks:
                if len(noun_phrase.text.split()) > 1:
                    fact = ExtractedFact(
                        content=noun_phrase.text,
                        fact_type=FactType.TECHNICAL_FACT,
                        confidence=0.4,
                        importance=0.3,
                        context=context,
                        entities=[noun_phrase.text],
                        keywords=noun_phrase.text.lower().split(),
                        timestamp=datetime.now(),
                        source=source
                    )
                    facts.append(fact)
        
        except Exception as e:
            logger.debug(f"NLP extraction error: {e}")
        
        return facts
    
    def _calculate_importance(self, content: str, context: Dict) -> float:
        """Calculate importance score for a fact."""
        importance = 0.5  # Base importance
        
        # Check for importance indicators
        for indicator, weight in self.importance_indicators.items():
            if indicator in content.lower():
                importance = max(importance, weight)
        
        # Context-based importance
        if context.get('cursor_session_id'):
            importance += 0.1
        
        if context.get('project_path'):
            importance += 0.1
        
        # Content-based importance
        if len(content) > 50:
            importance += 0.1
        
        if any(char in content for char in ['(', ')', '[', ']', '{', '}']):
            importance += 0.05  # Code-like content
        
        return min(1.0, importance)
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract entities from text."""
        entities = []
        
        # Extract file paths
        file_patterns = [
            r'[a-zA-Z]:[\\/][\w\\/.-]+\.\w+',
            r'[/~][\w/.-]+\.\w+',
            r'[\w.-]+\.py|[\w.-]+\.js|[\w.-]+\.html'
        ]
        
        for pattern in file_patterns:
            matches = re.findall(pattern, text)
            entities.extend(matches)
        
        # Extract function names
        function_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\('
        functions = re.findall(function_pattern, text)
        entities.extend([f[:-1] for f in functions])
        
        return list(set(entities))
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'this', 'that', 'these', 'those', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do',
            'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return list(set(keywords))
    
    def _post_process_facts(self, facts: List[ExtractedFact]) -> List[ExtractedFact]:
        """Post-process extracted facts."""
        # Remove duplicates
        seen = set()
        unique_facts = []
        
        for fact in facts:
            fact_hash = hashlib.md5(fact.content.encode()).hexdigest()
            if fact_hash not in seen:
                seen.add(fact_hash)
                unique_facts.append(fact)
        
        # Sort by importance
        unique_facts.sort(key=lambda x: x.importance, reverse=True)
        
        return unique_facts

class EvolutionDecisionMaker:
    """Makes decisions about how to evolve memory based on extracted facts."""
    
    def __init__(self, memory_database=None):
        """Initialize decision maker."""
        self.memory_database = memory_database
        self.similarity_threshold = 0.7
        self.update_threshold = 0.8
        self.delete_threshold = 0.9
        
        # Initialize sentence transformer for semantic similarity
        try:
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            logger.warning(f"Could not load sentence transformer: {e}")
            self.sentence_model = None
    
    def make_decisions(self, facts: List[ExtractedFact]) -> List[EvolutionDecision]:
        """Make evolution decisions for extracted facts."""
        decisions = []
        
        for fact in facts:
            decision = self._make_decision_for_fact(fact)
            decisions.append(decision)
        
        return decisions
    
    def _make_decision_for_fact(self, fact: ExtractedFact) -> EvolutionDecision:
        """Make evolution decision for a single fact."""
        
        # Find similar existing memories
        similar_memories = self._find_similar_memories(fact)
        
        if not similar_memories:
            # No similar memory found, add new one
            return EvolutionDecision(
                action=EvolutionAction.ADD,
                fact=fact,
                existing_memory_id=None,
                confidence=0.8,
                reasoning="No similar memory found, adding new fact",
                metadata={}
            )
        
        # Check the most similar memory
        most_similar = similar_memories[0]
        similarity = most_similar['similarity']
        
        if similarity >= self.delete_threshold:
            # Very similar, check if it contradicts
            if self._is_contradictory(fact, most_similar):
                return EvolutionDecision(
                    action=EvolutionAction.DELETE,
                    fact=fact,
                    existing_memory_id=most_similar['id'],
                    confidence=0.9,
                    reasoning="Contradictory information found, deleting old memory",
                    metadata={'replaced_by': fact.content}
                )
        
        if similarity >= self.update_threshold:
            # Similar enough to update
            if self._should_update(fact, most_similar):
                return EvolutionDecision(
                    action=EvolutionAction.UPDATE,
                    fact=fact,
                    existing_memory_id=most_similar['id'],
                    confidence=0.8,
                    reasoning="Similar memory found with new information, updating",
                    metadata={'previous_content': most_similar['content']}
                )
        
        if similarity >= self.similarity_threshold:
            # Similar but not enough to update
            return EvolutionDecision(
                action=EvolutionAction.NOOP,
                fact=fact,
                existing_memory_id=most_similar['id'],
                confidence=0.7,
                reasoning="Similar memory exists, no action needed",
                metadata={}
            )
        
        # Not similar enough, add new memory
        return EvolutionDecision(
            action=EvolutionAction.ADD,
            fact=fact,
            existing_memory_id=None,
            confidence=0.8,
            reasoning="Sufficiently different from existing memories, adding new fact",
            metadata={}
        )
    
    def _find_similar_memories(self, fact: ExtractedFact) -> List[Dict]:
        """Find similar memories in the database."""
        if not self.memory_database:
            return []
        
        try:
            # Get memories from database
            memories = self.memory_database.retrieve_memories(
                query=fact.content[:50],  # Use first 50 chars for search
                memory_type=fact.fact_type.value,
                limit=10
            )
            
            # Calculate similarity with each memory
            similar_memories = []
            for memory in memories:
                similarity = self._calculate_similarity(fact.content, memory['content'])
                if similarity > 0.3:  # Minimum similarity threshold
                    similar_memories.append({
                        'id': memory['id'],
                        'content': memory['content'],
                        'similarity': similarity,
                        'memory': memory
                    })
            
            # Sort by similarity
            similar_memories.sort(key=lambda x: x['similarity'], reverse=True)
            
            return similar_memories
        
        except Exception as e:
            logger.error(f"Error finding similar memories: {e}")
            return []
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts."""
        
        # Use sentence transformer if available
        if self.sentence_model:
            try:
                embeddings = self.sentence_model.encode([text1, text2])
                similarity = np.dot(embeddings[0], embeddings[1]) / (
                    np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
                )
                return float(similarity)
            except Exception as e:
                logger.debug(f"Sentence transformer error: {e}")
        
        # Fallback to simple similarity
        return self._simple_similarity(text1, text2)
    
    def _simple_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple word-based similarity."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def _is_contradictory(self, fact: ExtractedFact, similar_memory: Dict) -> bool:
        """Check if fact contradicts existing memory."""
        
        fact_content = fact.content.lower()
        memory_content = similar_memory['content'].lower()
        
        # Check for explicit contradictions
        contradiction_indicators = [
            ('not', 'is'), ('no', 'yes'), ('never', 'always'),
            ('wrong', 'right'), ('false', 'true'), ('bad', 'good'),
            ('avoid', 'use'), ('don\'t', 'do')
        ]
        
        for neg, pos in contradiction_indicators:
            if (neg in fact_content and pos in memory_content) or \
               (pos in fact_content and neg in memory_content):
                return True
        
        return False
    
    def _should_update(self, fact: ExtractedFact, similar_memory: Dict) -> bool:
        """Check if memory should be updated with new fact."""
        
        # Update if new fact has higher importance
        if fact.importance > similar_memory['memory'].get('importance_score', 0.5):
            return True
        
        # Update if new fact has more detail
        if len(fact.content) > len(similar_memory['content']) * 1.5:
            return True
        
        # Update if new fact is more recent and has sufficient confidence
        if fact.confidence > 0.7:
            return True
        
        return False

class Mem0EvolutionEngine:
    """Main Mem0-inspired evolution engine."""
    
    def __init__(self, memory_database=None):
        """Initialize evolution engine."""
        self.memory_database = memory_database
        self.fact_extractor = FactExtractor()
        self.decision_maker = EvolutionDecisionMaker(memory_database)
        
        # Statistics
        self.stats = {
            'total_interactions': 0,
            'facts_extracted': 0,
            'actions_add': 0,
            'actions_update': 0,
            'actions_delete': 0,
            'actions_noop': 0,
            'avg_facts_per_interaction': 0.0,
            'avg_processing_time': 0.0
        }
    
    def process_interaction(self, user_input: str, ai_response: str, 
                          context: Dict, cursor_session_id: str = None) -> EvolutionResult:
        """Process a user-AI interaction and evolve memory."""
        
        start_time = datetime.now()
        
        # Add session info to context
        if cursor_session_id:
            context['cursor_session_id'] = cursor_session_id
        
        # Extract facts from interaction
        facts = self.fact_extractor.extract_facts(user_input, ai_response, context)
        
        # Make evolution decisions
        decisions = self.decision_maker.make_decisions(facts)
        
        # Execute decisions
        actions_taken = self._execute_decisions(decisions)
        
        # Update statistics
        processing_time = (datetime.now() - start_time).total_seconds()
        self._update_statistics(facts, actions_taken, processing_time)
        
        # Create result
        result = EvolutionResult(
            facts_extracted=facts,
            decisions_made=decisions,
            actions_taken=actions_taken,
            statistics=self.stats.copy(),
            processing_time=processing_time
        )
        
        logger.info(f"Processed interaction: {len(facts)} facts, {len(actions_taken)} actions ({processing_time:.3f}s)")
        
        return result
    
    def _execute_decisions(self, decisions: List[EvolutionDecision]) -> List[Dict]:
        """Execute evolution decisions."""
        actions_taken = []
        
        for decision in decisions:
            action_result = self._execute_single_decision(decision)
            if action_result:
                actions_taken.append(action_result)
        
        return actions_taken
    
    def _execute_single_decision(self, decision: EvolutionDecision) -> Optional[Dict]:
        """Execute a single evolution decision."""
        
        if not self.memory_database:
            return None
        
        try:
            if decision.action == EvolutionAction.ADD:
                # Add new memory
                memory_id = self.memory_database.store_memory(
                    content=decision.fact.content,
                    memory_type=decision.fact.fact_type.value,
                    importance_score=decision.fact.importance,
                    context=json.dumps(decision.fact.context),
                    cursor_session_id=decision.fact.context.get('cursor_session_id'),
                    metadata={
                        'source': decision.fact.source,
                        'confidence': decision.fact.confidence,
                        'entities': decision.fact.entities,
                        'keywords': decision.fact.keywords
                    }
                )
                
                return {
                    'action': 'ADD',
                    'memory_id': memory_id,
                    'content': decision.fact.content,
                    'confidence': decision.confidence,
                    'reasoning': decision.reasoning
                }
            
            elif decision.action == EvolutionAction.UPDATE:
                # Update existing memory
                success = self.memory_database.update_memory(
                    memory_id=decision.existing_memory_id,
                    content=decision.fact.content,
                    importance_score=decision.fact.importance,
                    evolution_reason=decision.reasoning
                )
                
                if success:
                    return {
                        'action': 'UPDATE',
                        'memory_id': decision.existing_memory_id,
                        'new_content': decision.fact.content,
                        'confidence': decision.confidence,
                        'reasoning': decision.reasoning
                    }
            
            elif decision.action == EvolutionAction.DELETE:
                # Delete existing memory
                success = self.memory_database.delete_memory(
                    memory_id=decision.existing_memory_id,
                    soft_delete=True
                )
                
                if success:
                    return {
                        'action': 'DELETE',
                        'memory_id': decision.existing_memory_id,
                        'reason': decision.reasoning,
                        'confidence': decision.confidence
                    }
            
            elif decision.action == EvolutionAction.NOOP:
                # No operation
                return {
                    'action': 'NOOP',
                    'memory_id': decision.existing_memory_id,
                    'reasoning': decision.reasoning,
                    'confidence': decision.confidence
                }
        
        except Exception as e:
            logger.error(f"Error executing decision {decision.action}: {e}")
            return None
    
    def _update_statistics(self, facts: List[ExtractedFact], 
                          actions: List[Dict], processing_time: float):
        """Update engine statistics."""
        
        self.stats['total_interactions'] += 1
        self.stats['facts_extracted'] += len(facts)
        
        # Count actions
        for action in actions:
            action_type = action['action'].lower()
            if action_type in ['add', 'update', 'delete', 'noop']:
                self.stats[f'actions_{action_type}'] += 1
        
        # Update averages
        total_interactions = self.stats['total_interactions']
        self.stats['avg_facts_per_interaction'] = (
            self.stats['facts_extracted'] / total_interactions
        )
        
        # Update processing time average
        current_avg = self.stats['avg_processing_time']
        self.stats['avg_processing_time'] = (
            (current_avg * (total_interactions - 1) + processing_time) / total_interactions
        )
    
    def get_statistics(self) -> Dict:
        """Get evolution engine statistics."""
        return self.stats.copy()
    
    def export_memory_evolution_log(self, output_file: str):
        """Export memory evolution log to file."""
        try:
            with open(output_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
            logger.info(f"Memory evolution log exported to {output_file}")
        except Exception as e:
            logger.error(f"Error exporting evolution log: {e}")

# Example usage
if __name__ == "__main__":
    # Create evolution engine
    engine = Mem0EvolutionEngine()
    
    # Test interaction
    user_input = "I decided to use React for the frontend because it has better performance than Vue."
    ai_response = "That's a good choice! React has excellent performance optimizations and a large ecosystem."
    context = {
        'project_path': '/home/user/myproject',
        'conversation_topic': 'frontend framework selection'
    }
    
    # Process interaction
    result = engine.process_interaction(user_input, ai_response, context)
    
    print(f"Facts extracted: {len(result.facts_extracted)}")
    for fact in result.facts_extracted:
        print(f"  - {fact.content} (type: {fact.fact_type.value}, importance: {fact.importance:.3f})")
    
    print(f"\nActions taken: {len(result.actions_taken)}")
    for action in result.actions_taken:
        print(f"  - {action['action']}: {action.get('reasoning', 'N/A')}")
    
    print(f"\nProcessing time: {result.processing_time:.3f}s")
    
    # Get statistics
    stats = engine.get_statistics()
    print(f"\nEngine statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}") 