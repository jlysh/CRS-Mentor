# CRS-Mentor
CRS-Mentor

*** 使用模型 ***
** LANGUAGE MODELS: glm4-chat
** EMBEDDING MODELS: bce-embedding-base_v1
** RERANK MODELS: bce-reranker-base_v1


*** 使用数据集***

*** Aminer ***

** 数据集地址 https://www.aminer.cn/aminernetwork

** [Aminer.py](Aminer.py)Aminer.py 处理Aminer数据集代码

** [AMiner-Paper.txt](AMiner-Paper%2FAMiner-Paper.txt) 原数据集 2,092,356 条数据

** [aminer_data_mini.csv](aminer_data_mini.csv) 处理过的精简后的数据集 14,341 条数据

*** DBLP ***

** 原始数据集地址：https://dblp.uni-trier.de/xml/

** 处理后数据集地址 https://www.aminer.cn/citation

** [dblp.py](data%2FDBLP%2Fdblp.py) 处理DBLP数据集代码(实验使用的DBLP-Citation-network V14数据集)

** [dblp_v14.json](data%2FDBLP%2FDBLP-Paper%2Fdblp_v14.json) 原数据集 5,259,858 条数据

** [dbpl_data_mini.csv](data%2FDBLP%2FDBLP-Paper%2Fdbpl_data_mini.csv) 处理过的精简后的数据集 12,259 条数据

*** 实验代码 ***

** [code](code) CSR-Mentor代码
