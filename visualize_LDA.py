
import pandas as pd
import matplotlib.pyplot as plt
import gensim
from gensim.test.utils import datapath
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as mcolors
from os import walk

def beautifyLabel(lable):
    output = ""
    value = int(lable)
    if(value /1000 < 1000):
        output = str(int(value/1000))+"K"
    else:
         output = str(int(value/1000000))+"M"
    return output



def getLable(file):
    label = file.split("_")[-1].replace(".model","").replace(".xlsx","")
    if label == "comments":
        label =  beautifyLabel(file.split("_")[-2].replace("lda","")) + "_" + label
    else:
        label = label + "_subreddit"
    return label

def generate_word_cloud(topics,title):
    cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]  
    fig, axes = plt.subplots(ncols=2,nrows=5, figsize=(10,10), sharex=True, sharey=True)
    
    cloud = WordCloud(
                    background_color='white',
                    width=2500,
                    height=1800,
                    max_words=10,
                    colormap='tab10',
                    color_func=lambda *args, **kwargs: cols[i],
                    prefer_horizontal=1.0)

    for i, ax in enumerate(axes.flatten()):
        fig.add_subplot(ax)
        topic_words = dict(topics[i][1])
        cloud.generate_from_frequencies(topic_words, max_font_size=300)
        plt.gca().imshow(cloud)
        plt.gca().set_title('Topic ' + str(topics[i][0]), fontdict=dict(size=16))
        plt.gca().axis('off')
    fig.suptitle(title, fontsize=16)
    fig.savefig("figures/"+title+".png")
def generate_score_plot(data,label):
    fig = plt.figure()
    scores = data["ModelScores(u_mass)"]
    num_topics = data["NumTopics"]
    plt.plot(num_topics,scores)
    plt.ylabel("ModelScores(u_mass)")
    plt.xlabel("NumTopics")

    plt.title(label)
    fig.savefig("figures/"+label+".png")



def generate_world_clouds():
    mypath = "sub_models"    
    filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file  
    filenames = [file for file in filenames  if(file.split(".")[-1] == "model")]

    for file in filenames:
        model = gensim.models.LdaModel.load(mypath+"/"+file)
        topics = model.show_topics(formatted=False)
        label = getLable(file)
        print(label)
        generate_word_cloud(topics,label)
def generate_score_plots():
    mypath = "excel"    
    filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file 
    for file in filenames:
        label = getLable(file)+"_scores"
        scores_data = pd.read_excel("excel/"+file)
        generate_score_plot(scores_data,label)
generate_score_plot("experimental_results_lpa200000_comments.xlsx")
# generate_score_plots()