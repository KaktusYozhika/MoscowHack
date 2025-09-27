const switchInput = document.querySelector('.switch-input');
        
switchInput.addEventListener('change', function() {
    console.log('Выбрано:', this.checked ? 'Сдача' : 'Выдача');
});







const slider = document.getElementById('valueSlider');
const sliderValue = document.getElementById('sliderValue');

// Обновляем значение при изменении ползунка
slider.addEventListener('input', () => {
    sliderValue.textContent = slider.value; // Отображаем текущее значение
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





// // Функция для загрузки данных
// async function loadInstrumentsData() {
//     const tableContent = document.getElementById('tableContent');
    
//     try {
//         // Показываем индикатор загрузки
//         tableContent.innerHTML = '<div class="loading">Загрузка данных...</div>';
        
//         // Запрос к API или серверу
//         const response = await fetch('/api/instruments'); // Замените на ваш endpoint
//         const data = await response.json();
        
//         // Очищаем контейнер
//         tableContent.innerHTML = '';
        
//         // Заполняем таблицу данными
//         if (data.length === 0) {
//             tableContent.innerHTML = '<div class="loading">Нет данных для отображения</div>';
//             return;
//         }
        
//         data.forEach(item => {
//             const row = document.createElement('div');
//             row.className = 'table-row';
//             row.innerHTML = `
//                 <div class="instrument-col">${escapeHtml(item.instrument)}</div>
//                 <div class="finding-col">${escapeHtml(item.finding)}</div>
//             `;
//             tableContent.appendChild(row);
//         });
        
//     } catch (error) {
//         console.error('Ошибка загрузки данных:', error);
//         tableContent.innerHTML = '<div class="loading">Ошибка загрузки данных</div>';
//     }
// }

// // Функция для экранирования HTML (защита от XSS)
// function escapeHtml(unsafe) {
//     return unsafe
//         .replace(/&/g, "&amp;")
//         .replace(/</g, "&lt;")
//         .replace(/>/g, "&gt;")
//         .replace(/"/g, "&quot;")
//         .replace(/'/g, "&#039;");
// }

// // Загружаем данные при загрузке страницы
// document.addEventListener('DOMContentLoaded', loadInstrumentsData);

// // Опционально: обновление данных по кнопке или таймеру
// function refreshData() {
//     loadInstrumentsData();
// }

// // Пример: обновление каждые 30 секунд
// // setInterval(loadInstrumentsData, 30000);





// Если API еще не готово, можно использовать тестовые данные
async function loadInstrumentsData() {
    const tableContent = document.getElementById('tableContent');
    
    // Имитация задержки загрузки
    tableContent.innerHTML = '<div class="loading">Загрузка данных...</div>';
    
    // Имитируем задержку сети (можно убрать, если не нужно)
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Тестовые данные
    const mockData = [
        { instrument: "Молоток", finding: "96" },
        { instrument: "Отвертка", finding: "98" },
        { instrument: "Отвертка на смещенный крест", finding: "98" },
        { instrument: "Плоскогубцы", finding: "99" },
        { instrument: "Ключ рожковый/накидной  ¾ ", finding: "98.7" },
        { instrument: "Открывашка для банок с маслом", finding: "97" },
        { instrument: "Рубанок", finding: "97.4" },
        { instrument: "Стамеска", finding: "98.9" },
        { instrument: "Отвертка на смещенный крест", finding: "96" },
        { instrument: "Отвертка", finding: "98" },
        { instrument: "Гаечный ключ", finding: "98" },
        { instrument: "Плоскогубцы", finding: "99" },
        { instrument: "Ключ рожковый/накидной  ¾ ", finding: "98.7" },
        { instrument: "Открывашка для банок с маслом", finding: "97" },
        { instrument: "Рубанок", finding: "97.4" },
        { instrument: "Стамеска", finding: "98.9" },
        // ... больше данных
    ];
    
    tableContent.innerHTML = '';
    
    mockData.forEach(item => {
        const row = document.createElement('div');
        row.className = 'table-row';
        row.innerHTML = `
            <div class="instrument-col">${item.instrument}</div>
            <div class="finding-col">${item.finding}</div>
        `;
        tableContent.appendChild(row);
    });
}

// ВАЖНО: вызвать функцию после объявления
loadInstrumentsData();