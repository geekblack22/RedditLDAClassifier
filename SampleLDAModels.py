import reddit_db as db
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from pprint import pprint
from nltk.corpus import stopwords
import time
from progress.bar import ChargingBar
# nltk.download('punkt')
# nltk.download('omw-1.4')
# nltk.download('stopwords')
wordnet_lemmatizer = WordNetLemmatizer()
num_comments = 200000
comment_bodys = db.get_comment_bodys(num_comments)
print("Loaded "+ str(len(comment_bodys))+  " comments")
stopwords = set(stopwords.words('english'))
def tokanize_data(text):
    tokens = nltk.tokenize.word_tokenize(text.lower()) # split string into words (tokens)
    tokens = [t for t in tokens if t.isalpha()] # keep strings with only alphabets
    tokens = [wordnet_lemmatizer.lemmatize(t) for t in tokens] # put words into base form
    tokens = [t for t in tokens if len(t) > 4] # remove short words, they're probably not useful
    tokens = [t for t in tokens if t not in stopwords] # remove stopwords

    return tokens
start_time = time.time()
comments = pd.DataFrame(comment_bodys,columns=["Content"])
print("Tokanizing Data")
cleanded_data = comments["Content"].apply(tokanize_data)
print("Data tokanized")

print("Creating bag of words")
# Create a dictionary for vocabulary words with it's index and count
dictionary = gensim.corpora.Dictionary(cleanded_data)
# filter words that occurs in less than 5 documents and words that occurs in more than 50% of total documents
# keep top 100000 frequent words
dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=100000)
# crete bag-of-words ==> list(index, count) for words in doctionary
bow_corpus = [dictionary.doc2bow(doc) for doc in cleanded_data]
# Create a lda model with tf-idf vectorized corpus and dictionary
# Manually pick number of topic and then based on perplexity scoring, tune the number of topics


def generate_models(experiment_len):
    num_topics = 50
    lda_models = []
    model_scores = []
    model_topics = []
    topics_num_list = []
    bar = ChargingBar('Generating Models', max=experiment_len)
    for i in range(0,experiment_len):
        model = gensim.models.LdaModel(bow_corpus,
                                    id2word=dictionary,
                                    num_topics = num_topics)
        lda_models.append(model)
        coherence_model_lda = gensim.models.CoherenceModel(model=model, texts=cleanded_data, dictionary=dictionary, coherence='u_mass')
        coherance_score = coherence_model_lda.get_coherence()
        model_scores.append(coherance_score)
        model_topics.append(model.print_topics(num_topics=-1))
        topics_num_list.append(num_topics)
        # print("Number of Topics: "+str(num_topics))
        # # print("Model Scores: "+ str(coherance_score))
        # print("------Topics-------")
        # print(model_topics[i])
        num_topics += 50
        bar.next()
    bar.finish()
    results = {
        "NumTopics": topics_num_list,
        "ModelScores(u_mass)": model_scores,
        "Topics": model_topics
    }
    experiment_results  =  pd.DataFrame(results)     
    experiment_results.to_excel("experimental_results_lpa"+str(num_comments)+"_comments.xlsx")  
    best_model_ind = model_scores.index(min(model_scores))
    max_model = lda_models[best_model_ind]
    # pprint(max_model.print_topics())
    max_model.save("Best_Reddit_classifier_"+str(num_comments)+"_comments.model")
generate_models(10)




