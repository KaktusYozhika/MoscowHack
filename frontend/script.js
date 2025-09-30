const API_BASE = (window.API_BASE_URL || "http://localhost:8000").replace(/\/+$/,'');
/////////////////////      Для поля табельного номера       ///////////////////////

const inputElement = document.querySelector('.TebelID');

    inputElement.addEventListener('focus', function() {
        this.style.color = '#303F52'; // Устанавливаем цвет текста при фокусе
    });

    inputElement.addEventListener('blur', function() {
        if (this.value) {
            this.style.color = '#303F52'; // Устанавливаем цвет текста после ввода
        }
    });


/////////////////////      Выбор функции: Выдача или Сдача       ///////////////////////

const switchInput = document.querySelector('.switchInput');
let currentOperationType = 'issue'; // По умолчанию "Выдача"

switchInput.addEventListener('change', function() {
    currentOperationType = this.checked ? 'return' : 'issue';
    console.log('Выбрано:', this.checked ? 'Сдача' : 'Выдача');
});


/////////////////////      Выбор значения распознования       ///////////////////////

const slider = document.getElementById('valueSlider');
const sliderValue = document.getElementById('sliderValue');

// Обновляем значение при изменении ползунка
slider.addEventListener('input', () => {
    sliderValue.textContent = slider.value; // Отображаем текущее значение
});


/////////////////////      Изображение       ///////////////////////

const uploadedImage = document.getElementById('uploadedImage');
const downloadButton = document.getElementById('downloadButton');
const uploadInput = document.getElementById('uploadInput');

// Обработчик для кнопки "Загрузить"
downloadButton.addEventListener('click', function() {
    uploadInput.click(); // Программно кликаем на скрытый input
});

// Обработчик для выбора файла
uploadInput.addEventListener('change', function(event) {
    previewImage(event);
});

function previewImage(event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        const img = document.getElementById('uploadedImage');
        img.src = e.target.result;
        img.style.display = 'block'; // Показываем изображение
    }

    if (file) {
        reader.readAsDataURL(file);
    }
}


/////////////////////      Заполнение таблицы       ///////////////////////

