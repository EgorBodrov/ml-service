from datetime import datetime


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis
from rq.job import Job
from rq import Queue

from src.infrastructure.db.repositories import PredictorRepositoryImpl, UserBalanceRepositoryImpl, PredictionEventRepositoryImpl
from src.core.use_cases import PredictorUseCases, UserBalanceUseCases, PredictionEventUseCases
from src.infrastructure.web.controllers.get_current_user import get_current_user
from src.infrastructure.web.models.predict_models import (
    JobStatusResponse,
    PredictResponse,
    JobStatusRequest,
    PredictRequest,
    PredictorsResponse,
    EventsResponse,
)
from src.infrastructure.tasks.model_predict import predict as model_predict
from src.infrastructure.db.utils import get_session
from src.core.entities import User

router = APIRouter()

redis_conn = Redis(host="redis", port=6379)
queue = Queue(connection=redis_conn)


@router.get("/predictors", response_model=PredictorsResponse)
async def get_predictors(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    repo = PredictorRepositoryImpl(session)
    try:
        models = await PredictorUseCases(repo).get_all()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return PredictorsResponse(models=models or [])


@router.post("/predict", response_model=PredictResponse)
async def predict(
    request: PredictRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    repo = PredictorRepositoryImpl(session)
    try:
        predictor = await PredictorUseCases(repo).get(request.model_name)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    
    repo = UserBalanceRepositoryImpl(session)
    try:
        user_balance = await UserBalanceUseCases(repo).get(user.id)
        if user_balance.amount < predictor.price:
            raise HTTPException(status_code=400, detail="Not enough credits")

        await UserBalanceUseCases(repo).update(user.id, user_balance.amount - predictor.price)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    current_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    job = queue.enqueue(model_predict, request.model_name, request.data)

    repo = PredictionEventRepositoryImpl(session)
    try:
        await PredictionEventUseCases(repo).save(job.get_id(), user.id, request.model_name, current_time)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return PredictResponse(job_id=job.get_id())


@router.get("/predict")
async def job_status(request: JobStatusRequest, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    repo = PredictionEventRepositoryImpl(session)
    try:
        event = await PredictionEventUseCases(repo).get(request.job_id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    
    if not event.result:
        job = Job.fetch(request.job_id, connection=redis_conn)
        if job.is_finished:
            try:
                await PredictionEventUseCases(repo).set_result(request.job_id, job.result)
            except Exception as exc:
                raise HTTPException(status_code=400, detail=str(exc))
            
            return JobStatusResponse(
                status="finished",
                result=job.result,
                job_id=request.job_id,
                model_name=event.model_name,
                created_at=event.created_at,
                finished_at=event.finished_at
            )
        else:
            status = job.get_status()
    else:
        status = "finished"

    data = event.model_dump()
    del data["user_id"]
    data.update({"status": status})
    return JobStatusResponse.model_validate(data)


@router.get("/history")
async def get_history(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    repo = PredictionEventRepositoryImpl(session)
    try:
        job_ids = await PredictionEventUseCases(repo).get_all(user.id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    
    return EventsResponse(job_ids=job_ids or [])
