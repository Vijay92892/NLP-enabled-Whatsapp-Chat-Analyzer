from urlextract import URLExtract
from wordcloud import WordCloud
extract = URLExtract()
import pandas as pd
from collections import Counter

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    #num of messages
    num_messages = df.shape[0]

    words=[]
    for messages in df['message']:
        words.extend(messages.split())
    num_words = len(words)

    #fetch number of media messages
    num_media_messages = df[df['message'] == ' <Media omitted>'].shape[0]

    #fetch number of links shared
    links=[]
    for messages in df['message']:
        links.extend(extract.find_urls(messages))
    num_links = len(links)


    return num_messages, num_words, num_media_messages,num_links



def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df

def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notificatioin']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    
    wc = WordCloud(width = 500, height = 500, min_font_size = 10, background_color = 'white')
    temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    print(df['message'])
    return df_wc

##Most common words

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notificatioin']
    temp = temp[temp['message'] != '<Media omitted>\n']

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    words = []

    for message in df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    return pd.DataFrame(Counter(words).most_common(20))