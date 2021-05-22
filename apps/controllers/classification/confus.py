from wordcloud import WordCloud, STOPWORDS
from sklearn.metrics import confusion_matrix
import seaborn as sn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


def performance(df):
    print("DATAFRAME",df)
    if df.empty:
        return 0,0,0,""
    else:
        confus = confusion_matrix(df['analysis_manual'], df['analysis_system'])
        tn, fp, fn, tp = confus.ravel()
        accuracy = ((tp + tn)/(tp + tn + fp + fn))*100
        precision = (tp / (tp + fp))*100
        recall = (tp / (tp + fn))*100

        print('accuracy =', accuracy)
        print('precision =', precision)
        print('recall =', recall)

        #plot confus matrix
        fig, ax = plt.subplots()
        ax = sn.heatmap(confus, annot=True, fmt=".0f")
        plt.xlabel("Sistem Label")
        plt.ylabel("Aktual Label")
        plt.gca().invert_yaxis()
        plt.gca().invert_xaxis()
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        plotconfus = "data:image/png;base64,"
        plotconfus += base64.b64encode(pngImage.getvalue()).decode('utf8')

        return accuracy, precision, recall, plotconfus


def cloud(dataframe, backgroundcolor='white', width=800, height=600):
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color=backgroundcolor,
                          width=width, height=height).generate(' '.join(dataframe))
    pngImage = io.BytesIO()
    wordcloud.to_image().save(pngImage, 'PNG')
    pngImage.seek(0)
    return pngImage
