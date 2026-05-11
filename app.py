from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>IA Detector - Modo Gato</title>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
        <style>
            body { margin: 0; background: #121212; color: white; font-family: Arial; overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
            canvas { position: absolute; border-radius: 10px; transform: scaleX(-1); }
            video { position: absolute; opacity: 0; }
            #yt-container { display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 10; background: black; }
            iframe { width: 100%; height: 100%; border: none; }
            .instrucciones { z-index: 5; background: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; text-align: center; }
        </style>
    </head>
    <body>
        <div class="instrucciones">
            <h1>🐱 Detector de Pose Diego</h1>
            <p>Pon ambas manos frente a tu cara como el gato para activar el video.</p>
        </div>

        <video id="input_video"></video>
        <canvas id="output_canvas" width="640" height="480"></canvas>

        <div id="yt-container">
            <iframe id="yt-video" src="https://www.youtube.com/embed/xESS0f9qaEo?enablejsapi=1&mute=0&controls=0&loop=1&playlist=xESS0f9qaEo" allow="autoplay; encrypted-media"></iframe>
        </div>

        <script>
            const videoElement = document.getElementById('input_video');
            const canvasElement = document.getElementById('output_canvas');
            const canvasCtx = canvasElement.getContext('2d');
            const ytContainer = document.getElementById('yt-container');

            function onResults(results) {
                canvasCtx.save();
                canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
                canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
                
                let manosEnPose = 0;
                if (results.multiHandLandmarks) {
                    for (const landmarks of results.multiHandLandmarks) {
                        // Punto 9 es el centro de la palma (igual que en tu test_hands.py)
                        const yPalma = landmarks[9].y;
                        const xPalma = landmarks[9].x;

                        // Lógica de pose: manos cerca de la cara (Y entre 0.2 y 0.6)
                        if (yPalma > 0.2 && yPalma < 0.6 && xPalma > 0.2 && xPalma < 0.8) {
                            manosEnPose++;
                        }
                    }
                }

                // Si detecta 2 manos arriba, muestra el gato
                if (manosEnPose >= 2) {
                    ytContainer.style.display = 'block';
                } else {
                    ytContainer.style.display = 'none';
                }
                canvasCtx.restore();
            }

            const hands = new Hands({locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`});
            hands.setOptions({ maxNumHands: 2, modelComplexity: 1, minDetectionConfidence: 0.5, minTrackingConfidence: 0.5 });
            hands.onResults(onResults);

            const camera = new Camera(videoElement, {
                onFrame: async () => { await hands.send({image: videoElement}); },
                width: 640, height: 480
            });
            camera.start();
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True)