async function loadInstrumentsData(operationType = 'issue') {
    const tableContent = document.getElementById('tableContent');
    const tabelID = document.querySelector('.TebelID').value;
    
    // Если табельный номер не введен, показываем пустую таблицу
    if (!tabelID) {
        tableContent.innerHTML = '<div class="loading">Введите табельный номер, загрузите изображение и нажмите "Проверить"</div>';
        return;
    }
    
    try {
        // tableContent.innerHTML = '<div class="loading">Загрузка данных...</div>';
        
        // Загружаем данные в зависимости от типа операции
        let endpoint;
        if (operationType === 'issue') {
            endpoint = `${API_BASE}/api/issues`;
        } else {
            endpoint = `${API_BASE}/api/returns`;
        }


        
        const response = await fetch(endpoint);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        tableContent.innerHTML = '';
        
        if (data.length === 0) {
            tableContent.innerHTML = '<div class="loading">Нет данных для отображения</div>';
            return;
        }
        
        // Фильтруем данные по введенному табельному номеру
        const filteredData = data.filter(item => item.TabelID == tabelID);
        
        if (filteredData.length === 0) {
            tableContent.innerHTML = '<div class="loading">Нет данных для табельного номера ' + tabelID + '</div>';
            return;
        }
        
        // Берем последнюю запись для этого табельного номера
        const latestRecord = filteredData[filteredData.length - 1];
        
        // ЗАГРУЖАЕМ ДАННЫЕ РАСПОЗНАВАНИЯ ИЗ ПОСЛЕДНЕГО ЗАПРОСА
        // (это нужно сохранять где-то, например в localStorage или переменной)
        let recognitionData = JSON.parse(localStorage.getItem('last_recognition_data') || '{}');
        
        // Создаем массив инструментов на основе данных из БД
        const instrumentsList = [];
        
        // Маппинг для отображения русских названий
        const toolNames = {
            "screwdriver_minus": "Отвертка «-»",
            "screwdriver_plus": "Отвертка «+»", 
            "screwdriver_on_the_offset_cross": "Отвертка на смещенный крест",
            "whirlpool": "Коловорот",
            "contouring_pliers": "Пассатижи контровочные",
            "pliers": "Пассатижи",
            "sharnitsa": "Шарница",
            "adjustable_wrench": "Разводной ключ",
            "oil_can_opener": "Открывашка для банок с маслом",
            "horn_wrench_union": "Ключ рожковый/накидной ¾",
            "side_cutters": "Бокорезы"
        };
        
        // Маппинг для связи полей БД с классами YOLO
        const toolMapping = {
            "screwdriver_minus": "Отвертка_минус",
            "screwdriver_plus": "Отвертка_плюс",
            "screwdriver_on_the_offset_cross": "Отвертка_смещенный_крест",
            "whirlpool": "Коловорот",
            "contouring_pliers": "Пассатижи_контровочные", 
            "pliers": "Пассатижи",
            "sharnitsa": "Шэрница",
            "adjustable_wrench": "Разводной_ключ",
            "oil_can_opener": "Открывашка",
            "horn_wrench_union": "Ключ_рожковый_накидной_3_4",
            "side_cutters": "Бокорезы"
        };
        
        // Добавляем инструменты в список для отображения
        Object.keys(toolNames).forEach(toolKey => {
            const count = latestRecord[toolKey] || 0;
            if (count > 0) {
                const toolName = toolNames[toolKey];
                const yoloClass = toolMapping[toolKey];
                
                // Ищем confidence для этого инструмента
                let confidenceText = "";
                if (recognitionData.predictions) {
                    const toolPredictions = recognitionData.predictions.filter(
                        pred => pred.class_name === yoloClass
                    );
                    if (toolPredictions.length > 0) {
                        // Берем максимальное confidence среди всех экземпляров
                        const maxConfidence = Math.max(...toolPredictions.map(pred => pred.confidence));
                        confidenceText = ` (${Math.round(maxConfidence * 100)}%)`;
                    }
                }
                
                instrumentsList.push({ 
                    instrument: toolName, 
                    finding: count + confidenceText 
                });
            }
        });
        
        if (instrumentsList.length === 0) {
            tableContent.innerHTML = '<div class="loading">Не распознано ни одного инструмента</div>';
            return;
        }
        
        // Отображаем инструменты
        instrumentsList.forEach(item => {
            const row = document.createElement('div');
            row.className = 'tableRow';
            row.innerHTML = `
                <div class="instrumentCol">${item.instrument}</div>
                <div class="findingCol">${item.finding}</div>
            `;
            tableContent.appendChild(row);
        });
        
        // Проверяем соответствие
        const recognizedTools = {
            screwdriver_minus: latestRecord.screwdriver_minus,
            screwdriver_plus: latestRecord.screwdriver_plus,
            screwdriver_on_the_offset_cross: latestRecord.screwdriver_on_the_offset_cross,
            whirlpool: latestRecord.whirlpool,
            contouring_pliers: latestRecord.contouring_pliers,
            pliers: latestRecord.pliers,
            sharnitsa: latestRecord.sharnitsa,
            adjustable_wrench: latestRecord.adjustable_wrench,
            oil_can_opener: latestRecord.oil_can_opener,
            horn_wrench_union: latestRecord.horn_wrench_union,
            side_cutters: latestRecord.side_cutters
        };
        
        const complianceStatus = calculateComplianceStatus(recognizedTools);
        updateComplianceStatus(complianceStatus);
        
    } 
    catch (error) {
        console.error('Ошибка загрузки данных:', error);
        tableContent.innerHTML = '<div class="loading">Ошибка загрузки данных</div>';
    }
}

// Убираем автоматическую загрузку при старте и добавляем обработчики
document.addEventListener('DOMContentLoaded', function() {
    const checkButton = document.getElementById('check_Button');
    const tabelInput = document.querySelector('.TebelID');
    
    // Загружаем данные только при нажатии кнопки "Проверить"
    if (checkButton) {
        checkButton.addEventListener('click', function() {
            const tabelID = tabelInput.value;
            if (!tabelID) {
                alert('Пожалуйста, введите табельный номер');
                return;
            }

            // СРАЗУ показываем "Загрузка данных..." при нажатии кнопки
            const tableContent = document.getElementById('tableContent');
            tableContent.innerHTML = '<div class="loading">Загрузка данных...</div>';

            submitToolData(); // Эта функция вызовет loadInstrumentsData после успешной обработки
        });
    }
    
    // Показываем начальное сообщение вместо загрузки всех данных
    const tableContent = document.getElementById('tableContent');
    tableContent.innerHTML = '<div class="loading">Введите табельный номер и нажмите "Проверить"</div>';
});


