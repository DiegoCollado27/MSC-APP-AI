const webcamEl = document.querySelector("#webcam");
const liveView = document.querySelector("#liveView");
const appSection = document.querySelector("#app");
const enableWebcamButton = document.querySelector("#webcamButton");

function getUserMediaSupported() {
  return Boolean(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
}

if (getUserMediaSupported()) {
  enableWebcamButton.addEventListener("click", enableCam);
} else {
  console.warn("getUserMedia() is not supported by your browser");
}

let webcam;

async function enableCam(event) {
  if (!model) return;

  event.target.classList.add("removed");

  webcam = await tf.data.webcam(webcamEl);
  predictWebcam(webcam);
}

let model;

async function loadCocoSsdModel() {
  model = await cocoSsd.load();
  appSection.classList.remove("invisible");
}

try {
  loadCocoSsdModel();
} catch (error) {
  console.error(error);
}

const objects = [];

async function predictWebcam(webcam) {
  while (true) {
    const frame = await webcam.capture();
    const predictions = await model.detect(frame);
    for (let i = 0; i < objects.length; i++) {
      liveView.removeChild(objects[i]);
    }
    objects.splice(0);

    for (let n = 0; n < predictions.length; n++) {
      if (predictions[n].score > 0.66) {
        const p = document.createElement("p");
        const c = predictions[n].class;
        const score = Math.round(parseFloat(predictions[n].score) * 100);
        p.innerText = `${c} - with ${score}% confidence.`;
        p.style = `margin-left: ${predictions[n].bbox[0]}px; 
                   margin-top: ${predictions[n].bbox[1] - 10}px; 
                   width: ${predictions[n].bbox[2] - 10}px; 
                   top: 0; 
                   left: 0;`;

        const highlighter = document.createElement("div");
        highlighter.setAttribute("class", "highlighter");
        highlighter.style = `left: ${predictions[n].bbox[0]}px; 
                             top: ${predictions[n].bbox[1]}px; 
                             width: ${predictions[n].bbox[2]}px; 
                             height: ${predictions[n].bbox[3]}px;`;

        liveView.appendChild(highlighter);
        liveView.appendChild(p);
        objects.push(highlighter);
        objects.push(p);
      }
    }

    frame.dispose();
    await tf.nextFrame();
  }
}
