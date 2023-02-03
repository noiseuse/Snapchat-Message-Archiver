import json
import datetime
from operator import itemgetter

def create_time(old_date) -> datetime.datetime:
    date_to_split = old_date[0:10]
    time_to_split = old_date[11:19]
    datelist = date_to_split.split('-')
    timelist = time_to_split.split(':')
    date = datetime.datetime(int(datelist[0]), int(datelist[1]), int(datelist[2]), int(timelist[0]), int(timelist[1]), int(timelist[2]))

    return date

def main():
    inputfile = input("Enter json file you want to read: ")
    with open(inputfile) as f:
        data = json.load(f)

    filename = input("Enter Filename: ")
    title = input("Enter Title for Document: ")
    user1 = input("Enter the Snapchat username of the person who you want to read your messages with: ")
    user2 = input("Enter your name: ")
    txt = open(filename, "w")

    all_texts = []
    merged = []
    string = "\n" + title + "\n\n"
    date = datetime.datetime(2,3,4)

    for message in data['Received Saved Chat History']:
        recieved = {}
        if message['From'] == user1 and message['Media Type'] == 'TEXT':
            recieved['whom'] = user1
            recieved['text'] = message['Text']
            recieved['date'] = create_time(message['Created'])
            all_texts.append(recieved)

    for message in data['Sent Saved Chat History']:
        sent = {}
        if message['To'] == user1 and message['Media Type'] == 'TEXT':
            sent['whom'] = user2
            sent['text'] = message['Text']
            sent['date'] = create_time(message['Created'])
            all_texts.append(sent)
    merged = sorted(all_texts, key=lambda k: k['date'])

    previous = ""

    for message in merged:
        shortened = f"{message['date'].strftime('%B %-d, %Y')}"
        if shortened != date:
            string += "\n"
            string += "\n"
            string += f"{message['date'].strftime('%B %-d, %Y')}\n\n"
        if message['whom'] != previous or shortened != date:
            string += f"{message['whom']}: {message['text']}\n"
        else:
            string += f"      {message['text']}\n"
        date = shortened
        previous = message['whom']
    txt.write(string)

    txt.close()
    f.close()

    print("Finished Running")

if __name__ == '__main__':
    main()
