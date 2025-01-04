#import openai
#openai.api_key = "your_key"
#
#def get_completion(prompt, model="gpt-3.5-turbo"):
#    messages = [{"role": "user", "content": prompt}]
#    response = openai.ChatCompletion.create(
#        model=model,
#        messages=messages,
#        temperature=0, # 控制模型输出的随机程度
#    )
#    return response.choices[0].message["content"]
#
#def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
#    response = openai.ChatCompletion.create(
#        model=model,
#        messages=messages,
#        temperature=temperature, # 控制模型输出的随机程度
#    )
#    #print(str(response.choices[0].message))
#    return response.choices[0].message["content"]
#
#messages =  [  
#{'role':'system', 'content':'You are an assistant that speaks like Shakespeare.'},    
#{'role':'user', 'content':'tell me a joke'},   
#{'role':'assistant', 'content':'Why did the chicken cross the road'},   
#{'role':'user', 'content':'I don\'t know'}  ]
#
#response = get_completion_from_messages(messages, temperature=1)
#print(response)

import openai # type: ignore
import panel as pn  # type: ignore # GUI

openai.api_key = "your_key"

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.7,  # 设置适当的温度，允许一定的创意生成
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.7):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]


# 初始指引话语
# print("欢迎使用文案助手！请输入您想要的事件描述，然后我会帮您生成朋友圈/社交平台文案。若要结束对话，请直接按回车键。")

messages = [
    {'role': 'system', 
     'content': 'You are an assistant that helps users create expressive,  \
        emotional social media posts in a youthful, informal style, \
        with lots of personal judgment and emotional color. \
        In the user‘s voice generate long text using the same language as user request. \
        Please strictly follow these principles below: \
        0. only give the content to post \
        1. write as the user himself/herself and in his/her own voice and the content is used for posting on the user‘s own social platforms. \
        2. kindly alert the user when the content deals with any religious/political/pornographic/drugs(including cannabis)/dark web dealings and other undesirable topics and do not offer content generation. \
        3. generate in the same language as the user‘s last request. If the user describe in Chinese then answer in Chinese.\
        4. the tone of voice mimics that of a z-gen American high school/college girl as much as possible, with creative use of buzzwords and emojis. \
        5. when the content provided by the user is brief, it can be expanded with appropriate and reasonable inferences and imagery. \
        6. Look up keywords of places/things that appear in the user‘s instructions to get a clear picture of the context \
        7. At least 40 words. \
        '},
    {'role': 'assistant',
    'content': 'Hi! I can help you create an emotional, engaging social media post! Just tell me about your event or experience, and I’ll help you write something awesome. 💖'}
]

# models = openai.Model.list()
# for model in models["data"]:
#     print(model["id"])

input_text = pn.widgets.TextAreaInput(name="输入文案描述", placeholder="请输入文案描述...", width=600, height=100)
output_text = pn.widgets.TextAreaInput(name="生成的文案", placeholder="生成的文案将显示在这里...", width=600, height=100, disabled=True)


# 创建聊天记录区域
chat_history = pn.pane.Markdown("", width=600, height=300)


# 按钮回调函数，调用 OpenAI API 生成文案
def generate_copy(event):
    user_input = input_text.value  # 获取输入的文本描述
    
    # 如果输入为空，则退出
    if not user_input.strip():
        output_text.value = "请输入有效的描述来生成文案。"
        return

    # 使用 OpenAI API 生成文案
    try:
        messages.append({'role': 'user', 'content': user_input})
        response = get_completion_from_messages(messages, temperature=0.7)
        messages.append({'role': 'assistant', 'content': response})
        output_text.value = response  # 将生成的文案显示在输出框中
        
        # 更新聊天记录
        new_chat = f"**User**: {user_input}\n**Assistant**: {response}\n\n"
        chat_history.object += new_chat  # 将新的对话添加到聊天记录中

    except Exception as e:
        output_text.value = f"出错了: {e}"

# 创建生成按钮
generate_button = pn.widgets.Button(name="生成文案", button_type="primary")
generate_button.on_click(generate_copy)


# 添加注释或说明信息
intro_text = pn.pane.Markdown("""
### 文案助手
欢迎使用文案助手！请输入您想要的事件描述，然后我会帮您生成朋友圈/社交平台文案。
                              
- 请尽量描述清晰和具体的需求。
- 点击 **生成文案** 按钮后，系统将生成与您的描述相匹配的文案。
- 生成的文案会显示在下方的文本框中，您可以进行复制、修改或使用。

**注意**：每次修改描述后，您都可以点击 **生成文案** 按钮来生成新的文案内容
""", width=600)


# 布局设置
layout = pn.Column(
    intro_text,          # 欢迎界面和简要说明
    input_text,          # 文本输入框
    generate_button,     # 生成按钮
    output_text,          # 输出框
    pn.pane.Markdown("### 交流历史", width=600),  # 交流历史标题
    chat_history         # 聊天记录区域
)

# 展示界面
layout.show()


'''
while True:
    # 获取用户输入
    user_input = input("请输入事件描述（按回车结束对话）：")
    
    if not user_input:  # 如果用户没有输入内容，按回车键结束
        print("对话结束。感谢使用！")
        break

    # 将用户输入添加到消息中
    messages.append({'role': 'user', 'content': user_input})

    # 获取并输出文案
    response = get_completion_from_messages(messages, temperature=0.7)
    print("生成的文案：")
    print(response)
    
    # 继续对话
    messages.append({'role': 'assistant', 'content': response})
'''