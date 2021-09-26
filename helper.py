from urlextract import URLExtract
extract = URLExtract()
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

f = open('stop_hinglish.txt', 'r')
stop_words = f.read()

def unique_user(df):
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    user_list = [x for x in user_list if not x.startswith('+')]
    return  user_list

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df =df[df['user'] == selected_user]

    #fetch the number of messages
    num_msg = df.shape[0]

    #fetch the number of words
    words = []
    for msg in df['message']:
        words.extend(msg.split())

    #fetch number of media messages shared
    num_media = df[df['message'] == "<Media omitted>\n"].shape[0]

    #fetch number of links shared
    links = []
    for msg in df['message']:
        links.extend(extract.find_urls(msg))

    return num_msg, len(words), num_media, len(links)

#fetch most busy user in the group
def most_busy_users(df):
    x = df['user'].value_counts().head()
    percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'user': 'Percent'})

    return x, percent

def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df =df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']

    words = []
    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):

    if selected_user != "Overall":
        df =df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']

    words = []

    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

    common_words = pd.DataFrame(Counter(words).most_common(20))
    return common_words

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap