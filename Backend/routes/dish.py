from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional, Union
import requests
import json

from models import UserDB, DishDB
from schemas import UserRole, Dish, DishCreate
from dependencies import get_db, get_current_active_user, convert_to_db_types

dish_router = APIRouter(prefix="/dish", tags=["Dishes"])


async def enrich_dish_data_with_ai(name: str, description: Optional[str] = None, composition: Optional[str] = None) -> Dict[str, Any]:
    """
    Использует AI для заполнения отсутствующих данных о блюде:
    - описание и состав блюда
    - БЖУ и калорийность
    
    Args:
        name: Название блюда
        description: Описание блюда (если есть)
        composition: Состав блюда (если есть)
        
    Returns:
        Словарь с предполагаемыми значениями description, composition, proteins, fats, carbohydrates и kilocalories
    """
    # Определяем, нужно ли генерировать описание и состав
    need_description = is_empty_value(description)
    need_composition = is_empty_value(composition)
    
    # Формируем запрос для AI для получения БЖУ и калорийности
    nutrition_prompt = f"""Ты - диетолог и эксперт по пищевой ценности продуктов. 
Мне нужно, чтобы ты определил примерное содержание белков, жиров, углеводов и калорийность для блюда.

Название блюда: {name}"""
    
    if not need_description and description:
        nutrition_prompt += f"\nОписание: {description}"
    
    if not need_composition and composition:
        nutrition_prompt += f"\nСостав: {composition}"
    
    nutrition_prompt += """

Дай мне приблизительные данные в таком формате:
Белки (г): [значение]
Жиры (г): [значение]
Углеводы (г): [значение]
Калории (ккал): [значение]

Укажи только числовые значения с точностью до 0.1. Не добавляй никаких пояснений и комментариев."""
    
    # Если нужно сгенерировать описание и состав, создаем отдельный запрос
    if need_description or need_composition:
        description_prompt = f"""Ты - шеф-повар и эксперт по кулинарии.
Мне нужно, чтобы ты создал профессиональное описание и состав для блюда.

Название блюда: {name}

"""
        if need_description:
            description_prompt += """Напиши профессиональное описание блюда длиной не более 150 символов. Описание должно включать главные особенности блюда, вкус, текстуру и метод приготовления.

Описание:
"""
        
        if need_composition:
            description_prompt += """\nНапиши основные ингредиенты блюда, перечисляя их через запятую. Не включай точные количества, только названия всех основных продуктов в блюде.

Состав:
"""
    
    # Вызываем AI для получения питательной ценности
    nutrition_data = await call_ai_service(nutrition_prompt)
    
    # Подготавливаем результат
    result = {
        "proteins": None,
        "fats": None,
        "carbohydrates": None,
        "kilocalories": None
    }
    
    # Парсим данные о питательной ценности
    if nutrition_data and "content" in nutrition_data:
        nutrition_answer = nutrition_data["content"]
        
        for line in nutrition_answer.strip().split('\n'):
            if 'Белки' in line:
                try:
                    result['proteins'] = float(line.split(':')[1].strip().split(' ')[0])
                except:
                    result['proteins'] = None
            elif 'Жиры' in line:
                try:
                    result['fats'] = float(line.split(':')[1].strip().split(' ')[0])
                except:
                    result['fats'] = None
            elif 'Углеводы' in line:
                try:
                    result['carbohydrates'] = float(line.split(':')[1].strip().split(' ')[0])
                except:
                    result['carbohydrates'] = None
            elif 'Калории' in line:
                try:
                    result['kilocalories'] = float(line.split(':')[1].strip().split(' ')[0])
                except:
                    result['kilocalories'] = None
    
    # Если нужно, вызываем AI для получения описания и состава
    if need_description or need_composition:
        description_data = await call_ai_service(description_prompt)
        
        if description_data and "content" in description_data:
            description_answer = description_data["content"]
            
            # Парсим описание и состав
            extracted_description = None
            extracted_composition = None
            
            lines = description_answer.strip().split('\n')
            for i, line in enumerate(lines):
                if need_description and "Описание:" in line and i + 1 < len(lines):
                    extracted_description = lines[i + 1].strip()
                elif need_composition and "Состав:" in line and i + 1 < len(lines):
                    extracted_composition = lines[i + 1].strip()
            
            # Если описание не найдено, но есть другие строки, берем первую непустую строку
            if need_description and not extracted_description:
                for line in lines:
                    if line.strip() and "Состав:" not in line:
                        extracted_description = line.strip()
                        break
            
            # Если состав не найден, но есть другие строки после "Описание", берем их
            if need_composition and not extracted_composition:
                for i, line in enumerate(lines):
                    if "Описание:" in line and i + 2 < len(lines) and lines[i + 2].strip():
                        extracted_composition = lines[i + 2].strip()
                        break
            
            # Добавляем в результат
            if need_description:
                result['description'] = extracted_description if extracted_description else "Традиционное блюдо"
            
            if need_composition:
                result['composition'] = extracted_composition if extracted_composition else "Основные ингредиенты"
    
    return result


