"""
Context Refiner
Refines context while messages transit through the neural bus.

This is where the "en route" optimization happens:
- Relevance filtering
- Token optimization
- Focus mode application
- Compression
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from .neural_message import NeuralMessage, FocusMode

logger = logging.getLogger(__name__)


class RelevanceScorer:
    """
    Scores content relevance against keywords and focus mode.
    Uses both keyword matching and semantic scoring.
    """
    
    def __init__(self):
        # Keyword weights for different focus modes
        self.focus_weights = {
            FocusMode.RELEVANCE: {'keyword_match': 0.6, 'semantic': 0.4},
            FocusMode.EXTRACTION: {'keyword_match': 0.7, 'semantic': 0.3},
            FocusMode.ANALYSIS: {'keyword_match': 0.3, 'semantic': 0.7},
            FocusMode.SUMMARIZATION: {'keyword_match': 0.4, 'semantic': 0.6},
            FocusMode.NAVIGATION: {'keyword_match': 0.8, 'semantic': 0.2},
        }
    
    async def score_relevance(
        self,
        content: str,
        keywords: List[str],
        focus_mode: FocusMode,
        threshold: float = 0.7
    ) -> Dict:
        """
        Score content relevance.
        
        Returns:
            {
                'score': 0.0-1.0,
                'relevant': bool,
                'matching_keywords': [...],
                'reasoning': '...'
            }
        """
        if not content or not keywords:
            return {'score': 0.5, 'relevant': True, 'matching_keywords': [], 'reasoning': 'no content'}
        
        content_lower = content.lower()
        keyword_scores = []
        matched = []
        
        for keyword in keywords:
            if keyword.lower() in content_lower:
                # Count occurrences
                count = content_lower.count(keyword.lower())
                matched.append(keyword)
                # Score based on position and frequency
                position = content_lower.find(keyword.lower())
                position_score = 1.0 - (position / max(len(content), 1))
                frequency_score = min(count / 5, 1.0)  # Cap at 5 mentions
                keyword_scores.append((position_score + frequency_score) / 2)
        
        # Calculate final score
        if keyword_scores:
            avg_score = sum(keyword_scores) / len(keyword_scores)
        else:
            avg_score = 0.0
        
        weights = self.focus_weights.get(focus_mode, {'keyword_match': 0.5, 'semantic': 0.5})
        final_score = avg_score * weights['keyword_match']
        
        return {
            'score': min(final_score, 1.0),
            'relevant': final_score >= threshold,
            'matching_keywords': matched,
            'reasoning': f"Matched {len(matched)}/{len(keywords)} keywords"
        }


class ContextRefiner:
    """
    Refines context while messages transit through processors.
    
    Key features:
    - Relevance filtering based on focus mode
    - Token optimization for LLM efficiency
    - Compression tracking
    - Focus-aware content extraction
    """
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self.relevance_scorer = RelevanceScorer()
        self.refinement_stats = {
            'total_messages': 0,
            'avg_compression': 0.0,
            'avg_relevance': 0.0,
            'filtered_count': 0
        }
    
    async def refine_en_route(
        self,
        message: NeuralMessage,
        processor_id: str
    ) -> NeuralMessage:
        """
        Refine message context as it passes through a processor.
        
        This is the main entry point for en-route refinement.
        """
        self.refinement_stats['total_messages'] += 1
        
        # Track the hop
        message.context.add_hop(processor_id)
        
        # Apply focus mode refinements
        if message.focus and message.focus.mode:
            if message.focus.mode == FocusMode.RELEVANCE:
                await self._apply_relevance_filter(message)
            elif message.focus.mode == FocusMode.EXTRACTION:
                await self._apply_extraction_focus(message)
            elif message.focus.mode == FocusMode.SUMMARIZATION:
                await self._apply_summarization(message)
            elif message.focus.mode == FocusMode.ANALYSIS:
                await self._apply_analysis_focus(message)
        
        # Apply general optimizations
        await self._compress_payload(message)
        await self._remove_duplicates(message)
        await self._prune_metadata(message)
        
        return message
    
    async def _apply_relevance_filter(self, message: NeuralMessage):
        """Filter content based on relevance threshold."""
        payload = message.payload
        
        if 'html' in payload:
            # Score HTML relevance
            keywords = message.focus.keywords if message.focus else []
            threshold = message.focus.relevance_threshold if message.focus else 0.7
            
            score_result = await self.relevance_scorer.score_relevance(
                content=payload['html'],
                keywords=keywords,
                focus_mode=message.focus.mode if message.focus else FocusMode.RELEVANCE,
                threshold=threshold
            )
            
            message.context.relevance_score = score_result['score']
            
            if not score_result['relevant']:
                # Mark for filtering
                message.context.record_refinement(
                    'irrelevant_content',
                    len(payload.get('html', '')),
                    0
                )
                payload['html'] = ''
                payload['_filtered'] = True
                self.refinement_stats['filtered_count'] += 1
            else:
                # Extract only relevant sections
                relevant_html = await self._extract_relevant_sections(
                    payload['html'],
                    score_result['matching_keywords']
                )
                message.context.record_refinement(
                    'relevance_filter',
                    len(payload['html']),
                    len(relevant_html)
                )
                payload['html'] = relevant_html
    
    async def _apply_extraction_focus(self, message: NeuralMessage):
        """Focus on specific entities for extraction."""
        target_entities = message.focus.target_entities if message.focus else []
        
        payload = message.payload
        if 'html' in payload and target_entities:
            # Use small LLM to extract only target entities
            extraction_result = await self._llm_extract_entities(
                html=payload['html'],
                entities=target_entities,
                context=f"Focus: {message.focus.mode.value}"
            )
            
            original_size = len(payload.get('html', ''))
            payload['extracted'] = extraction_result
            payload['html'] = ''  # Remove full HTML
            
            message.context.record_refinement(
                'entity_extraction',
                original_size,
                len(str(extraction_result))
            )
    
    async def _apply_summarization(self, message: NeuralMessage):
        """Condense content based on focus."""
        payload = message.payload
        max_tokens = message.focus.max_tokens if message.focus else 4096
        
        if 'html' in payload:
            # Generate summary
            summary = await self._llm_summarize(
                content=payload['html'],
                max_tokens=max_tokens,
                focus=message.focus.keywords if message.focus else []
            )
            
            original_size = len(payload['html'])
            payload['summary'] = summary
            payload.pop('html', None)
            
            message.context.record_refinement(
                'summarization',
                original_size,
                len(summary)
            )
    
    async def _apply_analysis_focus(self, message: NeuralMessage):
        """Apply deep analysis focus."""
        # For analysis, we keep more context but structure it
        payload = message.payload
        
        if 'html' in payload:
            # Extract structure for analysis
            structure = await self._extract_structure(payload['html'])
            payload['structure'] = structure
            payload.pop('html', None)
            
            message.context.record_refinement(
                'analysis_focus',
                len(payload.get('html', '')),
                len(str(structure))
            )
    
    async def _compress_payload(self, message: NeuralMessage):
        """Apply compression to payload."""
        # Track original size
        original = len(str(message.payload))
        
        # Remove unnecessary whitespace
        if 'html' in message.payload:
            message.payload['html'] = self._remove_whitespace(message.payload['html'])
        
        if original > 0:
            current = len(str(message.payload))
            message.context.compression_ratio = 1.0 - (current / original)
    
    async def _remove_duplicates(self, message: NeuralMessage):
        """Remove duplicate content."""
        payload = message.payload
        
        # Simple deduplication for lists
        for key in ['links', 'emails', 'urls']:
            if key in payload and isinstance(payload[key], list):
                seen = set()
                unique = []
                for item in payload[key]:
                    if item not in seen:
                        seen.add(item)
                        unique.append(item)
                if len(unique) < len(payload[key]):
                    message.context.record_refinement(
                        'deduplication',
                        len(payload[key]),
                        len(unique)
                    )
                    payload[key] = unique
    
    async def _prune_metadata(self, message: NeuralMessage):
        """Remove unnecessary metadata."""
        payload = message.payload
        
        # Remove large metadata fields
        large_fields = ['full_page_source', 'raw_headers', 'debug_info']
        for field in large_fields:
            if field in payload:
                del payload[field]
    
    async def _extract_relevant_sections(
        self,
        html: str,
        keywords: List[str]
    ) -> str:
        """Extract HTML sections containing keywords."""
        if not keywords:
            return html[:10000]  # Truncate if no keywords
        
        # Simple extraction - find keyword occurrences
        relevant_parts = []
        html_lower = html.lower()
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            start = html_lower.find(keyword_lower)
            if start != -1:
                # Extract context around keyword (500 chars before, 500 after)
                context_start = max(0, start - 500)
                context_end = min(len(html), start + len(keyword) + 500)
                relevant_parts.append(html[context_start:context_end])
        
        if relevant_parts:
            return '\n---\n'.join(relevant_parts)
        return html[:10000]
    
    async def _llm_extract_entities(
        self,
        html: str,
        entities: List[str],
        context: str
    ) -> Dict:
        """Use small LLM to extract target entities."""
        # This would call the local LLM
        # For now, return placeholder
        return {
            'entities': {},
            'confidence_scores': {},
            'context_snippets': {}
        }
    
    async def _llm_summarize(
        self,
        content: str,
        max_tokens: int,
        focus: List[str]
    ) -> str:
        """Summarize content using LLM."""
        # Placeholder - would call LLM
        if len(content) > 1000:
            return content[:1000] + "... [summary]"
        return content
    
    async def _extract_structure(self, html: str) -> Dict:
        """Extract HTML structure for analysis."""
        # Placeholder
        return {'headings': [], 'sections': [], 'forms': []}
    
    def _remove_whitespace(self, text: str) -> str:
        """Remove unnecessary whitespace."""
        import re
        # Remove extra whitespace but preserve structure
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def get_refinement_stats(self) -> Dict:
        """Get refinement statistics."""
        return {
            'total_messages': self.refinement_stats['total_messages'],
            'avg_compression_ratio': self.refinement_stats['avg_compression'],
            'avg_relevance_score': self.refinement_stats['avg_relevance'],
            'filtered_count': self.refinement_stats['filtered_count']
        }


if __name__ == "__main__":
    import asyncio
    
    async def demo():
        print("Context Refiner Demo")
        print("=" * 50)
        
        refiner = ContextRefiner()
        
        # Create a test message
        from neural_message import NeuralMessage, FocusMode, MessagePriority
        
        msg = NeuralMessage(
            topic="scrape/request",
            payload={
                'url': 'https://example.com',
                'html': '<html><body><h1>Product Price</h1><p>Price: $99.99</p><div>Other content...</div></body></html>'
            },
            source='test',
            destination='test',
            priority=MessagePriority.HIGH
        )
        msg.focus.mode = FocusMode.EXTRACTION
        msg.focus.target_entities = ['price', 'product']
        msg.focus.keywords = ['price', 'product', 'cost']
        
        print(f"Original HTML length: {len(msg.payload.get('html', ''))}")
        
        # Refine
        refined = await refiner.refine_en_route(msg, "demo_processor")
        
        print(f"Refined payload keys: {list(refined.payload.keys())}")
        print(f"Context hops: {refined.context.hops}")
        print(f"Relevance score: {refined.context.relevance_score}")
    
    asyncio.run(demo())

