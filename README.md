# Productividad Basada en Herramientas Tecnológicas

Aplicación web para detectar areas verdes desde imagenes satelitales.

Para probar el código necesitas descargar el modelo desde [google drive](https://drive.google.com/file/d/1-TnJiLB5GeQ7pluB40vYohObznoGmsR4/view?usp=sharing) y ponerlo junto con los otros archivos.

La aplicación funciona con flask y TensorFlow asi que necesitas estas dos librerias instaladas junto con PIL y numpy para procesar las imagenes.

Puedes usar la imagen **prueba.jpg** para probar el modelo, o tomar una captura de Google Maps, la imagen tiene que tener un tamaño multiplo de 256 ya que la imagen se divide en cuadros de 256x256 pixeles. Puede ser un tamaño de 1024x2048 para que la ejecución sea mas rapida.

## Ejemplo de la Aplicación

![Example 1](
https://github.com/vincent1bt/fase3-detector/blob/main/example_images/app1.png)
![Example 2](
https://github.com/vincent1bt/fase3-detector/blob/main/example_images/app2.png)

