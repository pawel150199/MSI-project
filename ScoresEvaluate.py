import numpy as np
from sklearn.metrics import balanced_accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from imblearn.under_sampling import RandomUnderSampler, ClusterCentroids
from ModifiedClusterCentroid import ModifiedClusterCentroids
from imbalancelevel import Imbalance

""" Klasyfikatory uzyte w eksperymencie
    GNB: GaussianNB
    SVC: SVC
    kNN: KNeighborsClassifier
    Linear SVC: LinearSVC
"""

#metody undersampligu
preprocs = {
    'none': None,
    'RUS' : RandomUnderSampler(),
    'CC': ClusterCentroids(random_state=1234),
    'MCC': ModifiedClusterCentroids(CC_strategy='const')
}

#walidacja krzyzowa
n_splits = 5
n_repeats = 2
rskf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state = 1234)

#tablice z wynikami
scores_GNB = np.zeros((len(preprocs), n_splits*n_repeats))
scores_SVC = np.zeros((len(preprocs), n_splits*n_repeats))
scores_kNN = np.zeros((len(preprocs), n_splits*n_repeats))
scores_LSVC = np.zeros((len(preprocs), n_splits*n_repeats))

datasets = ['yeast6']
dataset = np.genfromtxt("datasets/%s.csv" % (datasets) , delimiter=',')
#ap = Imbalance(datasets)
#ap.calcutate()
#ap.plot()
X = dataset[:, :-1]
y = dataset[:, -1].astype(int)

for fold_id, (train, test) in enumerate(rskf.split(X, y)):
    for preproc_id, preproc_name in enumerate(preprocs):
        if preprocs[preproc_name] == None:
            X_res, y_res = X[train], y[train]
        else:
            X_res, y_res = preprocs[preproc_name].fit_resample(X[train],y[train])

        #GNB
        clf_GNB = GaussianNB()
        clf_GNB.fit(X_res, y_res)
        y_pred = clf_GNB.predict(X[test])
        scores_GNB[preproc_id, fold_id] = balanced_accuracy_score(y[test],y_pred)

        #SVC
        clf_SVC = SVC()
        clf_SVC.fit(X_res, y_res)
        y_pred = clf_SVC.predict(X[test])
        scores_SVC[preproc_id, fold_id] = balanced_accuracy_score(y[test],y_pred)

        #kNN
        clf_kNN = KNeighborsClassifier()
        clf_kNN.fit(X_res, y_res)
        y_pred = clf_kNN.predict(X[test])
        scores_kNN[preproc_id, fold_id] = balanced_accuracy_score(y[test],y_pred)
            
        #LSVC
        clf_LSVC = LinearSVC(random_state=1234, tol=1e-5)
        clf_LSVC.fit(X_res, y_res)
        y_pred = clf_LSVC.predict(X[test])
        scores_LSVC[preproc_id, fold_id] = balanced_accuracy_score(y[test],y_pred)

#zapisanie  wyników 
np.save('results_GNB', scores_GNB)
np.save('results_SVC', scores_SVC)
np.save('results_kNN', scores_kNN)
np.save('results_LSVC', scores_LSVC)