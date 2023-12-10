let model;
let video;
let canvas;
let ctx;

async function loadModel() {
    model = await faceDetection.createDetector(faceDetection.SupportedModels.MediaPipeFaceDetector, {
        runtime: 'mediapipe',
        solutionPath: 'https://cdn.jsdelivr.net/npm/@mediapipe/face_detection'
    });
}

async function setupCamera() {
    video = document.getElementById('webcam');
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');

    const stream = await navigator.mediaDevices.getUserMedia({ 'video': true });
    video.srcObject = stream;

    return new Promise((resolve) => {
        video.onloadedmetadata = () => {
            resolve(video);
        };
    });
}

async function detectFacesInRealTime() {
    await setupCamera();
    video.play();
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    async function detect() {
        const faces = await model.estimateFaces(video, false);

        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        faces.forEach(faceData => {
            // Dibujar la caja delimitadora y los puntos clave como antes
            drawBox(ctx, faceData.box);
            faceData.keypoints.forEach(keyPoint => {
                drawKeyPoint(ctx, keyPoint);
            });
        });

        requestAnimationFrame(detect);
    }

    detect();
}

function drawBox(ctx, box) {
    ctx.strokeStyle = 'green';
    ctx.lineWidth = 4;
    ctx.strokeRect(box.xMin, box.yMin, box.width, box.height);
}

function drawKeyPoint(ctx, keyPoint) {
    const radius = 5;
    ctx.beginPath();
    ctx.arc(keyPoint.x, keyPoint.y, radius, 0, 2 * Math.PI);
    ctx.fillStyle = 'red';
    ctx.fill();
    ctx.closePath();
}

loadModel().then(detectFacesInRealTime);
detectFaces();


