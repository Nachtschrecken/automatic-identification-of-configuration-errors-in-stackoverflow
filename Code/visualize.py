# Visualizing the Word2Vec gensim model to better see relations in data
# Loads a trained gensim model
#
# 2023, Ferris Kleier


from sklearn.manifold import TSNE
import numpy as np
import gensim
import datetime


def reduce_dimensions(model):
    num_dimensions = 2

    vectors = np.asarray(model.wv.vectors)
    labels = np.asarray(model.wv.index_to_key)

    tsne = TSNE(n_components=num_dimensions, random_state=0)
    vectors = tsne.fit_transform(vectors)

    x_vals = [v[0] for v in vectors]
    y_vals = [v[1] for v in vectors]
    return x_vals, y_vals, labels


def plot(x_vals, y_vals, labels):
    import matplotlib.pyplot as plt
    import random

    random.seed(0)

    plt.figure(figsize=(12, 12))
    plt.scatter(x_vals, y_vals)

    indices = list(range(len(labels)))
    selected_indices = random.sample(indices, 25)
    for i in selected_indices:
        plt.annotate(labels[i], (x_vals[i], y_vals[i]))

    plt.title(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
    plt.show()


def visualize(model):
    x_vals, y_vals, labels = reduce_dimensions(model)
    plot(x_vals, y_vals, labels)


model = gensim.models.Word2Vec.load("Models/cmpace_2023-08-17_20:13:18.model")
x_vals, y_vals, labels = reduce_dimensions(model)
plot(x_vals, y_vals, labels)
