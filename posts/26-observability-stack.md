# Debugging Democracy #26: Build the Observability Stack for Democracy
*An engineer’s blueprint for end‑to‑end civic telemetry*

If democracy is a production system, we need an **observability pipeline**: logs (events), metrics (system health), traces (who/what changed state), and **immutable storage**.

## Architecture
1. **Ingest**: public records (FOIA feeds), court dockets (PACER/RECAP), agency RSS, platform policy blogs, newsroom APIs. [1][2][3][4]  
2. **Normalize**: YAML events (see our `timeline/` schema), convert to JSON, enrich with tags/actors.  
3. **Store**: signed Git history + object storage with **content hashes**; mirror to Internet Archive. [5]  
4. **Index**: full‑text search + embeddings for RAG; attach **source hashes** to every chunk.  
5. **Dashboards**: SLIs like **verification latency**, **press‑injury incidence**, **impoundment non‑compliance**; alert on threshold breaches.  
6. **Publish**: daily posts + data download + reproducible notebooks.

## Practical sources & endpoints
- **RECAP** for federal dockets; **CourtListener** API; **GovInfo** for official docs. [6][7]  
- **MuckRock** and state portals for FOIA requests and released records. [8]  
- **GDELT** for event‑level media monitoring; **Internet Archive** for web captures; **OpenAlex** for research tracking. [9][5][10]

## Integrity & provenance
- Sign releases (git tags), publish **SHA‑256** for exhibits, and adopt **C2PA/sigstore** for assets. [11][12]

---

### References
[1] FOIA.gov — Agency FOIA resources: https://www.foia.gov/  
[2] Congress.gov — CRS reports search: https://crsreports.congress.gov/  
[3] Federal Register — Rulemaking & orders: https://www.federalregister.gov/  
[4] PACER — Docket access (with costs): https://pacer.uscourts.gov/  
[5] Internet Archive — Save Page Now: https://web.archive.org/save  
[6] RECAP / CourtListener API: https://www.courtlistener.com/recap/  
[7] GovInfo — Official publications: https://www.govinfo.gov/  
[8] MuckRock — FOIA platform: https://www.muckrock.com/  
[9] GDELT Project — Global database of events, language, tone: https://www.gdeltproject.org/  
[10] OpenAlex — Open index of scholarly works: https://openalex.org/  
[11] C2PA — Content provenance: https://c2pa.org/  
[12] sigstore — Transparent software signing: https://www.sigstore.dev/

*Filed: 2025-08-11*
