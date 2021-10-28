from bs4 import BeautifulSoup as bs
import urllib.request
import pandas as pd


def get_review_page_url(page=1):
	review_page_url = f"https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page{page}"
	return review_page_url


def get_review_page(page=1):
	url = get_review_page_url(page)
	print(url)
	with urllib.request.urlopen(url) as response:
		html = response.read()
	return html


def process_review_page(reviews_html):
	reviews = []
	for review in reviews_html:
		review_dict = {}

		# get review id
		review_id = review.a["name"]
		# no need to process further if there's no review_id
		if not review_id:
			continue
		review_dict["review_id"] = review_id
		print(review_dict["review_id"])

		# get overall rating
		review_dict["rating"] = get_general_rating(review)

		# get sales visit type
		review_dict["sales_visit_reason"], review_dict["car_purchase_type"] = get_sales_type_visit(review)

		# get username
		review_dict["username"] = get_username(review)

		# get review text
		review_dict["review_text"] = get_review_text(review)

		# specific ratings
		for k, v in get_specific_ratings(review).items():
			review_dict[k] = v

		# get dealer recommendation
		review_dict["recommend_dealer"] = get_dealer_recommendation(review)

		# get employee ratings
		review_dict["employee_ratings"] = get_employee_ratings(review)

		reviews.append(review_dict)
	return reviews


def get_general_rating(review):
	for ratingClass in review.find_all('div', 'rating-static')[0]["class"]:
		if 'rating-' in ratingClass and ratingClass != 'rating-static':
			return str(ratingClass)[len('rating-'):]
	return "0"


def get_sales_type_visit(review):
	sales_visit_reason = review.find('div', class_='col-xs-12 hidden-xs pad-none margin-top-sm small-text dr-grey')
	if sales_visit_reason:
		sales_visit_reason = sales_visit_reason.text
		car_purchase_type = sales_visit_reason.split('-')[-1].strip()
	else:
		sales_visit_reason = ""
		car_purchase_type = ""

	return sales_visit_reason, car_purchase_type


def get_username(review):
	username = review.find('span', class_='italic font-18 black notranslate')
	if username:
		username = username.text.split('-')[-1].strip()
	else:
		username = ""
	return username


def get_review_text(review):
	review_text = review.find('p', class_='font-16 review-content margin-bottom-none line-height-25')
	if review_text:
		review_text = review_text.text
	else:
		review_text = ""
	return review_text


def get_specific_ratings(review):
	review_dict = {"customer_service": 0, "friendliness": 0, "pricing": 0, "overall_experience": 0}
	specific_ratings = review.find('div', class_='review-ratings-all')
	for rating in specific_ratings.find_all('div', 'tr'):
		rating_category = rating.find('div', "lt-grey")
		if rating_category:
			rating_category = rating_category.text.casefold().replace(" ", "_")

			indiv_rating = rating.find('div', "rating-static-indv")
			if indiv_rating:
				for ratingClass in indiv_rating["class"]:
					if 'rating-' in ratingClass and ratingClass != 'rating-static-indv' and rating_category in review_dict:
						review_dict[rating_category] = str(ratingClass)[len('rating-'):]
	return review_dict


def get_dealer_recommendation(review):
	recommend_dealer = review.find('div', class_="td small-text boldest")
	if recommend_dealer:
		recommend_dealer = str(recommend_dealer.text).strip()
	else:
		recommend_dealer = ""
	return recommend_dealer


def get_employee_ratings(review):
	ratings_css = 'pull-left font-14 boldest lt-grey line-height-1 pad-right-sm margin-right-sm border-right'

	def employee_ratings_null_check(emp_rating):
		return emp_rating.find('a', "notranslate") and emp_rating.find('a', "notranslate").has_attr('data-emp-id') and emp_rating.find('span', ratings_css)

	employee_ratings = review.find_all('div', class_='col-xs-12 col-sm-6 col-md-4 pad-left-none pad-top-sm pad-bottom-sm review-employee')
	return [(emp_rating.find('a', "notranslate")["data-emp-id"], emp_rating.find('a', "notranslate").text.strip(), emp_rating.find('span', ratings_css).text.strip()) for emp_rating in employee_ratings if employee_ratings_null_check(emp_rating)]


def get_5_pages_of_reviews():
	reviews = []
	for page in range(1, 6):
		html = get_review_page(page)
		soup = bs(html, 'html.parser')
		reviews.extend(process_review_page(soup.find_all("div", "review-entry")))
	pd.DataFrame(reviews).to_csv("data/reviews.csv", index=False)


if __name__ == '__main__':
	get_5_pages_of_reviews()
