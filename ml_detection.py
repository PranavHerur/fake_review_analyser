import pickle

import pandas as pd
from nltk import tokenize
from nltk.corpus import stopwords

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB


stop = stopwords.words("english")


def clean_text(text):
	return ' '.join(' '.join(word for word in tokenize.word_tokenize(sentence) if word not in stop) for sentence in tokenize.sent_tokenize(text))


def get_lr(x_train, y_train, x_test, y_test):
	return build_model(LogisticRegression(max_iter=100000), x_train, y_train, x_test, y_test)


def get_naive_bayes(x_train, y_train, x_test, y_test):
	return build_model(MultinomialNB(), x_train, y_train, x_test, y_test)


def build_model(model, x_train, y_train, x_test, y_test):
	model.fit(x_train, y_train)
	pred = model.predict(x_test)
	score = accuracy_score(y_test, pred)
	print(score)
	return model, score


def process_dealer_reviews(model, le, cv):
	# use on dealership reviews
	reviews_df = pd.read_csv("data/reviews.csv")
	x = reviews_df.review_text.apply(clean_text)
	reviews_df["truthful_review"] = le.inverse_transform(model.predict(cv.transform(x)))
	# print(reviews_df[reviews_df["truthful_review"] == 'deceptive'].head().to_string())

	from find_suspect_reviews import analyze_reviews
	analyze_reviews(reviews_df[reviews_df["truthful_review"] == 'deceptive'])


def find_best_model(df):
	le = LabelEncoder()
	y = le.fit_transform(df['deceptive'])
	x = df['text'].apply(clean_text)
	x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0, test_size=0.2)

	vectorizer = TfidfVectorizer(ngram_range=(1, 4))
	x_train = vectorizer.fit_transform(x_train)
	x_test = vectorizer.transform(x_test)

	max_acc = 0
	best_model = None
	for func in [get_lr, get_naive_bayes]:
		model, acc = func(x_train, y_train, x_test, y_test)

		if acc > max_acc:
			max_acc = acc
			best_model = model
	with open("data/model.pkl", "wb") as f:
		pickle.dump(best_model, f)

	with open("data/model.pkl", "rb") as f:
		model = pickle.load(f)
	process_dealer_reviews(model, le, vectorizer)


def get_data():
	df = pd.read_csv('data/deceptive-opinion.csv')
	df.drop(["hotel", "source"], axis=1, inplace=True)
	print(df.head().to_string())
	return df


def analyze():
	df = get_data()
	find_best_model(df)


if __name__ == '__main__':
	analyze()

