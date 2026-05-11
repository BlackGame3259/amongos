from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Beatbox Gato</title>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { background: black; overflow: hidden; display: flex; align-items: center; justify-content: center; height: 100vh; }
            
            /* La cámara ocupa todo el fondo */
            #output_canvas { position: absolute; width: 100vw; height: 100vh; object-fit: cover; transform: scaleX(-1); }
            video#input_video { position: absolute; opacity: 0; }

            /* Tu video gato.mp4 (oculto hasta que hagas la pose) */
            #video_gato {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                object-fit: cover;
                z-index: 10;
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
                
                let manosEnPose = 0;
                if (results.multiHandLandmarks) {
                    for (const landmarks of results.multiHandLandmarks) {
                        const yPalma = landmarks[9].y; 
                        // Si la mano está en la parte central/superior (pose de gato)
                        if (yPalma > 0.2 && yPalma < 0.7) {
                            manosEnPose++;
                        }
                    }
                }

                if (manosEnPose >= 2) {
                    if (gatoVideo.style.display !== 'block') {
                        gatoVideo.style.display = 'block';
                        gatoVideo.play();
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
            hands.setOptions({ maxNumHands: 2, modelComplexity: 1, minDetectionConfidence: 0.5, minTrackingConfidence: 0.5 });
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
    app.run(debug=True)