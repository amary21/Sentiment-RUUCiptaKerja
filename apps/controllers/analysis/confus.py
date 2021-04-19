from apps import db
from apps.models.confusmatrix import ConfusMatrix
from wordcloud import WordCloud, STOPWORDS

def get_confus_lastdate():
    sub_query = db.session.query(ConfusMatrix.true_positive, ConfusMatrix.false_positive, ConfusMatrix.false_negative,
                                 ConfusMatrix.true_negative, db.func.max(ConfusMatrix.accuracy_date).label('date')).subquery()
    query = ConfusMatrix.query.join(
        sub_query, (sub_query.c.date == ConfusMatrix.accuracy_date))
    print(query)
    return query.first()

def performance():
    cl = get_confus_lastdate()
    accuracy = ((cl.true_positive + cl.true_negative)/(cl.true_positive +cl.true_negative + cl.false_positive + cl.false_negative))*100
    precision = (cl.true_positive / (cl.true_positive + cl.false_positive))*100
    recall = (cl.true_positive / (cl.true_positive + cl.false_negative))*100

    print('accuracy =', accuracy)
    print('precision =', precision)
    print('recall =', recall)
    return accuracy, precision, recall


def cloud(dataframe, backgroundcolor='white', width=800, height=600):
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color=backgroundcolor,
                          width=width, height=height).generate(' '.join(dataframe))
    wordcloud.to_file('apps/static/assets/img/word_cloud.png')
