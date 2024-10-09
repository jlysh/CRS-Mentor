import os, time
from config import embeddings_index_dir, topK
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from read_data import read_csv

# 加载embedding模型
embeddings = HuggingFaceEmbeddings(model_name="./model/all-MiniLM-L6-v2")
# 加载向量数据库索引
if not os.path.exists(embeddings_index_dir):
    sample_doc = [
        Document(page_content="sample context", metadata=dict(source="None"))
    ]
    db = FAISS.from_documents(sample_doc, embeddings)
    db.save_local(embeddings_index_dir)
db = FAISS.load_local(embeddings_index_dir, embeddings, allow_dangerous_deserialization=True)


def update_embeddings_index(doc):
    """将文本转为embeddings向量，并更新向量数据库索引"""
    # 嵌入文本
    global db  # 设置全局变量，使程序运行中能够保持更新
    global embeddings
    # embeddings = HuggingFaceEmbeddings(model_name="./all-MiniLM-L6-v2")
    if not os.path.exists(embeddings_index_dir):
        sample_doc = [
            Document(page_content="sample context", metadata=dict(source="None"))
        ]
        db = FAISS.from_documents(sample_doc, embeddings)
        db.save_local(embeddings_index_dir)

    # 更新索引，并存入本地中
    db = FAISS.load_local(embeddings_index_dir, embeddings, allow_dangerous_deserialization=True)
    db.add_documents(doc)
    db.save_local(embeddings_index_dir)


def text_search(query):
    """进行向量相似度搜索"""
    t2t_time_start = time.time()
    matching_docs = db.similarity_search(query, k=topK)  # k指返回的结果数
    t2t_time_end = time.time()
    print("t2t total time:", t2t_time_end - t2t_time_start)
    results = []
    for item in matching_docs:  # 显示页面的条目数
        content = item.page_content
        source = item.metadata['source']
        results.append({'content': content, 'source': source})
    return results



if __name__ == '__main__':
    file_path = 'data/min_aminer_papers.csv'
    df = read_csv(file_path)
    ## 样例：Document(page_content=row['title'], metadata=dict(source=row['file_path']))
    docs = []
    for _, row in df.iterrows():
        doc = [Document(page_content=row['Abstract'], metadata=dict(source=row['Title']))]  # source一般为路径或索引
        update_embeddings_index(doc)

    while True:
        query = input("请输入查询内容：")
        results = text_search(query)
        for item in results:
            print("title:",item['source'])
            print("content:",item['content'])
            print()


