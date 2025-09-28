import requests
import json

# Базовый URL вашего API
BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_root():
    """Тест корневого эндпоинта"""
    response = requests.get("http://127.0.0.1:8000/")
    print("✅ Корневой эндпоинт:", response.json())
    return response.status_code == 200

def test_create_tool_issue():
    """Тест создания заказа на выдачу инструментов"""
    issue_data = {
        "TabelID": 123,
        "screwdriver": 2,
        "hammer": 1,
        "wrench": 3,
        "pliers": 0,
        "saw": 0,
        "drill": 1,
        "measuring_tape": 1,
        "level": 0,
        "knife": 1,
        "scissors": 0,
        "flashlight": 0
    }
    
    response = requests.post(f"{BASE_URL}/issue-tools/", json=issue_data)
    print("✅ Выдача инструментов:", response.status_code, response.json())
    return response.status_code == 200

def test_create_tool_return():
    """Тест создания заказа на сдачу инструментов"""
    return_data = {
        "TabelID": 123,
        "screwdriver": 2,
        "hammer": 1,
        "wrench": 3,
        "pliers": 0,
        "saw": 0,
        "drill": 1,
        "measuring_tape": 1,
        "level": 0,
        "knife": 1,
        "scissors": 0,
        "flashlight": 0
    }
    
    response = requests.post(f"{BASE_URL}/return-tools/", json=return_data)
    print("✅ Сдача инструментов:", response.status_code, response.json())
    return response.status_code == 200

def test_get_employee_history():
    """Тест получения истории сотрудника"""
    response = requests.get(f"{BASE_URL}/employee-history/123")
    print("✅ История сотрудника:", response.status_code, response.json())
    return response.status_code == 200

def test_image_upload():
    """Тест загрузки изображения (с тестовым файлом)"""
    try:
        # Создаем тестовое изображение
        from PIL import Image
        import os
        
        # Создаем простой тестовый изображение
        img = Image.new('RGB', (100, 100), color='red')
        test_image_path = 'test_image.jpg'
        img.save(test_image_path)
        
        # Отправляем изображение
        with open(test_image_path, 'rb') as f:
            files = {'file': ('test_image.jpg', f, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/upload-image/", files=files)
        
        print("✅ Загрузка изображения:", response.status_code, response.json())
        
        # Удаляем тестовый файл
        os.remove(test_image_path)
        return response.status_code == 200
        
    except Exception as e:
        print("❌ Ошибка теста изображения:", e)
        return False

if __name__ == "__main__":
    print("🚀 Запуск тестов API...")
    
    # Запускаем тесты последовательно
    tests = [
        test_root,
        test_create_tool_issue,
        test_create_tool_return, 
        test_get_employee_history,
        test_image_upload
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Ошибка в тесте {test.__name__}: {e}")
            results.append(False)
    
    print(f"\n📊 Результаты: {sum(results)}/{len(results)} тестов пройдено")