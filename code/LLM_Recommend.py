import torch
import json
import re
from transformers import AutoModelForCausalLM, AutoTokenizer
from config import model_dir, prompt2


# 加载模型
device = "cuda"

tokenizer = AutoTokenizer.from_pretrained(model_dir,trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    trust_remote_code=True
).to(device).eval()


def answer_generator(user_input, similar_paper):
    # query = question  # 可替换
    query = prompt2.format(user_input=user_input, title=similar_paper['source'], abstract= similar_paper['content'])

    inputs = tokenizer.apply_chat_template([{"role": "user", "content": query}],
                                           add_generation_prompt=True,
                                           tokenize=True,
                                           return_tensors="pt",
                                           return_dict=True
                                           )

    inputs = inputs.to(device)

    gen_kwargs = {"max_length": 2500, "do_sample": True, "top_k":1}
    # gen_kwargs = {"do_sample": True, "top_k": 1, "max_new_tokens": 5000}
    with torch.no_grad():
        outputs = model.generate(**inputs, **gen_kwargs)
        outputs = outputs[:, inputs['input_ids'].shape[1]:]
        # print(tokenizer.decode(outputs[0], skip_special_tokens=True))

        LLM_answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # match = re.search(r"Final answer:\s*(.*)", LLM_answer)
        # match = re.search(r"Final answer:\s*([a-z]\))", LLM_answer)
        # if match:
        #     answer = match.group(1)
        #     # print("Extracted answer:", answer)
        # else:
        #     # print("No match found.LLM_answer:",LLM_answer)
        #     answer = LLM_answer
        return LLM_answer
