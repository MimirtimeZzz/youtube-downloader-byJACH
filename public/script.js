class YouTubeDownloader {
    constructor() {
        this.currentVideoInfo = null;
        this.selectedFormat = 'mp4';
        this.init();
    }

    init() {
        this.bindEvents();
        this.showWelcomeMessage();
    }

    bindEvents() {
        // Eventos de botones
        document.getElementById('analyze-btn').addEventListener('click', () => this.analyzeVideo());
        document.getElementById('download-btn').addEventListener('click', () => this.downloadVideo());
        document.getElementById('open-folder-btn').addEventListener('click', () => this.openDownloadsFolder());
        
        // Enter en input de URL
        document.getElementById('youtube-url').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.analyzeVideo();
            }
        });

        // Selección de formato
        document.querySelectorAll('.format-option').forEach(option => {
            option.addEventListener('click', (e) => {
                this.selectFormat(e.currentTarget.dataset.format);
            });
        });
    }

    showWelcomeMessage() {
        console.log('🎥 YouTube Downloader by JACH - ¡Listo para usar!');
    }

    async analyzeVideo() {
        const urlInput = document.getElementById('youtube-url');
        const analyzeBtn = document.getElementById('analyze-btn');
        const url = urlInput.value.trim();

        if (!url) {
            this.showError('Por favor, ingresa una URL válida de YouTube');
            return;
        }

        if (!this.isValidYouTubeUrl(url)) {
            this.showError('La URL no parece ser de YouTube. Verifica que sea correcta.');
            return;
        }

        // Mostrar estado de carga
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analizando...';

        try {
            const response = await fetch('/api/video-info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Error desconocido');
            }

            this.currentVideoInfo = data;
            this.showVideoInfo(data);
            this.showDownloadOptions();

        } catch (error) {
            this.showError('Error al analizar el video: ' + error.message);
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analizar';
        }
    }

    isValidYouTubeUrl(url) {
        const patterns = [
            /^https?:\/\/(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)/,
            /^https?:\/\/(www\.)?youtube\.com\/embed\//,
            /^https?:\/\/(www\.)?youtube\.com\/v\//
        ];
        return patterns.some(pattern => pattern.test(url));
    }

    showVideoInfo(videoInfo) {
        const videoInfoDiv = document.getElementById('video-info');
        const thumbnail = document.getElementById('video-thumbnail');
        const title = document.getElementById('video-title');
        const uploader = document.getElementById('video-uploader');
        const duration = document.getElementById('video-duration');

        thumbnail.src = videoInfo.thumbnail;
        title.textContent = videoInfo.title;
        uploader.textContent = `Canal: ${videoInfo.uploader}`;
        duration.textContent = this.formatDuration(videoInfo.duration);

        videoInfoDiv.style.display = 'block';
    }

    showDownloadOptions() {
        document.getElementById('download-options').style.display = 'block';
        // Seleccionar MP4 por defecto
        this.selectFormat('mp4');
    }

    selectFormat(format) {
        this.selectedFormat = format;
        
        // Actualizar UI
        document.querySelectorAll('.format-option').forEach(option => {
            option.classList.remove('selected');
        });
        document.querySelector(`[data-format="${format}"]`).classList.add('selected');

        // Actualizar texto del botón
        const downloadBtn = document.getElementById('download-btn');
        const icon = format === 'mp3' ? 'fas fa-music' : 'fas fa-video';
        const text = format === 'mp3' ? 'Descargar Audio' : 'Descargar Video';
        
        downloadBtn.innerHTML = `<i class="${icon}"></i> ${text}`;
    }

    async downloadVideo() {
        if (!this.currentVideoInfo) {
            this.showError('Primero analiza un video');
            return;
        }

        const url = document.getElementById('youtube-url').value.trim();
        const quality = document.getElementById('quality-select').value;

        // Ocultar opciones y mostrar progreso
        document.getElementById('download-options').style.display = 'none';
        document.getElementById('download-status').style.display = 'block';
        document.getElementById('download-result').style.display = 'none';

        this.updateDownloadProgress('Iniciando descarga...', 10);

        try {
            // Simular progreso durante la descarga
            this.simulateProgress();

            const response = await fetch('/api/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: url,
                    format: this.selectedFormat,
                    quality: quality
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Error en la descarga');
            }

            // Descarga completada
            this.updateDownloadProgress('¡Descarga completada!', 100);
            
            setTimeout(() => {
                document.getElementById('download-status').style.display = 'none';
                document.getElementById('download-result').style.display = 'block';
            }, 1000);

        } catch (error) {
            this.showError('Error durante la descarga: ' + error.message);
            document.getElementById('download-status').style.display = 'none';
            document.getElementById('download-options').style.display = 'block';
        }
    }

    simulateProgress() {
        const progressFill = document.querySelector('.progress-fill');
        const statusText = document.getElementById('status-text');
        
        let progress = 10;
        const interval = setInterval(() => {
            if (progress < 90) {
                progress += Math.random() * 15;
                if (progress > 90) progress = 90;
                
                progressFill.style.width = progress + '%';
                
                if (progress < 30) {
                    statusText.textContent = 'Conectando con YouTube...';
                } else if (progress < 60) {
                    statusText.textContent = 'Descargando video...';
                } else {
                    statusText.textContent = 'Procesando archivo...';
                }
            }
        }, 500);

        // Limpiar el intervalo después de 30 segundos máximo
        setTimeout(() => {
            clearInterval(interval);
        }, 30000);
    }

    updateDownloadProgress(message, percent) {
        document.getElementById('status-text').textContent = message;
        document.querySelector('.progress-fill').style.width = percent + '%';
    }

    async openDownloadsFolder() {
        try {
            const response = await fetch('/api/open-downloads', {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error('No se pudo abrir la carpeta');
            }

        } catch (error) {
            this.showError('Error al abrir la carpeta: ' + error.message);
        }
    }

    formatDuration(seconds) {
        if (!seconds) return '';
        
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;

        if (hours > 0) {
            return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        } else {
            return `${minutes}:${secs.toString().padStart(2, '0')}`;
        }
    }

    showError(message) {
        // Crear notificación de error temporal
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-notification';
        errorDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i>
            <span>${message}</span>
        `;

        // Agregar estilos si no existen
        if (!document.querySelector('.error-notification-styles')) {
            const style = document.createElement('style');
            style.className = 'error-notification-styles';
            style.textContent = `
                .error-notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: #e74c3c;
                    color: white;
                    padding: 15px 20px;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    z-index: 1000;
                    animation: slideIn 0.3s ease;
                    max-width: 400px;
                    box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
                }
                
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                
                .error-notification i {
                    font-size: 18px;
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(errorDiv);

        // Remover después de 5 segundos
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    reset() {
        // Resetear interfaz para nueva descarga
        document.getElementById('video-info').style.display = 'none';
        document.getElementById('download-options').style.display = 'none';
        document.getElementById('download-status').style.display = 'none';
        document.getElementById('download-result').style.display = 'none';
        document.getElementById('youtube-url').value = '';
        this.currentVideoInfo = null;
    }
}

// Inicializar aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.youtubeDownloader = new YouTubeDownloader();
    
    // Agregar botón de reset/nueva descarga
    const resultDiv = document.getElementById('download-result');
    const resetButton = document.createElement('button');
    resetButton.className = 'btn-primary';
    resetButton.innerHTML = '<i class="fas fa-plus"></i> Nueva Descarga';
    resetButton.style.marginTop = '15px';
    resetButton.addEventListener('click', () => {
        window.youtubeDownloader.reset();
    });
    
    document.querySelector('.success-message').appendChild(resetButton);
});
