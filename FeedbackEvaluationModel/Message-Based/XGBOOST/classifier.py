import os
import pickle
import joblib
from scipy import stats
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import metrics
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn.metrics import confusion_matrix, roc_curve, auc, roc_auc_score, accuracy_score, log_loss, f1_score
from sklearn.model_selection import StratifiedKFold
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import warnings
def confusion_matrix_plot(ytest,y_pred):
    matrix = confusion_matrix(ytest, y_pred)
    counts = ['{0:0.0f}'.format(value) for value in matrix.flatten()]
    percentage = ['{0:.2%}'.format(value) for value in matrix.flatten() / np.sum(matrix)]
    labels = [f'{v1}\n{v2}' for v1, v2 in zip(counts, percentage)]
    labels = np.asarray(labels).reshape(2, 2)
    fig,ax = plt.subplots(figsize = (7, 5.5))
    sns.heatmap(matrix, annot = labels, ax = ax, fmt = '',cmap = 'Blues', annot_kws = {"size": 15})
    label_font = {'size':'18'}  
    ax.set_xlabel(' \n Predicted', fontdict = label_font);
    ax.set_ylabel('Actual \n', fontdict = label_font);
    title_font = {'size':'20'}
    ax.set_title('Confusion Matrix \n', fontdict = title_font);
    ax.tick_params(axis = 'both', which = 'major', labelsize = 12) 
    ax.xaxis.set_ticklabels(['Fake', 'Real']);
    ax.yaxis.set_ticklabels(['Fake', 'Real']);
    plt.show()
def prediction_results(model, y_test, X_test, y_pred, probs):
    auc = roc_auc_score(y_test, probs)
    print('AUC score: %.2f' % auc)

    accuracy = (model.score(X_test, y_test) * 100)
    f1 = f1_score(y_test, y_pred)
    print('Accuracy: %.2f' % accuracy)
    print('F1 Score: %.2f' % f1)
    print('Logloss: %.2f' % (log_loss(y_test, y_pred)))
    fpr, tpr, _ = roc_curve(y_test, probs)
    plt.plot(fpr, tpr, marker = ',')
    plt.plot([0, 1], [0, 1], linestyle = '-.')
    plt.title('Characteristic Curve \n', fontsize = 16)
    plt.xlabel('\n FPR', fontsize = 13)
    plt.ylabel('TPR \n', fontsize = 13)
    plt.legend(["AUC = %.2f"%auc])
    plt.show();
    return accuracy, auc, f1
if __name__ == "__main__":
    xgb.set_config(verbosity=0)
    model_file_name = "trained_model.sav"
    flag = 0#it is needed to check whether the model is already trained
    for root,dirs,files in os.walk('./'):
        if model_file_name in files:
            flag = 1
    if flag == 1:
        #the model is already trained
        xgb_model = pickle.load(open(model_file_name,'rb'))
        print("The model is already traindfed")
    else:
        df = pd.read_csv('../dataset_features.csv')
        df_test = pd.read_csv('../dataset_TEST_features.csv')
        y = df['label']
        feauters = ['chars','redundancy','words','sents','typos','badwords','avgChars','avgwordsS',
               'avgPunctuation','pronoun','exclamations','questions','modal','terminiDiversi']
        X = df[feauters]
        X_test = df_test[feauters]
        y_test = df_test['label']
        y_train = y
        X_train = X
        feauters_names = df[feauters].columns.tolist()
        imbalance = y.value_counts(normalize = True)[-1]/y.value_counts(normalize = True)[1]
        xgb_model = XGBClassifier(eval_metric = 'auc', objective = 'binary:logistic', nthread = 1, seed = 77, 
                        scale_pos_weight = imbalance, verbosity = 0)
    
        xgb_params = {'learning_rate': [0.01],
                  'n_estimators': [1800],
                  'max_depth': [7], 
                  'subsample': [0.4], 
                  'colsample_bytree': [0.8],
                  'min_child_weight' : [0.4],
                  'lambda': [0],
                  'alpha': [0.1]}
    
        skf = StratifiedKFold(n_splits = 3, shuffle = True, random_state = 77)
        grid_search = GridSearchCV(estimator = xgb_model, param_grid = xgb_params, 
                                           scoring = 'roc_auc', n_jobs = -1, cv = skf.split(X_train, y_train), verbose = 2)
        grid_search.fit(X_train, y_train)
        #SAVE the model to disk
        print('Best hyperparameters:' , grid_search.best_params_)
        xgb_model = grid_search.best_estimator_
        #xgb_model.save_model("model")
        joblib.dump(xgb_model, "model") 
        #results
        y_pred = xgb_model.predict(X_test)
        probs = xgb_model.predict_proba(X_test)
        probs = probs[:, 1]
        xgb_accuracy_score, xgb_auc_score, xgb_f1_score = prediction_results(xgb_model, y_test, X_test, y_pred, probs)
        confusion_matrix_plot(y_test, y_pred)
        f, ax = plt.subplots(figsize = [7, 10])
        axsub = xgb.plot_importance(xgb_model, ax = ax)
        # get the original names back
        Text_yticklabels = list(axsub.get_yticklabels())
        list_yticklabels = [Text_yticklabels[i].get_text().lstrip('f') for i in range(len(Text_yticklabels))]
        # feature importance
        plt.title("Feature Importance", fontsize = 15)
        axsub.set_yticklabels(list_yticklabels)
        plt.show()
        result = xgb_model.score(X_test, y_test)
