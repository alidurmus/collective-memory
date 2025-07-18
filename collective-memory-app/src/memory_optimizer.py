#!/usr/bin/env python3
"""
Memory Usage Optimizer - Phase 8
Smart Context Bridge için bellek optimizasyonu
"""

import gc
import psutil
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class MemoryMetrics:
    """Bellek metrikleri"""
    current_memory_mb: float
    peak_memory_mb: float
    memory_increase_mb: float
    gc_collections: int
    timestamp: float


class MemoryOptimizer:
    """Bellek optimizasyonu sınıfı"""
    
    def __init__(self):
        self.process = psutil.Process()
        self.initial_memory = self.get_memory_usage()
        self.peak_memory = self.initial_memory
        self.memory_history: List[MemoryMetrics] = []
        self.optimization_enabled = True
        
    def get_memory_usage(self) -> float:
        """Mevcut bellek kullanımını MB cinsinden döndür"""
        return self.process.memory_info().rss / 1024 / 1024
    
    def record_memory_metrics(self) -> MemoryMetrics:
        """Bellek metriklerini kaydet"""
        current_memory = self.get_memory_usage()
        
        # Peak memory'i güncelle
        if current_memory > self.peak_memory:
            self.peak_memory = current_memory
        
        # GC istatistiklerini al
        gc_stats = gc.get_stats()
        total_collections = sum(stat['collections'] for stat in gc_stats)
        
        metrics = MemoryMetrics(
            current_memory_mb=current_memory,
            peak_memory_mb=self.peak_memory,
            memory_increase_mb=current_memory - self.initial_memory,
            gc_collections=total_collections,
            timestamp=time.time()
        )
        
        self.memory_history.append(metrics)
        return metrics
    
    def optimize_memory(self) -> Dict[str, Any]:
        """Bellek optimizasyonu yap"""
        if not self.optimization_enabled:
            return {"status": "disabled"}
        
        initial_memory = self.get_memory_usage()
        
        # Garbage collection'ı zorla
        collected = gc.collect()
        
        # Weak references'ları temizle
        gc.collect(2)  # Full collection
        
        final_memory = self.get_memory_usage()
        memory_freed = initial_memory - final_memory
        
        logger.info(f"Memory optimization: {memory_freed:.2f}MB freed")
        
        return {
            "status": "success",
            "memory_freed_mb": memory_freed,
            "collected_objects": collected,
            "current_memory_mb": final_memory
        }
    
    def check_memory_threshold(self, threshold_mb: float = 500) -> bool:
        """Bellek eşiğini kontrol et"""
        current_memory = self.get_memory_usage()
        return current_memory > threshold_mb
    
    def get_memory_report(self) -> Dict[str, Any]:
        """Bellek raporu oluştur"""
        current_metrics = self.record_memory_metrics()
        
        return {
            "current_memory_mb": current_metrics.current_memory_mb,
            "peak_memory_mb": current_metrics.peak_memory_mb,
            "memory_increase_mb": current_metrics.memory_increase_mb,
            "gc_collections": current_metrics.gc_collections,
            "memory_history_count": len(self.memory_history),
            "optimization_enabled": self.optimization_enabled
        }


