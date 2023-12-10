let model;

async function app() {
  console.log("Cargando MobileNet...");

  // Cargar el modelo.
  model = await mobilenet.load();
  console.log("MobileNet cargado con éxito");

  // Hacer una predicción con el modelo.
  const imgEl = document.querySelector("#img");
  const result = await model.classify(imgEl);
  console.log(result);
  const bestpred = result[0]
  console.log(bestpred);

  const consoleEL = document.querySelector("#console"); 
  consoleEL.innerHTML = result[0].className +" " + result[0].probability;
}

app();

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
