from itertools import chain
"""this function serves to be able to calculate the trust of each topic regardless of 
whether or not there is news related to each topic. The aim is to initialise the trust 
at a fixed value for each topic until a news item occurs.   """
def reorder_metrics (df, metric):
    metric_new = []
    for sub_metric in metric:
        if len(sub_metric) < len(df['Topic'].unique()):
            sub_metric.extend([0.2]*(len(df['Topic'].unique())-len(sub_metric)))
            metric_new.append(list(chain(sub_metric)))
        else:
            metric_new.append(list(chain(sub_metric)))
    return metric_new