/////////////////////      Отправка данных на сервер       ///////////////////////

async function submitToolData() {
    const tabelID = document.querySelector('.TebelID').value;
    const operationType = switchInput.checked ? 'return' : 'issue';
    const recognitionThreshold = slider.value;
    const imageFile = document.querySelector('.uploadInput').files[0];

    if (!tabelID) {
        alert('Пожалуйста, введите табельный номер');
        return;
    }
    
    if (!imageFile) {
        alert('Пожалуйста, загрузите изображение');
        return;
    }
    
    const formData = new FormData();
    formData.append('operation_type', operationType);
    formData.append('tabel_id', tabelID);
    formData.append('recognition_threshold', recognitionThreshold);
    formData.append('image', imageFile);
    
    try {
        const response = await fetch(`${API_BASE}/api/process-tools`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('Успешно:', result);

            // Сохранение данных распознавания для отображения Confidence
            // Здесь мы можем сохранить predictions из response CV-сервиса
            // Если в result есть данные распознавания, сохраняем их
            if (result.recognized_tools) {
                localStorage.setItem('last_recognition_data', JSON.stringify({
                    predictions: result.predictions_data // нужно убедиться, что этот параметр есть в ответе
                }));
            }

            // ОБНОВЛЯЕМ ИЗОБРАЖЕНИЕ НА РАЗМЕЧЕННОЕ
            if (result.image_base64) {
                updateImageWithBoundingBoxes(result.image_base64);
            }

            // Обновление таблицы после успешной операции
            updateTableWithResultData(result, operationType);
            // loadInstrumentsData(operationType);
        } else {
            const error = await response.json();
            console.error('Ошибка:', error);
            alert('Произошлаs ошибка: ' + (error.detail || error.message));
        }
    } catch (error) {
        console.error('Ошибка сети:', error);
        alert('Ошибка сети: ' + error.message);
    }
}

// Функция для обновления изображения с боксами
function updateImageWithBoundingBoxes(imageBase64) {
    const uploadedImage = document.getElementById('uploadedImage');
    if (uploadedImage) {
        // Создаем Data URL из base64
        uploadedImage.src = "data:image/jpeg;base64," + imageBase64;
        uploadedImage.style.display = 'block';
    }
}

// Вспомогательная функция для конвертации base64 обратно в File
async function convertBase64ToFile(base64Data) {
    const response = await fetch("data:image/jpeg;base64," + base64Data);
    const blob = await response.blob();
    return new File([blob], "annotated_image.jpg", { type: "image/jpeg" });
}

// Функция для экранирования HTML
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Назначаем обработчик на кнопку "Проверить"
document.addEventListener('DOMContentLoaded', function() {
    const checkButton = document.getElementById('check_Button');
    if (checkButton) {
        checkButton.addEventListener('click', submitToolData);
    }
    
    // Загружаем данные при загрузке страницы (по умолчанию "Выдача")
    loadInstrumentsData('issue');
});

// Функция для вычисления статуса соответствия с идеальным набором
function calculateComplianceStatus(tools) {
    const idealSet = {
        screwdriver_minus: 1,
        screwdriver_plus: 1,
        screwdriver_on_the_offset_cross: 1,
        whirlpool: 1,
        contouring_pliers: 1,
        pliers: 1,
        sharnitsa: 1,
        adjustable_wrench: 1,
        oil_can_opener: 1,
        horn_wrench_union: 1,
        side_cutters: 1
    };
    
    for (const [tool, idealCount] of Object.entries(idealSet)) {
        const actualCount = tools[tool] || 0;
        if (actualCount !== idealCount) {
            return "Есть расхождения";
        }
    }
    
    return "Полное";
}

// Функция для обновления статуса соответствия с идеальным набором
function updateComplianceStatus(status) {
    const complianceElement = document.querySelector('.tableFooter');
    if (complianceElement) {
        complianceElement.innerHTML = `Соответствие: <span class="complianceText">${status}</span>`;
        
        // Добавляем стили в зависимости от статуса
        const complianceText = complianceElement.querySelector('.complianceText');
        if (complianceText) {
            if (status === 'Есть расхождения') {
                complianceText.style.color = '#A20000';
            }
        }
    }
}

/////////////////////      Скачивание отчета       ///////////////////////

