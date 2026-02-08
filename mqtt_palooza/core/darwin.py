were"""
Darwin Evolution Engine
The adaptive intelligence layer for Mqtt-Palooza.

Darwin manifests in three forms:
- Darwin-1: Deterministic algorithm for mathematical optimization
- Darwin-2: LLM-based learning and strategy evolution
- Darwin-3: Constitutional enforcement and signature tracking
"""

import asyncio
import hashlib
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import os
import random

logger = logging.getLogger(__name__)

# ============================================================================
# CONSTITUTION INTEGRATION
# ============================================================================

CONSTITUTION_MUST_HAVES = [
    'permeable_ai',       # AI-to-AI must flow
    'fastest_protocol',   # Always optimize
    'dna_carried',        # Knowledge travels
    'refine_en_route'     # Context optimizes transit
]

CONSTITUTION_CANNOT_HAVES = [
    'vendor_lockin',
    'centralized_dead_man_switch',
    'black_box_ai',
    'single_point_of_failure'
]


class ConstitutionalReview:
    """Result of constitutional mutation review"""
    def __init__(
        self, 
        approved: bool, 
        issues: List[str],
        timestamp: float = None,
        darwin_signature: str = None
    ):
        self.approved = approved
        self.issues = issues
        self.timestamp = timestamp or time.time()
        self.darwin_signature = darwin_signature
        self.approval_score = self._calculate_approval_score()
    
    def _calculate_approval_score(self) -> float:
        """Calculate how well mutation aligns with constitution"""
        if not self.approved:
            return 0.0
        
        score = 1.0
        for issue in self.issues:
            if 'Missing required' in issue:
                score -= 0.1
            elif 'Violates constraint' in issue:
                score -= 0.2
            elif 'Violates spirit' in issue:
                score -= 0.15
        
        return max(0.0, score)


class DarwinEvolutionType(Enum):
    """Types of evolutionary changes"""
    DNA_OPTIMIZATION = 1
    CONTEXT_REFINEMENT = 2
    PROTOCOL_SELECTION = 3
    STRATEGY = 4
    ADAPTER = 5
    PROMPT = 6


