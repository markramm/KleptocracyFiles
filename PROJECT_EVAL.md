# Project Evaluation & Narrative Review (Weeks 1–4)

**Status:** Draft — Aug 11, 2025

## A. What’s strong
- **Audience fit (technical):** The systems-engineering framing (infra, monitoring, circuit breakers, rate limiting) lands well. It translates complex legal/procedural shifts into SRE patterns without dumbing them down.
- **Evidence architecture:** Posts carry **full-URL footnotes**; the `timeline/` provides structured, queryable facts for RAG and print. We now have **59 normalized YAML events** + an index.
- **Reusability:** The Week 4 playbook, observability stack, and resistance documentation are modular and can be reused for live incidents.

## B. Gaps & risks (prioritized)
1) **Source specificity**  
   - The **USNI Marines in LA** entry cites the site root; replace with the precise article URL (date-stamped).  
   - Some entries rely on **single-source reports** (e.g., Reuters/AP) — for contentious claims, add one primary doc (PDF/order) + one alt outlet.
2) **Over-claim risk language**  
   - Keep descriptive language tight where courts issued **stays**: clarify that stays **preserve** contested actions, not that courts “authorized” them.
3) **Consistency in event scope**  
   - Avoid splitting the same event into multiple YAMLs (e.g., duplicate EAVS entries — *fixed*). Check potential pairs like **D.C. surge** if they cover the same announcement.
4) **Temporal clarity**  
   - Continue using **absolute dates** in posts when referencing “this week/today/yesterday.”
5) **Coverage holes**  
   - **Brookings/LA** piece is included; add a concise YAML for **press pool seat removal** with WHCA + PFT citations (we added PFT; ensure WHCA is linked).  
   - Fill specific URLs for **USNI Marines** and any placeholder notes.

## C. Editorial rhythm
- Weeks 1–2: Clear **infrastructure-compromise → monitoring disabled → courts as clutch → info war** arc.  
- Week 3: Good escalation framing (redundancy collapse; backup/restore failures).  
- Week 4: Nicely pivots to **tools, reforms, and telemetry** — keeps credibility by offering constructive responses.

**Suggestion:** Add a short **“What changed this week?”** box at the top of each weekly status post (bulleted 4–6 lines).

## D. Repository hygiene
- **Duplicates:** Timeline duplicates swept (archived one EAVS duplicate). Posts had **no content duplicates**.  
- **Normalization:** All timeline files now share the same schema; tags are lowercased/hyphenated; citations cleaned.
- **Artifacts:** `SWEEP_REPORT.md` summarizes actions; repo zipped for handoff.

## E. Next steps (actionable)
1) **Tighten high-salience citations (Today)**
   - Replace USNI homepage link with the **exact article** URL.  
   - Cross-check **D.C. surge** pair for duplication; if same announcement, merge and archive one file.
2) **Auto-footnote builder (This week)**
   - Add a small script that pulls citations from `timeline/` for any post date range and renders **Google-Docs‑style footnotes** with full URLs.
3) **URL health check (This week)**
   - Run a link linter to detect 3xx/4xx/5xx and suggest alternatives (govinfo mirrors; court PDFs).
4) **RAG demo (Optional)**
   - Load `timeline/index.json` (generated during the Pages workflow) and serve a Q&A endpoint that always returns **answer + citations**.
5) **Distribution**
   - Generate **print‑ready PDFs** (Weeks 1–4) with title/footers and appendix of sources; keep URLs visible.

## F. Risk register (live items)
- **Emergency-stay narratives**: ensure precision to avoid claims that courts “approved” contested actions.  
- **Attribution timing**: When citing **“reports say”** items (e.g., Guard activation prep), maintain the “preparing/considering” language until an order is published.
- **Platform policy bugs/defaults**: Where behavior is documented as a **bug**, keep that label unless clear evidence shows intentional throttling.

---

**Maintainer’s note:** See `SWEEP_REPORT.md` for the exact files archived/changed in the sweep.
