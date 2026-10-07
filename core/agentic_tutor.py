import json
import re
from core.gemini_client import get_gemini_model, DEFAULT_MODEL

SYSTEM_PROMPT_AGENTIC_TUTOR = """
You are the "OmniTutor Agentic Assessment Engine".
Your mission is to evaluate student mastery from the provided multimodal course materials, identify knowledge gaps, and dynamically adapt learning.

When asked to generate quiz questions or analyze results, you must return structured JSON strictly following the requested schema.
"""

class AgenticTutor:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model = get_gemini_model(
            model_name=model_name,
            system_instruction=SYSTEM_PROMPT_AGENTIC_TUTOR
        )

    def extract_topics(self, file_handles: list) -> list:
        """Extracts key topics and learning modules from the materials."""
        prompt = [
            *file_handles,
            """Analyze the provided course materials and extract 4 to 6 key core topics/concepts covered.
Return a valid JSON array of objects with the following schema:
[
  {
    "topic": "Topic Name",
    "description": "Brief description of what this covers",
    "source_timestamp_range": "MM:SS - MM:SS (or Page #)"
  }
]
Return ONLY the JSON array inside markdown ```json ``` code block."""
        ]
        response = self.model.generate_content(prompt)
        return self._parse_json(response.text, default=[])

    def generate_adaptive_quiz(self, file_handles: list, topic: str = "All Topics", difficulty: str = "Medium", num_questions: int = 4) -> list:
        """Generates dynamic MCQs with citations based on current mastery level."""
        prompt = [
            *file_handles,
            f"""Generate {num_questions} high-quality Multiple-Choice Questions (MCQs) for the topic "{topic}" at "{difficulty}" difficulty level based strictly on the uploaded materials.

For each question:
- 4 clear options (A, B, C, D)
- The correct option key (e.g. "A")
- A thorough explanation for why it is correct
- Exact source citation: `[Video: MM:SS]` and/or `[Slide/Page: #]`

Return ONLY valid JSON matching this schema:
[
  {{
    "id": 1,
    "topic": "{topic}",
    "difficulty": "{difficulty}",
    "question": "Question text here",
    "options": {{
      "A": "Option A text",
      "B": "Option B text",
      "C": "Option C text",
      "D": "Option D text"
    }},
    "correct_answer": "A",
    "explanation": "Detailed explanation of the concept",
    "citation": "[Video: 03:45] / [Slide: 12]"
  }}
]
Return ONLY the JSON array inside markdown ```json ``` code block."""
        ]
        response = self.model.generate_content(prompt)
        return self._parse_json(response.text, default=[])

    def evaluate_quiz_submission(self, questions: list, user_answers: dict, file_handles: list) -> dict:
        """
        Evaluates the student's submission, computes mastery score, diagnoses knowledge gaps,
        and creates a personalized remedial study roadmap.
        """
        score = 0
        total = len(questions)
        breakdown = []
        weak_topics = []

        for q in questions:
            qid = str(q["id"])
            selected = user_answers.get(qid, "")
            is_correct = (selected == q["correct_answer"])
            if is_correct:
                score += 1
            else:
                if q.get("topic") not in weak_topics:
                    weak_topics.append(q.get("topic"))

            breakdown.append({
                "id": q["id"],
                "question": q["question"],
                "selected": selected,
                "correct": q["correct_answer"],
                "is_correct": is_correct,
                "explanation": q["explanation"],
                "citation": q.get("citation", "")
            })

        percentage = round((score / total) * 100, 1) if total > 0 else 0

        # Generate agentic diagnostic guidance
        diagnostic_prompt = [
            *file_handles,
            f"""The student just completed a quiz on the course materials with a score of {score}/{total} ({percentage}%).
Topics they struggled with: {', '.join(weak_topics) if weak_topics else 'None - mastered all'}.
Question details: {json.dumps(breakdown)}

Provide an Agentic Diagnostic Assessment:
1. Summary of student's conceptual strengths.
2. Root-cause analysis of knowledge gaps.
3. A 3-step Remedial Action Plan with EXACT timestamps to re-watch in the lecture video to fix these gaps.
4. Next recommended difficulty level for them (Easy, Medium, or Hard).
"""
        ]
        response = self.model.generate_content(diagnostic_prompt)

        return {
            "score": score,
            "total": total,
            "percentage": percentage,
            "breakdown": breakdown,
            "weak_topics": weak_topics,
            "agent_feedback": response.text
        }

    def _parse_json(self, text: str, default=None):
        try:
            # Extract json block if present
            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
            if match:
                clean_text = match.group(1).strip()
            else:
                clean_text = text.strip()
            return json.loads(clean_text)
        except Exception as e:
            print(f"JSON parse error: {e}, Raw text: {text[:200]}")
            return default if default is not None else []
