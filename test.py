import unittest
from bs4 import BeautifulSoup as soup


class TestCrawler(unittest.TestCase):

	def test_upper(self):
		from main import get_review_page_url
		self.assertEqual(get_review_page_url(), "https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page1")
		self.assertEqual(get_review_page_url(2), "https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page2")
		self.assertEqual(get_review_page_url(3), "https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page3")
		self.assertEqual(get_review_page_url(4), "https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page4")
		self.assertEqual(get_review_page_url(5), "https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page5")

	def test_review_info_extractor(self):
		from main import process_review_page
		from test_review_html import test_html

		results = process_review_page([soup(test_html, 'html.parser')])
		test_results = [{'review_id': 'r8764447', 'rating': '50', 'sales_visit_reason': 'SALES VISIT - USED', 'car_purchase_type': 'USED', 'username': 'Abygail', 'review_text': 'First time to finance and was super nervous but they made the process so easy and help me understand every little detail! Adrian was quick to help me find the PERFECT vehicle that’s reliable, affordable and something I am going to love for a long time!!!! ', 'customer_service': '50', 'friendliness': '50', 'pricing': '50', 'overall_experience': '50', 'recommend_dealer': 'Yes', 'employee_ratings': [('273456', 'Adrian "AyyDee" Cortes', '5.0'), ('640356', 'Taylor Prickett', '5.0')]}]
		self.assertEqual(results, test_results)

		results = process_review_page([soup("", 'html.parser')])
		self.assertEqual(results, [])

	def test_general_rating_extractor(self):
		from main import get_general_rating
		from test_review_html import general_rating_test_html, general_rating_test_html_501, general_rating_test_html_empty

		results = get_general_rating(soup(general_rating_test_html, 'html.parser'))
		self.assertEqual(results, '50')

		results = get_general_rating(soup(general_rating_test_html_501, 'html.parser'))
		self.assertEqual(results, '501')

		results = get_general_rating(soup(general_rating_test_html_empty, 'html.parser'))
		self.assertEqual(results, '')

	def test_sales_type_extractor(self):
		from main import get_sales_type_visit
		from test_review_html import general_rating_test_html, general_rating_test_html_empty

		results = get_sales_type_visit(soup(general_rating_test_html, 'html.parser'))
		self.assertEqual(results, ('SALES VISIT - USED', 'USED'))

		results = get_sales_type_visit(soup(general_rating_test_html_empty, 'html.parser'))
		self.assertEqual(results, ('', ''))

	def test_username_extractor(self):
		from main import get_username
		from test_review_html import username_test_html, username_test_html_empty

		results = get_username(soup(username_test_html, 'html.parser'))
		self.assertEqual(results, 'Abygail')

		results = get_username(soup(username_test_html_empty, 'html.parser'))
		self.assertEqual(results, '')

	def test_review_text_extractor(self):
		from main import get_review_text
		from test_review_html import review_text_test_html, review_text_test_html_empty

		test_review_text = 'First time to finance and was super nervous but they made the process so easy and help me understand every little detail! Adrian was quick to help me find the PERFECT vehicle that’s reliable, affordable and something I am going to love for a long time!!!! '
		results = get_review_text(soup(review_text_test_html, 'html.parser'))
		self.assertEqual(results, test_review_text)

		results = get_review_text(soup(review_text_test_html_empty, 'html.parser'))
		self.assertEqual(results, "")

	def test_specific_rating_info_extractor(self):
		from main import get_specific_ratings
		from test_review_html import specific_ratings_test_html, specific_ratings_test_html_complex_ratings

		results = get_specific_ratings(soup(specific_ratings_test_html, 'html.parser'))
		for k,v in results.items():
			self.assertEqual(v, '50')

		review_dict_test = {"customer_service": 11, "friendliness": 12, "pricing": 67, "overall_experience": 490}
		results = get_specific_ratings(soup(specific_ratings_test_html_complex_ratings, 'html.parser'))
		for k,v in results.items():
			self.assertEqual(v, str(review_dict_test[k]))

	def test_dealer_recommendation_extractor(self):
		from main import get_dealer_recommendation
		from test_review_html import specific_ratings_test_html, specific_ratings_test_html_complex_ratings

		results = get_dealer_recommendation(soup(specific_ratings_test_html, 'html.parser'))
		self.assertEqual(results, 'Yes')

		results = get_dealer_recommendation(soup(specific_ratings_test_html_complex_ratings, 'html.parser'))
		self.assertEqual(results, '')

	def test_employee_ratings_extractor(self):
		from main import get_employee_ratings
		from test_review_html import employee_ratings_test_html, employee_ratings_test_html_complex

		results = get_employee_ratings(soup(employee_ratings_test_html, 'html.parser'))
		self.assertEqual(results, [('273456', 'Adrian "AyyDee" Cortes', '5.0'), ('640356', 'Taylor Prickett', '5.0')])

		results = get_employee_ratings(soup(employee_ratings_test_html_complex, 'html.parser'))
		self.assertEqual(results, [('273456', 'Adrian "AyyDee" Cortes', '5.0')])


if __name__ == '__main__':
	unittest.main()
