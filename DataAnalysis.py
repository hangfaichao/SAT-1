import matplotlib.pyplot as plt
import numpy as np
import math
import string
import re
import nltk
from nltk.stem import SnowballStemmer
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter

class Commit(object):
    def __init__(self, number = '', sha = '', dist = '', log = ''):
        self.number = number
        self.sha = sha
        self.dist = dist
        self.log = log

def get_numbers_shas_dists_files_logs(path):
    f = open(path, 'r', encoding = 'utf-8')
    lines = f.readlines()
    numbers, shas, dists, logs = [], [], [], []
    for idx, line in enumerate(lines):
        words = line.split(" ")
        numbers.append(idx)
        shas.append(words[0])
        dists.append(int(words[1]))
        logs.append(" ".join(words[2:]))
    f.close()
    return numbers, shas, dists, logs
    
def get_times_logs(path, shas):
    f = open(path, 'r', encoding = 'utf-8')
    lines = f.readlines()
    times, logs = [], []
    for line in lines:
        words = line.split("'")
        shas.append
        times.append(words[1].strip())
        logs.append(words[2].strip())
    f.close()
    return times, logs

def get_logs(path):
    f = open(path, 'r', encoding = 'utf-8')
    lines = f.readlines()
    logs = []
    for line in lines:
        words = line.split(" ")
        logs.append(" ".join(words[2:]))
    f.close()
    return logs


def rq4(commits, percent, window):
    threshold = getThreshold(commits, percent)
    #print(threshold)
    commits.sort(key = lambda x:x.number, reverse = False)
    cnt = 0
    commits_big_continuous = []
    segment_count = 0
    for i in range(len(commits) - window):
        if commits[i].dist < threshold:
            if cnt >= window:
                commits_big_continuous.append(Commit())
                segment_count += 1
            cnt = 0
        else:
            cnt += 1
        if cnt == window:
            for n in range(window):
                commits_big_continuous.append(commits[i-window+n+1])
        if cnt > window:
            commits_big_continuous.append(commits[i])
    
    output_commits("big_continuous", commits_big_continuous)
    print('total ', segment_count, ' segment')

def output_commits(filename, commits):
    path = "commits_"
    f = open(path + filename, 'w', encoding = 'utf-8')
    for commit in commits:
        f.write(str(commit.number) + ' ' + str(commit.dist) + ' ' + commit.log + "\n")
    f.close()

def output_keywords(filename, c):
    path = "keywords_"
    f = open(path + filename, 'w', encoding = 'utf-8')
    for k, v in c:
        f.write(str(k) + ' ' + str(v) + ' ' + "\n")
    f.close()

def rq3():
    
    path_base = "commits_"
    for filename in ["big", "small"]:
        logs = get_logs(path_base + filename)
        text = " ".join([log for log in logs])
        #text = "Life is like a box of chocolates. You never know what you're gonna get."
        raw_words = re.findall(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*", text.lower())
        table = str.maketrans('','', string.punctuation)
        filtered_words = [word.translate(table) for word in raw_words if word not in stopwords.words('english') and len(word) > 1]

        #snowball_stemmer = SnowballStemmer("english")

        #words_stem = [snowball_stemmer.stem(filtered_word) for filtered_word in filtered_words]

        wordnet_lematizer = WordNetLemmatizer()
        words_lema = [wordnet_lematizer.lemmatize(filtered_word) for filtered_word in filtered_words]
        c = Counter()
        for word_lema in words_lema:
            c[word_lema] += 1
        words = c.most_common(100)
        output_keywords(filename, words)


def dataGenerate(path_dist):
    numbers, shas, dists, logs = get_numbers_shas_dists_files_logs(path_dist)

    commits = []
    for i in range(len(numbers)):
        commits.append(Commit(numbers[i], shas[i], dists[i], logs[i]))

    return commits
    
def getThreshold(commits, percent):
    commits.sort(key = lambda x: x.dist, reverse = False)
    return commits[int(len(commits)*percent)].dist

def bigandsmall(commits):
    commits.sort(key = lambda x:x.dist, reverse = False)
    output_commits("big", commits[-50:])
    output_commits("small", commits[:50])

def rq1(commits):
    commits.sort(key = lambda x: x.number, reverse = False)
    numbers = [commit.number for commit in commits]
    dists = [commit.dist for commit in commits]
    average = sum(dists) / len(dists)
    plt.figure()
    l1, = plt.plot(numbers, dists, 'r', label = "distance")
    l3, = plt.plot(numbers, [average]*len(dists), '-.r', label = 'distance_avg')
    plt.xlabel('commit numbers')
    plt.ylabel('distance')
    plt.legend(handles = [l1, l3], loc = 'upper right')
    plt.show()
    plt.figure()
    plt.hist([math.log10(dist) if dist != 0 else 0 for dist in dists], bins = 20)
    plt.xlabel('$log_{10}(distance)$')
    plt.ylabel('count')
    plt.show()

def rq2(path):
    f = open(path, 'r', encoding = 'utf-8')
    lines = f.readlines()
    versions, versions_func, versions_bug, dists = [], [], [], []
    for line in lines[::-1]:
        data = line.split(' ')
        versions.append(data[0])
        if data[0][5] == '0':
            versions_func.append(data[0])
        else:
            versions_bug.append(data[0])
        dists.append(int(data[2]))
    average = sum(dists)/len(dists)
    plt.figure()
    l1, = plt.plot(versions, dists, 'r', label = "distance")#, markevery = versions_func)
    #plt.scatter(versions, [dists[i] if versions[i][-1] == '0' for i in range(len(versions))])
    l3, = plt.plot(versions, [average]*len(versions), '-.r', label = "distance_avg")
    plt.xlabel('versions')
    plt.ylabel('distance')
    #plt.twinx()
    ##l2, = plt.plot(versions, files, 'b', linestyle = '--', label = "changed_file")#, markevery = versions_func)
    #plt.ylabel('changed_files')
    plt.legend(handles = [l1, l3], loc = 'upper right')
    plt.show()
    plt.figure()

if __name__ == "__main__":
    path_dist = '/home/zhh/Documents/SAT/output/result_continuous.txt'
    commits = dataGenerate(path_dist)
    commits.sort(key = lambda x: x.dist)
    #print(len([commit for commit in commits if commit.dist == 0]))
    bigandsmall(commits)
    rq1(commits)
    rq3()
    rq4(commits, 0.8, 5)
    path_versions = '/home/zhh/Documents/SAT/output/result_func.txt'
    rq2(path_versions)
