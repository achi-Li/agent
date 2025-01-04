# 文案助手

## 介绍

本项目基于openai的api接口，设计了一系列prompt来使得大模型在解决某些专业领域问题的时候具有更强的处理能力，同时我们也为该Agent设计了简单的UI用于交互。

## 提示原则

最核心的写一条好prompt的原则就是尽可能清晰、明确地表达你的需求。细分下来，具体原则包括：

- **清晰的指令：** 足够清晰明确地说明你希望模型为你返回什么，最后更加细致地说明需求，避免模糊表达。
- **提供上下文和例子：** 给出较为充分的上下文信息，让模型更好地理解相关背景。如果能够提供示例，模型能表现更好（类似传统LLM中的in-context learning）。
- **善用符号和语法：** 使用清晰的标点符号，标题，标记有助于转达意图，并使输出更加容易被解析
- **让模型一步一步的思考：** 在这种方法中，模型逐步进行思考，并呈现出涉及的步骤，这样做可以降低结果的不准确的可能性，并对模型响应的可解释性有很大的帮助。
- **激励模型反思和给出思路：** 可以在prompt中用一些措辞激励模型给出理由，这样有助于我们更好地分析模型生成结果，同时，思维过程的生成，也有助于其生成更高质量的结果。
- **给容错空间：** 如模型无法完成指定的任务，给模型提供一个备用路径，比如针对文本提问，可以加入如果答案不存在，则回复“无答案”
- **让模型给出信息来源：** 在模型结合搜索或者外部知识库时，要求模型提供他的答案的信息来源，可以帮助LLM的答案减少捏造，并获取到最新的信息。

##### 我们所使用的prompt

```python
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
```

在prompt中，我们希望大模型扮演 assistant的角色，帮助我们生成一些可以用于发送朋友圈的文案。大模型在生成文案时所遵循的原则如上所示，主要的原则包括文案要适宜发在社交平台，具有较多的个人情感和主观表达(从最终的生成结果来看，这一点表现得很明显)，违禁的成分不进行生成，文案风格可符合z-gen的高中或者大学女生，至少40个单词以上等等。

## 输出结果

- 文案助手的UI设计

![image-20250104105400885](C:\Users\lsc18\AppData\Roaming\Typora\typora-user-images\image-20250104105400885.png)



- 文案助手的生成效果

![image-20250104105445469](C:\Users\lsc18\AppData\Roaming\Typora\typora-user-images\image-20250104105445469.png)

- 从效果上来看，文案助手基本可以满足我们的需求，但是其中的行文风格有些固定。但文案助手具有交互的功能，可以模仿所提供的文案材料来生成对应的文案，通过微调，可以很好的完成其基本功能。