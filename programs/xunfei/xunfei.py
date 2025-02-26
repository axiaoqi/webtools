import json

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler  # pip install spark_ai_python
from sparkai.core.messages import ChatMessage
from programs.settings import SynologyDrive

# api秘钥存到自己电脑
config_file_path = SynologyDrive / r'Gitbooks\Quant\config_file\xunfei_config_file.json'
with open(config_file_path, 'r') as f:
    data = json.load(f)

#星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v1.1/chat'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = data.get('SPARKAI_APP_ID')
SPARKAI_API_SECRET = data.get('SPARKAI_API_SECRET')
SPARKAI_API_KEY = data.get('SPARKAI_API_KEY')
#星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'lite'


def __init_client():
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    return spark


def xunfei_lite(content):
    """
    一句话提问
    """
    spark = __init_client()

    # 添加用户输入到消息列表
    message = [ChatMessage(role="user", content=content)]
    # 处理回调
    handler = ChunkPrintHandler()
    # 生成回复
    response = spark.generate([message], callbacks=[handler])
    # 提取答案
    answer = response.generations[0][0].text

    return answer


def run():
    """
    可以连续提问
    """
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )

    # 初始化消息列表
    messages = []

    # system用于设置对话背景（仅Max、Ultra版本支持）
    # messages.append(ChatMessage(role="system", content="对话背景，自己修改"))

    while True:
        # 获取用户输入
        user_input = input("请输入您的问题 (输入'exit'退出)：")

        if user_input.lower() == 'exit':
            print("退出程序。")
            break

        # 添加用户输入到消息列表
        messages.append(ChatMessage(role="user", content=user_input))

        # 处理回调
        handler = ChunkPrintHandler()

        # 生成回复
        response = spark.generate([messages], callbacks=[handler])

        # 打印模型返回的结果
        if response and response.generations:
            for generation in response.generations[0]:
                assistant_response = generation.text
                print("AI回复:", assistant_response)

                # 添加助手回复到消息列表
                messages.append(ChatMessage(role="assistant", content=assistant_response))
        else:
            print("未收到有效的回复。")


if __name__ == '__main__':
    while True:
        content = input('输入文案：')
        s = xunfei_lite(content)
        print(s)
