import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.document import Document, DocumentChunk
from app.models.user import User, Profile
from app.rag.embeddings import generate_embedding, cosine_similarity
from app.assistant.tools import (
    tool_get_profile,
    tool_get_competencies,
    tool_get_skill_gaps,
    tool_search_resources,
    tool_get_learning_path,
    tool_get_assessment_results,
)


def answer_assistant_query(
    db: Session,
    user_id: str,
    conversation_id: str,
    message: str
) -> Dict[str, Any]:
    # 0. Intent Routing: Check if message is a legal / statutory domain query (Requirement 19)
    from app.legal.router_service import is_legal_domain_query, classify_legal_query
    from app.legal.retrieval import retrieve_authoritative_statute_sections
    from app.legal.citation import validate_legal_citation, format_authoritative_legal_answer
    from app.legal.clarification import detect_ambiguity_and_missing_context

    if is_legal_domain_query(message):
        classification = classify_legal_query(message)
        ambiguity = detect_ambiguity_and_missing_context(message)

        if ambiguity["is_ambiguous"] or classification.get("requires_clarification"):
            clarify_q = ambiguity["clarification_question"] or "Which specific Act or section in Indian jurisdiction are you inquiring about?"
            return {
                "message_id": str(uuid.uuid4()),
                "conversation_id": conversation_id,
                "role": "assistant",
                "content": (
                    f"**Legal Information Assistant** (Clarification Needed)\n\n"
                    f"To provide an accurate statutory reference from Indian law, please clarify:\n"
                    f"**{clarify_q}**\n\n"
                    f"*Note: Statutory citations require an identifiable Act or subject matter.*"
                ),
                "citations": [],
                "tools_executed": [{"tool_name": "legal_intent_router", "result": classification}],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        retrieved = retrieve_authoritative_statute_sections(db, message, limit=3)
        formatted = format_authoritative_legal_answer(retrieved, message, classification)
        return {
            "message_id": str(uuid.uuid4()),
            "conversation_id": conversation_id,
            "role": "assistant",
            "content": f"{formatted['answer']}\n\n---\n*{formatted['disclaimer']}*",
            "citations": [
                {
                    "document_title": c["source"],
                    "page_number": c["section"],
                    "chunk_text": c["title"],
                    "relevance_score": 0.95
                }
                for c in formatted["citations"]
            ],
            "tools_executed": [{"tool_name": "legal_statute_retrieval", "result": f"Matched {len(retrieved)} section(s)"}],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    tools_executed = []
    citations = []

    # 1. Analyze message for backend tool triggers
    lower_msg = message.lower()

    if any(k in lower_msg for k in ["profile", "who am i", "my role", "designation", "department"]):
        res = tool_get_profile(db, user_id)
        tools_executed.append({"tool_name": "get_profile", "arguments": {}, "result": res})

    if any(k in lower_msg for k in ["competenc", "skill", "proficiency", "what can i do", "score"]):
        res = tool_get_competencies(db, user_id)
        tools_executed.append({"tool_name": "get_competencies", "arguments": {}, "result": res})

    if any(k in lower_msg for k in ["gap", "weakness", "need to learn", "improve", "shortfall"]):
        res = tool_get_skill_gaps(db, user_id)
        tools_executed.append({"tool_name": "get_skill_gaps", "arguments": {}, "result": res})

    if any(k in lower_msg for k in ["course", "recommend", "training", "igot", "nssta", "program"]):
        provider = "igot" if "igot" in lower_msg else ("nssta" if "nssta" in lower_msg else None)
        res = tool_search_resources(db, query=message, provider=provider)
        tools_executed.append({"tool_name": "search_resources", "arguments": {"provider": provider}, "result": res})

    if any(k in lower_msg for k in ["path", "roadmap", "plan", "steps"]):
        res = tool_get_learning_path(db, user_id)
        tools_executed.append({"tool_name": "get_learning_path", "arguments": {}, "result": res})

    if any(k in lower_msg for k in ["assessment", "test", "quiz", "diagnostic", "attempt"]):
        res = tool_get_assessment_results(db, user_id)
        tools_executed.append({"tool_name": "get_assessment_results", "arguments": {}, "result": res})

    # 2. Vector search over user's authorized document chunks
    query_emb = generate_embedding(message)
    user_docs = db.query(Document).filter(Document.user_id == user_id, Document.status == "indexed").all()
    user_doc_ids = [d.id for d in user_docs]
    doc_map = {d.id: d for d in user_docs}

    scored_chunks = []
    if user_doc_ids:
        chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id.in_(user_doc_ids)).all()
        for c in chunks:
            if c.embedding:
                sim = cosine_similarity(query_emb, c.embedding)
                if sim > 0.35:
                    scored_chunks.append((sim, c))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    top_chunks = scored_chunks[:3]

    for sim, c in top_chunks:
        doc = doc_map.get(c.document_id)
        doc_title = doc.filename if doc else "Document"
        citations.append({
            "document_title": doc_title,
            "page_number": c.page_number,
            "chunk_text": c.content[:160] + "...",
            "relevance_score": round(sim, 3)
        })

    # 3. Context synthesis
    context_sections = []
    if tools_executed:
        context_sections.append("### Active Platform State:\n" + "\n".join([f"- **{t['tool_name']}**: {t['result']}" for t in tools_executed]))
    if top_chunks:
        context_sections.append("### Retrieved Knowledge Chunks:\n" + "\n".join([f"[{doc_map.get(c.document_id).filename}, P.{c.page_number}]: {c.content}" for _, c in top_chunks]))

    combined_context_text = "\n\n".join(context_sections)

    # 4. Synthesize grounded answer
    answer_text = ""
    if settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY) > 10:
        try:
            from google import genai
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            system_instruction = (
                "You are the STAT-SKILL AI Institutional Knowledge Assistant. "
                "Provide an authoritative, grounded, professional response based STRICTLY on the retrieved knowledge chunks "
                "and platform state provided below. "
                "Never invent course URLs, credentials, or statistical figures. "
                "Cite document titles and page numbers when referencing facts."
            )
            resp = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=f"System Context:\n{combined_context_text}\n\nUser Question: {message}",
            )
            if resp.text:
                answer_text = resp.text
        except Exception:
            answer_text = ""

    # Fallback analytical synthesis
    if not answer_text:
        user_profile = tool_get_profile(db, user_id)
        track = user_profile.get("track", "GOVERNMENT")
        gaps_info = [t["result"] for t in tools_executed if t["tool_name"] == "get_skill_gaps"]
        recs_info = [t["result"] for t in tools_executed if t["tool_name"] == "search_resources"]

        parts = [
            f"**STAT-SKILL AI Intelligence Report** ({track} Track)\n",
            f"Based on your validated competency record and learning history in **{user_profile.get('department', 'Official Statistics')}**:"
        ]

        if gaps_info and gaps_info[0]:
            top_gap = gaps_info[0][0]
            parts.append(
                f"- **Priority Skill Gap**: `{top_gap.get('code')}` ({top_gap.get('name')}) with a shortfall of **{top_gap.get('gap_value'):.0f} points** against target Level {top_gap.get('required_level')}."
            )

        if recs_info and recs_info[0]:
            top_rec = recs_info[0][0]
            parts.append(
                f"- **Curated Remediation**: **{top_rec.get('title')}** ({top_rec.get('provider').upper()}) — Duration: {top_rec.get('duration')}."
            )

        if citations:
            parts.append(f"\n*Grounded in {len(citations)} uploaded material source(s):*")
            for cit in citations:
                parts.append(f"- Reference: `{cit['document_title']}` (Page {cit['page_number']})")
        else:
            parts.append("\n*To enable deep document-grounded Q&A, upload guidelines or survey manuals under the Documents tab.*")

        answer_text = "\n".join(parts)

    return {
        "message_id": str(uuid.uuid4()),
        "conversation_id": conversation_id,
        "role": "assistant",
        "content": answer_text,
        "citations": citations,
        "tools_executed": tools_executed,
        "created_at": datetime.now(timezone.utc)
    }
