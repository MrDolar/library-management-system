# 馃摎 鏅鸿兘鍥句功绠＄悊绯荤粺

AI 椹卞姩鐨勭幇浠ｅ寲鍥句功绠＄悊骞冲彴锛岄泦鎴愭櫤鑳芥帹鑽愩€佽涔夋悳绱€佽嚜鍔ㄥ垎绫荤瓑 AI 鍔熻兘銆?
## 鉁?鍔熻兘鐗规€?
### 鏍稿績鍔熻兘
- 馃摉 **鍥句功绠＄悊** - CRUD銆佸垎绫汇€佸簱瀛樼鐞?- 馃攧 **鍊熼槄绠＄悊** - 鍊熶功銆佽繕涔︺€佺画鍊熴€侀€炬湡澶勭悊
- 馃懁 **鐢ㄦ埛绠＄悊** - 娉ㄥ唽銆佺櫥褰曘€佽鑹叉潈闄?- 馃搳 **鏁版嵁缁熻** - 鍊熼槄鎶ヨ〃銆佺儹闂ㄥ浘涔?
### AI 鏅鸿兘鍔熻兘 馃
- 馃幆 **鏅鸿兘鎺ㄨ崘** - 鍩轰簬鍊熼槄鍘嗗彶鐨勪釜鎬у寲鎺ㄨ崘
- 馃攳 **璇箟鎼滅储** - 鑷劧璇█鎻忚堪鎵句功锛堝"鍏充簬澶┖鐨勭骞诲皬璇?锛?- 馃彿锔?**鏅鸿兘鍒嗙被** - AI 鑷姩鎺ㄨ崘鍥句功鍒嗙被
- 馃摑 **鎽樿鐢熸垚** - 鑷姩鐢熸垚鍥句功绠€浠?- 馃挰 **瀵硅瘽鍔╂墜** - AI 鍥炵瓟鍥句功棣嗙浉鍏抽棶棰?
## 馃彈锔?鎶€鏈爤

