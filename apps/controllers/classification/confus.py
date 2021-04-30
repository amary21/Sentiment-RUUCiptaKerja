from wordcloud import WordCloud, STOPWORDS
from sklearn.metrics import confusion_matrix

def performance(df):
    confus = confusion_matrix(df['analysis_manual'], df['analysis_system'])
    tp = confus[0][0]
    fp = confus[0][1]
    fn = confus[1][0]
    tn = confus[1][1]
    accuracy = ((tp + tn)/(tp + tn + fp + fn))*100
    precision = (tp / (tp + fp))*100
    recall = (tp / (tp + fn))*100

    print('accuracy =', accuracy)
    print('precision =', precision)
    print('recall =', recall)
    return accuracy, precision, recall


def cloud(dataframe, backgroundcolor='white', width=800, height=600):
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color=backgroundcolor,
                          width=width, height=height).generate(' '.join(dataframe))
    wordcloud.to_file('apps/static/assets/img/word_cloud.png')
