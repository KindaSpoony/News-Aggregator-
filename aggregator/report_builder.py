"""Utilities to build Nightwalker markdown reports."""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

from aggregator.analyzer import GPTClient

logger = logging.getLogger(__name__)


class ReportBuilder:
    """Compose and persist the daily Nightwalker report."""

    def __init__(self, output_dir: str, gpt_client: GPTClient | None = None) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.gpt = gpt_client

    def build(self, analyses: Iterable[Dict]) -> Path:
        lines: List[str] = []
        lines.append("# Nightwalker Daily Report")
        lines.append(f"Generated: {datetime.utcnow().isoformat()}Z")
        lines.append("")

        major_events = self._summarize_events(analyses)
        source_comparisons = self._compare_sources(analyses)
        narrative_drift = self._detect_drift(analyses)
        threat_vectors = self._detect_threats(analyses)
        pulse_summary = self._pulse_summary(analyses)

        lines.append("## Major Events")
        lines.extend([f"- {event}" for event in major_events])

        lines.append("\n## Source Comparisons")
        lines.extend([f"- {comparison}" for comparison in source_comparisons])

        lines.append("\n## Narrative Drift Detection")
        lines.extend([f"- {drift}" for drift in narrative_drift])

        lines.append("\n## Threat Vectors")
        lines.extend([f"- {threat}" for threat in threat_vectors])

        lines.append("\n## Nightwalker OODA Pulse")
        lines.extend([f"- {pulse}" for pulse in pulse_summary])

        if self.gpt:
            logger.info("Generating GPT-authored final report section")
            ai_section = self.gpt.generate_report(
                summary="\n".join(major_events), insights=list(pulse_summary)
            )
            if ai_section:
                lines.append("\n## GPT-5 Daily Narrative")
                lines.append(ai_section)

        output_path = self._report_path()
        output_path.write_text("\n".join(lines), encoding="utf-8")
        logger.info("Report written to %s", output_path)
        return output_path

    def _summarize_events(self, analyses: Iterable[Dict[str, Any]]) -> List[str]:
        events = []
        for item in analyses:
            analysis = item["analysis"]
            title = item["article"].title
            summary = analysis["summary"]
            events.append(f"{title}: {summary}")
        return events

    def _compare_sources(self, analyses: Iterable[Dict[str, Any]]) -> List[str]:
        comparisons = {}
        for item in analyses:
            source = item["article"].source
            comparisons.setdefault(source, 0)
            comparisons[source] += 1
        return [f"{source} provided {count} items" for source, count in comparisons.items()]

    def _detect_drift(self, analyses: Iterable[Dict[str, Any]]) -> List[str]:
        drift = []
        for item in analyses:
            analysis = item["analysis"]
            if analysis["logical"].get("contradictions"):
                drift.append(
                    f"{item['article'].title} shows logical tension: {len(analysis['logical']['contradictions'])} contradictions"
                )
        return drift or ["No significant narrative drift detected"]

    def _detect_threats(self, analyses: Iterable[Dict[str, Any]]) -> List[str]:
        threats = []
        for item in analyses:
            analysis = item["analysis"]
            if "caution" in analysis["emotional"].get("tones", []):
                threats.append(f"{item['article'].title} carries cautionary framing")
        return threats or ["No explicit threat vectors surfaced"]

    def _pulse_summary(self, analyses: Iterable[Dict[str, Any]]) -> List[str]:
        pulses = []
        for item in analyses:
            analysis = item["analysis"]
            pulse = analysis["agents"]["pulse"]
            pulses.append(
                f"{item['article'].title}: context={pulse['context']} tension={pulse['tension']}"
            )
        return pulses

    def _report_path(self) -> Path:
        today = datetime.utcnow().date().isoformat()
        return self.output_dir / f"{today}-nightwalker-daily.md"
