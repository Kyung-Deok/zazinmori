from fastapi import FastAPI, Depends, Request, APIRouter
import uvicorn
from typing import Optional, List
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
#from models.textrank_new import Textderivation
from models.cvl_keywords import textcount
import nltk

# ========== model load ==============
app = FastAPI()
routes = APIRouter()

print('server_start')
nltk.download('punkt')
model_jiwon= Doc2Vec.load("/home/ubuntu/zzm_modelserver/models/ep250vec300_jiwon.doc2vec") # 지원
model1= Doc2Vec.load("/home/ubuntu/zzm_modelserver/models/ep250vec300_exp.doc2vec") # 경험
model2= Doc2Vec.load("/home/ubuntu/zzm_modelserver/models/ep250vec300_grow.doc2vec") # 성장
model3= Doc2Vec.load("/home/ubuntu/zzm_modelserver/models/ep250vec300_duty.doc2vec") # 직무
model4= Doc2Vec.load("/home/ubuntu/zzm_modelserver/models/ep250vec300_cha.doc2vec") #성격 장단점
model5= Doc2Vec.load("/home/ubuntu/zzm_modelserver/models/ep250vec300_iss.doc2vec") # 이슈
model6= Doc2Vec.load("/home/ubuntu/zzm_modelserver/models/ep250vec300_etc.doc2vec") #기타

# =====================================
class Request_by(BaseModel):
    corp_nm : str

@app.get('/')
def hello():
    return {"hello":"hello"}

'''
@app.post('/prediction/text_rank/')
async def text_rank(request: Request_by):
    kk = Textderivation(request.corp_nm) # 도출 예시
    context = {"result" : kk['']}
    return JSONResponse(context)
'''

@app.post('/prediction/cvl_keywords/')
def cvl_corp_nm(request: Request_by) :
    results= {}
    results['results'] = textcount(request.corp_nm)
    print(results['results'])
    # {"results" : []}
    return JSONResponse(results, status_code=200)

@app.post('/prediction/cvl_corp_nm/')
def cvl_corp_nm(request: Request_by) : 
    results = {}

    """지원항목이 비슷한 기업을 찾아준다"""
    results['similar_doc_jiwon'] = model_jiwon.docvecs.most_similar(request.corp_nm,topn=5)
    """경험항목이 비슷한 기업들"""
    results['similar_doc_exp'] = model1.docvecs.most_similar(request.corp_nm,topn=5)
    """자소서 작성시 성장과정이 유사한 기업들 """
    results['similar_doc_grow'] = model2.docvecs.most_similar(request.corp_nm,topn=5)
    """자소서 작성시 직무 유사한 기업들 """
    results['similar_doc_duty'] = model3.docvecs.most_similar(request.corp_nm,topn=5)
    """자소서 작성시 성격 장단점이 유사한 기업들 """
    results['similar_doc_cha'] = model4.docvecs.most_similar(request.corp_nm,topn=5)
    """자소서 작성시 이슈가 유사한 기업들 """
    results['similar_doc_iss'] = model5.docvecs.most_similar(request.corp_nm,topn=5)
    """자소서 작성시 기타 란이 유사한 기업들 """
    results['similar_doc_etc'] = model6.docvecs.most_similar(request.corp_nm,topn=5)
    print(results['similar_doc_iss'])
    return JSONResponse(results, status_code=200)


import doc_routes
# app.include_router(doc_routes.routes)



print('server_standby')
if __name__ == "__main__":
    # model 로드되는 함수, 파일 읽는 함수 전부 여기에 박기
    print("success")
    uvicorn.run("zzm:app", host="0.0.0.0", port=8988, reload=True)
    