| 灞傜骇 | 鎶€鏈?|
|------|------|
| 鍓嶇 | React 18 + TypeScript + Ant Design |
| 鍚庣 | Python 3.11 + FastAPI + SQLAlchemy |
| 鏁版嵁搴?| SQLite (寮€鍙? / PostgreSQL (鐢熶骇) |
| AI | OpenAI Compatible API |
| 璁よ瘉 | JWT |

## 馃殌 蹇€熷紑濮?
### 鍓嶇疆瑕佹眰
- Python 3.11+
- Node.js 18+ (鍓嶇寮€鍙?
- AI API Key (OpenAI / DeepSeek 绛?

### 鍚庣鍚姩

```bash
cd backend

# 瀹夎渚濊禆
pip install -r requirements.txt

# 閰嶇疆鐜鍙橀噺
cp .env.example .env
# 缂栬緫 .env锛屽～鍏ヤ綘鐨?AI_API_KEY

# 鍚姩鏈嶅姟
uvicorn app.main:app --reload --port 8000
```

鍚姩鍚庤闂?
- API 鏂囨。: http://localhost:8000/docs
- 鍋ュ悍妫€鏌? http://localhost:8000/health

### 鍓嶇鍚姩

```bash
cd frontend

# 瀹夎渚濊禆
npm install

# 鍚姩寮€鍙戞湇鍔″櫒
npm start
```

### Docker 閮ㄧ讲

```bash
docker-compose up -d
```

## 馃搧 椤圭洰缁撴瀯

```
library-management-system/
鈹溾攢鈹€ docs/                    # 馃搫 椤圭洰鏂囨。
鈹?  鈹溾攢鈹€ PRD.md              # 浜у搧闇€姹傛枃妗?鈹?  鈹溾攢鈹€ SYSTEM_DESIGN.md    # 绯荤粺璁捐鏂囨。
鈹?  鈹斺攢鈹€ TEST_PLAN.md        # 娴嬭瘯鍒嗘瀽鏂囨。
鈹溾攢鈹€ backend/                 # 馃悕 鍚庣鏈嶅姟
鈹?  鈹溾攢鈹€ app/
鈹?  鈹?  鈹溾攢鈹€ api/            # API 璺敱
鈹?  鈹?  鈹溾攢鈹€ models/         # 鏁版嵁妯″瀷
鈹?  鈹?  鈹溾攢鈹€ services/       # 涓氬姟閫昏緫
鈹?  鈹?  鈹斺攢鈹€ core/           # 鏍稿績妯″潡
鈹?  鈹斺攢鈹€ requirements.txt
鈹溾攢鈹€ frontend/                # 鈿涳笍 鍓嶇搴旂敤 (寰呭疄鐜?
鈹溾攢鈹€ docker-compose.yml
鈹斺攢鈹€ README.md
```

## 馃攼 瀹夊叏璁捐

### AI 瀵嗛挜瀹夊叏
- 鉁?API Key 浠呭瓨鍌ㄥ湪鏈嶅姟绔幆澧冨彉閲?- 鉁?鍓嶇涓嶆帴瑙︿换浣曞瘑閽?- 鉁?鎵€鏈?AI 璇锋眰閫氳繃鍚庣浠ｇ悊
- 鉁?`.env` 宸插姞鍏?`.gitignore`
- 鉁?鏀寔 Key 杞崲

### 璁よ瘉瀹夊叏
- JWT Token 璁よ瘉
- bcrypt 瀵嗙爜鍝堝笇
- 瑙掕壊鍒嗙骇鏉冮檺
- SQL 娉ㄥ叆闃叉姢

## 馃摉 API 鎺ュ彛

### 璁よ瘉
```
POST /api/auth/register    娉ㄥ唽
POST /api/auth/login       鐧诲綍
GET  /api/auth/me          褰撳墠鐢ㄦ埛
```

### 鍥句功
```
GET    /api/books           鍥句功鍒楄〃
POST   /api/books           鏂板鍥句功 (绠＄悊鍛?
GET    /api/books/{id}      鍥句功璇︽儏
PUT    /api/books/{id}      鏇存柊鍥句功 (绠＄悊鍛?
DELETE /api/books/{id}      鍒犻櫎鍥句功 (绠＄悊鍛?
GET    /api/books/search    鎼滅储鍥句功
```

### 鍊熼槄
```
POST /api/borrows              鍊熶功
PUT  /api/borrows/{id}/return  杩樹功
PUT  /api/borrows/{id}/renew   缁€?GET  /api/borrows/my           鎴戠殑鍊熼槄
```

### AI 鍔熻兘
```
POST /api/ai/recommend     鏅鸿兘鎺ㄨ崘
POST /api/ai/search        璇箟鎼滅储
POST /api/ai/classify      鏅鸿兘鍒嗙被
POST /api/ai/summarize     鎽樿鐢熸垚
POST /api/ai/chat          瀵硅瘽鍔╂墜
```

## 鈿欙笍 鐜鍙橀噺

| 鍙橀噺 | 璇存槑 | 榛樿鍊?|
|------|------|--------|
| `AI_API_KEY` | LLM API Key | (蹇呭～) |
| `AI_BASE_URL` | LLM API 鍦板潃 | https://api.openai.com/v1 |
| `AI_MODEL` | 瀵硅瘽妯″瀷 | gpt-3.5-turbo |
| `AI_EMBEDDING_MODEL` | 鍚戦噺妯″瀷 | text-embedding-ada-002 |
| `JWT_SECRET` | JWT 瀵嗛挜 | (鑷姩鐢熸垚) |
| `DATABASE_URL` | 鏁版嵁搴撳湴鍧€ | sqlite:///./library.db |

## 馃 鏀寔鐨?AI 鏈嶅姟

鏈郴缁熶娇鐢?OpenAI Compatible API锛屾敮鎸佷互涓嬫湇鍔★細

| 鏈嶅姟 | BASE_URL | 璇存槑 |
|------|----------|------|
| OpenAI | https://api.openai.com/v1 | 瀹樻柟 API |
| DeepSeek | https://api.deepseek.com/v1 | 鍥戒骇澶фā鍨?|
| 鏈湴妯″瀷 | http://localhost:11434/v1 | Ollama 绛?|
| 鍏朵粬 | 鑷畾涔?| 鍏煎 OpenAI 鏍煎紡鍗冲彲 |

## 馃搫 鏂囨。

- [浜у搧闇€姹傛枃妗?(PRD)](docs/PRD.md)
- [绯荤粺璁捐鏂囨。](docs/SYSTEM_DESIGN.md)
- [娴嬭瘯鍒嗘瀽鏂囨。](docs/TEST_PLAN.md)

## 馃摑 License

MIT License