async def call_ai_service(prompt_text: str) -> Dict[str, Any]:
    """
    Вызывает AI сервис и возвращает результат.
    
    Args:
        prompt_text: Текст запроса к AI
        
    Returns:
        Словарь с ответом AI или None в случае ошибки
    """
    # Вызываем AI
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
    
    # Обрабатываем результат
    if response.status_code != 200:
        print(f"Ошибка при вызове AI: {response.status_code}, {response.text}")
        return None
    
    try:
        response_data = response.json()
        return {
            "content": response_data['choices'][0]['message']['content']
        }
    except Exception as e:
        print(f"Ошибка при обработке ответа AI: {e}")
        return None


def is_empty_value(value: Any) -> bool:
    """
    Проверяет, является ли значение "пустым" и требующим заполнения через AI.
    Пустыми считаются: None, 0, пустая строка, строка "string" или строка там, где ожидается число.
    
    Args:
        value: Проверяемое значение
        
    Returns:
        True если значение пустое, False в противном случае
    """
    if value is None:
        return True
    
    if isinstance(value, (int, float)) and value == 0:
        return True
    
    if isinstance(value, str):
        # Проверяем, является ли строка пустой, состоящей из пробелов или значением "string"
        return value == "" or value.isspace() or value.strip().lower() == "string"
    
    return False


@dish_router.get("", response_model=List[Dish])
async def read_dishes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dishes = db.query(DishDB).offset(skip).limit(limit).all()
    return dishes


@dish_router.get("/{dish_id}", response_model=Dish)
async def read_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(DishDB).filter(
        DishDB.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


@dish_router.post("", response_model=Dish)
async def create_dish(dish: DishCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only admins and teachers can create dish")

    dish_dict = convert_to_db_types(dish)
    
    # Проверяем, нужно ли заполнить данные с помощью AI
    needs_ai_enrichment = (
        is_empty_value(dish_dict.get('proteins')) or 
        is_empty_value(dish_dict.get('fats')) or 
        is_empty_value(dish_dict.get('carbohydrates')) or 
        is_empty_value(dish_dict.get('kilocalories')) or
        is_empty_value(dish_dict.get('description')) or
        is_empty_value(dish_dict.get('composition'))
    )
    
    if needs_ai_enrichment:
        # Получаем данные от AI
        ai_data = await enrich_dish_data_with_ai(
            name=dish_dict.get('name', ''),
            description=dish_dict.get('description'),
            composition=dish_dict.get('composition')
        )
        
        # Заполняем только отсутствующие поля
        if is_empty_value(dish_dict.get('proteins')):
            dish_dict['proteins'] = ai_data.get('proteins')
        
        if is_empty_value(dish_dict.get('fats')):
            dish_dict['fats'] = ai_data.get('fats')
        
        if is_empty_value(dish_dict.get('carbohydrates')):
            dish_dict['carbohydrates'] = ai_data.get('carbohydrates')
        
        if is_empty_value(dish_dict.get('kilocalories')):
            dish_dict['kilocalories'] = ai_data.get('kilocalories')
        
        if is_empty_value(dish_dict.get('description')) and 'description' in ai_data:
            dish_dict['description'] = ai_data.get('description')
        
        if is_empty_value(dish_dict.get('composition')) and 'composition' in ai_data:
            dish_dict['composition'] = ai_data.get('composition')

    db_dish = DishDB(**dish_dict)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


@dish_router.put("/{dish_id}", response_model=Dish)
async def update_dish(dish_id: int, dish: DishCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only admins and teachers can update dish")

    db_dish = db.query(DishDB).filter(
        DishDB.id == dish_id).first()
    if db_dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")

    dish_dict = convert_to_db_types(dish)
    
    # Проверяем, нужно ли заполнить данные с помощью AI
    needs_ai_enrichment = (
        is_empty_value(dish_dict.get('proteins')) or 
        is_empty_value(dish_dict.get('fats')) or 
        is_empty_value(dish_dict.get('carbohydrates')) or 
        is_empty_value(dish_dict.get('kilocalories')) or
        is_empty_value(dish_dict.get('description')) or
        is_empty_value(dish_dict.get('composition'))
    )
    
    if needs_ai_enrichment:
        # Получаем данные от AI
        ai_data = await enrich_dish_data_with_ai(
            name=dish_dict.get('name', ''),
            description=dish_dict.get('description'),
            composition=dish_dict.get('composition')
        )
        
        # Заполняем только отсутствующие поля
        if is_empty_value(dish_dict.get('proteins')):
            dish_dict['proteins'] = ai_data.get('proteins')
        
        if is_empty_value(dish_dict.get('fats')):
            dish_dict['fats'] = ai_data.get('fats')
        
        if is_empty_value(dish_dict.get('carbohydrates')):
            dish_dict['carbohydrates'] = ai_data.get('carbohydrates')
        
        if is_empty_value(dish_dict.get('kilocalories')):
            dish_dict['kilocalories'] = ai_data.get('kilocalories')
        
        if is_empty_value(dish_dict.get('description')) and 'description' in ai_data:
            dish_dict['description'] = ai_data.get('description')
        
        if is_empty_value(dish_dict.get('composition')) and 'composition' in ai_data:
            dish_dict['composition'] = ai_data.get('composition')

    for key, value in dish_dict.items():
        setattr(db_dish, key, value)

    db.commit()
    db.refresh(db_dish)
    return db_dish


@dish_router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_daily_menu(dish_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only admins and teachers can delete dish")

    db_dish = db.query(DishDB).filter(
        DishDB.id == dish_id).first()
    if db_dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")

    db.delete(db_dish)
    db.commit()
    return None
