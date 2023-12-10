const BodyPart = { NOSE: 0, LEFT_EYE: 1, RIGHT_EYE: 2, LEFT_EAR: 3, RIGHT_EAR: 4, LEFT_SHOULDER: 5, RIGHT_SHOULDER: 6, LEFT_ELBOW: 7, RIGHT_ELBOW: 8, LEFT_WRIST: 9, RIGHT_WRIST: 10, LEFT_HIP: 11, RIGHT_HIP: 12, LEFT_KNEE: 13, RIGHT_KNEE: 14, LEFT_ANKLE: 15, RIGHT_ANKLE: 16 };
const poses = ["Utkatasana", "Bhujangasana", "Adhomukhasvanasana", "Vrikshana", "Virabhadrasana III"];

const predictionTextEl = document.querySelector("#txt-prediction");
const webcamEl = document.querySelector("#webcam");
const buttonTestModel = document.querySelector("#btn-test-model");
const buttonLoadModel = document.querySelector("#btn-load-model");
const buttonLoadMoveNetModel = document.querySelector("#btn-load-movenet");
const buttonTestMoveNet = document.querySelector("#btn-test-movenet");
const buttonTestWebcam = document.querySelector("#btn-webcam");

buttonTestModel.classList.toggle('btn-disable');
buttonTestMoveNet.classList.toggle('btn-disable');
buttonTestWebcam.classList.toggle('btn-disable');

const imgEl = document.querySelector("#img");
const canvas = document.querySelector("#canvas");
const context = canvas.getContext("2d");
const camerabbox =imgEl.getBoundingClientRect();
canvas.style.top = camerabbox.y + 'px';
canvas.style.left = camerabbox.x + 'px';

async function app() 
{
    const testDataObj = await loadTestData("../dataset_test/data.json");
    let model;
    let movenetModel;
    const URLmodel =  "https://tfhub.dev/google/tfjs-model/movenet/singlepose/lightning/4";

    buttonLoadModel.addEventListener('click', async function () 
    {
        buttonLoadModel.classList.toggle('btn-disable');
        model = await loadModel('../model/model.json');
        buttonTestModel.classList.toggle('btn-disable');
        buttonTestMoveNet.classList.toggle('btn-disable');
        buttonTestWebcam.classList.toggle('btn-disable');    
    });

    buttonTestModel.addEventListener('click', async function () 
    {
        buttonTestModel.classList.toggle('btn-disable');
        await testModel(model,testDataObj)
        buttonTestModel.classList.toggle('btn-disable');
    });

    buttonLoadMoveNetModel.addEventListener('click', async function () 
    {
        buttonLoadMoveNetModel.classList.toggle('btn-disable');
        model = await loadModel('../model/model.json');
        movenetModel = await tf.loadGraphModel(URLmodel, { fromTFHub: true });
        console.log(movenetModel);               
        buttonTestMoveNet.classList.toggle('btn-disable');
        buttonTestModel.classList.toggle('btn-disable');  
        buttonTestWebcam.classList.toggle('btn-disable');             
    });

    buttonTestMoveNet.addEventListener('click', async function () 
    {
        buttonTestMoveNet.classList.toggle('btn-disable');
        await loadNewImage();
        await testModelMoveNet(movenetModel,model);
        buttonTestMoveNet.classList.toggle('btn-disable');
    });


    buttonTestWebcam.addEventListener('click', async function () 
    {
        buttonTestWebcam.classList.toggle('btn-disable');
        const webcam = await tf.data.webcam(webcamEl, {resizeWidth: 192,resizeHeight: 192});
        const camerabbox = webcamEl.getBoundingClientRect();
        canvas.style.top = camerabbox.y + "px";
        canvas.style.left = camerabbox.x + "px";        
        const contextCam = canvas.getContext("2d");
        contextCam.translate(webcamEl.width, 0);
        contextCam.scale(-1, 1);
        while (true) 
        {
            const img = await webcam.capture();`    1q`
            const resizedImgTensorV = tf.image.resizeBilinear(img, [192, 192]);
            const predictionMoveNet = movenetModel.predict(resizedImgTensorV.toInt().expandDims());
            const pointsMoveNet = await predictionMoveNet.array();
            const tensorLandmarkMoveNetAux = pointsMoveNet[0][0];
            const LandmarksCam = [];
            for (let i = 0; i < tensorLandmarkMoveNetAux.length; i++) 
            {
                const aux = tensorLandmarkMoveNetAux[i].slice(0, 2);
                const yx = aux.map(valor => valor * 300);
                LandmarksCam.push(yx);
            }
            const tensorData = LandmarksCam.map(point => point.flat());
            const landmarksCamNet = tf.tensor2d(tensorData);    
            drawLandmarksOnImage(canvas, landmarksCamNet);
            const normalizeLandmarksMoveNet = normalizePoseLandmarks(landmarksCamNet).reshape([1, 34]);
            const predictionPose = classifyPose(model, normalizeLandmarksMoveNet);
            predictionTextEl.innerHTML = poses[predictionPose];
        }
    });
        
}


