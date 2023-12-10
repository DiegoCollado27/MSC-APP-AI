const webcamElement = document.querySelector("#webcam");
const consoleEl = document.querySelector("#console");
let model;

async function app() {
  console.log("Cargando MobileNet...");

  // Cargar el modelo.
  model = await mobilenet.load();
  console.log("MobileNet cargado con éxito");

  // Crear un objeto desde la API de datos de Tensorflow.js para capturar la imagen (fotograma)
  // desde la cámara web como Tensor.
  const webcam = await tf.data.webcam(webcamElement);
  while (true) {
    const img = await webcam.capture();
    const result = await model.classify(img);

    consoleEl.innerText = `
      predicción: ${result[0].className}\n
      probabilidad: ${result[0].probability}
    `;
    //Eliminamos el tensor para recuperar memoria
    img.dispose();

    //Esperamos al siguiente animationframe
    await tf.nextFrame();
  }
}

app();
