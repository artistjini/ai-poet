from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


import streamlit as st
#from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
#load_dotenv()

#Gemini 모델 초기화
llm=init_chat_model(
    model="gemini-flash-latest",
    temperature=0.7,
    max_tokens=2048,
    model_provider="google_genai",) 
    

#프롬프트 템플릿 생성
prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "{input}")
])

#문자열 출력 파서
output_parser=StrOutputParser()

#LLM 체인 구성
chain = prompt | llm | output_parser

#제목
st.title("인공지능 시인")

#시 주제 입력  필드
content = st.text_input("시의 주제를 제시해주세요")
st.write( "시의 주제는",content)

#시 작성 요청하기
st.button("Reset", type="primary")
if st.button("시 작성 요청하기"):
  with st.spinner("시를 작성하는 중입니다..."):
    result = chain.invoke({"input": content + "에 대한 시를 써줘"})
    st.write(result)

import os
from google import genai

# API 키 가져오기
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("오류: .env 파일에 'GOOGLE_API_KEY'가 설정되어 있지 않습니다.")
else:
    # 새로운 SDK 클라이언트 초기화
    client = genai.Client(api_key=api_key)

    try:
        # 안정적인 gemini-flash-latest 모델 사용
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents="안녕하세요, 자기소개 부탁드려요."
        )
        print("Gemini 응답:")
        print(response.text)
    except Exception as e:
        print(f"오류 발생: {e}")

