# recommend algorithm
import numpy as np
import scipy
import pandas as pd
import math
import random
import sklearn
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix
from scipy.stats import pearsonr
import scipy.sparse as sp
import nltk

# connect mysql
from .ConnectDB import MYSQLDB

# filtering algorithm model
from .RecommendModel import CFRecommender, ContentBasedRecommender, HybridRecommender

def get_filtering_tea(user_id):
    myDB = MYSQLDB()

    # user_id = int(user_id)

    # 만약 신규유저라면 common filtering 수행 -> common 과 hybrid 분리
    # if (user_id not in list(myDB.test_boolean['user_id'])):
    #     return (common_filtering.tea_filtering(user_teatype, user_scent, user_effect, user_caff))

    # 변수선언
    User_df = myDB.users
    # UserAge = int(User_df[User_df['user_id'] == user_id].age)
    Tea_df = myDB.teas
    Tea_df.caffeine.replace(
        ['O', 'X'],
        ['true', 'false'], inplace=True
    )


    #interaction하는 df들을 모두 선언한다.
    recommend_test_result_df = myDB.recommend_test_result[['tea_id', 'user_id', 'interaction_type']] 
    user_buy_df = myDB.user_buy_df[['tea_id', 'user_id', 'interaction_type']]
    user_click_df = myDB.user_click_df[['tea_id', 'user_id', 'interaction_type']]

    interaction_df = pd.DataFrame({'tea_id' : [], 'user_id' : [], 'interaction_type': []})
    interaction_df = pd.concat([interaction_df, recommend_test_result_df, user_buy_df, user_click_df])
    interaction_df['user_id'] = (
        interaction_df
        .loc[:, 'user_id']
        # .apply(lambda d: d if((UserAge + 10 >= int(User_df[User_df['user_id'] == d].age)) and (UserAge - 10 <= int(User_df[User_df['user_id'] == d].age))) else None)
    )
    interaction_df.dropna(inplace=True)

    event_type_strength = {
    'Recommend_test': 1.2,
    'Click': 1.0,
    'Search': 2.0,
    'Cart': 2.8,
    'LIKE': 2.3,
    'FOLLOW': 3.0,
    'Buy': 3.5,
    }

    interaction_df['eventStrength'] = (
    interaction_df
        .loc[:, 'interaction_type']
        .apply(lambda d: event_type_strength[d])
    )

    interaction_df_over5 = (interaction_df
    .groupby('user_id', group_keys=False)
    .apply(lambda df: df.assign(interactCnt = lambda d: d['tea_id'].nunique()))
    .loc[lambda d: d['interactCnt'] >= 5]
    )

    interaction_full_df = (
    interaction_df_over5
        .groupby(['user_id', 'tea_id'], as_index=False)['eventStrength']
        .sum()
        .assign(eventScore = lambda d: np.log2(1+d['eventStrength']))
    )

    # 평가와 같은 값나오는지 확인용
    # interaction_train, interaction_test = train_test_split( 
    #     interaction_full_df,
    #     stratify=interaction_full_df['user_id'],
    #     test_size=0.2,
    #     random_state=777
    # )

    # interaction_full_indexed = interaction_full_df.set_index('user_id') 
    # interaction_train_indexed = interaction_train.set_index('user_id') 
    # interaction_test_indexed = interaction_test.set_index('user_id')


    #collaborative filtering
    users_items_pivot_df = (interaction_full_df # 평가할땐 interaction_train
    .pivot(index='user_id', columns='tea_id', values='eventStrength')
    .fillna(0) 
    ) 

    # 피어슨 상관계수를 통한 유저간 유사도 DataFrame 만들기
    # print(users_items_pivot_df.index)
    pearson_similar = {}
    for i in range(len(users_items_pivot_df.index)):
        if users_items_pivot_df.index[i] != user_id:
            pearson_similar[users_items_pivot_df.index[i]] = pearsonr(users_items_pivot_df.loc[user_id], users_items_pivot_df.iloc[i])[0]

    pearson_similar_df = pd.DataFrame(list(pearson_similar.items()), columns=['user_id', 'similar']).sort_values('similar', ascending=False)
    similar_user_topn = pearson_similar_df[['user_id']].head(55)

    # matrix update를 위해 유사도 이웃에 본인 추가
    similar_user_topn = list(similar_user_topn['user_id'])

    #유사도 topn에 들어가는 user가 아니면 pivot matrix에서 제거해준다.
    similar_users_items_pivot_df = users_items_pivot_df[((users_items_pivot_df.index.isin(similar_user_topn)) | (users_items_pivot_df.index == user_id))]

    # interaction 데이터를 이웃 모델에 맞게 변경 해준다.
    interaction_full_df = interaction_full_df[(interaction_full_df['user_id'].isin(similar_user_topn)) | (interaction_full_df['user_id'] == user_id)]

    # recall 평가를 위한 데이터셋 나누기
    # interaction_train, interaction_test = train_test_split( 
    #     interaction_full_df,
    #     stratify=interaction_full_df['user_id'],
    #     test_size=0.2,
    #     random_state=777 # 어떤수라도 상관없지만 같은 숫자면 같은 내용으로 나눠진다.
    # )


    # pivot matrix 설정
    # users_items_pivot_matrix = users_items_pivot_df.values 
    users_items_pivot_matrix = similar_users_items_pivot_df.to_numpy()
    users_ids = list(similar_users_items_pivot_df.index)
    users_items_pivot_sparse_matrix = csr_matrix(users_items_pivot_matrix)

    # Truncated SVD 사용 ( 차원축소 특이값 분해 )
    # User-Item matrix에서 요인의 개수를 정한다 
    NUMBER_OF_FACTORS_MF = min(19, min(users_items_pivot_sparse_matrix.shape) - 1) #축소할 차원을 정한다.
    # User-Item Matrix을 분해한다 
    U, sigma, Vt = svds(users_items_pivot_sparse_matrix, k=NUMBER_OF_FACTORS_MF) 
    sigma_mat = np.diag(sigma) 

    all_user_predicted_ratings = np.dot(np.dot(U, sigma_mat), Vt) 
    all_user_predicted_ratings_norm = (all_user_predicted_ratings - all_user_predicted_ratings.min()) / (all_user_predicted_ratings.max() - all_user_predicted_ratings.min())


    cf_preds_df = ( 
    pd.DataFrame(all_user_predicted_ratings_norm, 
                columns=similar_users_items_pivot_df.columns, 
                index=users_ids) 
        .transpose() 
    )

    cf_recommender_model = CFRecommender(cf_preds_df, Tea_df)
    # print(cf_recommender_model.recommend_items(user_id, topn=10, verbose=False))

    # content_based_filtering
    # nltk.download('stopwords') 
    # nltk.download('punkt')

    vectorizer = TfidfVectorizer( 
        analyzer='word',
        ngram_range=(1, 2),
        min_df=0.003, 
        # max_df=0.5,
        max_features=1000, 
    ) 

    item_ids = Tea_df['id'].tolist() 
    tfidf_matrix = vectorizer.fit_transform(Tea_df['flavor']) 
    # tfidf_feature_names = vectorizer.get_feature_names_out() 
    tfidf_matrix_eff = vectorizer.fit_transform(Tea_df['efficacies']) 
    # tfidf_feature_names_eff = vectorizer.get_feature_names_out() 
    tfidf_matrix_fla = vectorizer.fit_transform(Tea_df['flavor']) 
    # tfidf_feature_names_fla = vectorizer.get_feature_names_out() 
    tfidf_matrix_caff = vectorizer.fit_transform(Tea_df['caffeine']) 
    # tfidf_feature_names_caff = vectorizer.get_feature_names_out() 
    tfidf_matrix_type = vectorizer.fit_transform(Tea_df['type']) 
    # tfidf_feature_names_type = vectorizer.get_feature_names_out() 

    def get_item_profile(item_id, feature_type):
        idx = item_ids.index(item_id)
        if feature_type == 'flavor':
            item_profile = tfidf_matrix_fla[idx:idx+1]
        elif feature_type == 'efficacies':
            item_profile = tfidf_matrix_eff[idx:idx+1]
        elif feature_type == 'caffeine':
            item_profile = tfidf_matrix_caff[idx:idx+1]
        elif feature_type == 'type':
            item_profile = tfidf_matrix_type[idx:idx+1]
        else:
            item_profile = tfidf_matrix[idx:idx+1]
        return item_profile

    def get_item_profiles(ids, feature_type):
        item_profiles_list = [get_item_profile(x, feature_type) for x in ids]
        item_profiles = scipy.sparse.vstack(item_profiles_list)
        return item_profiles

    def build_user_profile(person_id, interaction_indexed_df, feature_type):
        interaction_person_df = interaction_indexed_df.loc[person_id]
        user_item_profiles = get_item_profiles(interaction_person_df['tea_id'], feature_type)
        
        user_item_strengths = np.array(interaction_person_df['eventStrength']).reshape(-1, 1)
        
        # 상호작용 강도를 바탕으로 가중치를 부여하여 평균 계산한다
        user_item_strengths_weighted_avg = \
            np.sum(user_item_profiles.multiply(user_item_strengths), axis=0) /\
            np.sum(user_item_strengths)
        user_item_strengths_weighted_avg = np.asarray(user_item_strengths_weighted_avg)
        user_profile_norm = sklearn.preprocessing.normalize(user_item_strengths_weighted_avg)
        return user_profile_norm

    def build_user_profiles(feature_type):
        interaction_indexed_df = (interaction_full_df
            .loc[lambda d: d['tea_id'].isin(Tea_df['id'])]
            .set_index('user_id')
        )
        user_profiles = {}
        
        for person_id in interaction_indexed_df.index.unique():
            user_profiles[person_id] = build_user_profile(person_id, interaction_indexed_df, feature_type)
            
        return user_profiles

    user_profiles_fla = build_user_profiles('flavor') 
    user_profiles_eff = build_user_profiles('efficacies') 
    user_profiles_caff = build_user_profiles('caffeine') 
    user_profiles_type = build_user_profiles('type')

    # myprofile_fla = user_profiles_fla[user_id].flatten().tolist() 
    # myprofile_eff = user_profiles_eff[user_id].flatten().tolist() 
    # myprofile_caff = user_profiles_caff[user_id].flatten().tolist()
    # myprofile_type = user_profiles_type[user_id].flatten().tolist() 

    feature_type_list = ['flavor', 'efficacies', 'caffeine', 'type']
    user_profiles_list = [user_profiles_fla, user_profiles_eff, user_profiles_caff, user_profiles_type]
    tfidf_matrix_list = [tfidf_matrix_fla, tfidf_matrix_eff, tfidf_matrix_caff, tfidf_matrix_type]

    content_based_model = ContentBasedRecommender(item_ids, feature_type_list, user_profiles_list, tfidf_matrix_list, Tea_df)


    #hybrid filtering
    hybrid_recommender_model = HybridRecommender(content_based_model, cf_recommender_model, Tea_df)
    # print(hybrid_recommender_model.recommend_items( user_id, topn=10, verbose=False))
    hybrid_recommend_tea = hybrid_recommender_model.recommend_items( user_id, topn=3, verbose=False)[['tea_id']]
    hybrid_recommend_tea['tea_name'] = ( 
        hybrid_recommend_tea
        .loc[:, 'tea_id']
        .apply(lambda d: Tea_df[Tea_df['id']==int(d)].name.values[0])
    )
    hybrid_recommend_tea['tea_brand'] = ( 
        hybrid_recommend_tea
        .loc[:, 'tea_id']
        .apply(lambda d: Tea_df[Tea_df['id']==int(d)].brand.values[0])
    )


    # hybrid_recommend_tea['tea_type'] = ( 
    #     hybrid_recommend_tea
    #     .loc[:, 'tea_id']
    #     .apply(lambda d: Tea_df[Tea_df['id']==int(d)].type.values[0])
    # )
    # hybrid_recommend_tea['tea_flavor'] = ( 
    #     hybrid_recommend_tea
    #     .loc[:, 'tea_id']
    #     .apply(lambda d: Tea_df[Tea_df['id']==int(d)].flavor.values[0])
    # )
    # hybrid_recommend_tea['tea_caffeine'] = ( 
    #     hybrid_recommend_tea
    #     .loc[:, 'tea_id']
    #     .apply(lambda d: Tea_df[Tea_df['id']==int(d)].caffeine.values[0])
    # )
    # hybrid_recommend_tea['tea_efficacies'] = ( 
    #     hybrid_recommend_tea
    #     .loc[:, 'tea_id']
    #     .apply(lambda d: Tea_df[Tea_df['id']==int(d)].efficacies.values[0])
    # )
    # hybrid_recommend_tea['tea_siteurl'] = ( 
    #     hybrid_recommend_tea
    #     .loc[:, 'tea_id']
    #     .apply(lambda d: Tea_df[Tea_df['id']==int(d)].site_url.values[0])
    # )
    # hybrid_recommend_tea['tea_price'] = ( 
    #     hybrid_recommend_tea
    #     .loc[:, 'tea_id']
    #     .apply(lambda d: Tea_df[Tea_df['id']==int(d)].price.values[0])
    # )
    # hybrid_recommend_tea['tea_stock'] = ( 
    #     hybrid_recommend_tea
    #     .loc[:, 'tea_id']
    #     .apply(lambda d: Tea_df[Tea_df['id']==int(d)].stock.values[0])
    # )
    return (hybrid_recommend_tea)