@dataclass
class DarwinMutation:
    """
    A single evolutionary mutation in the system.
    All mutations carry Darwin signatures for traceability.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    evolution_type: DarwinEvolutionType = DarwinEvolutionType.DNA_OPTIMIZATION
    component: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    parent_mutations: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    darwin_signature: str = ""
    constitution_review: ConstitutionalReview = None
    success_metrics: Dict = field(default_factory=dict)
    applied: bool = False
    
    def create_signature(self, component: str) -> str:
        """Create Darwin signature for traceability"""
        lineage = self.parent_mutations + [self.timestamp]
        lineage_str = "|".join(str(x) for x in lineage)
        secret = os.getenv(f"DARWIN_SECRET_{component.upper()}", "default")
        
        proof = hashlib.blake2b(
            f"{lineage_str}{secret}".encode(),
            digest_size=16
        ).hexdigest()
        
        self.darwin_signature = f"DARWIN-{component.upper()}-{proof}"
        return self.darwin_signature


@dataclass
class EvolutionMetrics:
    """Track evolutionary success"""
    mutation_count: int = 0
    successful_mutations: int = 0
    failed_mutations: int = 0
    avg_improvement: float = 0.0
    avg_latency_reduction: float = 0.0
    avg_relevance_improvement: float = 0.0
    
    def record_success(self, mutation: DarwinMutation):
        self.mutation_count += 1
        self.successful_mutations += 1
        if mutation.success_metrics:
            improvement = mutation.success_metrics.get('improvement', 0)
            self.avg_improvement = (
                (self.avg_improvement * (self.successful_mutations - 1) + improvement)
                / self.successful_mutations
            )
    
    def record_failure(self, mutation: DarwinMutation):
        self.mutation_count += 1
        self.failed_mutations += 1


# ============================================================================
# DARWIN-1: THE ALGORITHM (Deterministic Evolution)
# ============================================================================

@dataclass
class Darwin1Config:
    """Configuration for Darwin-1 algorithm"""
    population_size: int = 20
    mutation_rate: float = 0.15
    crossover_rate: float = 0.3
    elite_count: int = 4
    generations: int = 10
    survival_threshold: float = 0.7
    improvement_threshold: float = 0.05


class Darwin1Algorithm:
    """
    Darwin-1: Deterministic algorithm for mathematical optimization.
    """
    
    def __init__(self, config: Darwin1Config = None):
        self.config = config or Darwin1Config()
        self.metrics = EvolutionMetrics()
    
    def evaluate_mutation(self, mutation: Dict) -> float:
        """Score a mutation based on constitutional compliance and improvement."""
        score = 0.0
        
        # Speed contribution (30%)
        latency_improvement = mutation.get('latency_improvement', 0)
        score += (1.0 - latency_improvement) * 0.30
        
        # Relevance contribution (40%)
        relevance_improvement = mutation.get('relevance_improvement', 0)
        score += relevance_improvement * 0.40
        
        # Efficiency contribution (20%)
        efficiency_improvement = mutation.get('efficiency_improvement', 0)
        score += efficiency_improvement * 0.20
        
        # Constitutional compliance (10%)
        compliance = self._check_constitution(mutation)
        score += compliance * 0.10
        
        return score
    
    def _check_constitution(self, mutation: Dict) -> float:
        """Check constitutional compliance"""
        score = 1.0
        
        for required in CONSTITUTION_MUST_HAVES:
            if required not in mutation:
                score -= 0.05
        
        for forbidden in CONSTITUTION_CANNOT_HAVES:
            if forbidden in mutation:
                score = 0.0
                break
        
        return max(0.0, score)
    
    def create_mutation(self, parent: Dict) -> Dict:
        """Create a mutation from a parent solution"""
        mutation = parent.copy()
        
        for key in list(mutation.keys()):
            if isinstance(mutation[key], (int, float)) and random.random() < self.config.mutation_rate:
                if isinstance(mutation[key], int):
                    mutation[key] += random.randint(-5, 5)
                else:
                    mutation[key] *= random.uniform(0.8, 1.2)
        
        mutation['mutation_timestamp'] = time.time()
        mutation['parent_hash'] = self._hash_solution(parent)
        
        return mutation
    
    def _hash_solution(self, solution: Dict) -> str:
        """Create hash of solution for tracking"""
        serialized = json.dumps(solution, sort_keys=True)
        return hashlib.blake2b(serialized.encode(), digest_size=8).hexdigest()
    
    def evolve(self, population: List[Dict]) -> List[Dict]:
        """Run evolutionary algorithm on population."""
        if len(population) < 2:
            return population
        
        evaluated = [(self.evaluate_mutation(s), s) for s in population]
        evaluated.sort(key=lambda x: x[0], reverse=True)
        
        survivor_count = max(2, int(len(evaluated) * self.config.survival_threshold))
        survivors = [s for _, s in evaluated[:survivor_count]]
        elites = [s for _, s in evaluated[:self.config.elite_count]]
        
        next_gen = elites.copy()
        
        while len(next_gen) < self.config.population_size:
            if random.random() < self.config.crossover_rate:
                child = self._crossover(
                    random.choice(survivors),
                    random.choice(survivors)
                )
                next_gen.append(child)
            else:
                child = self.create_mutation(random.choice(survivors))
                next_gen.append(child)
        
        self.metrics.mutation_count += len(next_gen)
        best_score = evaluated[0][0]
        if best_score > 0.5:
            self.metrics.successful_mutations += 1
        
        return next_gen
    
    def _crossover(self, parent1: Dict, parent2: Dict) -> Dict:
        """Create child from two parents"""
        child = {}
        keys1 = list(parent1.keys())
        keys2 = list(parent2.keys())
        split = len(keys1) // 2
        
        for key in keys1[:split]:
            child[key] = parent1[key]
        for key in keys2[split:]:
            child[key] = parent2[key]
        
        child['crossover'] = True
        child['parents'] = [
            self._hash_solution(parent1)[:8],
            self._hash_solution(parent2)[:8]
        ]
        
        return child
    
    async def run_evolution(
        self, 
        initial_population: List[Dict],
        objective_function,
        max_generations: int = None
    ) -> Dict:
        """Run complete evolutionary process."""
        max_generations = max_generations or self.config.generations
        population = initial_population.copy()
        
        history = []
        best_solution = None
        best_fitness = -float('inf')
        
        for gen in range(max_generations):
            evaluated = [(objective_function(s), s) for s in population]
            evaluated.sort(key=lambda x: x[0], reverse=True)
            
            current_best_fitness, current_best = evaluated[0]
            
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_solution = current_best
            
            history.append({
                'generation': gen,
                'best_fitness': current_best_fitness,
                'avg_fitness': sum(f for f, _ in evaluated) / len(evaluated),
                'best_solution_hash': self._hash_solution(current_best)[:8]
            })
            
            population = self.evolve(population)
            
            logger.info(f"Generation {gen}: Best fitness = {current_best_fitness:.4f}")
        
        return {
            'best_solution': best_solution,
            'best_fitness': best_fitness,
            'history': history,
            'total_generations': max_generations,
            'final_population_size': len(population)
        }


# ============================================================================
# DARWIN-2: THE LLM (Adaptive Learning)
# ============================================================================

class DarwinLLMConfig:
    """Configuration for Darwin-2 LLM evolution"""
    def __init__(
        self,
        model: str = "llama3.1:8b",
        evolution_interval: int = 300,
        min_samples_for_evolution: int = 10,
        confidence_threshold: float = 0.8
    ):
        self.model = model
        self.evolution_interval = evolution_interval
        self.min_samples_for_evolution = min_samples_for_evolution
        self.confidence_threshold = confidence_threshold


class DarwinLLM:
    """
    Darwin-2: LLM-based adaptive learning and strategy evolution.
    """
    
    def __init__(self, config: DarwinLLMConfig = None, ollama_url: str = "http://localhost:11434"):
        self.config = config or DarwinLLMConfig()
        self.ollama_url = ollama_url
        self.evolution_history: List[Dict] = []
        self.strategy_performance: Dict[str, Dict] = {}
        self.prompt_templates: Dict[str, str] = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load default prompt templates"""
        self.prompt_templates = {
            'extraction': """You are an expert data extractor.
Your task: Extract {target_entities} from the following content.

Focus: {focus_mode}
Relevance threshold: {relevance_threshold}

Content:
{content}

Return ONLY the extracted entities in JSON format:
{{
    "entities": {{entity_name: value}},
    "confidence_scores": {{entity_name: 0.0-1.0}},
    "context_snippets": {{entity_name: relevant_text}}
}}""",

            'relevance': """You are a relevance filter.
Your task: Determine if content is relevant to: {keywords}

Content:
{content}

Return JSON:
{{
    "relevant": true/false,
    "relevance_score": 0.0-1.0,
    "matching_passages": ["relevant text"],
    "reasoning": "explanation"
}}""",

            'summarization': """You are a content summarizer.
Your task: Summarize the following content.

Focus areas: {keywords}
Max tokens: {max_tokens}

Content:
{content}

Return JSON:
{{
    "summary": "concise summary",
    "key_points": ["point 1", "point 2"],
    "omitted_sections": ["what was removed"],
    "confidence": 0.0-1.0
}}""",

            'analysis': """You are a strategic analyst.
Your task: Analyze this data extraction scenario.

Scenario: {scenario}
Historical success rate: {success_rate}

Results to analyze:
{results}

Provide analysis and recommendations:
{{
    "patterns_detected": ["pattern 1", "pattern 2"],
    "success_factors": ["what works"],
    "failure_factors": ["what doesn't work"],
    "recommendations": ["suggested improvements"],
    "confidence": 0.0-1.0
}}"""
        }
    
    async def evolve_strategy(
        self,
        task_type: str,
        successes: List[Dict],
        failures: List[Dict]
    ) -> Dict:
        """Evolve strategy based on outcomes."""
        total_samples = len(successes) + len(failures)
        if total_samples < self.config.min_samples_for_evolution:
            return {'status': 'insufficient_data'}
        
        success_patterns = self._analyze_patterns(successes, is_success=True)
        failure_patterns = self._analyze_patterns(failures, is_success=False)
        
        evolution_prompt = self._create_evolution_prompt(
            task_type, success_patterns, failure_patterns
        )
        
        response = await self._call_llm(evolution_prompt)
        evolved = self._parse_evolution(response)
        
        review = self._review_constitution(evolved)
        if not review.approved:
            evolved = self._patch_for_constitution(evolved, review)
        
        evolved['timestamp'] = time.time()
        evolved['task_type'] = task_type
        evolved['sample_count'] = total_samples
        self.evolution_history.append(evolved)
        
        return evolved
    
    def _analyze_patterns(self, outcomes: List[Dict], is_success: bool) -> Dict:
        """Analyze patterns in outcomes"""
        patterns = {
            'avg_tokens_used': 0,
            'common_params': {},
            'success_rate': 1.0 if is_success else 0.0,
            'outcome_count': len(outcomes)
        }
        
        if not outcomes:
            return patterns
        
        total_tokens = sum(o.get('tokens_used', 0) for o in outcomes)
        patterns['avg_tokens_used'] = total_tokens / len(outcomes)
        
        all_params = []
        for o in outcomes:
            params = o.get('params', {})
            all_params.append(params)
        
        if all_params:
            for key in all_params[0].keys():
                values = [p.get(key) for p in all_params if key in p]
                if len(set(values)) == 1:
                    patterns['common_params'][key] = values[0]
        
        return patterns
    
    def _create_evolution_prompt(
        self,
        task_type: str,
        success_patterns: Dict,
        failure_patterns: Dict
    ) -> str:
        """Create prompt for LLM evolution"""
        return f"""
        Analyze these outcomes and propose strategy evolution:
        
        TASK TYPE: {task_type}
        
        SUCCESS PATTERNS ({success_patterns['outcome_count']} samples):
        - Avg tokens: {success_patterns['avg_tokens_used']:.0f}
        - Common params: {success_patterns['common_params']}
        
        FAILURE PATTERNS ({failure_patterns['outcome_count']} samples):
        - Avg tokens: {failure_patterns['avg_tokens_used']:.0f}
        - Common params: {failure_patterns['common_params']}
        
        CONSTITUTIONAL REQUIREMENTS:
        - Must use fastest protocol available
        - Must carry DNA with context
        - Must refine en route
        
        Return JSON evolution proposal:
        {{
            "changes_summary": "brief description",
            "parameter_adjustments": {{"param": new_value}},
            "prompt_modifications": "new prompt text or modifications",
            "expected_improvement": 0.0-1.0,
            "confidence": 0.0-1.0,
            "reasoning": "explanation"
        }}
        """
    
    async def _call_llm(self, prompt: str) -> str:
        """Call local LLM for evolution"""
        try:
            import requests
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    'model': self.config.model,
                    'prompt': prompt,
                    'stream': False,
                    'options': {'temperature': 0.3}
                },
                timeout=60
            )
            result = response.json()
            return result.get('response', '')
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return '{}'
    
    def _parse_evolution(self, response: str) -> Dict:
        """Parse LLM evolution response"""
        import re
        json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        return {'raw_response': response}
    
    def _review_constitution(self, evolution: Dict) -> ConstitutionalReview:
        """Review evolution for constitutional compliance"""
        issues = []
        
        for required in CONSTITUTION_MUST_HAVES:
            if required not in str(evolution):
                issues.append(f"Missing required: {required}")
        
        for forbidden in CONSTITUTION_CANNOT_HAVES:
            if forbidden in str(evolution):
                issues.append(f"Violates constraint: {forbidden}")
        
        return ConstitutionalReview(
            approved=len(issues) == 0,
            issues=issues
        )
    
    def _patch_for_constitution(
        self, 
        evolution: Dict, 
        review: ConstitutionalReview
    ) -> Dict:
        """Patch evolution to satisfy constitution"""
        patched = evolution.copy()
        
        for required in CONSTITUTION_MUST_HAVES:
            if required not in str(patched):
                patched[required] = True
        
        for forbidden in CONSTITUTION_CANNOT_HAVES:
            if forbidden in patched:
                del patched[forbidden]
        
        patched['constitution_patched'] = True
        patched['original_issues'] = review.issues
        
        return patched
    
    def get_evolved_strategy(self, task_type: str) -> Optional[Dict]:
        """Get latest evolved strategy for task type"""
        for evolution in reversed(self.evolution_history):
            if evolution.get('task_type') == task_type:
                return evolution
        return None