class ContextCacheOptimizer:
    """Context cache optimizasyonu"""
    
    def __init__(self, max_cache_size: int = 1000):
        self.max_cache_size = max_cache_size
        self.cache: Dict[str, Any] = {}
        self.access_times: Dict[str, float] = {}
        
    def add_to_cache(self, key: str, value: Any) -> None:
        """Cache'e ekle ve boyut kontrolü yap"""
        # Cache boyutunu kontrol et
        if len(self.cache) >= self.max_cache_size:
            self._evict_oldest()
        
        self.cache[key] = value
        self.access_times[key] = time.time()
    
    def get_from_cache(self, key: str) -> Optional[Any]:
        """Cache'den al ve access time'ı güncelle"""
        if key in self.cache:
            self.access_times[key] = time.time()
            return self.cache[key]
        return None
    
    def _evict_oldest(self) -> None:
        """En eski cache entry'sini sil"""
        if not self.access_times:
            return
        
        oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
        del self.cache[oldest_key]
        del self.access_times[oldest_key]
    
    def clear_cache(self) -> int:
        """Cache'i temizle ve temizlenen entry sayısını döndür"""
        cleared_count = len(self.cache)
        self.cache.clear()
        self.access_times.clear()
        return cleared_count
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Cache istatistiklerini döndür"""
        return {
            "cache_size": len(self.cache),
            "max_cache_size": self.max_cache_size,
            "cache_usage_percent": (len(self.cache) / self.max_cache_size) * 100
        }


class ContextGenerationOptimizer:
    """Context generation optimizasyonu"""
    
    def __init__(self):
        self.optimization_rules = {
            "max_summary_length": 500,
            "max_decisions_count": 10,
            "max_technical_details": 20,
            "enable_compression": True,
            "use_caching": True
        }
        self.cache_optimizer = ContextCacheOptimizer()
        
    def optimize_context_generation(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """Context generation'ı optimize et"""
        # Cache'den kontrol et
        cache_key = f"context_{conversation.get('id', hash(str(conversation)))}"
        cached_result = self.cache_optimizer.get_from_cache(cache_key)
        
        if cached_result and self.optimization_rules["use_caching"]:
            return cached_result
        
        # Context generation'ı optimize et
        optimized_context = self._generate_optimized_context(conversation)
        
        # Cache'e ekle
        if self.optimization_rules["use_caching"]:
            self.cache_optimizer.add_to_cache(cache_key, optimized_context)
        
        return optimized_context
    
    def _generate_optimized_context(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize edilmiş context oluştur"""
        context = {
            "summary": "",
            "key_decisions": [],
            "technical_details": [],
            "next_steps": [],
            "project_info": {},
            "relevance_score": 0.0,
        }
        
        messages = conversation.get("messages", [])
        if not messages:
            return context
        
        # Son mesajları al (optimizasyon için sınırla)
        recent_messages = messages[-5:]  # Son 5 mesaj
        
        # Özet oluştur (uzunluk sınırı ile)
        summary = self._create_optimized_summary(recent_messages)
        context["summary"] = summary[:self.optimization_rules["max_summary_length"]]
        
        # Kararları çıkar (sayı sınırı ile)
        decisions = self._extract_decisions(recent_messages)
        context["key_decisions"] = decisions[:self.optimization_rules["max_decisions_count"]]
        
        # Teknik detayları çıkar (sayı sınırı ile)
        technical_details = self._extract_technical_details(recent_messages)
        context["technical_details"] = technical_details[:self.optimization_rules["max_technical_details"]]
        
        # Relevance score hesapla
        context["relevance_score"] = self._calculate_relevance_score(recent_messages)
        
        return context
    
    def _create_optimized_summary(self, messages: List[Dict[str, Any]]) -> str:
        """Optimize edilmiş özet oluştur"""
        if not messages:
            return ""
        
        # Son user mesajını al
        user_messages = [msg["content"] for msg in messages if msg.get("role") == "user"]
        
        if user_messages:
            last_user_msg = user_messages[-1]
            # İlk 100 karakter özet olarak kullan
            summary = last_user_msg[:100] + "..." if len(last_user_msg) > 100 else last_user_msg
            return summary
        
        return "Konuşma devam ediyor"
    
    def _extract_decisions(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Kararları çıkar"""
        decisions = []
        decision_keywords = ["karar", "seçtik", "yapacağız", "kullanacağız", "implements", "decided"]
        
        for msg in messages:
            content = msg.get("content", "").lower()
            for keyword in decision_keywords:
                if keyword in content:
                    # İlk 50 karakter al
                    decision = content[:50] + "..." if len(content) > 50 else content
                    decisions.append(decision)
                    break
        
        return decisions
    
    def _extract_technical_details(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Teknik detayları çıkar"""
        technical_details = []
        tech_keywords = ["api", "database", "model", "framework", "library", "function", "class"]
        
        for msg in messages:
            content = msg.get("content", "").lower()
            for keyword in tech_keywords:
                if keyword in content:
                    # İlk 50 karakter al
                    detail = content[:50] + "..." if len(content) > 50 else content
                    technical_details.append(detail)
                    break
        
        return technical_details
    
    def _calculate_relevance_score(self, messages: List[Dict[str, Any]]) -> float:
        """Relevance score hesapla"""
        if not messages:
            return 0.0
        
        # Basit relevance scoring
        important_keywords = ["proje", "geliştirme", "modül", "özellik", "bug", "hata"]
        total_score = 0.0
        
        for msg in messages:
            content = msg.get("content", "").lower()
            for keyword in important_keywords:
                if keyword in content:
                    total_score += 0.1
        
        # 0-1 arasında normalize et
        return min(total_score, 1.0)
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Optimizasyon istatistiklerini döndür"""
        cache_stats = self.cache_optimizer.get_cache_stats()
        
        return {
            "optimization_rules": self.optimization_rules,
            "cache_stats": cache_stats,
            "optimization_enabled": True
        }


def main():
    """Test fonksiyonu"""
    # Memory optimizer test
    memory_optimizer = MemoryOptimizer()
    print("Memory Optimizer initialized")
    
    # Context generation optimizer test
    context_optimizer = ContextGenerationOptimizer()
    print("Context Generation Optimizer initialized")
    
    # Test conversation
    test_conv = {
        'id': 'optimization_test',
        'title': 'Optimization Test',
        'messages': [
            {'role': 'user', 'content': 'We need to optimize the memory usage'},
            {'role': 'assistant', 'content': 'Here are some optimization strategies...'},
        ],
        'timestamp': time.time()
    }
    
    # Optimize context generation
    optimized_context = context_optimizer.optimize_context_generation(test_conv)
    print(f"Optimized context generated: {len(optimized_context)} keys")
    
    # Memory report
    memory_report = memory_optimizer.get_memory_report()
    print(f"Memory report: {memory_report['current_memory_mb']:.2f}MB")
    
    # Optimization stats
    optimization_stats = context_optimizer.get_optimization_stats()
    print(f"Cache usage: {optimization_stats['cache_stats']['cache_usage_percent']:.1f}%")


if __name__ == "__main__":
    main() 