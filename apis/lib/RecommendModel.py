import sklearn
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class ContentBasedRecommender:
    
    MODEL_NAME = 'Content-Based'
    
    def __init__(self, item_ids, feature_type_list, user_profiles_list, tfidf_matrix_list, items_df=None,):
        self.item_ids = item_ids
        self.items_df = items_df
        self.user_profiles_list = user_profiles_list
        self.tfidf_matrix_list = tfidf_matrix_list
        self.feature_type_list = feature_type_list
        
    def get_model_name(self):
        return self.MODEL_NAME
    
    def _get_similar_items_to_user_profile(self, person_id, index, topn=1000):
        # 유저 특성과 항목 특성 사이의 코사인 유사도를 구한다
        # 여러개의 feature를 한번에 반영할 수 있도록 모델 수정
        user_profiles = self.user_profiles_list[index]
        tfidf_matrix = self.tfidf_matrix_list[index]
        cosine_similarities = cosine_similarity(user_profiles[person_id], tfidf_matrix)
        
        # 가장 유사한 항목을 찾는다
        similar_indices = cosine_similarities.argsort().flatten()[-topn:]
        
        # 유사도를 기준으로 유사한 항목을 정렬한다
        similar_items = sorted(
            [(self.item_ids[i], cosine_similarities[0, i]) for i in similar_indices],
            key=lambda x: -x[1]
        )
        return similar_items
    
    def recommend_items(self, user_id, items_to_ignore=[], topn=10, verbose=False):
        # 모든 feature을 한번에 다룰 수 있게 수정
        for i in range(len(self.user_profiles_list)):
            feature_type = self.feature_type_list[i]
            similar_items = self._get_similar_items_to_user_profile(user_id, i)
            # 기존에 상호작용했던 항목은 제거한다
            similar_items_filtered = list(filter(lambda x: x[0] not in items_to_ignore, similar_items))
        
            # dataframe으로 변환
            if (i==0):
                recommendations = (
                    pd.DataFrame(similar_items_filtered, columns=['tea_id', 'recStrength_{0}'.format(feature_type)])
                    .head(topn)
                )
            else:
                recommendations = pd.merge(recommendations, pd.DataFrame(similar_items_filtered, columns=['tea_id', 'recStrength_{0}'.format(feature_type)]).head(topn), on="tea_id", how="outer")
        recommendations.fillna(0)
        recommendations['recStrength_efficacies'] /= 2
        # divid number is len(self.user_profiles_list), not len(~) + 1
        value = (recommendations.drop(['tea_id'], axis=1).sum(axis=1)) / (len(self.user_profiles_list))
        recommendations['recStrength'] = value
        recommendations = recommendations[['tea_id', 'recStrength']].sort_values('recStrength', ascending=False)
        
        if verbose:
            if self.items_df is None:
                raise Exception('"items_df" is required in verbose mode')
            recommendations = (recommendations
                .merge(self.items_df, how='left', left_on='tea_id', right_on='tea_id')
                .loc[:, ['recStrength', 'tea_id', 'title', 'url', 'lang']]
            )
        
        return recommendations


class CFRecommender:
    
    MODEL_NAME = 'Collaborative Filtering'
    
    def __init__(self, cf_predictions_df, items_df=None):
        self.cf_predictions_df = cf_predictions_df
        self.items_df = items_df
        
    def get_model_name(self):
        return self.MODEL_NAME
    
    def recommend_items(self, user_id, items_to_ignore=[], topn=10, verbose=False):
        # 사용자에 대한 예측값을 가져와서 정렬한다
        sorted_user_prediction = (self.cf_predictions_df
            .loc[:, user_id]
            .sort_values(ascending=False)
            .reset_index()
            .rename(columns={user_id: 'recStrength'})
        )
        
        recommendations = (sorted_user_prediction
            .loc[lambda d: ~d['tea_id'].isin(items_to_ignore)]
            .sort_values('recStrength', ascending=False)
            .head(topn)
        )
        
        if verbose:
            if self.item_df is None:
                raise Exception('"items_df" is required in verbose mode')
            
            recommendations = (recommendations
                .merge(self.items_df, how='left', left_on='tea_id', right_on='tea_id')
                .loc[:, ['recStrength', 'tea_id', 'title', 'url', 'lang']]
            )
            
        return recommendations

class HybridRecommender:
    
    MODEL_NAME = 'Hybrid'
    
    def __init__(self, cb_rec_model, cf_rec_model, items_df):
        self.cb_rec_model = cb_rec_model
        self.cf_rec_model = cf_rec_model
        self.items_df = items_df
        
    def get_model_name(self):
        return self.MODEL_NAME
    
    def recommend_items(self, user_id, items_to_ignore=[], topn=10, verbose=False):
        # 상위 1000개의 컨텐츠 기반 모형 추천을 가져온다
        cb_recs = (self.cb_rec_model
            .recommend_items(user_id, items_to_ignore=items_to_ignore, verbose=verbose, topn=1000)
            .rename(columns={'recStrength': 'recStrengthCB'})
        )
        
        # 상위 1000개의 협업필터링 추천을 가져온다
        cf_recs = (self.cf_rec_model
            .recommend_items(user_id, items_to_ignore=items_to_ignore, verbose=verbose, topn=1000)
            .rename(columns={'recStrength': 'recStrengthCF'})
        )
        
        # 1) 두 모형의 결과를 합친다
        # 2) CF, CB 모형의 점수를 바탕으로 Hybrid 모형의 점수를 계산한다
        # 3) Hybrid 점수를 기준으로 정렬한다
        recommendations = (cb_recs
            .merge(cf_recs, how='inner', left_on='tea_id', right_on='tea_id')
            .assign(recStrengthHybrid = lambda d: (0.6 * d['recStrengthCB']) + (0.4 *d['recStrengthCF']))
            .sort_values('recStrengthHybrid', ascending=False)
            .head(topn)
        )
        
        if verbose:
            if self.items_df is None:
                raise Exception('"items_df" is required in verbose mode')
            
            recommendations = (recommendations
                .merge(self.items_df, how='left', left_on='tea_id', right_on='tea_id')
                .loc[:, ['recStrengthHybrid', 'tea_id', 'title', 'url', 'lang']]
            )
        
        return recommendations