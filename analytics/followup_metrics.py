from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss, confusion_matrix
def followup_metrics(y,p,threshold=.5):
    pred=(p>=threshold).astype(int); tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
    return {'auroc':roc_auc_score(y,p),'average_precision':average_precision_score(y,p),'brier_score':brier_score_loss(y,p),'sensitivity':tp/(tp+fn) if tp+fn else 0,'specificity':tn/(tn+fp) if tn+fp else 0,'ppv':tp/(tp+fp) if tp+fp else 0}
