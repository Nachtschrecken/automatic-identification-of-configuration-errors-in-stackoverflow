# Implementation of Word2Vec feature extraction and SVM classification
# Using gensim for Word2Vec part
# Using sklearn for SVM part
# Model Name: CM-PaCE (Classification Model for Posts about Configuration Errors)
#
# 2023, Ferris Kleier

import gensim
from gensim.models import Word2Vec
from gensim.parsing.preprocessing import *
import sklearn.svm
from sklearn.model_selection import train_test_split
import numpy as np
import datetime
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import GridSearchCV


CUSTOM_FILTERS = [lambda x: x.lower(), strip_tags, strip_punctuation,
                  remove_stopwords, strip_multiple_whitespaces, strip_numeric, stem_text]


# Word2Vec Functions

def labeled_sets():
    full_set = []
    with open("Posts/positives_body.txt", 'r') as f:
        for line in f:
            line = preprocess_string(line, CUSTOM_FILTERS)
            full_set.append([line, True])
    with open("Posts/negatives_body.txt", 'r') as f:
        for line in f:
            line = preprocess_string(line, CUSTOM_FILTERS)
            full_set.append([line, False])
    return full_set


def get_bodies(set):
    return [row[0] for row in set]


def logging(string):
    with open("Code/cmpace_log.txt", "a") as f:
        f.write("\n\n--------------------------------")
        f.write(string)


# SVM Functions

def get_features(set):
    return [row[1] for row in set]


def get_labels(set):
    return [row[2] for row in set]


def get_featurelength(set):
    max = 0
    for fv in set:
        if len(fv) > max:
            max = len(fv)
    return max


def padding_vecs(set, max):
    padded_vectors = []
    for fv in set:
        padded_vec = [0] * max
        padded_vec[:len(fv)] = fv
        padded_vectors.append(padded_vec)
    return padded_vectors


def get_features_and_labels(data):
    features = np.array(get_features(data))
    labels = np.array(get_labels(data))
    return features, labels


# =========================
# Word2Vec Section
# =========================

train_set, test_set = train_test_split(labeled_sets(), test_size=0.1)


# minimum amount of times a word has to appear in corpus
min_count = 5
# initial learning rate
alpha = 0.01
# iterations over corpus
epochs = 500
# 0 for CBOW, 1 for Skip-Gram
sg = 1
# 1 for hierarchical soft max
hs = 1
# window size for shifting
window = 4


time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
modelName = "Models/Word2Vec/cmpace_w2v_{time}.model".format(time=time)


# create new model
# model = Word2Vec(sentences=get_bodies(train_set), min_count=min_count,
#                  sg=sg, hs=hs, window=window,
#                  alpha=alpha, epochs=epochs, compute_loss=True)
# model.save(modelName)


# load existing model
modelName = "Models/Word2Vec/cmpace_2023-08-21_12:01:16.model"
model = gensim.models.Word2Vec.load(modelName)


logString = f"\n{modelName}\n" + \
    f"min_count = {model.min_count}\n" + \
    f"alpha = {model.alpha}\n" + \
    f"sg = {model.sg}\n" + \
    f"hs = {model.hs}\n" + \
    f"window = {model.window}\n" + \
    f"epochs = {model.epochs}"
lossString = f"\nloss = {model.get_latest_training_loss()}\n"
logString += lossString

wv = model.wv
word_vectors = wv.vectors


# Results

# top 10 relevant words
for index, word in enumerate(wv.index_to_key):
    if index == 11:
        break
    indexString = f"{index}/{len(wv.index_to_key)}: {word}"
    logString += f"\n{indexString}"

# testing with words
w1 = 'config'
w2 = 'error'
w3 = 'configur'
wList = ['configur', 'error', 'invalid', 'java', 'problem', 'cloud']

resString = (
    f"\nSimilarity between {w1} and {w2}:\n{wv.similarity(w1, w2)}\n\n"
    + f"Most similar words for {w1}:\n{wv.most_similar(positive=[w1], topn=5)}\n\n"
    + f"Similarity between {w3} and {w2}:\n{wv.similarity(w3, w2)}\n\n"
    + f"Most similar words for {w3}:\n{wv.most_similar(positive=[w3], topn=5)}\n\n"
    + f"Which does not fit in {wList}:\n{wv.doesnt_match(wList)}\n"
)
logString += f"\n{resString}"


# print(logString)
# logging(logString)


# =========================
# SVM section
# =========================

# Full sets
train_data = [[sentence[0], [wv[word] for word in sentence[0] if word in wv], sentence[1]] for sentence in train_set]
test_data = [[sentence[0], [wv[word] for word in sentence[0] if word in wv], sentence[1]] for sentence in test_set]


# Split the features and labels from the data
train_features, train_labels = get_features_and_labels(train_data)
test_features, test_labels = get_features_and_labels(test_data)


# Data preparation by flattening the feature matrices
flat_train_features = np.array([np.array(sentence).flatten()
                         for sentence in train_features])
max_train = get_featurelength(flat_train_features)
flat_test_features = np.array([np.array(sentence).flatten()
                         for sentence in test_features])
max_test = get_featurelength(flat_test_features)
max = (max_train if max_train > max_test else max_test)

flat_train_features = padding_vecs(flat_train_features, max)
train_features = flat_train_features
flat_test_features = padding_vecs(flat_test_features, max)
test_features = flat_test_features


# Parameter selection

# using grid search to find the best parameters
# param_grid = {'C': [0.001, 0.005, 0.01, 0.02, 0.05],
#               'gamma': [0.00001, 0.00005, 0.0001, 0.0002, 0.0005],
#               'kernel': ['linear']}

# grid_search = GridSearchCV(svm_model, param_grid=param_grid)
# grid_search.fit(train_features, train_labels)

# best_model = grid_search.best_estimator_
# print(best_model)

model_c = 0.01
model_gamma = 0.0001
model_kernel = 'linear'


# Model creation
svm_model = sklearn.svm.SVC(C=model_c, gamma=model_gamma, kernel=model_kernel)
svm_model.fit(train_features, train_labels)


# Results
predictions = svm_model.predict(test_features)

truepos = 0
falseneg = 0
trueneg = 0
falsepos = 0

for prediction,test_label in zip(predictions,test_labels):
    print(prediction,test_label)
    if prediction == False and test_label == False:
        trueneg += 1
    if prediction == True and test_label == True:
        truepos += 1
    if prediction == False and test_label == True:
        falseneg += 1
    if prediction == True and test_label == False:
        falsepos += 1


accuracy = accuracy_score(test_labels, predictions)
precision = precision_score(test_labels, predictions)
recall = recall_score(test_labels, predictions)
f1 = f1_score(test_labels, predictions)

result_string = f"""
Parameters and Results of SVM
C: {model_c}
gamma: {model_gamma}
Kernel: {model_kernel}

Accuracy: {accuracy}
Precision: {precision}
Recall: {recall}
F1 score: {f1}
"""

print(result_string)
logging(result_string)