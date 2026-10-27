import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from france_tech_jobs.classify import classify


class ClassificationTests(unittest.TestCase):
    def test_french_junior_data_engineer(self):
        result = classify("Ingénieur données junior", "", "Paris, France", "CDI")
        self.assertEqual(result["categories"], ["data"])
        self.assertEqual(result["seniority"], "junior")
        self.assertEqual(result["geography"], "france")
        self.assertTrue(result["eligible"])

    def test_new_graduate_machine_learning_engineer(self):
        result = classify("Graduate Machine Learning Engineer", "", "Lyon, France")
        self.assertEqual(result["categories"], ["ai"])
        self.assertEqual(result["seniority"], "junior")
        self.assertTrue(result["eligible"])

    def test_mid_level_experience_from_description(self):
        result = classify("Software Engineer", "Requires 3 years of professional experience", "Berlin, Germany")
        self.assertEqual(result["categories"], ["software"])
        self.assertEqual(result["seniority"], "mid")
        self.assertEqual(result["geography"], "international")
        self.assertTrue(result["eligible"])

    def test_multiple_relevant_categories(self):
        result = classify("Junior Software Engineer, Generative AI", "", "Toulouse, France")
        self.assertEqual(result["categories"], ["ai", "software"])
        self.assertTrue(result["eligible"])

    def test_french_generative_ai_in_engineering_title(self):
        result = classify("DevOps Cloud/IA générative engineer (H/F)", "3 ans d'expérience", "Paris, France")
        self.assertIn("ai", result["categories"])
        self.assertTrue(result["eligible"])

    def test_generative_ai_product_manager_is_not_an_ai_engineer(self):
        result = classify("Junior GenAI Product Manager", "", "Paris, France")
        self.assertEqual(result["categories"], [])
        self.assertFalse(result["eligible"])

    def test_ai_mentioned_in_data_engineer_description_is_not_a_role_tag(self):
        result = classify("Data Engineer Confirmé(e)", "Expérimenter avec l’IA générative pour booster tes workflows data.", "Lille")
        self.assertEqual(result["categories"], ["data"])
        self.assertEqual(result["seniority"], "mid")
        self.assertTrue(result["eligible"])

    def test_confirmed_english_title_is_mid_level(self):
        result = classify("Data Engineer Confirmed - Core Data Product", "", "Paris, France")
        self.assertEqual(result["seniority"], "mid")
        self.assertTrue(result["eligible"])

    def test_expert_marketing_phrase_does_not_invent_seniority(self):
        result = classify("Data Engineer – Deviens un expert augmenté", "", "Luxembourg")
        self.assertEqual(result["seniority"], "unknown")
        self.assertFalse(result["eligible"])

    def test_expert_engineering_titles_are_excluded(self):
        for title in ("Expert Data Engineer", "Data Engineer Expert"):
            with self.subTest(title=title):
                self.assertEqual(classify(title, "", "France")["seniority"], "excluded")

    def test_international_junior_software_roles_with_known_cities(self):
        for location in ("Hong Kong", "Rotterdam"):
            with self.subTest(location=location):
                result = classify("Junior Software Developer", "", location)
                self.assertEqual(result["geography"], "international")
                self.assertTrue(result["eligible"])

    def test_niort_is_france(self):
        result = classify("GenAI Engineer (F/H) - Niort", "", "Niort")
        self.assertEqual(result["geography"], "france")
        self.assertEqual(result["seniority"], "unknown")

    def test_senior_role_is_excluded(self):
        result = classify("Senior Data Engineer", "", "Paris, France")
        self.assertEqual(result["seniority"], "excluded")
        self.assertFalse(result["eligible"])

    def test_internship_and_alternance_are_excluded(self):
        for title, contract in [("AI Engineer Intern", ""), ("Data Engineer", "Alternance"), ("Développeur logiciel", "Stage")]:
            with self.subTest(title=title, contract=contract):
                result = classify(title, "", "Paris, France", contract)
                self.assertEqual(result["seniority"], "excluded")
                self.assertFalse(result["eligible"])

    def test_unknown_experience_does_not_get_published(self):
        result = classify("Data Engineer", "Build data pipelines", "France")
        self.assertEqual(result["seniority"], "unknown")
        self.assertFalse(result["eligible"])

    def test_remote_without_country_is_unknown(self):
        result = classify("Junior Backend Engineer", "", "Remote")
        self.assertEqual(result["geography"], "unknown")
        self.assertFalse(result["eligible"])

    def test_mixed_country_location_is_ambiguous(self):
        result = classify("Junior Backend Engineer", "", "Paris, France or Berlin, Germany")
        self.assertEqual(result["geography"], "unknown")
        self.assertFalse(result["eligible"])

    def test_job_description_about_mentoring_does_not_make_internship(self):
        result = classify("Junior Software Engineer", "You will mentor interns and collaborate with senior engineers.", "France")
        self.assertEqual(result["seniority"], "junior")
        self.assertTrue(result["eligible"])

    def test_irrelevant_role_is_not_published(self):
        result = classify("Junior Product Manager", "Works with data engineers and machine learning", "France")
        self.assertEqual(result["categories"], [])
        self.assertFalse(result["eligible"])

    def test_experience_ranges_that_cross_levels_are_unknown(self):
        result = classify("Data Engineer", "You have 2-5 years of experience", "Paris")
        self.assertEqual(result["seniority"], "unknown")
        self.assertFalse(result["eligible"])

    def test_unbounded_minimum_does_not_imply_a_maximum(self):
        for description in ("2+ years of experience", "At least 2 years of experience", "Au moins 2 ans d'expérience"):
            with self.subTest(description=description):
                result = classify("Data Engineer", description, "Paris")
                self.assertEqual(result["seniority"], "unknown")
                self.assertFalse(result["eligible"])

    def test_french_experience_and_city(self):
        result = classify("Développeur full stack", "3 ans d'expérience professionnelle", "Toulouse")
        self.assertEqual(result["seniority"], "mid")
        self.assertEqual(result["geography"], "france")
        self.assertEqual(result["categories"], ["software"])
        self.assertTrue(result["eligible"])

    def test_all_requirements_are_checked_even_after_company_history(self):
        description = "Company has 2 years of experience; candidates must have 8 years of experience"
        result = classify("Data Engineer", description, "Paris, France")
        self.assertEqual(result["seniority"], "excluded")
        self.assertFalse(result["eligible"])

    def test_company_experience_does_not_establish_candidate_level(self):
        for description in ("Company has 2 years of experience", "Notre entreprise possède 3 ans d'expérience"):
            with self.subTest(description=description):
                result = classify("Data Engineer", description, "Paris, France")
                self.assertEqual(result["seniority"], "unknown")
                self.assertFalse(result["eligible"])

    def test_company_history_does_not_exclude_junior_candidate(self):
        description = "Our company has 10 years of experience; candidate needs 1-2 years of experience"
        result = classify("Data Engineer", description, "Paris, France")
        self.assertEqual(result["seniority"], "junior")
        self.assertTrue(result["eligible"])

    def test_french_minimum_experience_takes_precedence_over_title(self):
        for description in ("5 ans minimum d’expérience", "5 ans d’expérience minimum", "Au minimum 5 ans d'expérience"):
            with self.subTest(description=description):
                result = classify("Data Engineer junior", description, "Paris, France")
                self.assertEqual(result["seniority"], "excluded")
                self.assertFalse(result["eligible"])

    def test_french_low_minimum_does_not_imply_maximum(self):
        for description in ("2 ans minimum d’expérience", "2 ans d’expérience minimum"):
            with self.subTest(description=description):
                result = classify("Data Engineer junior", description, "Paris, France")
                self.assertEqual(result["seniority"], "unknown")
                self.assertFalse(result["eligible"])

    def test_conflicting_requirements_are_unknown(self):
        result = classify("Data Engineer", "Requires 2 years of experience; requires 3 years of experience", "Paris")
        self.assertEqual(result["seniority"], "unknown")
        self.assertFalse(result["eligible"])

    def test_french_a_partir_de_experience_is_open_ended(self):
        result = classify("Développeur C++ junior", "Vous avez à partir de 2 ans d’expérience en développement.", "Valbonne, France")
        self.assertEqual(result["seniority"], "unknown")
        self.assertFalse(result["eligible"])

    def test_english_hyphenated_front_end_engineering_title(self):
        result = classify("Junior Front-end Developer", "", "Rotterdam")
        self.assertEqual(result["categories"], ["software"])
        self.assertTrue(result["eligible"])

    def test_ai_platform_engineering_in_title(self):
        result = classify("Software Engineer - AI Platform Tooling", "", "Rotterdam")
        self.assertIn("ai", result["categories"])
        self.assertIn("software", result["categories"])
        self.assertFalse(result["eligible"])

    def test_ai_software_engineer_has_both_role_tags(self):
        result = classify("AI Software Engineer", "", "Toulouse")
        self.assertEqual(result["categories"], ["ai", "software"])

    def test_bounded_range_with_qualification_words_spans_both_levels(self):
        result = classify("Junior Software Engineer", "Preferably 2 to 4 years of hands-on software development experience.", "Hong Kong")
        self.assertEqual(result["seniority"], "junior-mid")
        self.assertTrue(result["eligible"])

    def test_junior_intermediate_title_spans_both_levels(self):
        result = classify("Junior / Intermediate Machine Learning Engineer", "", "Paris, France")
        self.assertEqual(result["seniority"], "junior-mid")
        self.assertEqual(result["categories"], ["ai"])
        self.assertTrue(result["eligible"])

    def test_senior_requirement_overrides_range_in_title(self):
        result = classify("Junior / Intermediate Machine Learning Engineer", "Requires 6 years of experience", "Paris, France")
        self.assertEqual(result["seniority"], "excluded")
        self.assertFalse(result["eligible"])

    def test_senior_requirement_with_qualification_words_is_excluded(self):
        result = classify("Junior Software Engineer", "At least 5 years of professional software development experience.", "Paris")
        self.assertEqual(result["seniority"], "excluded")
        self.assertFalse(result["eligible"])


if __name__ == "__main__":
    unittest.main()
