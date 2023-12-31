<p align="center"><img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png"></p>

<h1 align='center'> Proyecto Individual N°1</h1>

<h2 align='center'>Carlos Hidalgo, PART TIME 05</h2>

---


- ## **`Links`**
    - [Carpeta con los dataset](./Datasets/)
    - [Proceso de ETL y EDA](./ETL%20-%20EDA/)
    - [API desplegada en Render](https://steam-api1.onrender.com/docs)
    - [Link al video]()



---

# Introducción

En este proyecto, aplicaremos los conocimientos adquiridos durante nuestro tiempo en Henry para el proyecto de Data Science. Nos enfrentaremos a diversos desafíos, tanto a nivel personal como profesional.

1. **Exploración y Transformación de Datos:**
Se llevarán a cabo operaciones necesarias para leer archivos en formato JSON comprimido. Estos archivos contienen columnas anidadas, por lo que se utilizará el diccionario de datasets para identificar las relaciones entre ellos y operar de manera eficiente.


2. **Preparación de Datos:**
Los datos se prepararán meticulosamente para comprender las relaciones entre las variables. Además, se construirán funciones para realizar consultas a los datos, las cuales serán accesibles a través de una API.


3. **Modelado:**
Desarrollaremos modelos de Machine Learning con el objetivo de comprender las relaciones y predecir correlaciones entre variables (Item-Item).

¡Estamos emocionados por abordar este proyecto y aprovechar al máximo nuestras habilidades en Data Science!


## Diccionario de los Datos

<p align="center"><img src="./Imagenes/Diccionario de Datos STEAM.jpeg"></p>

---

# Desarrollo

### Exploración, Transformación y Carga (ETL)

A partir de los 3 dataset proporcionados (steam_games, user_reviews y user_items) referentes a la plataforma de Steam, en primera instancia se realizó el proceso de extraccion de los datos necesarios los cuales se resaltan en la anterior imagen.

## `steam_games`

#### Carga de Datos
- Se cargó el conjunto de datos steam_games desde el archivo comprimido, utilizando la biblioteca Pandas para facilitar el manejo y análisis de datos.

#### Limpieza de Datos
- Eliminación de filas totalmente nulas en el conjunto de datos para garantizar la calidad y consistencia de los datos.

#### Manejo de Valores Nulos
- Se identificaron y manejaron valores nulos en columnas específicas, utilizando estrategias como la eliminación de filas o la imputación de valores basados en 
información relevante.

#### Procesamiento de Fechas
- Se extrajeron años de la columna release_date para facilitar el análisis temporal.

#### Manipulación de Categorías
- Se desanidó la columna genres, que originalmente contenía múltiples géneros para un mismo juego, facilitando así un análisis más detallado.

#### Variables Dummy
- Se crearon variables dummy para la columna genres, lo que permitirá un análisis más fácil y preciso de los géneros de los juegos.

#### Exportación del Conjunto de Datos
- Se exportó el conjunto de datos limpio a un archivo CSV, proporcionando una versión final y limpia para futuras etapas del proyecto.

## `user_reviews`

#### Carga de Datos
- Se extrajeron datos del archivo comprimido "user_reviews.json.gz" y se organizó en un DataFrame.

#### Desanidado de Comentarios
- La columna "reviews" se desanidó, permitiendo un análisis individual de cada comentario al vincularlo con el usuario y el ID del juego correspondiente.

#### Análisis de Sentimientos
- Se utilizó NLTK para realizar un análisis de sentimientos en los comentarios. Se creó una nueva columna, "sentiment_analysis", con valores numéricos que representan sentimientos positivos, negativos o neutrales.

#### Visualización de Sentimientos
- Se creó un Violinplot con Seaborn para visualizar la distribución de las puntuaciones de sentimiento.

#### Manejo de Datos Faltantes
- Se identificaron y eliminaron filas con valores nulos.

#### ubconjunto de Datos
- Se seleccionó aleatoriamente el 10% del conjunto de datos para reducir su tamaño, facilitando el trabajo futuro.

#### Exportación de Datos
- El conjunto de datos procesado se exportó a un archivo CSV para su posterior uso.

## `user_items`

Descompresión del Conjunto de Datos
- Se descomprimió el archivo JSON anidado mediante la función descomprimir_json. Este método convirtió la información en un DataFrame de Pandas para facilitar el análisis.

#### Análisis Estadístico Preliminar
- Se realizó un análisis estadístico descriptivo utilizando el método describe(), revelando estadísticas clave sobre las columnas relevantes como "items_count," "playtime_forever," y "playtime_2weeks."

#### Manejo de Datos Faltantes
- Se identificaron y eliminaron las filas que contenían valores nulos en la columna "item_id," y se visualizaron las filas afectadas.

#### Eliminación de Columnas No Relevantes
- Se eliminaron las columnas "user_url," "playtime_2weeks," "steam_id," y "item_name" para enfocarse en la información esencial.

#### Visualización de Outliers
- Se utilizó un diagrama de caja (boxplot) para identificar outliers en la columna "playtime_forever," considerando que los valores pueden representar minutos y no necesariamente errores.

#### Exportación de Datos
- El conjunto de datos procesado se exportó a un archivo CSV y se comprimió en formato Gzip para facilitar el almacenamiento y uso eficiente de recursos.

#### Subconjunto de Datos
- Se seleccionó aleatoriamente el 10% del conjunto de datos original, proporcionando un conjunto de trabajo más manejable.



### Despliegue para la API

Se desarrollaron las siguientes funciones, a las cuales se podrá acceder desde la API en la página Render:

- **'def PlayTimeGenre( genero: str )'**: Retorna el año con más horas jugadas para dicho género.
- **'def UserForGenre( genero: str )'**: Retorna el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
- **'def UsersRecommend( año: int )'**: Devuelve el top 3 de juegos MÁSrecomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales).
- **'def UsersWorstDeveloper( año: int )'**: Devuelve el top 3 de desarrolladores con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos).
- **'def sentiment_analysis( empresa desarrolladora: str )**': Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentran categorizados con un análisis de sentimiento como valor.


### Modelo de Recomendación

#### Filtro Basado en Contenido

La función recomendacion_juego implementa un modelo de recomendación basado en contenido para juegos de Steam. A continuación, se describen los pasos y enfoques utilizados en el desarrollo de este modelo:

#### Generación de Recomendaciones:

Con base en la similitud calculada, se identifican los juegos más similares al juego de entrada. Estos juegos se almacenan en la variable juegos_recomendados.

#### Salida de Resultados:
La función devuelve una lista de nombres de aplicaciones correspondientes a los juegos recomendados.



## Contacto

<div style="display: flex; align-items: center;">
  <a href="https://www.linkedin.com/in/carlos-hidalgo84/" style="margin-right: 10px;">
    <img src="./images/in_linked_linkedin_media_social_icon_124259.png" alt="LinkedIn" width="40" height="40">
  </a>
  <a href="mailto:hidalgo.carlos1984@gmail.com" style="margin-right: 10px;">
    <img src="./images/gmail_new_logo_icon_159149.png" alt="Gmail" width="40" height="40">
  </a>
</div>