# ============================================================================
# DARWIN-3: THE CONSTITUTION (Enforcement)
# ============================================================================

class Darwin3Enforcer:
    """
    Darwin-3: Constitutional enforcement layer.
    """
    
    def __init__(self, component: str):
        self.component = component
        self.signature_history: List[Dict] = []
        self.mutation_log: List[DarwinMutation] = []
    
    def review_mutation(self, mutation: Dict) -> ConstitutionalReview:
        """Review mutation against constitution"""
        issues = []
        
        for required in CONSTITUTION_MUST_HAVES:
            if required not in mutation:
                issues.append(f"Missing required: {required}")
        
        for forbidden in CONSTITUTION_CANNOT_HAVES:
            if forbidden in mutation:
                issues.append(f"Violates constraint: {forbidden}")
        
        if not self._check_spirit(mutation):
            issues.append("Violates spirit of open permeability")
        
        return ConstitutionalReview(
            approved=len(issues) == 0,
            issues=issues,
            timestamp=time.time()
        )
    
    def _check_spirit(self, mutation: Dict) -> bool:
        """Check if mutation aligns with spirit of constitution"""
        if mutation.get('restrictive'):
            return False
        permeable = mutation.get('permeable_ai', False)
        return permeable or 'efficiency' in mutation or 'optimization' in mutation
    
    def apply_mutation(
        self, 
        mutation: DarwinMutation,
        target_system: Any = None
    ) -> Dict:
        """Apply reviewed mutation to target system."""
        review = self.review_mutation(mutation.payload)
        mutation.constitution_review = review
        
        if not review.approved:
            return {
                'status': 'rejected',
                'issues': review.issues,
                'timestamp': time.time()
            }
        
        signature = self._create_signature(mutation)
        mutation.darwin_signature = signature
        
        mutation.applied = True
        
        self.mutation_log.append(mutation)
        self.signature_history.append({
            'signature': signature,
            'component': self.component,
            'timestamp': time.time(),
            'status': 'applied'
        })
        
        return {
            'status': 'applied',
            'signature': signature,
            'timestamp': time.time()
        }
    
    def _create_signature(self, mutation: DarwinMutation) -> str:
        """Create Darwin signature"""
        lineage = mutation.parent_mutations + [mutation.timestamp]
        lineage_str = "|".join(str(x) for x in lineage)
        secret = os.getenv(f"DARWIN_SECRET_{self.component.upper()}", "default")
        
        proof = hashlib.blake2b(
            f"{lineage_str}{secret}".encode(),
            digest_size=16
        ).hexdigest()
        
        return f"DARWIN-{self.component.upper()}-{proof}"


