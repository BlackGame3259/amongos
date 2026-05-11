from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    # El ID del video de Youtube que me pasaste es xESS0f9qaEo
    return """
    <html>
        <head>
            <title>Gato Fullscreen</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { background-color: black; overflow: hidden; }
                
                .contenedor-video {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                }

                iframe {
                    width: 100vw;
                    height: 100vh;
                    border: none;
                }
            </style>
        </head>
        <body>
            <div class="contenedor-video">
                <iframe 
                    src="https://www.youtube.com/embed/xESS0f9qaEo?autoplay=1&mute=0&controls=0&loop=1&playlist=xESS0f9qaEo" 
                    allow="autoplay; encrypted-media" 
                    allowfullscreen>
                </iframe>
            </div>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)