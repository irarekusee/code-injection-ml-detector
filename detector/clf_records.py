#!/usr/bin/python3

from argparse import ArgumentParser
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC # Support Vector Machine - classification algorithm
from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.linear_model import LogisticRegression as LR
from sklearn.metrics import precision_recall_fscore_support, accuracy_score

arg_parser = ArgumentParser()
arg_parser.add_argument('-f', '--files', type=str, required=False, help='set input file names')
arg_parser.add_argument('-d', '--directory', type=str, required=False, help='set input directory')
args = arg_parser.parse_args()

if args.files is None and args.directory is None:
    exit("At least one of input argument '--files' or '--directory' must be set")

files = None
if args.files is not None:
    files = args.files.split(',')
directory = args.directory

recs = None
all_files = ([] if files is None else files) + \
    ([] if directory is None or not os.path.isdir(directory) else
     [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.features_with_labels') and os.path.isfile(os.path.join(directory, f))])

for f in all_files:
    n = None
    with open(f, 'r') as fh:
        n = len(fh.readline().split(','))
    r = np.genfromtxt(f, delimiter=',', dtype=int, skip_header=1, usecols=range(n))
    if r.ndim == 1:
        r = np.array([r])
    recs = r if recs is None else np.append(recs, r, axis=0)

(features, labels) = (recs[:,:-1], recs[:,-1])

train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.25)

for (cls, cls_name) in [(make_pipeline(StandardScaler(), SVC()), 'SVM'),
                        (DTC(), 'decision tree'),
                        (make_pipeline(StandardScaler(), LR()), 'logistic regression')]:
    cls.fit(train_features, train_labels)
    for (f, l, n) in [(train_features, train_labels, 'training'), (test_features, test_labels, 'testing')]:
#        print(n)
#        print(l)
        predicted_labels = cls.predict(f)
#        print(predicted_labels)
        (precision, recall, fscore, _) = precision_recall_fscore_support(l, predicted_labels)
        accuracy = accuracy_score(l, predicted_labels)
        for (metrics, metrics_name) in [(precision, 'precision'), (recall, 'recall'), (fscore, 'fscore'), (accuracy, 'accuracy')]:
            print('{} of {} on {} sample ({} instances): {}'.format(metrics_name, cls_name, n, len(l), metrics))

#print(np.shape(recs))
#print(recs)
    

