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

const downloadButton = document.getElementById('downloadButton');
const uploadInput = document.getElementById('uploadInput');

// Обработчик для кнопки "Вставить"
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
        tableContent.innerHTML = '<div class="loading">Загрузка данных...</div>';
        
        // Загружаем данные в зависимости от типа операции
        let endpoint;
        if (operationType === 'issue') {
            endpoint = 'http://localhost:8000/api/issues';
        } else {
            endpoint = 'http://localhost:8000/api/returns';
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
        
        // Проверка на соответсвие с идеальным набором
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
        
        // Определение статуса соответсвия
        const complianceStatus = calculateComplianceStatus(recognizedTools);
        updateComplianceStatus(complianceStatus);

        // Создаем массив инструментов на основе данных из БД
        const instrumentsList = [];
        
        if (latestRecord.screwdriver_minus > 0) instrumentsList.push({ instrument: "Отвертка «-»", finding: latestRecord.screwdriver_minus });
        if (latestRecord.screwdriver_plus > 0) instrumentsList.push({ instrument: "Отвертка «+»", finding: latestRecord.screwdriver_plus });
        if (latestRecord.screwdriver_on_the_offset_cross > 0) instrumentsList.push({ instrument: "Отвертка на смещенный крест", finding: latestRecord.screwdriver_on_the_offset_cross });
        if (latestRecord.whirlpool > 0) instrumentsList.push({ instrument: "Коловорот", finding: latestRecord.whirlpool });
        if (latestRecord.contouring_pliers > 0) instrumentsList.push({ instrument: "Пассатижи контровочные", finding: latestRecord.contouring_pliers });
        if (latestRecord.pliers > 0) instrumentsList.push({ instrument: "Пассатижи", finding: latestRecord.pliers });
        if (latestRecord.sharnitsa > 0) instrumentsList.push({ instrument: "Шарница", finding: latestRecord.sharnitsa });
        if (latestRecord.adjustable_wrench > 0) instrumentsList.push({ instrument: "Разводной ключ", finding: latestRecord.adjustable_wrench });
        if (latestRecord.oil_can_opener > 0) instrumentsList.push({ instrument: "Открывашка для банок с маслом", finding: latestRecord.oil_can_opener });
        if (latestRecord.horn_wrench_union > 0) instrumentsList.push({ instrument: "Ключ рожковый/накидной ¾", finding: latestRecord.horn_wrench_union });
        if (latestRecord.side_cutters > 0) instrumentsList.push({ instrument: "Бокорезы", finding: latestRecord.side_cutters });
        
        if (instrumentsList.length === 0) {
            tableContent.innerHTML = '<div class="loading">Не распознано ни одного инструмента</div>';
            return;
        }
        
        // Отображаем инструменты в формате как в mockData
        instrumentsList.forEach(item => {
            const row = document.createElement('div');
            row.className = 'tableRow';
            row.innerHTML = `
                <div class="instrumentCol">${item.instrument}</div>
                <div class="findingCol">${item.finding}</div>
            `;
            tableContent.appendChild(row);
        });

        // // Показ размеченной картинки от CV
        // if (latestRecord.image_base64) {
        //     const imgElement = document.getElementById("cvResultImage");
        //     if (imgElement) {
        //         imgElement.src = "data:image/jpeg;base64," + latestRecord.image_base64;
        //         imgElement.style.display = "block";  // на всякий случай включаем
        //     }
        // }
        
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
        tableContent.innerHTML = '<div class="loading">Ошибка загрузки данных</div>';
    }
}

// Убираем автоматическую загрузку при старте и добавляем обработчики
document.addEventListener('DOMContentLoaded', function() {
    const checkButton = document.getElementById('check_save_Button');
    const tabelInput = document.querySelector('.TebelID');
    
    // Загружаем данные только при нажатии кнопки "Проверить"
    if (checkButton) {
        checkButton.addEventListener('click', function() {
            const tabelID = tabelInput.value;
            if (!tabelID) {
                alert('Пожалуйста, введите табельный номер');
                return;
            }
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
        const response = await fetch('http://localhost:8000/api/process-tools', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('Успешно:', result);

            // Обновление таблицы после успешной операции
            loadInstrumentsData(operationType);
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
    const checkButton = document.getElementById('check_save_Button');
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