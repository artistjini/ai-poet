# AI 시인 만들기: 아이디어에서 배포까지

**날짜:** 2026년 6월 11일  
**작성자:** artistjini

---

주제를 입력하면 시를 써주는 웹 앱을 만들었다. 브라우저에서 바로, 실시간으로, Google의 Gemini AI가 시를 생성한다. 앱 이름은 **AI 시인**이고, 지금 실제로 배포되어 있다.

이 글은 어떻게 만들었는지, 무엇을 배웠는지, 무엇이 고장났고 어떻게 고쳤는지에 대한 기록이다.

---

## 무엇을 만들었나

**AI 시인**은 Streamlit으로 만든 웹 앱이다. 사용자가 주제를 입력하면, LangChain 프레임워크를 통해 Google Gemini 모델이 시를 생성해서 보여준다.

**라이브 앱:** [https://artistjini-ai-poet.streamlit.app/](https://artistjini-ai-poet.streamlit.app/)

**기술 스택:**
- Python
- LangChain
- Google Gemini API (`gemini-1.5-flash-latest`)
- Streamlit + Streamlit Community Cloud
- Miniconda (환경 관리)
- Git + GitHub

---

## 무엇을 배웠나

### LangChain

LangChain은 대규모 언어 모델(LLM) 위에 애플리케이션을 만들기 위한 프레임워크다. API에 날것의 프롬프트를 던지는 방식을 넘어서, 프롬프트 관리, 모델 체이닝, 외부 데이터 연결 등을 구조적으로 다룰 수 있게 해준다.

코드를 깔끔하고 확장 가능하게 유지하기 위해 이 프레임워크를 선택했다. 나중에 모델을 교체하거나 기능을 추가할 때, 이 구조 덕분에 훨씬 수월하게 작업할 수 있다.

### LLM 체인

앱의 핵심은 LLM 체인이다. 세 가지를 순서대로 연결하는 파이프라인이다.

```
PromptTemplate | LLM | OutputParser
```

`PromptTemplate`이 사용자의 주제를 모델에게 전달할 구조화된 지시문으로 만든다. `LLM`이 시를 생성한다. `OutputParser`가 표시할 텍스트를 추출한다. 이걸 명령형 호출의 연속이 아닌 선언적인 체인으로 작성하니 로직이 훨씬 명확해지고 수정도 쉬워졌다.

### Gemini API

생성 엔진으로 Google의 `gemini-1.5-flash-latest` 모델을 선택했다. 응답 속도가 빠르고, 한국어 시 창작 능력이 뛰어나며, `langchain-google-genai` 패키지를 통해 LangChain과 깔끔하게 연동된다.

### Streamlit

Streamlit을 쓰면 순수 Python만으로 완전한 웹 UI를 만들 수 있다. HTML도, CSS도, JavaScript도 필요 없다. 이 프로젝트에서는 그게 맞는 선택이었다. 프론트엔드 프레임워크를 따로 배우지 않고 AI 로직에 집중하면서 작동하는 인터페이스를 배포까지 완성할 수 있었다.

### Miniconda

Miniconda로 프로젝트 환경을 관리했다. 프로젝트별로 의존성을 분리하면 버전 충돌을 막고, 클라우드 배포 서버를 포함한 다른 환경에서도 동일하게 재현하기 쉬워진다.

---

## 어떻게 만들었나

### 1단계: 로컬 개발

Conda 전용 환경을 만들고 필요한 패키지를 설치했다: `langchain`, `langchain-google-genai`, `streamlit`.

`main.py`에서:
- `init_chat_model`로 Gemini 모델을 불러왔다
- 주제를 받아 시 작성을 지시하는 프롬프트 템플릿을 작성했다
- Streamlit UI를 구성했다: 제목, 텍스트 입력 필드, 제출 버튼, 로딩 스피너

API 키는 로컬 `.env` 파일에 저장했고, 시 생성이 끝에서 끝까지 잘 작동할 때까지 로컬에서 테스트했다.

### 2단계: 버전 관리와 GitHub 연동

Git 저장소를 초기화하고, 푸시 전에 한 가지를 의도적으로 바꿨다. 기본 브랜치 이름을 `master`에서 `main`으로 변경했고, 앞으로 모든 프로젝트에서 `main`을 기본으로 사용하도록 Git 전역 설정도 업데이트했다.

그런 다음 GitHub CLI(`gh`)로 원격 저장소를 만들고 코드를 푸시했다:

```bash
gh repo create ai-poet --public --source=. --remote=origin --push
```

원격 저장소: [https://github.com/artistjini/ai-poet.git](https://github.com/artistjini/ai-poet.git)

### 3단계: 배포와 디버깅

GitHub 저장소를 Streamlit Community Cloud에 연결하고 첫 번째 배포를 시작했다. 실패했다. 고쳤다. 또 실패했다, 다른 이유로. 또 고쳤다.

무엇이 잘못됐고 어떻게 해결했는지 기록한다.

---

## 배포 과정의 디버깅

### 이슈 1: 의존성 설치 오류

**에러:** `Error installing requirements`

**원인:** `requirements.txt`가 내 로컬 머신의 절대 경로를 포함한 채로 생성되어 있었다. 클라우드 환경에서는 그 경로를 해석할 수 없었다.

**해결:** `requirements.txt`를 표준 형식으로 처음부터 다시 작성했다. 한 줄에 패키지 이름 하나(필요하면 버전 고정). 로컬 경로 없음, 불필요한 메타데이터 없음. 재배포 성공.

### 이슈 2: API 인증 오류

**에러:** `ChatGoogleGenerativeAIError` — API 키를 찾을 수 없음

**원인:** 클라우드 환경은 내 로컬 `.env` 파일에 접근할 수 없다. 거기에 저장한 API 키가 배포 서버 입장에서는 아예 존재하지 않는 셈이었다.

**해결:** Streamlit Community Cloud 대시보드에는 **Secrets** 관리 기능이 있다. 거기에 `GOOGLE_API_KEY`를 등록하고, 앱 코드도 `.env` 파일 대신 `st.secrets`에서 키를 읽도록 수정했다. 인증 문제 해결.

### 이슈 3: 할당량 초과

**에러:** `429 RESOURCE_EXHAUSTED`

**원인:** Gemini API 무료 티어에는 요청 제한이 있다. 테스트 중에 그 한도에 도달했다.

**해결:** 이건 코드를 수정할 필요가 없었다. 로그를 읽어 원인을 확인하고, 할당량 초기화 시간을 기다렸다. 그리고 앞으로 실서비스를 설계할 때는 할당량 관리를 처음부터 고려해야 한다는 걸 배웠다.

---

## 최종 결과

앱은 배포되어 작동 중이다. 최종 결과물이 하는 일:

- 텍스트 입력으로 주제를 받는다
- LangChain 체인을 통해 Gemini에 전달한다
- 생성된 시를 실시간으로 표시한다
- 출력을 초기화하는 리셋 버튼을 포함한다

더 중요한 것은, 이 프로젝트가 전체 개발 사이클에 대한 직접적인 경험을 줬다는 점이다. 로컬 개발, 버전 관리, 클라우드 배포, 실제 운영 환경 디버깅. 마주한 에러들을 통해 더 값진 배움을 얻었다.

---

## 다음 단계
다국어 이메일 생성기 만들기 실습
- Ollama
- Lianma 3.1
- Local Liama 2
- CTransformers
