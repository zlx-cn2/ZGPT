import streamlit as st
from PIL import Image
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI


# 配置网页
icon = Image.open('icon.png')
st.set_page_config(page_title='AIChat', layout='wide', page_icon = icon)
#初始化
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []
if "temp" not in st.session_state:
    st.session_state["temp"] = ""

def clear_text():
    st.session_state["temp"] = st.session_state["input"]
    st.session_state["input"] = ""

# 获取输入
def get_text():
    input_text = st.text_input("You: ", st.session_state["input"], key="input", 
                            placeholder="请在这里输入",
                            on_change=clear_text,    
                            label_visibility='hidden')
    input_text = st.session_state["temp"]
    return input_text

#左边栏
with st.sidebar:
    icon = Image.open('icon.png')
    st.image(icon, caption="", width=200)
    st.markdown("---")
    st.markdown("# 简介")
    st.markdown("ChatGPT免费、免注册、免魔法，直接使用！")
    st.markdown("大家好，这里是:blue[《Z-CHATAI》]！")
    st.markdown(
       "欢迎在:green[B站]或者:green[微信视频号]关注，"
       "了解更多精彩内容!"
            )
    image = Image.open("shipinhao.jpg")
    st.image(image, caption="微信视频号", width=200)

#标题
st.title("❤️ Chat with GPT ♥️")
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

#调用chatgpt
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
MODEL = "gpt-3.5-turbo"
if OPENAI_API_KEY:
    llm = OpenAI(temperature=0,
                openai_api_key=OPENAI_API_KEY,
                model_name=MODEL, 
                verbose=False)

    if 'entity_memory' not in st.session_state:
            st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=100)
    Conversation = ConversationChain(
            llm=llm, 
            prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
            memory=st.session_state.entity_memory
        )  
else:
    st.sidebar.warning('请填入API key')

# 输出
user_input = get_text()
if user_input:
    output = Conversation.run(input=user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

# 可折叠对话框，下载
download_str = []
with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.info(st.session_state["past"][i],icon="👨‍💼")
        st.success(st.session_state["generated"][i], icon="🤖")
        download_str.append(st.session_state["past"][i])
        download_str.append(st.session_state["generated"][i])
    download_str = '\n'.join(download_str)
    if download_str:
        st.download_button('Download 下载',download_str)

for i, sublist in enumerate(st.session_state.stored_session):
        with st.sidebar.expander(label= f"Conversation-Session:{i}"):
            st.write(sublist)


st.write("您好,非常感谢您的使用与支持！🙏")
st.write("为确保提供持续高质量的服务,我需要支付OpenAI API的使用费用。💰")
st.write("如果你喜欢这个服务,请考虑通过微信赞赏~ 😍一元也是爱😍")
st.write("您的支持是我前进的动力,爱你🤞让我们一起探索AI的魅力吧!")
st.write("我会加油的!记得关注我噢~会持续更新有趣的内容!🤔️")

#图片展示
image1 = Image.open("shoukuanma.jpg")
image2 = Image.open("dingyuehao.jpg")
image3 = Image.open("wexin2.jpg")
col1, col2, col3 = st.columns(3)
with col1:
    st.image(image1, caption="买瓶可乐", width=200)
with col2:
    st.image(image2, caption="微信订阅号", width=200)
with col3:
    st.image(image3, caption="微信交流", width=200)

