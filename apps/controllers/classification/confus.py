import os
from wordcloud import WordCloud, STOPWORDS
from sklearn.metrics import confusion_matrix
import seaborn as sn
import matplotlib.pyplot as plt

def performance(df):
    confus = confusion_matrix(df['analysis_manual'], df['analysis_system'])
    tn, fp, fn, tp = confus.ravel()
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

def confus_plot(y_test, y_predict):
    confus = confusion_matrix(y_test, y_predict)
    sn.heatmap(confus, annot=True, fmt=".0f")
    plt.xlabel("Sistem Label")
    plt.ylabel("Aktual Label")
    plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()
    plt.savefig('apps/static/assets/img/confus_matrix.png')
