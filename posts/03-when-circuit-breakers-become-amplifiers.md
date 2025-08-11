# Debugging Democracy #3: When Circuit Breakers Become Amplifiers
*Emergency judicial procedures that preserve contested power*

**TL;DR for engineers:** Our “circuit breakers” (emergency stays) are failing open. Courts are preserving the *state of the world created by an executive action* while merits cases crawl along. In practice, the stay becomes the policy.

## Incident log (June–August 2025)

- **Jun 7, 2025 — Executive memo:** The White House issued a memorandum authorizing DoD “security” in support of DHS operations nationwide, enabling federalized National Guard and active-duty support for immigration enforcement.[^wh-memo]  
- **Jun 9, 2025 — Force posture change:** U.S. Northern Command and USNI reported ~**700 Marines (2/7)** deploying into greater Los Angeles to support federal personnel and property protection.[^northcom][^usni]  
- **Mid–late June — District ruling, then stay:** A federal district judge in California concluded the deployment likely exceeded statutory/constitutional authority; within days, the **Ninth Circuit** stayed that order, keeping the Guard/Marines in place pending appeal.[^ap-la-trial][^9th-pdf][^lat-stay][^calmatters-stay]  
- **Jun 26, 2025 — Expert alarm:** Brookings analyzed the legal posture, warning how Section 12406 and related authorities were being stretched—and how “temporary” deployments risk normalization.[^brookings-la]  
- **Aug 8–11, 2025 — D.C. surge:** The White House directed a **federal law-enforcement surge** in Washington, D.C., with FBI agents pulled to street patrols and preparations to activate **hundreds of D.C. National Guard** personnel.[^reuters-dc-surge][^wapo-fbi][^reuters-guard]

### Why this is a systems problem
In distributed systems, a breaker that “fails open” under stress will **propagate** the fault state. In constitutional systems, **emergency stays** that preserve contested actions do the same: they **propagate the executive’s de facto policy** while review drags on.

## Pattern: The stay becomes the policy

- **EPA Good Neighbor Plan stay (2024):** The Supreme Court’s emergency docket stayed EPA’s interstate ozone rule, reshaping national air policy through a stay order before merits resolution.[^ohio-v-epa][^gibson]  
- **Standing as shield (2024):** In *Murthy v. Missouri*, the Court found no standing for plaintiffs challenging alleged federal coercion of platforms—foreclosing immediate merits review of government–platform interactions.[^murthy][^mayer]  
- **Agency adjudication shifted (2024):** *SEC v. Jarkesy* pushed civil-penalty actions to jury trials, moving chokepoints to Article III courts—affecting timelines and leverage in enforcement.[^jarkesy][^crs-jarkesy]  
- **Chevron deference ended (2024):** *Loper Bright* replaced deference with greater judicial discretion—amplifying the power of stay-stage readings of statutory authority.[^loper][^hls-summary]

**Net effect:** The legal “control plane” privileges *status quo maintenance* via emergency orders. When the status quo **is the contested action**, the stay **operationalizes** that action for months.

## Case study: Los Angeles deployment

- **Authority invoked:** The June 7 memo directed DoD support for DHS and turned to 10 U.S.C. § 12406 (federalization of Guard) alongside other protective authorities; legal analysts flagged Posse Comitatus constraints and the narrow historical scope of domestic troop use.[^wh-memo][^lawfare-guard][^pbs-law][^vladeck-substack]  
- **Force package:** NORTHCOM confirmed ~700 Marines (2/7) integrating under Title 10 tasking to protect federal personnel and facilities.[^northcom]  
- **Judicial path:** A district court found the deployment likely unlawful; the Ninth Circuit’s **stay** kept troops on-station pending appeal, transforming a preliminary ruling against the government into **ongoing operational authority** on the ground.[^9th-pdf][^lat-stay][^calmatters-stay][^ap-la-trial]

**Operational takeaway:** A single ex parte or emergency-stage win can **lock in** high-impact security posture changes—even when merits analysis leans the other way.

## Case study: Washington, D.C. surge

- **Federal law-enforcement surge ordered:** Reuters and others reported increased **visible deployments** by federal agencies at tourist corridors beginning Aug. 8.[^reuters-dc-surge]  
- **FBI street assignments:** *Washington Post* detailed up to **120 FBI agents** reassigned to overnight patrols, diverting personnel from core missions.[^wapo-fbi]  
- **Guard activation prepped:** Reuters reported the **military preparing** to activate **hundreds** of D.C. National Guard.[^reuters-guard]

**Control-plane implication:** Even before courts can assess limits, **temporary operational changes** reshape the lived environment—policing patterns, chilling effects, and press access dynamics.

## What to monitor (SRE-style probes)

1. **Stay cadence & duration:** Track how long emergency stays maintain contested actions versus time-to-merits in each circuit.  
2. **Scope creep:** Compare the geographic and functional scope described in stay orders against **on-the-ground** mission creep.  
3. **Feedback loops:** Watch whether stayed actions **generate facts** (arrests, clearances, dispersals) that later moot challenges.  
4. **Cross-domain reuse:** Note stays in environmental, immigration, and speech cases—do they share a doctrinal throughline that privileges executive continuity?

## Mitigations (design hypotheses)

