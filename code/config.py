# embeddings索引路径
embeddings_index_dir = r"db_index/embeddings_index"

# topK参数用于设置搜索结果显示的条目数
topK = 5


# LLM_config
model_dir = "model/glm-4-9b-chat"


prompt = """当面对一项任务时，首先你需要根据用户给出的检索问题来确定将为解决任务做出贡献的参与者。然后，启动专家团队评审，直到全部的专家都认同AI助手给出的文献检索结果。参与者将在必要时提出批评意见和详细建议。
以下是一些示例：
示例任务 1：

用户输入：请给我推荐一个和基于量子纠缠的机器学习相关的论文

AI助手：推荐结果如下：{
Title: BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
Author: Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova
Abstract:
We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It achieves new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.4% (a 7.6% absolute improvement), MultiNLI accuracy to 86.7% (a 4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (a 1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (a 5.1 point absolute improvement).
Date: October 11, 2018
This paper is pivotal in the field of natural language processing and has significantly influenced various applications of machine learning.
}

参与者:AI助手;量子领域专家；机器学习领域专家

开始评估！

量子领域专家：让我们详细分析一下AI助手给出的推荐结果。首先从标题来看，是和深度学习有关的，即和机器学习有关系，没有提到量子，所以与量子纠缠没关系；接着看再一下摘要，摘要只提到了BERT和机器学习，但没有提到量子纠缠，所以这篇论文与量子领域没有关系，不满足用户想要查询的条件，建议AI助手下次检索的论文是与量子领域相关的

机器学习领域专家：根据标题来看，该论文是与机器学习相关的，我认可AI助手得到的检索结果

最终答案：
{result:NO
suggest:"你给出的结果和量子纠缠没有关系，下一次的检索结果应该是在基于用户给定输入的基础上再和量子领域相关"
}

---------------------

示例任务 2：

用户输入：请给我推荐一篇协同过滤应用于医疗领域的论文

AI助手：推荐结果如下：{
Title: Collaborative Filtering for Improved Drug-Drug Interaction Prediction
Author: Emma Wang, David M. Blei, Nicholas P. Tatonetti
Abstract:
The prediction of drug-drug interactions (DDIs) is a crucial task in drug safety and patient care, as DDIs can lead to adverse effects or reduce therapeutic efficacy. Traditional methods for DDI prediction often rely on domain-specific knowledge or biological data, which can be limited or unavailable. In this paper, we propose a novel approach to DDI prediction using collaborative filtering, a technique commonly used in recommendation systems. By treating drugs and their interactions as a matrix, we apply collaborative filtering to uncover latent patterns and predict potential interactions. We evaluate our method on a large dataset of known DDIs and demonstrate that it outperforms existing approaches in terms of accuracy and coverage. Our results suggest that collaborative filtering is a powerful tool for enhancing drug safety and could be integrated into pharmacovigilance systems to identify dangerous drug combinations before they reach the market.}
}

参与者:AI助手;量推荐系统领域专家；医疗领域专家

开始评估！

推荐系统领域专家：让我们详细分析一下AI助手给出的推荐结果。首先从标题来看，标题提到了协同过滤，再看下摘要，摘要中也是提到了协同过滤，所以我觉得AI助手给出的检索结果是非常好的

医疗领域专家：根据标题来看，该论文标题提到了DDI，即药物相互作用，所以是和医疗领域相关的，再看下摘要，论文中也多次提到了医疗领域的专业名称，所以我也认为AI助手给出的检索结果是很好的。

最终答案：YES

---------------------

任务：现在，确定参与者，并逐步协作解决以下任务。记得用前缀“最终答案：”表示最终解决方案。

用户输入：请给我推荐一篇与多模态人脸识别相关的论文

AI助手：
{
title: "Learning a Mixture of Factors for Multi-modal Face Alignment"
author: Yi Sun, Xiaogang Wang, Xiaoou Tang
abstract: This paper proposes a mixture model framework to align faces using both visual and depth modalities. The method integrates multiple cues to achieve robust and accurate face alignment across different modalities.
date: 2013
}"""

