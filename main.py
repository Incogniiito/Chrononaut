from flask import Flask, render_template, redirect, request, jsonify
from squad.demo_prepro import prepro
from basic.demo_cli import Demo
from bs4 import BeautifulSoup
import requests
import re
import os
#import cookielib
import json
import urllib.request

app = Flask(__name__)


demo = Demo()

def getAnswer(paragraph, question):
    pq_prepro = prepro(paragraph, question)
    if len(pq_prepro['x'])>1000:
        return "[Error] Sorry, the number of words in paragraph cannot be more than 1000."
    if len(pq_prepro['q'])>100:
        return "[Error] Sorry, the number of words in question cannot be more than 100."
    return demo.run(pq_prepro)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('file.html', Title='mkg')

@app.route('/submit', methods=['GET', 'POST'])
def Submit():
    if request.method == 'GET':
        id = request.args.get('id')
        question = request.args.get('question')
        paragraph = ''
        answer = ''
        if id == 'mkg':
            paragraph = "I am Mahatma Gandhi. Mahatma Gandhi is very famous in India as “Bapu” or “Rastrapita”. The full name of him is Mohandas Karamchand Gandhi. He was a great freedom fighter who led India as a leader of the nationalism against British rule. He was born on 02 October 1869 in Porbandar, Gujarat, India. He died on 30th of January in 1948. M.K. Gandhi was assassinated by the Hindu activist, Nathuram Godse, who was hanged later as a punishment by the government of India. He has been given another name by the Rabindranath Tagore as “Martyr of the Nation” since 1948."
        if id == 'albert':
            paragraph = "I am Albert Einstein. Albert Einstein was a German American scientist. He is best known for his theories on relativity and theories of matter and heat. Einstein is considered one of the greatest physicists of all time because he is thought to have changed the way one looks at the universe. Einstein was born in Ulm, southern Germany, to Jewish parents. A year after he was born he moved to Munich, Germany. Einstein showed no signs of being a genius at an early age. He did not like to receive instructions in school, therefore his education had to begin at home. He would still have to attend school in Munich though, and would get exceptional grades especially in Mathematics; however, he hated it, a teacher suggested him to leave and just study at home because of his dislike toward the school. Merely his presence caused the other students to disrespect the teachers. A story that Einstein loved to tell was that he once saw a compass and saw that the needle had a northward swing. He knew there was something behind it and he wanted to know the hidden mysteries. Einstein first learned algebra and the pythagora’s theorem when his uncle taught it to him. His uncle would visit the family frequently and was Einstein’s mentor. He would help him and encourage him to go on and never give up. Einstein loved to solve the algebraic and geometrical problems on his own. At the age of twelve he read a couple of books on Euclid Geometry and learned the whole thing on his own. At the age of fourteen he read a few science books and the books had an immense influence on his life."
        if id == 'apj':
            paragraph = "Full name of 'Dr APJ Abdul Kalam' was 'Dr Avul Pakir Jainulabdeen Abdul Kalam'. He was born on 1931-10-15. He was born in at Dhanushkothi in the temple town Rameshwaram in Tamil Nadu. He was born in a poor family, but he was an exceptionally brilliant child. Kalam passed the BSc examination from Saint Joseph College, Thiruchirapalli. He joined Madras Institute of Technology (MIT). His further knowledge in the field got upgraded when he joined Defense Research and Development Organization (DRDO) in 1958 and Indian Space Research Organization (ISRO) in 1963.He is known as the Missile Man of India. The various Indian Missiles of world order like Prithvi, Trishul, Akash, Agni, etc are mainly the result of his efforts and caliber.Dr APJ Abdul Kalam became the 11th President of India. He served the country from 2002 to 2007. For his excellence and brilliance, he was awarded the prestigious Bharat Ratna in 1998; Padma Vibhushan in 1990; and Padma Bhushan in 1981. Dr Kalam expired on Monday 27 July 2015. He suddenly fell unconscious when he was delivering a lecture at the Indian Institute of Management at Shillong. On 30-July-2015, the former President was laid to rest at Rameswaram's Pei Karumbu Ground with full state honours. Over 350,000 people attended the last rites, including the Prime Minister, the governor of Tamil Nadu and the chief ministers of Karnataka, Kerala and Andhra Pradesh.Dr APJ Abdul Kalam was mainly interested in work.He was a bachelor. He was not interested in going abroad. He wanted to serve his motherland first. He said that he thinks his first and foremost duty is to serve his motherland. He was fond of music and the Koran and the Gita. Ever since becoming the head of the Indian State, he had been having interaction with children all over the country. He was by no means a miracle man. His advice to the youngster of the nation was to 'dream dream and convert these into thoughts and later into actions'. "
        question.lower()
        if question == "hello" or question == "hi" or question == "howdie" or question == "namaste":
            if id == 'mkg':
                answer = "Namaste!"
            if id == "albert":
                answer = "Hello, I am Albert Einstien!"
            if id == "apj":
                answer = "Hello Friend!"
        else:
            answer = getAnswer(paragraph, question)
        return answer


@app.route('/pri', methods=['GET', 'POST'])
def pri(question = ''):
    if request.method == 'POST':
        def get_soup(url, header):
            return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')

        # html = urlopen("http://www.google.com/")
        # print(html)
        query = question  # you can change the query for the image  here
        image_type = "ActiOn"
        query = query.split()
        query = '+'.join(query)
        url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"
        # add the directory for your image here
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
            }
        soup = get_soup(url, header)

        ActualImages = []  # contains the link for Large original images, type of  image
        for a in soup.find_all("div", {"class": "rg_meta"}):
            link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
            ActualImages.append((link, Type))

        return str(ActualImages[0][0])

@app.route('/mkg', methods=['GET', 'POST'])
def mkg():
    if request.method == 'GET':
        title = "Mahatma Gandhi"
        return render_template("in.html", Title=title)


@app.route('/albert', methods=['GET', 'POST'])
def albert():
    if request.method == 'GET':
        title = "Albert Einstein"
        return render_template("albert.html", Title=title)



@app.route('/apj', methods=['GET', 'POST'])
def apj():
    if request.method == 'GET':
        title = "APJ Abdul Kalam"
        return render_template("apj.html", Title=title)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=15080)