- **Time-boxed stays:** Advocate for presumptive sunsets on emergency stays that preserve government action (renewable on transparent showings).  
- **Transparent records:** Require contemporaneous public reporting of operations conducted **solely under stayed authority**.  
- **Parallel oversight:** Build civil-society “observability” (FOIA pipelines, real-time logs) so emergency actions don’t become **black boxes**.

---

### Footnotes

[^wh-memo]: White House, *Memorandum — Department of Defense Security for the Protection of DHS Functions* (June 7, 2025), https://www.whitehouse.gov/presidential-actions/2025/06/department-of-defense-security-for-the-protection-of-department-of-homeland-security-functions/  
[^northcom]: U.S. Northern Command press release (June 9, 2025), https://www.northcom.mil/Newsroom/Press-Releases/Article/4210889/usnorthcom-statement-on-additional-military-personnel-in-the-los-angeles-area/  
[^usni]: USNI News, “700 Marines Deploying to Downtown Los Angeles” (June 9, 2025), https://news.usni.org/2025/06/09/700-marines-deploying-to-downtown-los-angeles  
[^ap-la-trial]: Associated Press, “Trial to start on whether deployment of National Guard to Los Angeles violated federal law” (Aug. 11, 2025), https://apnews.com/article/924491849641549828c4f52a41d54e6b  
[^9th-pdf]: Ninth Circuit order addressing TRO/preliminary injunction posture (June 19, 2025), https://cdn.ca9.uscourts.gov/datastore/opinions/2025/06/19/25-3727.pdf  
[^lat-stay]: *Los Angeles Times*, “Trump can command National Guard as California’s legal challenge proceeds” (June 20, 2025), https://www.latimes.com/california/story/2025-06-19/9th-circuit-court-of-appeals-rules-on-los-angeles-military-deployment  
[^calmatters-stay]: CalMatters, “Trump can keep troops in LA for now, appeals court rules” (June 19, 2025), https://calmatters.org/justice/2025/06/9th-circuit-los-angeles-national-guard/  
[^brookings-la]: Brookings, “How can the president put soldiers on the streets of Los Angeles?” (June 26, 2025), https://www.brookings.edu/articles/how-can-the-president-put-soldiers-on-the-streets-of-los-angeles/  
[^lawfare-guard]: Lawfare, “The National Guard in Los Angeles” (June 2025), https://www.lawfaremedia.org/article/the-national-guard-in-los-angeles  
[^pbs-law]: PBS NewsHour, “What U.S. law says about Trump’s deployment of active-duty troops to Los Angeles” (June 12, 2025), https://www.pbs.org/newshour/politics/what-u-s-law-says-about-trumps-deployment-of-active-duty-troops-to-los-angeles  
[^vladeck-substack]: Steve Vladeck, “Federalizing the California National Guard” (June 7, 2025), https://www.stevevladeck.com/p/156-federalizing-the-california-national  
[^reuters-dc-surge]: Reuters, “White House ups federal law enforcement at tourist hot spots in Washington, D.C.” (Aug. 8, 2025), https://www.reuters.com/world/us/white-house-ups-federal-law-enforcement-tourist-hot-spots-washington-dc-2025-08-08/  
[^wapo-fbi]: *Washington Post*, “FBI dispatching agents to D.C. streets as Trump weighs calling National Guard” (Aug. 10, 2025), https://www.washingtonpost.com/dc-md-va/2025/08/10/dc-crime-trump-crackdown/  
[^reuters-guard]: Reuters, “U.S. military preparing for National Guard activation in Washington D.C., officials say” (Aug. 11, 2025), https://www.reuters.com/world/us/us-military-preparing-national-guard-activation-washington-dc-officials-say-2025-08-11/  
[^ohio-v-epa]: *Ohio v. EPA*, Nos. 23A349 et al., stay order (June 27, 2024), https://www.supremecourt.gov/opinions/23pdf/23a349_0813.pdf  
[^gibson]: Gibson Dunn client alert, “Supreme Court Grants Stay Suspending EPA’s ‘Good Neighbor’ Plan” (June 27, 2024), https://www.gibsondunn.com/supreme-court-grants-stay-suspending-epas-good-neighbor-emissions-regulation-plan/  
[^murthy]: *Murthy v. Missouri*, 603 U.S. ___ (June 26, 2024), https://www.supremecourt.gov/opinions/23pdf/23-411_3dq3.pdf  
[^mayer]: Mayer Brown, “Decision Alert: *Murthy v. Missouri*” (June 26, 2024), https://www.mayerbrown.com/en/insights/publications/2024/06/decision-alert-murthy-v-missouri-no-23-411  
[^jarkesy]: *SEC v. Jarkesy*, 603 U.S. ___ (June 27, 2024), https://www.supremecourt.gov/opinions/23pdf/22-859_1924.pdf  
[^crs-jarkesy]: CRS Legal Sidebar LSB11229, “SEC v. Jarkesy: Constitutionality of Administrative Adjudication” (Sept. 16, 2024), https://www.congress.gov/crs-product/LSB11229  
[^loper]: *Loper Bright Enterprises v. Raimondo*, 603 U.S. ___ (June 28, 2024), https://www.supremecourt.gov/opinions/23pdf/22-451_7m58.pdf  
[^hls-summary]: Harvard Environmental & Energy Law Program summary (July 12, 2024), https://eelp.law.harvard.edu/wp-content/uploads/2024/07/Loper-Bright-Relentless-Summary.pdf

*Filed: 2025-08-11*
