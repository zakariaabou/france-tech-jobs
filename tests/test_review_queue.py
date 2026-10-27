"""Tests for clearly identified, conservatively selected review candidates."""

import unittest

from france_tech_jobs.render import render_all, render_review_page


def candidate(**overrides):
    job = {
        "source_id": "company-board", "sources": ["company-board"],
        "job_id": "1", "company": "Acme", "title": "AI Engineer",
        "location": "Paris, France", "geography": "france", "seniority": "unknown",
        "categories": ["ai"], "status": "active", "eligible": False,
        "application_url": "https://example.com/jobs/1", "first_seen": "2026-10-27",
    }
    job.update(overrides)
    return job


class ReviewPageTests(unittest.TestCase):
    def test_ambiguous_experience_and_location_are_explained(self):
        page = render_review_page([candidate(geography="unknown", location="Remote")], "2026-10-27")
        self.assertIn("Experience level not confirmed", page)
        self.assertIn("Location not confirmed", page)
        self.assertIn("Remote", page)
        self.assertIn("company-board", page)
        self.assertIn("https://example.com/jobs/1", page)

    def test_only_active_ambiguous_engineering_roles_are_displayed(self):
        jobs = [candidate(), candidate(job_id="2", status="unknown", title="Stale AI Engineer"),
                candidate(job_id="3", status="closed", title="Closed AI Engineer"),
                candidate(job_id="4", seniority="excluded", title="Senior AI Engineer"),
                candidate(job_id="5", title="AI Engineer Intern"),
                candidate(job_id="6", title="Senior AI Engineer"),
                candidate(job_id="7", title="AI Engineer", contract="Alternance"),
                candidate(job_id="8", categories=[], title="Product Manager"),
                candidate(job_id="9", seniority="mid", geography="france", eligible=True, title="Confirmed AI Engineer"),
                candidate(job_id="10", seniority="senior", geography="unknown", title="Explicit seniority AI Engineer")]
        page = render_review_page(jobs, "2026-10-27")
        self.assertIn("| AI Engineer |", page)
        for forbidden in ("Stale AI Engineer", "Closed AI Engineer", "Senior AI Engineer", "AI Engineer Intern", "Product Manager", "Confirmed AI Engineer", "Alternance", "Explicit seniority AI Engineer"):
            self.assertNotIn(forbidden, page)

    def test_only_uncertain_reasons_are_shown(self):
        page = render_review_page([candidate(seniority="mid", geography="unknown")], "2026-10-27")
        self.assertIn("Location not confirmed", page)
        self.assertNotIn("Experience level not confirmed", page)
        self.assertIn("| mid |", page)

    def test_untrusted_markdown_and_urls_are_safe(self):
        page = render_review_page([candidate(company="A | *B*", title="AI `Engineer`", sources=["one|two"], application_url="javascript:alert(1)")], "2026-10-27")
        self.assertIn(r"A \| \*B\*", page)
        self.assertIn(r"AI \`Engineer\`", page)
        self.assertIn(r"one\|two", page)
        self.assertNotIn("javascript:", page)
        self.assertIn("Unavailable", page)

    def test_limit_is_visible_and_prioritizes_france(self):
        jobs = [candidate(job_id="a", title="International AI Engineer", geography="international", first_seen="2026-10-28"),
                candidate(job_id="b", title="France AI Engineer", geography="france", first_seen="2026-10-27")]
        page = render_review_page(jobs, "2026-10-28", limit=1)
        self.assertIn("France AI Engineer", page)
        self.assertNotIn("International AI Engineer", page)
        self.assertIn("1 of 2", page)

    def test_render_all_creates_review_page_and_keeps_confirmed_views(self):
        confirmed = candidate(seniority="mid", eligible=True)
        pages = render_all([confirmed], "2026-10-27", review_jobs=[candidate()])
        self.assertIn("jobs/review.md", pages)
        self.assertIn("AI Engineer", pages["jobs/france-ai.md"])
        self.assertIn("Experience level not confirmed", pages["jobs/review.md"])

    def test_international_candidates_remain_accessible_with_france_first_limit(self):
        jobs = [candidate(title="France AI Engineer"), candidate(title="International AI Engineer", geography="international", location="Berlin, Germany")]
        pages = render_all([], "2026-10-27", review_jobs=jobs, review_limit=1)
        self.assertIn("France AI Engineer", pages["jobs/review-france.md"])
        self.assertIn("International AI Engineer", pages["jobs/review-international.md"])
        self.assertNotIn("France AI Engineer", pages["jobs/review-international.md"])
