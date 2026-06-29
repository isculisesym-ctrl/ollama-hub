"""Code review orchestration — Haiku coordinates multiple Ollama specialists"""

import json
from collections.abc import AsyncGenerator

import httpx
from app.config import settings
from app.services.ollama_service import ollama_service
from app.services.claude_service import claude_service


class CodeReviewService:
    """Haiku acts as PM, routes to specialist Ollamas or Claude"""

    async def review_code_swarm(
        self, code: str, description: str = ""
    ) -> AsyncGenerator[str, None]:
        """
        Route code to multiple reviewers in parallel.
        Haiku (small, fast) orchestrates; Ollamas specialize.
        """
        context = f"""Code to review:
```
{code}
```

Description: {description}

Provide a focused, actionable review for your specialty."""

        specialists = [
            ("Security", "Identify security vulnerabilities, unsafe patterns, injection risks"),
            ("Performance", "Find performance bottlenecks, memory leaks, inefficient algorithms"),
            ("Readability", "Check naming, complexity, documentation, best practices"),
        ]

        tasks = []
        for specialty, prompt_suffix in specialists:
            prompt = f"{context}\n\nFocus on {specialty}:\n{prompt_suffix}"
            tasks.append((specialty, self._review_with_ollama(prompt)))

        yield json.dumps({"event": "started", "specialists": len(specialists)})

        results = {}
        for specialty, gen in tasks:
            full_review = ""
            async for chunk in gen:
                chunk_obj = json.loads(chunk)
                if chunk_obj.get("token"):
                    full_review += chunk_obj["token"]
                    yield json.dumps({
                        "event": "chunk",
                        "specialist": specialty,
                        "token": chunk_obj["token"],
                    })
            results[specialty] = full_review

        yield json.dumps({"event": "reviews_done", "specialists": results})

        haiku_summary = await self._summarize_reviews(code, results)
        yield json.dumps({
            "event": "summary",
            "executive_summary": haiku_summary,
        })

    async def _review_with_ollama(self, prompt: str) -> AsyncGenerator[str, None]:
        """Single Ollama specialist review"""
        try:
            async for chunk in ollama_service.generate_stream(prompt, model="llama3.2"):
                yield chunk
        except Exception as e:
            yield json.dumps({"error": str(e)})

    async def _summarize_reviews(self, code: str, reviews: dict) -> str:
        """Haiku synthesizes all specialist reviews into a concise summary"""
        try:
            prompt = f"""As a code review PM, synthesize these specialist reviews:

Code:
```
{code}
```

Reviews from specialists:
{chr(10).join(f"- {k}: {v[:200]}" for k, v in reviews.items())}

Provide a 1-2 sentence executive summary of the most critical issues."""

            result = await claude_service.generate(prompt, model="claude-haiku-4-5-20251001")
            return result["response"]
        except Exception:
            return "Summary generation failed. See specialist reviews above."


review_service = CodeReviewService()
