// Обновление статистики для становой
function updateStats() {
    fetch('/deadlift_stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('reps-count').textContent = data.reps;
            
            const formElement = document.getElementById('form-status');
            const formBadge = document.getElementById('form-badge');
            
            let formText = '';
            let formColor = '';
            
            switch(data.form) {
                case 'GOOD FORM':
                    formText = 'Отлично! ✨';
                    formColor = 'linear-gradient(135deg, #00b894, #00cec9)';
                    break;
                case 'TOO DEEP':
                    formText = 'Слишком глубоко ⚠️';
                    formColor = 'linear-gradient(135deg, #d63031, #e17055)';
                    break;
                case 'TOO HIGH':
                    formText = 'Слишком высоко 📏';
                    formColor = 'linear-gradient(135deg, #fdcb6e, #e17055)';
                    break;
                case 'ROUND BACK':
                    formText = 'Круглая спина ⚠️';
                    formColor = 'linear-gradient(135deg, #d63031, #e17055)';
                    break;
                default:
                    formText = 'Ожидание...';
                    formColor = 'linear-gradient(135deg, #b2bec3, #636e72)';
            }
            
            formElement.textContent = formText;
            formBadge.style.background = formColor;
            
            formBadge.style.transform = 'scale(1.05)';
            setTimeout(() => formBadge.style.transform = 'scale(1)', 200);

            updateCameraStatus(true);
        })
        .catch(error => {
            console.error('Error:', error);
            updateCameraStatus(false);
        });
}

function updateCameraStatus(isActive) {
    const statusBadge = document.getElementById('camera-status');
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');
    
    if (isActive) {
        statusBadge.style.background = 'rgba(0, 0, 0, 0.3)';
        statusDot.style.background = '#4CAF50';
        statusDot.style.animation = 'blink 2s infinite';
        statusText.textContent = 'Камера активна';
    } else {
        statusBadge.style.background = 'rgba(255, 0, 0, 0.3)';
        statusDot.style.background = '#ff4444';
        statusDot.style.animation = 'none';
        statusText.textContent = 'Камера не доступна';
        document.getElementById('form-status').textContent = 'Нет сигнала';
    }
}

function resetCounter() {
    fetch('/deadlift_reset')
        .then(response => response.json())
        .then(data => {
            document.getElementById('reps-count').textContent = data.reps;
            document.getElementById('form-status').textContent = 'Ожидание...';
            showNotification('Счетчик сброшен! 🔄');
            
            const counter = document.querySelector('.reps-badge .stats-value');
            counter.style.transform = 'scale(1.5)';
            counter.style.transition = 'transform 0.3s';
            setTimeout(() => counter.style.transform = 'scale(1)', 300);
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Ошибка при сбросе', 'error');
        });
}

function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = 'notification show';
    notification.style.background = type === 'error' 
        ? 'linear-gradient(135deg, #ff6b6b, #ee5253)' 
        : 'linear-gradient(135deg, #4158D0, #C850C0)';
    setTimeout(() => notification.classList.remove('show'), 3000);
}

function checkVideoFeed() {
    const videoFeed = document.getElementById('video-feed');
    setTimeout(() => {
        if (!videoFeed.complete || videoFeed.naturalHeight === 0) {
            updateCameraStatus(false);
        }
    }, 5000);
}

document.addEventListener('DOMContentLoaded', function() {
    updateStats();
    checkVideoFeed();
});

setInterval(updateStats, 500);