from dependencies import get_db, get_current_active_user
from schemas import AssistantPrompt, AssistantAnswer, AssistantHints, ChatHistory, ChatHistoryCreate
from models import ChatHistoryDB, UserDB
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import requests
import json
import os
from typing import List

assistant_router = APIRouter(prefix="/assistant", tags=["Assistant"])


@assistant_router.get("", response_model=List[ChatHistory])
async def get_chat_history(current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_chat_history = db.query(ChatHistoryDB).filter(
        ChatHistoryDB.user_id == current_user.id).first()
    if not db_chat_history:
        return []

    chat_history = ChatHistory.from_orm(db_chat_history)
    chat_history.messages = chat_history.messages.split("#")
    return [chat_history]


@assistant_router.post("", response_model=AssistantAnswer)
async def make_prompt(prompt: AssistantPrompt, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_chat_history = db.query(ChatHistoryDB).filter(
        ChatHistoryDB.user_id == current_user.id).first()
    is_new_chat = False
    if db_chat_history:
        chat_history = ChatHistory.from_orm(
            db_chat_history).messages.split("#")
        chat_history = [{"Student" if i % 2 == 0 else "Assistant": chat_history[i]}
                        for i in range(len(chat_history))]
    else:
        chat_history = []
        is_new_chat = True

    with open("./site_guide.txt", "r", encoding="utf-8") as file:
        site_guide = file.read().strip()

    prompt_text = f"Ты - помощник для студента на сайте с сервисами для университета. Ты разговариваешь на русском языке, не используешь грубую лексику, не отвечаешь на посторонние вопросы - только те, которые касаются твоей работы. Если тебе задали вопрос не по теме - ответь 'К сожалению, я не могу ответить на этот вопрос, так как он не касается работы сайта.'. Тебе не нужно отправлять абстрактные предложения о помощи, например, нельзя писать 'Если что-то не понятно, то я могу помочь'. Твое сообщение должно быть исчерпывающим, но не длинным. Не нужно предоставлять лишней информации, о которой пользователь не просил. Не используй символ '#' в ответе. Вот что представляет собой сайт: {site_guide}."
    if chat_history != "":
        prompt_text += f"До этого с этим студентом была следующая история переписки: {chat_history}. Учитывай эту историю при ответе на следующий вопрос. Возможно, студент будет задавать вопросы, связанные со своими предыдущими вопросами, либо твоими предыдущими ответами."
    prompt_text += f"Сейчас студент находится на странице, на которой представлены следующие данные: {prompt.context}. У него к тебе следующий вопрос (учитывай, что возможно студент задает вопросы, связанные с предыдущими вопросами, либо с твоими предыдущими ответами): {prompt.prompt}. Помоги ему решить этот вопрос - выполни задачу, которую он тебе поставил, используя информацию о сайте и о текущей странице."

    api_key = 'cpk_b9f646794b554414935934ec5a3513de.f78245306f06593ea49ef7bce2228c8e.kHJVJjyK8dtqB0oD2Ofv4AaME6MSnKDy'
    response = requests.post(
        url="https://llm.chutes.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}"
            # "Authorization": f"Bearer {os.getenv('CHUTES_API_KEY')}"
        },
        data=json.dumps({
            "model": "deepseek-ai/DeepSeek-V3-0324",
            "messages": [
                {
                    "role": "user",
                    "content": prompt_text
                }
            ]
        })
    )

    if response.status_code == 200:
        response_data = response.json()
        try:
            answer = response_data['choices'][0]['message']['content']

            if len(chat_history) >= 7 * 2 and len(chat_history) != 0:
                del chat_history[:2]
            chat_history += [{"Student": prompt.prompt}, {"Assistant": answer}]
            chat_history_str = "#".join(
                list(d.values())[0] for d in chat_history)

            if is_new_chat:
                chat_history_data = ChatHistoryCreate(
                    user_id=current_user.id, messages=chat_history_str)
                db_chat_history = ChatHistoryDB(**chat_history_data.dict())
                db.add(db_chat_history)
            else:
                db_chat_history.messages = chat_history_str

            db.commit()
            db.refresh(db_chat_history)

        except KeyError:
            print(json.loads(response.text))  # логирование ошибки
            raise HTTPException(
                status_code=404, detail="AI Assistant is not available at the moment")
        return AssistantAnswer(answer=answer)
    else:
        print(json.loads(response.text))  # логирование ошибки
        raise HTTPException(
            status_code=404, detail="AI Assistant is not available at the moment")


@assistant_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_history(current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_chat_history = db.query(ChatHistoryDB).filter(
        ChatHistoryDB.user_id == current_user.id).first()
    if db_chat_history:
        db.delete(db_chat_history)
        db.commit()
    return None


@assistant_router.get("/hints", response_model=AssistantHints)
async def get_hints(context: str):
    with open("./assistant_hints.json", "r", encoding="utf-8") as file:
        site_guide = json.load(file)
    if context not in site_guide:
        raise HTTPException(status_code=404, detail="Context not found")
    hints = site_guide[context]
    return AssistantHints(hints=hints)
