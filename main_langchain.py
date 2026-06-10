import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# API 키 확인
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("오류: .env 파일에 'GOOGLE_API_KEY'가 설정되어 있지 않습니다.")
else:
    # LangChain용 Gemini 모델 설정
    # 안정적인 쿼터를 가진 'models/gemini-flash-latest'를 사용합니다.
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-flash-latest",
        google_api_key=api_key,
        temperature=0.7
    )

    try:
        # LangChain 방식으로 질문 던지기
        print("LangChain을 통한 Gemini 호출 중...")
        response = llm.invoke("안녕! LangChain으로 대화하니 기분이 어때?")
        
        print("\nGemini(LangChain) 응답:")
        print(response.content)
    except Exception as e:
        print(f"오류 발생: {e}")
