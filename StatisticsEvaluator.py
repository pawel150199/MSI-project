import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from imblearn.under_sampling import RandomUnderSampler, ClusterCentroids, NearMiss
from ModifiedClusterCentroid import ModifiedClusterCentroids
from strlearn.metrics import balanced_accuracy_score



# Klasyfikatory
clfs = {
    'GNB': GaussianNB(),
    'SVC': SVC(),
    'kNN': KNeighborsClassifier(),
    'Linear SVC': LinearSVC()
}

# Metody undersampligu
preprocs = {
    'none': None,
    'RUS' : RandomUnderSampler(random_state=1234),
    'CC': ClusterCentroids(random_state=1234),
    'NM': NearMiss(version=1),
    'MCC': ModifiedClusterCentroids(CC_strategy='const', cluster_algorithm='DBSCAN'),
    'MCC-2': ModifiedClusterCentroids(CC_strategy='auto', cluster_algorithm='DBSCAN'),
    'MCC-3': ModifiedClusterCentroids(CC_strategy='const', cluster_algorithm='OPTICS'),
    'MCC-4': ModifiedClusterCentroids(CC_strategy='auto', cluster_algorithm='OPTICS')

}

# Zbiór danych
#datasets = ['cpu_act','cpu_small']
#datasets = ['kc1', 'kc2', 'kc3']
datasets = ['glass1', 'wisconsin', 'pima', 'iris0', 'glass0', 'yeast1', 'haberman', 'vehicle2', 'vehicle3', 'ecoli1', 'segment0', 'glass6']

if __name__ =='__main__':
    # Stratyfikowana, wielokrotna, walidacja krzyzowa
    n_splits = 5
    n_repeats = 5
    rskf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state = 1234)

    # Tablice z wynikami
    scores = np.zeros((len(datasets), len(preprocs), n_splits*n_repeats, len(clfs)))
    
    # Eksperyment
    for data_id, data_name in enumerate(datasets):
        dataset = np.genfromtxt("datasets/%s.csv" % (data_name) , delimiter=',')
        X = dataset[:, :-1]
        y = dataset[:, -1].astype(int)

        for fold_id, (train, test) in enumerate(rskf.split(X, y)):
            for preproc_id, preproc_name in enumerate(preprocs):
                if preprocs[preproc_name] == None:
                    X_res, y_res = X[train], y[train]
                else:
                    X_res, y_res = preprocs[preproc_name].fit_resample(X[train],y[train])

                for clf_id, clf_name in enumerate(clfs):
                    clf = clfs[clf_name]
                    clf.fit(X_res, y_res)
                    y_pred = clf.predict(X[test])
                    # Tablica z wynikami w formacie DATAxPREPROCSxFOLDxCLASSIFIERS
                    scores[data_id, preproc_id, fold_id, clf_id] = balanced_accuracy_score(y[test],y_pred)

    # Zapisanie  wyników 
    np.save('Results/statistic_results', scores)