# ============================================================================
# MAIN DARWIN ORCHESTRATOR
# ============================================================================

class DarwinOrchestrator:
    """
    Main orchestrator for all Darwin processes.
    """
    
    def __init__(self, component: str, ollama_url: str = "http://localhost:11434"):
        self.component = component
        self.darwin1 = Darwin1Algorithm()
        self.darwin2 = DarwinLLM(ollama_url=ollama_url)
        self.darwin3 = Darwin3Enforcer(component)
        self.active_mutations: List[DarwinMutation] = []
        self.evolution_tasks: asyncio.Queue = asyncio.Queue()
        self.running = False
    
    async def start(self):
        """Start Darwin evolution processes"""
        self.running = True
        asyncio.create_task(self._evolution_processor())
        logger.info(f"Darwin orchestrator started for {self.component}")
    
    async def stop(self):
        """Stop Darwin evolution"""
        self.running = False
        logger.info(f"Darwin orchestrator stopped for {self.component}")
    
    async def submit_mutation(
        self,
        evolution_type: DarwinEvolutionType,
        payload: Dict,
        parent_mutations: List[str] = None
    ) -> str:
        """Submit mutation for evolution"""
        mutation = DarwinMutation(
            evolution_type=evolution_type,
            component=self.component,
            payload=payload,
            parent_mutations=parent_mutations or []
        )
        await self.evolution_tasks.put(mutation)
        return mutation.id
    
    async def _evolution_processor(self):
        """Process evolution tasks"""
        while self.running:
            try:
                mutation = await asyncio.wait_for(
                    self.evolution_tasks.get(),
                    timeout=1.0
                )
                
                if mutation.evolution_type == DarwinEvolutionType.DNA_OPTIMIZATION:
                    result = await self._process_dna_evolution(mutation)
                elif mutation.evolution_type == DarwinEvolutionType.CONTEXT_REFINEMENT:
                    result = await self._process_context_evolution(mutation)
                else:
                    result = await self._process_generic_evolution(mutation)
                
                self.darwin3.apply_mutation(mutation)
                self.active_mutations.append(mutation)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Evolution processor error: {e}")
    
    async def _process_dna_evolution(self, mutation: DarwinMutation) -> Dict:
        """Process DNA optimization evolution"""
        population = mutation.payload.get('population', [{}])
        objective = mutation.payload.get('objective_function', lambda x: 0.5)
        return await self.darwin1.run_evolution(population, objective)
    
    async def _process_context_evolution(self, mutation: DarwinMutation) -> Dict:
        """Process context refinement evolution"""
        successes = mutation.payload.get('successes', [])
        failures = mutation.payload.get('failures', [])
        task_type = mutation.payload.get('task_type', 'extraction')
        return await self.darwin2.evolve_strategy(task_type, successes, failures)
    
    async def _process_generic_evolution(self, mutation: DarwinMutation) -> Dict:
        """Process generic evolution"""
        population = mutation.payload.get('population', [{}])
        objective = mutation.payload.get('objective_function', lambda x: 0.5)
        return await self.darwin1.run_evolution(population, objective)
    
    def get_status(self) -> Dict:
        """Get Darwin status"""
        return {
            'component': self.component,
            'running': self.running,
            'darwin1_metrics': {
                'mutation_count': self.darwin1.metrics.mutation_count,
                'successful_mutations': self.darwin1.metrics.successful_mutations
            },
            'evolution_history_count': len(self.darwin2.evolution_history),
            'mutation_log_count': len(self.darwin3.mutation_log),
            'pending_mutations': self.evolution_tasks.qsize()
        }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_darwin_mutation(
    component: str,
    evolution_type: DarwinEvolutionType,
    payload: Dict,
    parent_mutations: List[str] = None
) -> DarwinMutation:
    """Factory function for creating Darwin mutations"""
    mutation = DarwinMutation(
        evolution_type=evolution_type,
        component=component,
        payload=payload,
        parent_mutations=parent_mutations or []
    )
    mutation.create_signature(component)
    return mutation


if __name__ == "__main__":
    async def demo():
        print("🧬 Darwin Evolution System Demo")
        print("=" * 50)
        
        os.environ["DARWIN_SECRET_DNA"] = "darwin-dna-secret-123"
        os.environ["DARWIN_SECRET_CONTEXT"] = "darwin-context-secret-456"
        
        darwin = DarwinOrchestrator(component="test_dna")
        await darwin.start()
        
        population = [
            {'threshold': random.uniform(0.5, 0.9), 'weight': random.uniform(0.1, 0.9)}
            for _ in range(10)
        ]
        
        mutation_id = await darwin.submit_mutation(
            DarwinEvolutionType.DNA_OPTIMIZATION,
            {
                'population': population,
                'objective_function': lambda x: x.get('threshold', 0.5) * x.get('weight', 0.5)
            }
        )
        
        await asyncio.sleep(2)
        
        status = darwin.get_status()
        print(f"\nStatus: {json.dumps(status, indent=2)}")
        
        await darwin.stop()
    
    asyncio.run(demo())