document.getElementById('downloadReportButton').addEventListener('click', function() {
    downloadRawReport(); // Исправлено: вызываем существующую функцию
});

async function downloadRawReport() {
    try {
        const recognitionData = JSON.parse(localStorage.getItem('last_recognition_data') || '{}');
        
        if (!recognitionData.predictions || recognitionData.predictions.length === 0) {
            alert('Нет данных для отчета. Сначала выполните распознавание изображения.');
            return;
        }
        
        // Скачиваем "сырые" данные от модели
        const rawReport = {
            model_output: recognitionData,
            download_time: new Date().toISOString(),
            additional_info: {
                tabel_id: document.querySelector('.TebelID').value || 'Не указан',
                operation_type: switchInput.checked ? 'Сдача' : 'Выдача',
                recognition_threshold: slider.value + '%'
            }
        };
        
        const reportJson = JSON.stringify(rawReport, null, 2);
        const blob = new Blob([reportJson], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `instrument_report_${new Date().toISOString().slice(0, 10)}_${document.querySelector('.TebelID').value || 'unknown'}.json`;
        document.body.appendChild(a);
        a.click();
        
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        console.log('Отчет успешно скачан');
        
    } catch (error) {
        console.error('Ошибка при скачивании отчета:', error);
        alert('Ошибка при создании отчета: ' + error.message);
    }
}


// И добавьте новую функцию:
function updateTableWithResultData(result, operationType) {
    const tableContent = document.getElementById('tableContent');
    tableContent.innerHTML = '';
    
    // Используем данные из result, а не из БД
    const recognizedTools = result.recognized_tools;
    
    // Маппинг для отображения русских названий
    const toolNames = {
        "screwdriver_minus": "Отвертка «-»",
        "screwdriver_plus": "Отвертка «+»", 
        "screwdriver_on_the_offset_cross": "Отвертка на смещенный крест",
        "whirlpool": "Коловорот",
        "contouring_pliers": "Пассатижи контровочные",
        "pliers": "Пассатижи",
        "sharnitsa": "Шарница",
        "adjustable_wrench": "Разводной ключ",
        "oil_can_opener": "Открывашка для банок с маслом",
        "horn_wrench_union": "Ключ рожковый/накидной ¾",
        "side_cutters": "Бокорезы"
    };
    
    // Добавляем инструменты в список для отображения
    Object.keys(toolNames).forEach(toolKey => {
        const count = recognizedTools[toolKey] || 0;
        if (count > 0) {
            const toolName = toolNames[toolKey];
            
            // Ищем confidence для этого инструмента
            let confidenceText = "";
            if (result.predictions_data) {
                const toolPredictions = result.predictions_data.filter(
                    pred => pred.class_name === getYoloClassName(toolKey)
                );
                if (toolPredictions.length > 0) {
                    const maxConfidence = Math.max(...toolPredictions.map(pred => pred.confidence));
                    confidenceText = ` (${Math.round(maxConfidence * 100)}%)`;
                }
            }
            
            const row = document.createElement('div');
            row.className = 'tableRow';
            row.innerHTML = `
                <div class="instrumentCol">${toolName}</div>
                <div class="findingCol">${count}${confidenceText}</div>
            `;
            tableContent.appendChild(row);
        }
    });
    
    if (tableContent.children.length === 0) {
        tableContent.innerHTML = '<div class="loading">Не распознано ни одного инструмента</div>';
        return;
    }
    
    // Проверяем соответствие
    const complianceStatus = calculateComplianceStatus(recognizedTools);
    updateComplianceStatus(complianceStatus);
}

// Вспомогательная функция для получения YOLO имени класса
function getYoloClassName(toolKey) {
    const toolMapping = {
        "screwdriver_minus": "Отвертка_минус",
        "screwdriver_plus": "Отвертка_плюс",
        "screwdriver_on_the_offset_cross": "Отвертка_смещенный_крест",
        "whirlpool": "Коловорот",
        "contouring_pliers": "Пассатижи_контровочные", 
        "pliers": "Пассатижи",
        "sharnitsa": "Шэрница",
        "adjustable_wrench": "Разводной_ключ",
        "oil_can_opener": "Открывашка",
        "horn_wrench_union": "Ключ_рожковый_накидной_3_4",
        "side_cutters": "Бокорезы"
    };
    return toolMapping[toolKey];
}