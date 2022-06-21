# 추천 모델 평가 모듈

import random

def get_items_interacted(person_id, interaction_df):
    interated_items = interaction_df.loc[person_id]['contentId']
    return set(interated_items if type(interated_items) == pd.Series else [interated_items])

class ModelEvaluator:
    def __init__(self, n_non_interacted=100):
        self.EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS = n_non_interacted
        
    def get_non_interacted_items_sample(self, person_id, sample_size, seed=42):
        interacted_items = get_items_interacted(person_id, interaction_full_indexed)
        all_items = set(articles_df['contentId'])
        non_interacted_items = all_items - interacted_items
        
        random.seed(seed)
        non_interacted_items_sample = random.sample(non_interacted_items, sample_size)
        return set(non_interacted_items_sample)
        
    def _verify_hit_top_n(self, item_id, recommend_items, topn):
        try:
            index = next(i for i, c in enumerate(recommend_items) if c == item_id)
        except:
            index = -1
        hit = int(index in range(0, topn))
        return hit, index
    
    def evaluate_model_for_user(self, model, person_id):
        interacted_values_testset = interaction_test_indexed.loc[person_id]
        if type(interacted_values_testset['contentId']) == pd.Series:
            person_interacted_items_testset = set(interacted_values_testset['contentId'])
        else:
            person_interacted_items_testset = set([int(interacted_values_testset['contentId'])])
        
        interacted_items_count_testset = len(person_interacted_items_testset)
        
        # 특정 사용자에 대한 추천 순위 목록을 받아온다
        person_recs = model.recommend_items(
            person_id,
            items_to_ignore=get_items_interacted(person_id, interaction_train_indexed),
            topn=10000000000
        )
        
        hits_at_5_count = 0
        hits_at_10_count = 0
        
        # test셋에서 사용자가 상호작용한 모든 항목에 대해 반복한다
        for item_id in person_interacted_items_testset:
            
            # 사용자가 상호작용하지 않은 100개 항목을 샘플링한다
            non_interacted_items_sample = self.get_non_interacted_items_sample(
                person_id,
                sample_size=self.EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS,
                seed=item_id % (2**32)
            )
            
            # 현재 선택한 item_id(상호작용 있었던 항목)와 100개 랜덤 샘플을 합친다
            items_to_filter_recs = non_interacted_items_sample.union(set([item_id]))
            
            # 추천 결과물 중에서 현재 선택한 item_id와 100개 랜덤 샘플의 결과물로만 필터링한다
            valid_recs_df = person_recs[person_recs['contentId'].isin(items_to_filter_recs)]
            valid_recs = valid_recs_df['contentId'].values
            
            # 현재 선택한 item_id가 Top-N 추천 결과 안에 있는지 확인한다
            hit_at_5, index_at_5 = self._verify_hit_top_n(item_id, valid_recs, 5)
            hits_at_5_count += hit_at_5
            hit_at_10, index_at_10 = self._verify_hit_top_n(item_id, valid_recs, 10)
            hits_at_10_count += hit_at_10
            
        # Recall 값은 상호작용 있었던 항목들 중에서 관련없는 항목들과 섞였을 때 Top-N에 오른 항목들의 비율로 나타낼 수 있다
        recall_at_5 = hits_at_5_count / interacted_items_count_testset
        recall_at_10 = hits_at_10_count / interacted_items_count_testset
        
        person_metrics = {
            'hits@5_count': hits_at_5_count,
            'hits@10_count': hits_at_10_count,
            'interacted_count': interacted_items_count_testset,
            'recall@5': recall_at_5,
            'recall@10': recall_at_10
        }
        return person_metrics
    
    def evaluate_model(self, model):
        people_metrics = []
        for idx, person_id in enumerate(list(interaction_test_indexed.index.unique().values)):
            person_metrics = self.evaluate_model_for_user(model, person_id)
            person_metrics['_person_id'] = person_id
            people_metrics.append(person_metrics)

        print('{} users processed'.format(idx))
        
        detailed_result = (
            pd.DataFrame(people_metrics)
              .sort_values('interacted_count', ascending=False)
        )
        
        global_recall_at_5 = detailed_result['hits@5_count'].sum() / detailed_result['interacted_count'].sum()
        global_recall_at_10 = detailed_result['hits@10_count'].sum() / detailed_result['interacted_count'].sum()
        
        global_metrics = {
            'model_name': model.get_model_name(),
            'recall@5': global_recall_at_5,
            'recall@10': global_recall_at_10
        }
        
        return global_metrics, detailed_result
