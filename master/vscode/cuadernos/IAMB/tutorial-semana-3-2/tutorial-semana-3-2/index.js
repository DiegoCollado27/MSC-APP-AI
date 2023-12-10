/* eslint-disable */
const imgEl = document.querySelector("#img");
const canvas = document.querySelector("#canvas");
const context = canvas.getContext("2d");

const imgbbox = imgEl.getBoundingClientRect();
canvas.style.top = imgbbox.y + "px";
canvas.style.left = imgbbox.x + "px";

const MODEL_URL =
  "https://tfhub.dev/google/tfjs-model/movenet/singlepose/lightning/4";

async function app() {
  const model = await tf.loadGraphModel(MODEL_URL, { fromTFHub: true });

  const imgTensor = await tf.browser.fromPixels(imgEl);

  const resizedImgTensor = tf.image.resizeBilinear(imgTensor, [192, 192]);
  resizedImgTensor.print(true);

  // detectamos la pose del cuerpo
  const prediction = await model.predict(resizedImgTensor.toInt().expandDims());
  const arrayOut = await prediction.array();
  const points = arrayOut[0][0];

  for (let i = 0; i < points.length; i++) {
    const point = points[i];

    if (point[2] > 0.4) {
      drawCircle(context, point[1] * 252, point[0] * 252, 3, "#003300");
    }
  }

  imgTensor.dispose();
  resizedImgTensor.dispose();
}

app();

function drawCircle(context, cx, cy, radius, color) {
  context.beginPath();
  context.arc(cx, cy, radius, 0, 2 * Math.PI, false);
  context.fillStyle = "red";
  context.fill();
  context.lineWidth = 1;
  context.strokeStyle = color;
  context.stroke();
}
