import pickle

import pandas as pd
from nltk import tokenize
from nltk.corpus import stopwords
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.neural_network import MLPClassifier

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

stop = stopwords.words("english")


def clean_text(text):
	# remove stop words
	return ' '.join(' '.join(word for word in tokenize.word_tokenize(sentence) if word not in stop) for sentence in tokenize.sent_tokenize(text))


# get models
def get_lr():
	return LogisticRegression(max_iter=100000)


def get_naive_bayes():
	return MultinomialNB()


def get_gradient_boosting():
	return GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)


def get_multilayer_perceptron():
	return MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)


def get_random_forest():
	return RandomForestClassifier(n_estimators=10)


# build model
def build_model(model, x_train, y_train, x_test, y_test):
	model.fit(x_train, y_train)
	pred = model.predict(x_test)
	score = accuracy_score(y_test, pred)
	return model, score


def process_dealer_reviews(model, le, cv):
	# use on dealership reviews
	reviews_df = pd.read_csv("data/reviews.csv")
	x = reviews_df.review_text.apply(clean_text)
	reviews_df["truthful_review"] = le.inverse_transform(model.predict(cv.transform(x)))

	from find_suspect_reviews import analyze_reviews
	analyze_reviews(reviews_df[reviews_df["truthful_review"] == 'deceptive'])


def find_best_model(df):
	# encode output
	print("encoding output")
	le = LabelEncoder()
	y = le.fit_transform(df['deceptive'])

	# clean text
	print("cleaning text")
	x = df['text'].apply(clean_text)

	x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0, test_size=0.2)

	# TF-IDF vectorize the inputs
	print("vectorize outputs")
	vectorizer = TfidfVectorizer(ngram_range=(1, 4))
	x_train = vectorizer.fit_transform(x_train)
	x_test = vectorizer.transform(x_test)

	# find best model
	print("finding best model")
	model_funcs = [get_lr, get_naive_bayes, get_gradient_boosting, get_multilayer_perceptron, get_random_forest]
	best_model, acc = max((build_model(func(), x_train, y_train, x_test, y_test) for func in model_funcs), key=lambda res: res[1])
	with open("data/model.pkl", "wb") as f:
		pickle.dump(best_model, f)
		print("model saved")

	# use best model
	with open("data/model.pkl", "rb") as f:
		model = pickle.load(f)
	print("using best model")
	process_dealer_reviews(model, le, vectorizer)


def get_data():
	df = pd.read_csv('data/deceptive-opinion.csv')
	df.drop(["hotel", "source"], axis=1, inplace=True)
	return df


def analyze():
	df = get_data()
	find_best_model(df)


if __name__ == '__main__':
	analyze()

