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