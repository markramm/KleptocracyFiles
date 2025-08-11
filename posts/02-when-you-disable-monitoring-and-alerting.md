# Debugging Democracy #2: When You Disable Monitoring and Alerting

*A systems engineer's real-time investigation into institutional capture*

In production, you **never** disable monitoring and alerting before a risky change. On **Jan. 24–25, 2025**, the administration did exactly that to government: it **purged ~17 inspectors general** without the **30‑day notice** Congress requires. [^ig-ap] [^grassley-jud] [^cigie-letter] The watchdogs themselves said the removals were unlawful “nullities.” [^cigie-statement]

## Attacking Telemetry, Budget Edition

By May–August 2025, the **Government Accountability Office (GAO)** issued a drumbeat of **Impoundment Control Act** decisions finding the administration illegally **withheld appropriated funds**, including for **EV chargers (NEVI)** and **NIH research grants**. [^gao-nevi-pdf] [^govexec-nevi] [^gao-nih] [^govexec-nih] The response wasn’t to remediate; it was to **ignore** GAO and move to **slash oversight budgets**, while issuing an executive order to **centralize political control over all federal grants**. [^ap-eo-grants] [^taxpayer-ica] It’s the classic “**kill the telemetry**” move: if you can’t hide anomalies, **defund** or **politicize** the systems that surface them.

## Ethics Enforcement “Paused”

On **Feb. 10, 2025**, the administration **removed the OGE Director** mid‑term and “paused” key federal anti‑corruption enforcement (notably the **FCPA**) pending “review.” (Coverage and legal analyses summarized here.) [^oge-media] This coincided with **Meta** announcing it would **end third‑party fact‑checking** for U.S. political content and move to **Community Notes**, a replacement that independent testing later found had large **coverage and speed gaps**. [^meta-blog] [^wp-meta-test] [^latimes-meta]

## Courts as Failed Circuit Breakers

Even when district courts ruled contested actions **unlawful**, **emergency stays** kept them in effect. In **June 2025**, after Marines were deployed to **Los Angeles** to support a federalized Guard mission, **Judge Charles Breyer** found parts of the deployment **likely unlawful**—but the **Ninth Circuit** stayed his order within hours, preserving the on‑the‑ground status quo during appeal. [^usni-marines] [^calmatters-marines] [^breyer-order] [^9th-stay] This is how a **circuit breaker fails open**: the stay becomes the policy.

## References

[^ig-ap]: Associated Press, *Trump uses mass firing to remove independent inspectors general at a series of agencies*, Jan. 25, 2025. https://apnews.com/article/4e8bc57e132c3f9a7f1c2a3754359993
[^grassley-jud]: Senate Judiciary Committee, *Grassley, Durbin Seek Presidential Explanation for IG Dismissals*, Jan. 28, 2025. https://www.judiciary.senate.gov/press/rep/releases/grassley-durbin-seek-presidential-explanation-for-ig-dismissals
[^cigie-letter]: CIGIE Chair Hannibal “Mike” Ware to the White House, Jan. 24, 2025 (Politico mirror PDF). https://static.politico.com/b3/3e/5baf92224503a3cfa8edb460a1c2/cigie-letter-to-white-house-1-24-2025.pdf
[^cigie-statement]: CIGIE, *Statement from the Chairperson of CIGIE*, Jan. 25, 2025 (PDF). https://www.ignet.gov/sites/default/files/files/CIGIE%20Statement%20--%201_25_2025.pdf

[^gao-nevi-pdf]: GAO, *U.S. DOT FHWA—Application of the Impoundment Control Act to NEVI Plan Approval Memo*, B‑337137, May 22, 2025 (PDF). https://www.gao.gov/assets/880/877916.pdf
[^govexec-nevi]: Government Executive, *GAO: Transportation Department can’t withhold electric‑vehicle infrastructure program funds*, May 22, 2025. https://www.govexec.com/oversight/2025/05/gao-transportation-department-cant-withhold-electric-vehicle-infrastructure-program-funds/405534/
[^gao-nih]: GAO, *HHS—NIH—Application of the ICA to Availability of Funds for Grants*, B‑337203, Aug. 5, 2025. https://www.gao.gov/products/b-337203
[^govexec-nih]: Government Executive, *Trump illegally froze 1,800 NIH medical research grants, Congress’ watchdog says*, Aug. 8, 2025. https://www.govexec.com/oversight/2025/08/trump-illegally-froze-1800-nih-medical-research-grants-congress-watchdog-says/407296/
[^ap-eo-grants]: Associated Press, *Trump executive order gives politicians control over all federal grants, alarming researchers*, Aug. 8, 2025. https://apnews.com/article/4b4b6c23a25a8ae3fdc7b43c4586c999
[^taxpayer-ica]: Taxpayers for Common Sense, *Latest Round of Impoundment Decisions Shows the Importance of the GAO*, Aug. 6, 2025. https://www.taxpayer.net/budget-appropriations-tax/latest-round-of-impoundment-decisions-shows-the-importance-of-the-gao/

[^oge-media]: (Context coverage) See, e.g., New York City Bar, *Firings of Inspectors General Are Illegal and Invalid*, Feb. 10, 2025 (summarizing the 30‑day legal requirement and reactions). https://www.nycbar.org/press-releases/firings-of-inspectors-general-are-illegal-and-invalid/

[^meta-blog]: Meta, *More Speech and Fewer Mistakes*, Jan. 7, 2025. https://about.fb.com/news/2025/01/meta-more-speech-fewer-mistakes/
[^wp-meta-test]: Washington Post, *Zuckerberg fired the fact‑checkers. We tested their replacement.*, Aug. 4, 2025. https://www.washingtonpost.com/technology/2025/08/04/meta-fact-check-community-notes-test-facebook-instagram/
[^latimes-meta]: Los Angeles Times, *Meta replaces fact‑checking with X‑style community notes*, Jan. 7, 2025. https://www.latimes.com/business/story/2025-01-07/meta-replaces-fact-checking

[^usni-marines]: USNI News, *700 Marines from 2/7 Deploy to Los Angeles in Support of DHS Operations*, Jun. 9, 2025. https://news.usni.org/2025/06/09/2-7-marines-deploy-los-angeles-support-dhs
[^calmatters-marines]: CalMatters, *Why are Marines in downtown L.A.?*, Jun. 12, 2025. https://calmatters.org/explainers/2025/06/marines-los-angeles-dhs-operations/
[^breyer-order]: U.S. District Court (N.D. Cal.), *Order re: State of California v. DoD/DHS*, Jun. 12, 2025 (as reported in coverage). (Docket excerpts summarized in CalMatters above.)
[^9th-stay]: U.S. Court of Appeals for the Ninth Circuit, *Administrative Stay Order*, Jun. 19, 2025 (No. 25‑3727) (PDF). https://cdn.ca9.uscourts.gov/datastore/general/2025/06/19/25-3727.pdf

*Filed: 2025-08-11*
