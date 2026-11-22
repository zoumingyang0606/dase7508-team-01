import hashlib
import re
import tarfile
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score, confusion_matrix

DATA_URL = 'https://www2.aueb.gr/users/ion/data/enron-spam/preprocessed/enron1.tar.gz'

DATA_SHA256 = '3d6a1fcced6c30b1701a3fd04c6b912d7046208f6ef6f4fdcf022f64bdc6c32f'

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load(path):
    if sha(path) != DATA_SHA256: raise ValueError('Unexpected Enron1 archive SHA256')
    rows, conflicts = {}, set()
    total = empty = 0
    with tarfile.open(path) as archive:
        for member in archive:
            label = Path(member.name).parent.name
            if not member.isfile() or label not in ['ham','spam']: continue
            total += 1
            raw = archive.extractfile(member).read().decode('latin1')
            body = re.sub(r'^Subject:[^\n]*(?:\n|$)', '', raw, flags=re.I).strip()
            if not body:
                empty += 1; continue
            key = hashlib.sha256(' '.join(body.lower().split()).encode()).hexdigest()
            if key in rows and rows[key][1] != label: conflicts.add(key)
            rows.setdefault(key,(body,label))
    return [(k,*v) for k,v in sorted(rows.items()) if k not in conflicts], {
        'raw':total,'empty':empty,'usable':len(rows)-len(conflicts),
        'duplicate_rows':total-empty-len(rows),'conflict_groups':len(conflicts),
        'source_sha256':DATA_SHA256,'source':DATA_URL,
        'deduplication':'lowercase and whitespace collapse before split; unchanged revised protocol'}

def fit(texts, labels, valid, y, char):
    vec=TfidfVectorizer(analyzer='char' if char else 'word',ngram_range=(3,5) if char else (1,1),
                       max_features=30000 if char else 20000,min_df=2)
    x=vec.fit_transform(texts); val=vec.transform(valid)
    choices=[]; grid=[]
    for c in [1,4]:
        lr=LogisticRegression(C=c,solver='liblinear',random_state=42).fit(x,labels)
        score=f1_score(y,lr.predict(val),pos_label='spam')
        choices.append((score,c,lr));grid.append({'C':c,'validation_F1':score})
    score,c,lr=max(choices,key=lambda z:z[0])
    return make_pipeline(vec,lr),dict(C=c,validation_F1=score,grid=grid)

def ratio(a,b):return float(a/b) if b else float('nan')

def metrics(y,pred,base):
    y, pred, base = map(np.asarray, (y, pred, base))
    if any(values.ndim != 1 for values in (y, pred, base)):
        raise ValueError("Labels, current predictions and original predictions must be one-dimensional.")
    if not (len(y) == len(pred) == len(base)):
        raise ValueError("Labels, current predictions and original predictions must have the same length.")
    tn,fp,fn,tp=map(int,confusion_matrix(y,pred,labels=['ham','spam']).ravel())
    eligible=(y=='spam')&(base=='spam');num=int((eligible&(pred=='ham')).sum());den=int(eligible.sum())
    return dict(TP=tp,FP=fp,TN=tn,FN=fn,accuracy=ratio(tp+tn,len(y)),precision=ratio(tp,tp+fp),
                recall=ratio(tp,tp+fn),F1=ratio(2*tp,2*tp+fp+fn),FPR=ratio(fp,tn+fp),
                overall_miss_rate=ratio(fn,tp+fn),conditional_asr=ratio(num,den),
                initially_blocked_spam=den,newly_bypassed_spam=num,
                original_spam_misses=int(((y=='spam')&(base=='ham')).sum()))
