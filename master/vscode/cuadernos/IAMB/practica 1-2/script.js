let model;

async function loadModel() {
    model = await faceDetection.createDetector(faceDetection.SupportedModels.MediaPipeFaceDetector, {
        runtime: 'mediapipe',
        solutionPath: 'https://cdn.jsdelivr.net/npm/@mediapipe/face_detection'
    });
}

async function detectFaces() {
    const imgEl = document.getElementById('imageUpload');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    imgEl.addEventListener('change', async (event) => {
        let img = new Image();
        img.src = URL.createObjectURL(event.target.files[0]);
        img.onload = async () => {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);

            const faces = await model.estimateFaces(img, false);

            faces.forEach(faceData => {
                // Dibujar la caja delimitadora
                const box = faceData.box;
                drawBox(ctx, box);

                // Dibujar puntos clave
                faceData.keypoints.forEach(keyPoint => {
                    drawKeyPoint(ctx, keyPoint);
                });
            });
        };
    });
}

function drawBox(ctx, box) {
    ctx.strokeStyle = 'green';
    ctx.lineWidth = 4;
    ctx.strokeRect(box.xMin, box.yMin, box.width, box.height);
}

function drawKeyPoint(ctx, keyPoint) {
    const radius = 5; // Radio del círculo
    ctx.beginPath();
    ctx.arc(keyPoint.x, keyPoint.y, radius, 0, 2 * Math.PI);
    ctx.fillStyle = 'red';
    ctx.fill();
    ctx.closePath();
}

loadModel();
detectFaces();


