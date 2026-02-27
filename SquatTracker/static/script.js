// Обновление статистики
function updateStats() {
    fetch('/stats')
        .then(response => response.json())
        .then(data => {
            // Обновляем счетчик повторений
            document.getElementById('reps-count').textContent = data.reps;
            
            // Обновляем статус формы
            const formElement = document.getElementById('form-status');
            const formBadge = document.getElementById('form-badge');
            
            let formText = '';
            let formColor = '';
            
            switch(data.form) {
                case 'GOOD DEPTH':
                    formText = 'Отлично! ✨';
                    formColor = 'linear-gradient(135deg, #00b894, #00cec9)';
                    break;
                case 'TOO DEEP':
                    formText = 'Слишком глубоко ⚠️';
                    formColor = 'linear-gradient(135deg, #d63031, #e17055)';
                    break;
                case 'BAD FORM':
                    formText = 'Неправильно 📏';
                    formColor = 'linear-gradient(135deg, #fdcb6e, #e17055)';
                    break;
                default:
                    formText = 'Ожидание...';
                    formColor = 'linear-gradient(135deg, #b2bec3, #636e72)';
            }
            
            formElement.textContent = formText;
            formBadge.style.background = formColor;
            
            // Анимация при обновлении
            formBadge.style.transform = 'scale(1.05)';
            setTimeout(() => {
                formBadge.style.transform = 'scale(1)';
            }, 200);

            // ЕСЛИ ПОЛУЧИЛИ ДАННЫЕ - ЗНАЧИТ КАМЕРА РАБОТАЕТ
            updateCameraStatus(true);
        })
        .catch(error => {
            console.error('Error:', error);
            // ЕСЛИ ОШИБКА - КАМЕРА НЕ РАБОТАЕТ
            updateCameraStatus(false);
        });
}

// Функция обновления статуса камеры
function updateCameraStatus(isActive) {
    const statusBadge = document.getElementById('camera-status');
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');
    
    if (isActive) {
        // Камера активна
        statusBadge.style.background = 'rgba(0, 0, 0, 0.3)';
        statusDot.style.background = '#4CAF50';
        statusDot.style.animation = 'blink 2s infinite';
        statusText.textContent = 'Камера активна';
    } else {
        // Камера не активна
        statusBadge.style.background = 'rgba(255, 0, 0, 0.3)';
        statusDot.style.background = '#ff4444';
        statusDot.style.animation = 'none';
        statusText.textContent = 'Камера не доступна';
        
        // Меняем текст формы
        document.getElementById('form-status').textContent = 'Нет сигнала';
    }
}

// Сброс счетчика
function resetCounter() {
    fetch('/reset')
        .then(response => response.json())
        .then(data => {
            // Обновляем счетчик
            document.getElementById('reps-count').textContent = data.reps;
            
            // Обновляем форму
            const formElement = document.getElementById('form-status');
            formElement.textContent = 'Ожидание...';
            
            showNotification('Счетчик сброшен! 🔄');
            
            // Анимация счетчика
            const counter = document.querySelector('.reps-badge .stats-value');
            counter.style.transform = 'scale(1.5)';
            counter.style.transition = 'transform 0.3s';
            setTimeout(function() {
                counter.style.transform = 'scale(1)';
            }, 300);
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Ошибка при сбросе', 'error');
        });
}

// Показ уведомления
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = 'notification show';
    
    if (type === 'error') {
        notification.style.background = 'linear-gradient(135deg, #ff6b6b, #ee5253)';
    } else {
        notification.style.background = 'linear-gradient(135deg, #4158D0, #C850C0)';
    }
    
    setTimeout(function() {
        notification.classList.remove('show');
    }, 3000);
}

// Проверка загрузки видео
function checkVideoFeed() {
    const videoFeed = document.getElementById('video-feed');
    
    // Если видео не загружается через 5 секунд
    setTimeout(function() {
        // Проверяем, загрузилось ли изображение
        if (!videoFeed.complete || videoFeed.naturalHeight === 0) {
            updateCameraStatus(false);
        }
    }, 5000);
}

// Запускаем обновление при загрузке
document.addEventListener('DOMContentLoaded', function() {
    updateStats();
    checkVideoFeed();
});

// Обновление статистики каждые 100мс для плавности
setInterval(updateStats, 100);