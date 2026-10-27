# Employer terms audit

Research date: 2026-10-27. This record distinguishes employer-site rules from the third-party job-board API actually queried by the pipeline. It is an evidence inventory, not a legal opinion or proof that a source is authorized for aggregation or republication.

## Provider-level information

The [Lever Postings API documentation](https://github.com/lever/postings-api) says published postings are publicly viewable and may be scraped by third parties. This is a provider statement, not verification of an individual employer's rights or restrictions. The [Greenhouse Job Board API documentation](https://docs.greenhouse.io/job-board.html#authentication) says its GET endpoints do not require authentication, and the [SmartRecruiters Posting API documentation](https://developers.smartrecruiters.com/docs/posting-api) describes access to public postings and customer career-site use. Technical access alone does not verify third-party republication rights.

## Employer policies located

| Registry ID | Official employer policy and evidence | Relationship to the configured endpoint | Status |
| --- | --- | --- | --- |
| `datadog` | [Acceptable Use Policy](https://www.datadoghq.com/legal/acceptable-use/) defines its Service and `www.datadoghq.com` Site and restricts automated retrieval, indexing and scraping of those without prior written consent. | The collector uses `boards-api.greenhouse.io` for Datadog postings. The policy does not clearly establish in the material reviewed whether the hosted Greenhouse API is within that defined scope. | Applicability to this feed and republication remains unverified; request an authoritative determination before marking it cleared. |
| `kpler` | [Terms of Use](https://www.kpler.com/company/terms-of-use) restrict scraping and automated collection of its defined platforms, services and data without written authorization. | The collector uses `api.lever.co` for Kpler postings. The reviewed terms define Kpler platforms around its own website and related platforms, but do not clearly identify the external Lever endpoint. | Applicability to this feed and republication remains unverified; request an authoritative determination before marking it cleared. |
| `agicap` | [Website terms](https://agicap.com/fr/cguv/) restrict reproduction, distribution and certain uses of content on the defined `agicap.com` site without written consent. | The collector uses `api.lever.co` for Agicap postings. The policy does not clearly identify that external API as part of its defined site. | Applicability to this feed and republication remains unverified; request an authoritative determination before marking it cleared. |
| `meritis` | [Legal notice](https://meritis.fr/mentions-legales/) defines the site as `www.meritis.fr` and restricts copying and distribution of its site content without written authorization. | The collector uses `api.smartrecruiters.com` for Meritis public postings. The reviewed notice does not clearly identify that external endpoint as part of the defined site. | Applicability to this feed and republication remains unverified; request an authoritative determination before marking it cleared. |
| `decathlon-digital` | The [Decathlon.com retail website terms](https://www.decathlon.com/pages/terms-of-use) restrict automated access and republication of their defined website. | The configured French technology source uses `boards-api.greenhouse.io`. The retail-domain terms do not establish whether they apply to the separate employer board or this API. | Applicable career-board terms and republication remain unverified; do not treat retail terms as a conclusive determination for the job API. |
| `mendix` | [Mendix website terms](https://www.mendix.com/legal/terms-of-use/) restrict copying or reproduction of content from the defined Mendix Website without written permission. | The collector accesses `api.lever.co` for Mendix postings; the reviewed website terms do not clearly identify that endpoint as part of the defined site. | Applicability to this feed and republication remains unverified; seek a determination before marking it cleared. |
| `shift-technology` | [Shift website terms](https://www.shift-technology.com/de/terms-of-use) identify `www.shift-technology.com` as the Website and restrict copying and distribution without express written authorization. | The configured job feed is on `boards-api.greenhouse.io`, not the specified employer website. | Applicability to this feed and republication remain unverified. |
| `mirakl-labs` | [Mirakl website terms](https://www.mirakl.com/fr-fr/terms-of-service/) identify `www.mirakl.fr` as the Site and restrict extraction and reproduction of its contents. | The configured job feed is on `boards-api.greenhouse.io`; the reviewed terms do not explicitly identify that endpoint. | Applicability to this feed and republication remain unverified. |

The findings above do **not** establish that third-party ATS endpoints are expressly prohibited, nor that they are cleared. The scope of each policy must be evaluated against the exact endpoint and use; do not apply restrictions for a company's separate paid product to a job board automatically.

## Other searches performed

The following narrow public searches located an employer page but did not establish job-feed reuse permission:

- `sfeir`: [SFEIR Institute legal notice](https://institute.sfeir.com/fr/mentions-legales/) restricts reproduction for the Institute website; its scope is not established for the separate Lever job feed.
- `infinit`: [INFINIT's careers page](https://infinit.com/careers) identifies the business. Search results for `infinit.tech` concern a different business and were not used as its terms.
- `swile`: [Swile's legal notice](https://www.swile.co/legal/company-details) identifies its website publisher but does not provide job-feed reuse authorization in the notice.
- `theodo`: [Theodo's legal notice](https://www.theodo.com/mentions-legales) identifies the company website and publisher but does not provide job-feed reuse authorization in the notice.
- `ekimetrics`: [Ekimetrics' legal notice](https://www.ekimetrics.com/zh-cn/legal/legal-notices) identifies the publisher; it is not a job-feed reuse license.
- `doctrine`: [Doctrine's legal notice](https://www.doctrine.fr/mentions-legales) identifies its own site and publisher; it is not a job-feed reuse license.
- `odaseva`: an [Odaseva.com terms document](https://www.odaseva.com/assets/pdf/Odaseva-TermsofUse.pdf) appeared in search, but direct access redirected unexpectedly and its current contents and scope were not verified.
- `algolia`: [Algolia service subscription terms](https://www.algolia.com/policies/terms) are framed around Algolia services and subscribers; their relevance to the external Greenhouse job board was not established.
- `doctolib`: terms located for the separate [Siilo/Doctolib Connect site](https://connect.doctolib.com/nl/legal-notice-terms-of-use) are not evidence of terms for Doctolib's Greenhouse job board.

Focused searches for `beamy`, `winamax`, and `margo-group` did not locate an applicable employer job-feed reuse policy in the material reviewed. These limited searches do not prove no policy exists. Every source listed in this section remains **unknown** for employer-specific reuse authorization. The registry's prior public-access checks and provider documentation remain separate evidence.

To close the source-permission review, the maintainer should record evidence specific to each enabled endpoint and intended reuse, including the policy's scope and retrieval date, or obtain an appropriate authorization. No requests for permission have been sent as part of this audit. A source that provides no clear applicable policy should remain explicitly unresolved rather than being marked approved.
