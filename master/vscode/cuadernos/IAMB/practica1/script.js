let net;

async function loadModel() {
    console.log("Cargando modelo...");
    net = await cocoSsd.load();
    console.log("Modelo cargado con éxito.");
}

async function predictWithCocoModel() {
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
            const predictions = await net.detect(img);

            predictions.forEach(prediction => {
                const [x, y, width, height] = prediction.bbox;
                ctx.strokeStyle = 'red';
                ctx.lineWidth = 4;
                ctx.strokeRect(x, y, width, height);
                // Estilo para el texto
                ctx.fillStyle = 'red';
                ctx.font = '16px Arial';

                // Dibuja el nombre del objeto detectado
                ctx.fillText(prediction.class + ' (' + prediction.score.toFixed(2) + ')', x, y - 5);
            });
        };
    });
}

loadModel();
predictWithCocoModel();

/*
console.log("Cargando MobileNet...");

// Cargar el modelo.
mobilenet.load().then((model) => {
  console.log("MobileNet cargado con éxito");

  // Hacer una predicción con el modelo.
  const imgEl = document.querySelector("#img");
  model.classify(imgEl).then((result) => {
    console.log(result);
  });
});
*/
