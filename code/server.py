import gradio as gr
import pandas as pd
import re
import json
from doc2embeddings import text_search
from LLM_Recommend import answer_generator


# 检索功能
def search(user_input):
    results = text_search(user_input)

    # print("results[0]['source']",results[0]['source'])

    # return results[0]['source']

    # text = '最终答案：{result:"NO",retrieval:"关于三维分子结构的论文"}'
    flag = "NO"
    json_list = []
    output_list = []
    for result in results:
        text = answer_generator(user_input, result)
        print("LLM_reply:",text)
        try:
            json_match = re.search(r'{.*}', text).group(0)
        except:
            print("--No match found")
            continue
        result_json = json.loads(json_match)
        print("--result_json:",result_json)
        print("--result_json['result']:",result_json['result'])

        if result_json['result'] == 'YES':
            output_list.append((result['source'],result['content']))
            json_list.append(result_json)
            flag = "YES"
            print("--YES:", result['source'])
        else:
            retrieval_str = result_json['retrieval']
            sub_results = text_search(retrieval_str)
            for sub_result in sub_results[:1]:  # 这里只设置一次重新检索，提高速度
                text = answer_generator(user_input, sub_result)
                print("LLM_reply:", text)
                try:
                    json_match = re.search(r'{.*}', text).group(0)
                except:
                    print("--No match found")
                    continue
                result_json = json.loads(json_match)
                if result_json['result'] == 'YES':
                    output_list.append((result['source'], result['content']))
                    json_list.append(result_json)
                    # print("--result_json:", result_json)
                    flag = "YES"
                    break
        print("\n\n")


    if flag == "NO":
        json_list.append("数据库没有相关的推荐")


    # print("--text:",text)
    # print("--results[0]",results[0])

    # pattern = r'\{.*\}'
    # match = re.search(pattern, text)
    # if match:
    #     json_part = match.group(0)
    #     print("json_part:",json_part)
    #     try:
    #         json_data = json.loads(json_part)
    #         print("json_data:",json_data)
    #     except json.JSONDecodeError as e:
    #         print(f"JSON 解析错误: {e}")
    # else:
    #     json_data = None
    #     print("未找到 JSON 部分。")
    print("--json_list:", json_list)
    print("--output_list:", output_list)
    # return json_list
    return output_list
    # return [(str(title), str(abstract)) for abstract, title in results]



examples = [
    "relational databases design",
    "entity relationship models",
    "conceptual knowledge model",
    "NF2 relations in DBMS"
]

# 创建Gradio界面
with gr.Blocks() as demo:
    with gr.Column():
        query_input = gr.Textbox(label="Search Query")
        search_button = gr.Button("Search")
        # search_output = gr.Dataframe(headers=["Title", "Content"])
        # search_output = gr.Textbox(label="Result")
        # search_output = [gr.JSON(label=f"JSON {i + 1}") for i in range(len(json_list))]
        # search_output = gr.JSON(label="Extracted JSON List")
        search_output = gr.Dataframe(headers=["Title", "Abstract"], datatype=["str", "str"])
        search_button.click(fn=search, inputs=query_input, outputs=search_output)
        gr.Examples(examples=examples, inputs=query_input)

# 运行Gradio界面
demo.launch(share=True, server_name="0.0.0.0", server_port=7531)
