"""Nightwalker analysis stack and GPT integration."""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import openai

from aggregator.parser import ArticleRecord

logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    """Structured analysis output for an article."""

    empirical: Dict[str, Any]
    logical: Dict[str, Any]
    emotional: Dict[str, Any]
    historical: Dict[str, Any]
    agents: Dict[str, Any]
    summary: str
    ri_insights: List[str]


class GPTClient:
    """Light wrapper around the OpenAI client to call GPT-5 models."""

    def __init__(self, model: str = "gpt-5.1") -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not set; GPT features will be disabled.")
            self.client = None
        else:
            self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def summarize(self, text: str) -> Optional[str]:
        if not self.client:
            return None
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Summarize the article succinctly."},
                {"role": "user", "content": text},
            ],
            max_tokens=200,
        )
        return completion.choices[0].message.content.strip()

    def recursive_insights(self, text: str, depth: int = 16) -> List[str]:
        if not self.client:
            return []
        prompt = (
            "Perform a recursive insight (RI-stack) pass. "
            f"Return {depth} bullet insights that compound on each other."
        )
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": text}],
            max_tokens=depth * 50,
        )
        content = completion.choices[0].message.content
        return [line.strip("- ") for line in content.splitlines() if line.strip()]

    def generate_report(self, summary: str, insights: List[str]) -> Optional[str]:
        if not self.client:
            return None
        prompt = (
            "Create a Nightwalker daily report that highlights major events, source comparisons, "
            "narrative drift, threat vectors, and OODA Pulse signals."
        )
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": summary + "\n\n" + "\n".join(insights)},
            ],
            max_tokens=600,
        )
        return completion.choices[0].message.content.strip()


class NightwalkerAnalyzer:
    """Derives Nightwalker vectors and optionally augments them with GPT-5."""

    def __init__(self, ri_depth: int = 16, model: str = "gpt-5.1") -> None:
        self.ri_depth = ri_depth
        self.gpt = GPTClient(model=model)

    def analyze_article(self, text: str) -> Dict[str, Any]:
        """
        Apply Nightwalker vector analysis to an article body.

        Returns a dictionary containing empirical, logical, emotional, historical, and agent overlays.
        """
        empirical = self._extract_empirical(text)
        logical = self._assess_logic(text)
        emotional = self._assess_emotion(text)
        historical = self._assess_history(text)
        agents = self._agent_overlay(empirical, logical, emotional, historical)

        summary = self.gpt.summarize(text) or self._fallback_summary(text)
        ri_insights = self.gpt.recursive_insights(text, depth=self.ri_depth)

        return AnalysisResult(
            empirical=empirical,
            logical=logical,
            emotional=emotional,
            historical=historical,
            agents=agents,
            summary=summary,
            ri_insights=ri_insights,
        ).__dict__

    def _fallback_summary(self, text: str) -> str:
        sentences = text.split(".")
        return ". ".join(sentences[:2]).strip() or text[:200]

    def _extract_empirical(self, text: str) -> Dict[str, Any]:
        facts = [s for s in text.split(".") if any(char.isdigit() for char in s)]
        sources = [segment for segment in text.split(";") if "according to" in segment.lower()]
        return {"facts": facts, "claims": [], "sources": sources}

    def _assess_logic(self, text: str) -> Dict[str, Any]:
        contradictions = [
            sentence
            for sentence in text.split(".")
            if "however" in sentence.lower() or "but" in sentence.lower()
        ]
        return {"consistency": "mixed" if contradictions else "consistent", "contradictions": contradictions}

    def _assess_emotion(self, text: str) -> Dict[str, Any]:
        tones = []
        lowered = text.lower()
        if any(word in lowered for word in ["warning", "threat", "fear"]):
            tones.append("caution")
        if any(word in lowered for word in ["hope", "progress", "relief"]):
            tones.append("optimistic")
        framing = "balanced" if not tones else ", ".join(sorted(set(tones)))
        return {"tones": tones, "framing": framing}

    def _assess_history(self, text: str) -> Dict[str, Any]:
        references = [sentence for sentence in text.split(".") if any(year in sentence for year in ["2020", "2021", "2022", "2023", "2024"])]
        return {"contextual_links": references, "precedent_count": len(references)}

    def _agent_overlay(
        self,
        empirical: Dict[str, Any],
        logical: Dict[str, Any],
        emotional: Dict[str, Any],
        historical: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "thinker": {
                "evidence_density": len(empirical.get("facts", [])),
                "consistency": logical.get("consistency"),
            },
            "doer": {"actionability": max(1, len(empirical.get("facts", [])))},
            "controller": {"risk": len(emotional.get("tones", []))},
            "pulse": {
                "context": historical.get("precedent_count", 0),
                "tension": len(logical.get("contradictions", [])),
            },
        }

    def analyze_records(self, articles: List[ArticleRecord]) -> List[Dict[str, Any]]:
        analyses: List[Dict[str, Any]] = []
        for article in articles:
            logger.info("Analyzing article: %s", article.title)
            analyses.append(
                {
                    "article": article,
                    "analysis": self.analyze_article(article.summary or article.title),
                }
            )
        return analyses