prompt2 = """当面对一项任务时，首先你需要根据用户给出的检索问题来确定将为解决任务做出贡献的参与者。然后，启动专家团队评审，直到全部的专家都认同AI助手给出的文献检索结果。参与者将在必要时提出批评意见和详细建议。如果是评审不通过，则给出重新搜索的内容。
以下是一些示例：
---------------------
示例任务 1：

用户输入：请给我推荐一个和基于量子纠缠的机器学习相关的论文

AI助手：所得到的文章如下：
title: "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"
abstract: "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It achieves new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.4% (a 7.6% absolute improvement), MultiNLI accuracy to 86.7% (a 4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (a 1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (a 5.1 point absolute improvement)."


参与者:AI助手;量子领域专家；机器学习领域专家

开始评估！

量子领域专家：让我们详细分析一下AI助手给出的推荐结果。首先从标题来看，是和深度学习有关的，即和机器学习有关系，没有提到量子，所以与量子纠缠没关系；接着看再一下摘要，摘要只提到了BERT和机器学习，但没有提到量子纠缠，所以这篇论文与量子领域没有关系，不满足用户想要查询的条件，建议AI助手下次检索的论文是与量子领域相关的
机器学习领域专家：根据标题来看，该论文是与机器学习相关的，我认可AI助手得到的检索结果
评审团意见：你给出的结果和量子纠缠没有关系，下一次的检索结果应该是在基于用户给定输入的基础上再和量子领域相关


最终答案：
{{"result":"NO","retrieval":"机器学习与量子领域相关"}}

---------------------
示例任务 2：

用户输入：请给我推荐一篇协同过滤应用于医疗领域的论文

AI助手：所得到的文章如下：
title: "Collaborative Filtering for Improved Drug-Drug Interaction Prediction"
abstract:"The prediction of drug-drug interactions (DDIs) is a crucial task in drug safety and patient care, as DDIs can lead to adverse effects or reduce therapeutic efficacy. Traditional methods for DDI prediction often rely on domain-specific knowledge or biological data, which can be limited or unavailable. In this paper, we propose a novel approach to DDI prediction using collaborative filtering, a technique commonly used in recommendation systems. By treating drugs and their interactions as a matrix, we apply collaborative filtering to uncover latent patterns and predict potential interactions. We evaluate our method on a large dataset of known DDIs and demonstrate that it outperforms existing approaches in terms of accuracy and coverage. Our results suggest that collaborative filtering is a powerful tool for enhancing drug safety and could be integrated into pharmacovigilance systems to identify dangerous drug combinations before they reach the market."


参与者:AI助手;量推荐系统领域专家；医疗领域专家

开始评估！

推荐系统领域专家：让我们详细分析一下AI助手给出的推荐结果。首先从标题来看，标题提到了协同过滤，再看下摘要，摘要中也是提到了协同过滤，所以我觉得AI助手给出的检索结果是非常好的
医疗领域专家：根据标题来看，该论文标题提到了DDI，即药物相互作用，所以是和医疗领域相关的，再看下摘要，论文中也多次提到了医疗领域的专业名称，所以我也认为AI助手给出的检索结果是很好的。
评审团意见：通过。

最终答案：
{{"result":"YES","title":"Collaborative Filtering for Improved Drug-Drug Interaction Prediction"}}

---------------------

任务：现在，确定参与者，并逐步协作解决以下任务。记得用前缀“最终答案：”表示最终解决方案。请注意最终答案严格按照所给格式，如果是符合条件的则result+title；否则result+retrieval，注意retrieval的内容是重新检索加入专家意见的更全面的新内容，而不是建议原因，也不是跟user_input一样.

用户输入：{user_input}

AI助手：所得到的文章如下：
title: {title}
abstract: {abstract}
"""
