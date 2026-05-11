import os
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Beatbox Gato - Pro</title>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { background: black; overflow: hidden; display: flex; align-items: center; justify-content: center; height: 100vh; }
            
            /* Cámara en pantalla completa de fondo */
            #output_canvas { position: absolute; width: 100vw; height: 100vh; object-fit: cover; transform: scaleX(-1); }
            video#input_video { position: absolute; opacity: 0; }

            /* Video del gato en ESPACIO PEQUEÑO (esquina superior derecha) */
            #video_gato {
                display: none;
                position: fixed;
                top: 20px;
                right: 20px;
                width: 320px; /* Tamaño pequeño */
                height: auto;
                border: 3px solid #00ff00; /* Un borde para que resalte */
                border-radius: 15px;
                z-index: 10;
                box-shadow: 0px 0px 20px rgba(0,255,0,0.5);
            }
        </style>
    </head>
    <body>
        <video id="input_video"></video>
        <canvas id="output_canvas"></canvas>

        <video id="video_gato" loop>
            <source src="{{ url_for('static', filename='gato.mp4') }}" type="video/mp4">
        </video>

        <script>
            const videoElement = document.getElementById('input_video');
            const canvasElement = document.getElementById('output_canvas');
            const canvasCtx = canvasElement.getContext('2d');
            const gatoVideo = document.getElementById('video_gato');

            canvasElement.width = window.innerWidth;
            canvasElement.height = window.innerHeight;

            function onResults(results) {
                canvasCtx.save();
                canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
                canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
                
                let manoEnBoca = false;
                let manoEnCabeza = false;

                if (results.multiHandLandmarks) {
                    for (const landmarks of results.multiHandLandmarks) {
                        const yPalma = landmarks[9].y; 

                        // Lógica de pose:
                        // 1. Mano en la boca (Zona central baja de la cara: Y entre 0.5 y 0.75)
                        if (yPalma > 0.5 && yPalma < 0.75) {
                            manoEnBoca = true;
                        }
                        // 2. Mano en la cabeza (Zona superior: Y entre 0.05 y 0.35)
                        if (yPalma > 0.05 && yPalma < 0.35) {
                            manoEnCabeza = true;
                        }
                    }
                }

                // Solo si AMBAS condiciones se cumplen al mismo tiempo
                if (manoEnBoca && manoEnCabeza) {
                    if (gatoVideo.style.display !== 'block') {
                        gatoVideo.style.display = 'block';
                        gatoVideo.play().catch(e => {});
                    }
                } else {
                    if (gatoVideo.style.display !== 'none') {
                        gatoVideo.style.display = 'none';
                        gatoVideo.pause();
                        gatoVideo.currentTime = 0; 
                    }
                }
                canvasCtx.restore();
            }

            const hands = new Hands({locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`});
            hands.setOptions({ maxNumHands: 2, modelComplexity: 1, minDetectionConfidence: 0.6, minTrackingConfidence: 0.6 });
            hands.onResults(onResults);

            const camera = new Camera(videoElement, {
                onFrame: async () => { await hands.send({image: videoElement}); },
                width: 1280, height: 720
            });
            camera.start();
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)