async function loadTestData(url) 
{
    const response = await fetch(url);
    const test_dataset = await response.json();
    return test_dataset;
}

async function loadModel(url) 
{
    try 
    {
        const model = await tf.loadLayersModel(url);
        console.log('Modelo:');
        model.summary();   
        return model; 
      } 
      catch (error) {console.error('Error al cargar:', error.message);  }
    return;
}

// inputData es el objeto JSON que contiene los datos del dataset de prueba
function loadRandomTestImage(inputData) 
{
        const randomIndex = Math.floor(Math.random() * inputData.length);
        const img = inputData[randomIndex];
        const path = `../dataset_test/${img.fileName}`;
        imgEl.src = path;
        console.log(path);
        const landmarks = tf.tensor2d(img.landmarks, [17,2]);
        return landmarks;
}
async function loadNewImage() 
{
    const input = document.createElement('input');
    input.type = 'file';
    return new Promise((resolve) => {
        input.addEventListener('change', async () => {
            const file = input.files[0];
            const imgPath = await readFileAsDataURL(file);
            imgEl.src = imgPath;
            resolve();
        });
        input.click();
    });
}

async function readFileAsDataURL(file) 
{
    return new Promise((resolve) => {
        const reader = new FileReader();

        reader.onloadend = function () {
            resolve(reader.result);
        };

        reader.readAsDataURL(file);
    });
}

// landmarks es un tensor [17,2]
function drawLandmarksOnImage(canvas, landmarks) 
{ 
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(imgEl, 0, 0, canvas.width, canvas.height);      
    landmarks.arraySync().forEach((point) => {
        drawCircle(context, point[1], point[0], 5, "red");
    });
}

// inputData es el objeto JSON que contiene los datos del dataset de prueba
async function testModel(model, inputData) 
{
    await tf.tidy(function () 
    {
        const landmarks =  loadRandomTestImage(inputData);        
        drawLandmarksOnImage(canvas, landmarks); 
        const normLandmarks = normalizePoseLandmarks(landmarks);
        const flatInputTensor = tf.reshape(normLandmarks, [1,34]);
        const prediction = classifyPose(model,flatInputTensor);
        predictionTextEl.innerHTML = poses[prediction];
    });
}

async function testModelMoveNet(movenetModel, model) 
{
    const imgTensor = tf.browser.fromPixels(imgEl);
    const resizedImgTensor = tf.image.resizeBilinear(imgTensor, [192, 192]);
    const prediction = movenetModel.predict(resizedImgTensor.toInt().expandDims());
    const points = await prediction.array();
    const tensorLandmarksaux = points[0][0];
    const landmarksMovenet = [];
    for (let i = 0; i < tensorLandmarksaux.length; i++) 
    {
        const aux = tensorLandmarksaux[i].slice(0, 2);
        const yx = aux.map(valor => valor * 300);
        landmarksMovenet.push(yx);
    }
    const tensorData = landmarksMovenet.map(point => point.flat());
    const landmarksNet = tf.tensor2d(tensorData);
    drawLandmarksOnImage(canvas, landmarksNet);
    const normalizeLandmarks = normalizePoseLandmarks(landmarksNet).reshape([1, 34]);
    const predictionPose = classifyPose(model, normalizeLandmarks);
    predictionTextEl.innerHTML = poses[predictionPose];
}


// inputTensor es un tensor [1,34]
function classifyPose(model, inputTensor) 
{
    const prediction = model.predict(inputTensor);
    const classification = tf.argMax(prediction, 1).dataSync()[0];
    console.log("Postura: ",classification);
    return classification;    
}

// landmarks es un tensor [17,2]
function getCenterPoint(landmarks, bodypartLeft, bodypartRight) 
{
    const left = tf.gather(landmarks, bodypartLeft);
    const right = tf.gather(landmarks, bodypartRight); 
    const center = tf.div(tf.add(left, right), 2); 
    return center;
}

// landmarks es un tensor [17,2]
function normalizePoseLandmarks(landmarks) 
{
    const poseCenter = getCenterPoint(landmarks, BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP);
    const poseSize = getPoseSize(landmarks);
    const normalizedPoseLandmarks = tf.div(tf.sub(landmarks, poseCenter), poseSize);
    return normalizedPoseLandmarks;
}

// landmarks es un tensor [17,2]
function getPoseSize(landmarks) 
{
    const hipCenter = getCenterPoint(landmarks, BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP);
    const shouldersCenter = getCenterPoint(landmarks, BodyPart.LEFT_SHOULDER, BodyPart.RIGHT_SHOULDER);    
    const torsoSize = tf.norm(tf.sub(shouldersCenter, hipCenter));
    const distToPoseCenter = tf.norm(tf.sub(landmarks, hipCenter), 2, 1);
    const poseSize = tf.max(tf.stack([torsoSize, tf.max(distToPoseCenter)]));
    return poseSize;
}

function drawCircle(ctx, cx, cy, radius, color) 
{
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, 2 * Math.PI, false);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.lineWidth = 1;
    ctx.strokeStyle = "#003300";
    ctx.stroke();
}

app();