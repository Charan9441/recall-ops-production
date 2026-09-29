import json
import logging
from typing import Any, Optional
from app.config import settings
from app.models import IncidentRequest

logger = logging.getLogger(__name__)

try:
    import groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


class LLMService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self.client = None

        if GROQ_AVAILABLE and self.api_key:
            try:
                self.client = groq.Groq(api_key=self.api_key)
                logger.info(f"Initialized Groq LLM client with model: {self.model}")
            except Exception as e:
                logger.warning(f"Groq LLM client initialization warning: {e}")
                self.client = None

    def analyze_incident(
        self, incident: IncidentRequest, memories: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Analyzes current incident telemetry against retrieved Hindsight historical memories."""

        # Format historical memory context
        if memories:
            mem_blocks = []
            for idx, m in enumerate(memories, 1):
                text_content = m.get("text", str(m))
                mem_blocks.append(f"Memory #{idx}:\n{text_content}")
            memory_context = "\n\n---\n\n".join(mem_blocks)
        else:
            memory_context = "NO HISTORICAL MEMORIES RETRIEVED FROM HINDSIGHT."

        system_prompt = (
            "You are Recall-Ops, an expert production incident-response assistant.\n\n"
            "Analyze the current incident using the provided historical memories retrieved from Hindsight.\n\n"
            "Instructions:\n"
            "1. Identify the likely root cause.\n"
            "2. Recommend specific resolution/mitigation actions.\n"
            "3. Explain why the actions are recommended.\n"
            "4. Reference relevant historical incidents when available.\n"
            "5. Provide a confidence level (HIGH, MEDIUM, or LOW).\n"
            "6. NEVER invent or hallucinate historical incidents.\n"
            "7. Clearly state if there is insufficient historical evidence.\n"
            "8. Respond with structured JSON output containing keys: "
            '"likely_root_cause", "recommended_actions", "explanation", "historical_references", "confidence".'
        )

        user_prompt = f"""CURRENT INCIDENT:
Service: {incident.service}
Severity: {incident.severity}
Error: {incident.error}
Logs: {incident.logs or 'N/A'}
Deployment Version: {incident.deployment_version or 'N/A'}

HISTORICAL MEMORIES RETRIEVED FROM HINDSIGHT:
{memory_context}

Generate the structured incident analysis JSON.
"""

        if self.client:
            try:
                chat_completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.1,  # Low temperature for consistent analysis
                )
                response_content = chat_completion.choices[0].message.content or ""
                return self._parse_llm_response(response_content, incident, memories)
            except Exception as e:
                logger.warning(f"Groq API call error: {e}. Utilizing operational rules synthesis engine.")

        return self._generate_rule_based_fallback(incident, memories)

    def _parse_llm_response(
        self, response_text: str, incident: IncidentRequest, memories: list[dict[str, Any]]
    ) -> dict[str, Any]:
        try:
            # Clean JSON formatting if wrapped in code blocks
            clean_text = response_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]

            parsed = json.loads(clean_text.strip())
            return {
                "likely_root_cause": parsed.get("likely_root_cause", "Under investigation"),
                "recommended_actions": parsed.get("recommended_actions", ["Check service health and logs"]),
                "explanation": parsed.get("explanation", "Diagnosis generated from operational analysis."),
                "historical_references": parsed.get("historical_references", []),
                "confidence": parsed.get("confidence", "MEDIUM"),
                "raw_response": response_text,
            }
        except Exception as e:
            logger.warning(f"Failed to parse LLM JSON: {e}. Output was: {response_text[:150]}")
            return {
                "likely_root_cause": f"Incident on {incident.service}: {incident.error}",
                "recommended_actions": ["Inspect application metrics", "Check deployment logs"],
                "explanation": response_text[:300],
                "historical_references": [m.get("text", "")[:100] for m in memories[:2]],
                "confidence": "MEDIUM",
            }

    def _generate_rule_based_fallback(
        self, incident: IncidentRequest, memories: list[dict[str, Any]]
    ) -> dict[str, Any]:
        if memories:
            top_mem = memories[0]
            top_text = top_mem.get("text", "")
            return {
                "likely_root_cause": f"High probability of regression matching historical evidence in Hindsight.",
                "recommended_actions": [
                    f"Inspect {incident.service} logs for pattern: {incident.error}",
                    f"Consider rollback if version {incident.deployment_version or 'recent'} introduced the failure.",
                    "Restart affected instances after verifying connection state.",
                ],
                "explanation": f"Retrieved historical memory from Hindsight indicated: {top_text[:200]}...",
                "historical_references": [top_text[:150]],
                "confidence": "HIGH",
            }

        return {
            "likely_root_cause": f"Service failure on {incident.service} ({incident.error}).",
            "recommended_actions": [
                "Inspect live service telemetry and application logs",
                "Verify database connection pools and upstream dependencies",
                "Record resolution into Hindsight memory bank after triage",
            ],
            "explanation": "No prior organizational memory match was retrieved from Hindsight. Recommendation is based on standard operational triaging.",
            "historical_references": [],
            "confidence": "LOW",
        }


llm_service = LLMService()
