#!/usr/bin/env node

const express = require('express');
const cors = require('cors');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');
const open = require('open');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Servir archivos estáticos desde la carpeta public
app.use(express.static(path.join(__dirname, 'public')));

// Ruta principal
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Ruta para obtener información del video
app.post('/api/video-info', async (req, res) => {
    const { url } = req.body;
    
    if (!url) {
        return res.status(400).json({ error: 'URL es requerida' });
    }

    try {
        // Verificar que yt-dlp esté disponible
        const ytDlpPath = path.join(__dirname, 'bin', 'yt-dlp.exe');
        
        const ytDlp = spawn(ytDlpPath, [
            '--dump-json',
            '--no-playlist',
            url
        ]);

        let output = '';
        let error = '';

        ytDlp.stdout.on('data', (data) => {
            output += data.toString();
        });

        ytDlp.stderr.on('data', (data) => {
            error += data.toString();
        });

        ytDlp.on('close', (code) => {
            if (code === 0) {
                try {
                    const videoInfo = JSON.parse(output);
                    res.json({
                        title: videoInfo.title,
                        duration: videoInfo.duration,
                        uploader: videoInfo.uploader,
                        thumbnail: videoInfo.thumbnail,
                        formats: videoInfo.formats?.filter(f => f.ext).map(f => ({
                            format_id: f.format_id,
                            ext: f.ext,
                            quality: f.format_note || f.quality,
                            filesize: f.filesize
                        })) || []
                    });
                } catch (parseError) {
                    res.status(500).json({ error: 'Error procesando información del video' });
                }
            } else {
                res.status(500).json({ error: 'Error obteniendo información del video: ' + error });
            }
        });
    } catch (err) {
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// Ruta para descargar video
app.post('/api/download', async (req, res) => {
    const { url, format, quality } = req.body;
    
    if (!url) {
        return res.status(400).json({ error: 'URL es requerida' });
    }

    try {
        const downloadsPath = path.join(__dirname, 'downloads');
        if (!fs.existsSync(downloadsPath)) {
            fs.mkdirSync(downloadsPath, { recursive: true });
        }

        const ytDlpPath = path.join(__dirname, 'bin', 'yt-dlp.exe');
        
        // Configurar argumentos según el formato seleccionado
        let args = [
            '--output', path.join(downloadsPath, '%(title)s.%(ext)s'),
            url
        ];

        if (format === 'mp3') {
            args.push('--extract-audio', '--audio-format', 'mp3', '--audio-quality', '192K');
        } else if (format === 'mp4') {
            args.push('--format', quality || 'best[ext=mp4]');
        } else {
            args.push('--format', 'best');
        }

        const ytDlp = spawn(ytDlpPath, args);

        let output = '';
        let error = '';

        ytDlp.stdout.on('data', (data) => {
            output += data.toString();
        });

        ytDlp.stderr.on('data', (data) => {
            error += data.toString();
        });

        ytDlp.on('close', (code) => {
            if (code === 0) {
                res.json({ 
                    success: true, 
                    message: 'Descarga completada exitosamente',
                    downloadPath: downloadsPath
                });
            } else {
                res.status(500).json({ error: 'Error en la descarga: ' + error });
            }
        });
    } catch (err) {
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// Ruta para abrir carpeta de descargas
app.post('/api/open-downloads', (req, res) => {
    const downloadsPath = path.join(__dirname, 'downloads');
    
    try {
        // Abrir carpeta en el explorador de archivos
        spawn('explorer', [downloadsPath], { detached: true });
        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ error: 'No se pudo abrir la carpeta de descargas' });
    }
});

// Iniciar servidor
app.listen(PORT, () => {
    console.log(`🎥 YouTube Downloader by JACH ejecutándose en http://localhost:${PORT}`);
    console.log('🚀 Abriendo navegador...');
    
    // Abrir navegador automáticamente
    setTimeout(() => {
        open(`http://localhost:${PORT}`);
    }, 1000);
});
