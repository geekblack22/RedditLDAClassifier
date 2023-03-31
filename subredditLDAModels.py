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
import time
from progress.bar import ChargingBar




def tokanize_data(text):
    from nltk.corpus import stopwords
    wordnet_lemmatizer = WordNetLemmatizer()
    stopwords = set(stopwords.words('english'))
    tokens = nltk.tokenize.word_tokenize(text.lower()) # split string into words (tokens)
    tokens = [t for t in tokens if t.isalpha()] # keep strings with only alphabets
    tokens = [wordnet_lemmatizer.lemmatize(t) for t in tokens] # put words into base form
    tokens = [t for t in tokens if len(t) > 4] # remove short words, they're probably not useful
    tokens = [t for t in tokens if t not in stopwords] # remove stopwords

    return tokens
def clean_data(comment_bodys):

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
    return cleanded_data,bow_corpus,dictionary


def generate_models(cleanded_data,bow_corpus,dictionary,subrredit,experiment_len):
    num_topics = 10
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
        num_topics += 10
        bar.next()
    bar.finish()
    results = {
        "NumTopics": topics_num_list,
        "ModelScores(u_mass)": model_scores,
        "Topics": model_topics
    }
    experiment_results  =  pd.DataFrame(results)     
    experiment_results.to_excel("excel/experimental_results_lda_"+subrredit+".xlsx")  
    best_model_ind = model_scores.index(min(model_scores))
    max_model = lda_models[best_model_ind]
    # pprint(max_model.print_topics())
    max_model.save("sub_models/Best_Reddit_classifier_"+subrredit+".model")
subbredits = db.get_subredits()
i = 0
for subreddit in subbredits:
    comments = db.get_sub_comments(subreddit)

    cleanded_data,bow_corpus,dictionary = clean_data(comments)
    generate_models(cleanded_data,bow_corpus,dictionary,subreddit,10)
    i+= 1
    print("Yay "+subreddit+" completed thats "+ str(i) + " out of " + str(len(subbredits)))
