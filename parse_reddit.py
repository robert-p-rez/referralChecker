import praw, secrets, bs4, requests
from praw.models import MoreComments
import io

reddit = praw.Reddit(client_id=secrets.id,client_secret=secrets.api_key,user_agent=secrets.user_agent)

lines = []
lines = reddit.subreddit('churning').wiki.__getitem__('ccreferrals').content_md.split('*')

for x in list(reversed(range(0,len(lines)))):
    if ')' not in lines[x]:
        lines.remove(lines[x])
    else:
        lines[x] = lines[x].split('[')[1].split(']')[0]


for line in lines:
    submission = reddit.subreddit('churning').search("Official " + line + " Referral",sort='new').next()
    text = {}
    submission.comments.replace_more(limit=0)
    for top_level_comment in submission.comments:
            res = requests.get(top_level_comment.body)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text,'html.parser')
            bodyText = soup.find('body').text.split('\n')
            bodyText = [x for x in bodyText if ';' not in x]
            bodyText = "\n".join(bodyText)
            if bodyText in text.keys():
                text[bodyText] = text[bodyText] + 1
            else:
                with open(str(len(text))+".txt",'w',encoding='utf-8') as f:
                    f.write(bodyText)
                text[bodyText] = 1
    print(10)