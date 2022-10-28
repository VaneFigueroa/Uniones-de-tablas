#!/usr/bin/env python
# coding: utf-8

# ## Uniones internas y externas

# Para combinar información de varias tablas usamos las joins (uniones).
# El conjunto de datos no tiene claves primarias declaradas por lo que realizar uniones externas es una tarea desafiante debido a relaciones de muchos a muchos, la presencia de filas duplicadas y valores NULL en las columnas empleadas para combinar tablas. Ejecutamos uniones internas y externas. 

# In[1]:


get_ipython().run_line_magic('load_ext', 'sql')


# In[3]:


get_ipython().run_line_magic('sql', 'mysql://studentuser:studentpw@localhost/dognitiondb')


# In[4]:


get_ipython().run_line_magic('sql', 'USE dognitiondb')


# Las tablas en las bases de datos relacionales están vinculadas a través de claves primarias y, a veces, otros campos que son comunes a varias tablas. Nuestro objetivo cuando ejecutamos un JOIN o creamos una tabla unida es usar esas columnas comunes para permitir que la base de datos descubra qué filas en una tabla coinciden con qué filas en otra tabla. 
# Una vez que se establece la asignación utilizando al menos un campo o columna común, la base de datos puede extraer las columnas que desee de las tablas asignadas o unidas y generar los datos coincidentes en una tabla común. 
# Una inner join es una unión que genera solo filas que tienen una coincidencia exacta en ambas tablas que se unen:
# <img src="https://duke.box.com/shared/static/xazeqtyq6bjo12ojvgxup4bx0e9qcn5d.jpg" width=400 alt="INNER_JOIN" />
# 
# Es posible que desee incluir todos los datos de una tabla en sus cálculos o su salida, incluso si esos datos no coinciden con los datos de las otras tablas con las que se está uniendo. En este tipo de situaciones, utilizará uniones externas para conectar tablas. Las uniones externas incluyen uniones izquierdas, uniones derechas o uniones externas completas. Las uniones externas completas NO son compatibles con MySQL. 
# 
# <img src="https://duke.box.com/shared/static/4s89rmm8a75tep4puyqt1tdlhic0stzx.jpg" width=400 alt="SELECT FROM WHERE" />

# Por ejemplo, queremos obtener la información de los perros contenida en la tabla dogs, y la información de los resultados de la tabla de reviews para los usuarios que realizaron mas de 10  pruebas. 
# En este caso debemos unir información contenida en dos tablas; dogs y reviews, que tienen en común el campo de dog_guid y user_guid. Para evitar error en la consulta tenemos que especificar el nombre de la tabla antes de indicar el nombre del campo, y separar los dos nombres por un punto, de caso contrario MySQL no sabe cuál campo queremos dado que el título de la columna existe en ambas tablas. 
# Vemos primero qué sucede, si no le indicamos a qué tabla pertenece los campos de SELECT.

# In[5]:


get_ipython().run_cell_magic('sql', '', 'SELECT dog_guid AS DogID, user_guid AS UserID, AVG(rating) AS AvgRating, COUNT(rating) AS NumRatings, breed, breed_group, breed_type\nFROM dogs, reviews\nGROUP BY user_guid, dog_guid, breed, breed_group, breed_type\nHAVING NumRatings>= 10\nORDER BY AvgRating DESC\nLIMIT 5;')


# In[ ]:


get_ipython().run_cell_magic('sql', '', 'SELECT dogs.dog_guid AS DogID, dogs.user_guid AS UserID, AVG(reviews.rating) AS AvgRating,     \n       COUNT(reviews.rating) AS NumRatings, dogs.breed, dogs.breed_group, dogs.breed_type\nFROM dogs, reviews\nGROUP BY dogs.user_guid, dogs.dog_guid, dogs.breed, dogs.breed_group, dogs.breed_type\nHAVING NumRatings >= 10\nORDER BY AvgRating DESC\nLIMIT 5;')


# La consulta tal como está escrita no le dice a la base de datos cómo se relacionan las dos tablas. Hacer coincidir las dos tablas de acuerdo con los valores en la columna id_usuario y/o id_perro, cada fila de la tabla de perros se emparejará con cada fila de la tabla de reviews. Esto se conoce como un producto cartesiano. No solo será una carga pesada para la base de datos generar una tabla que tenga la longitud total de una tabla multiplicada por la longitud total de otra y la consulta tardaría mucho tiempo en ejecutarse, sino también la salida sería casi inútil.Para evitar que esto suceda, debemos indicar a la base de datos cómo relacionar las tablas en la cláusula WHERE:

# In[ ]:


get_ipython().run_cell_magic('sql', '', 'SELECT d.dog_guid AS DogID, d.user_guid AS UserID, AVG(r.rating) AS AvgRating, \n       COUNT(r.rating) AS NumRatings, d.breed, d.breed_group, d.breed_type\nFROM dogs d, reviews r\nWHERE d.dog_guid=r.dog_guid\nGROUP BY UserID, DogID, d.breed, d.breed_group, d.breed_type\nHAVING NumRatings >= 10\nORDER BY AvgRating DESC\nLIMIT 5;')


# Para tener mucho cuidado y excluir cualquier entrada dog_guid o user_guid incorrecta, puede incluir ambas columnas compartidas en la cláusula WHERE:

# In[ ]:


get_ipython().run_cell_magic('sql', '', 'SELECT d.dog_guid AS DogID, d.user_guid AS UserID, AVG(r.rating) AS AvgRating, \n       COUNT(r.rating) AS NumRatings, d.breed, d.breed_group, d.breed_type\nFROM dogs d, reviews r\nWHERE d.dog_guid=r.dog_guid AND d.user_guid=r.user_guid\nGROUP BY UserID, DogID, d.breed, d.breed_group, d.breed_type\nHAVING NumRatings >= 10\nORDER BY AvgRating DESC\nLIMIT 10;')


# Si queremos saber cuántos Golden Retrievers únicos que viven en Carolina del Norte hay en la base de datos, necesitamos los datos contenidos en las tablas de users y dogs:

# In[ ]:


get_ipython().run_cell_magic('sql', '', 'SELECT u.state AS state, d.breed AS breed, COUNT(DISTINCT d.dog_guid)\nFROM users u, dogs d\nWHERE d.user_guid=u.user_guid AND breed="Golden Retriever"\nGROUP BY state\nHAVING state="NC";')


# Nos preguntan para qué 3 razas de perros tenemos la mayor cantidad de datos de actividad del sitio ( usamos script_detail_id).

# In[ ]:


get_ipython().run_cell_magic('sql', '', 'SELECT d.breed, COUNT(s.script_detail_id) AS activity\nFROM dogs d, site_activities s\nWHERE d.dog_guid=s.dog_guid AND s.script_detail_id IS NOT NULL\nGROUP BY breed\nORDER BY activity DESC\nLIMIT 3;')


# Para unir varias tablas, se adopta el mismo enfoque que tomamos cuando estábamos uniendo dos tablas. Se enumera todos los campos que se desea extraer en la instrucción SELECT, enumeramos todas las tablas de las que se necesitará extraer los campos en la instrucción FROM y luego indicamos a la base de datos cómo conectar las tablas en la instrucción WHERE.
# 
# Para extraer el user_guid, el estado de residencia, el código postal del usuario, el dog_guid, la raza, el tipo de raza y el grupo de raza de todos los que completaron el juego "Yawn Warm-up", es posible que tenga la tentación de consultar:
# 

# In[ ]:


get_ipython().run_cell_magic('sql', '', 'SELECT c.user_guid AS UserID, u.state, u.zip, d.dog_guid AS DogID, d.breed, d.breed_type, d.breed_group\nFROM dogs d, complete_tests c, users u\nWHERE d.dog_guid=c.dog_guid \n   AND c.user_guid=u.user_guid\n   AND c.test_name="Yawn Warm-up"\nLIMIT 5;')


# Esta consulta enfoca las relaciones principalmente en la tabla complete_tests. Sin embargo, resulta que esta tabla tiene valores NULL en la columna user_guid. Por eso, si bien se ejecuta sin error, la salida no tiene filas. Entonces, vamos a emplear la tabla dogs para vicular las tablas pruebas_completas y usuarios. 

# In[ ]:


get_ipython().run_cell_magic('sql', '', 'SELECT d.user_guid AS UserID, u.state, u.zip, d.dog_guid AS DogID, d.breed, d.breed_type, d.breed_group\nFROM dogs d, complete_tests c, users u\nWHERE d.dog_guid=c.dog_guid \n   AND d.user_guid=u.user_guid\n   AND c.test_name="Yawn Warm-up"\nLIMIT 5;')


# Las uniones izquierda y derecha usan una sintaxis diferente a la que usamos en uniones internas. Vamos a decirle a la base de datos cómo conectar las tablas usando una cláusula ON que viene justo después de la cláusula FROM. Esto nos deja libre la cláusula WHERE para otras cosas que quizás desee incluir en su consulta, e irá después de la cláusula ON y antes de la cláusula GROUP BY.
# 
# En MySQL, JOIN significa unión interna, por lo que incluir la palabra "INNER" es opcional, y se puede ejecutar una unión interna con la sintaxis de las uniones externas. 

# In[ ]:


get_ipython().run_cell_magic('sql', '', "SELECT d.user_guid AS UserID, d.dog_guid AS DogID, d.breed, d.breed_type, d.breed_group\nFROM dogs d JOIN complete_tests c\nON d.dog_guid=c.dog_guid\nWHERE test_name='Yawn Warm-up';")


# In[ ]:


get_ipython().run_cell_magic('', '', "SELECT d.user_guid AS UserID, d.dog_guid AS DogID, \n       d.breed, d.breed_type, d.breed_group\nFROM dogs d, complete_tests c\nWHERE d.dog_guid=c.dog_guid AND test_name='Yawn Warm-up';")


# En las uniones externas, sin embargo, el orden importa mucho. Una combinación externa izquierda incluirá todas las filas de la tabla a la izquierda de las palabras clave LEFT JOIN. Una combinación externa derecha incluirá todas las filas de la tabla a la derecha de las palabras clave RIGHT JOIN. 
# Recuperar una lista completa de perros que completaron al menos 10 pruebas en la tabla de revisiones e incluir tanta información de raza como sea posible, podríamos consultar:

# In[ ]:


get_ipython().run_cell_magic('sql', '', 'SELECT r.dog_guid AS rDogID, d.dog_guid AS dDogID, r.user_guid AS rUserID, d.user_guid AS dUserID, AVG(r.rating) AS AvgRating, COUNT(r.rating) AS NumRatings, d.breed, d.breed_group, d.breed_type  \nFROM dogs d RIGHT JOIN reviews r  \nON   d.dog_guid=r.dog_guid   AND   d.user_guid=r.user_guid  \nWHERE r.dog_guid IS NOT NULL  \nGROUP BY r.dog_guid  \nHAVING NumRatings>=10  \nORDER BY AvgRating DESC\nLIMIT 5;  ')


# In[ ]:


get_ipython().run_cell_magic('sql', '', 'SELECT r.dog_guid AS rDogID, d.dog_guid AS dDogID, r.user_guid AS rUserID, d.user_guid AS dUserID, AVG(r.rating) AS AvgRating, COUNT(r.rating) AS NumRatings, d.breed, d.breed_group, d.breed_type\nFROM reviews r LEFT JOIN dogs d\n  ON r.dog_guid=d.dog_guid AND r.user_guid=d.user_guid\nWHERE r.dog_guid IS NOT NULL\nGROUP BY r.dog_guid\nHAVING NumRatings >= 10\nORDER BY AvgRating DESC\nLIMIT 5;')


# En la salida de la versión izquierda y derecha de la combinación externa, todas las filas que tenían un dog_guid en la tabla de reviews pero NO tenían un dog_guid coincidente en la tabla de perros, tienen la palabra "None" ingresada en las columnas de salida. "None", en este caso, es la forma en que Jupyter dice que el valor es NULL.

# La estrategia general que usan las bases de datos relacionales para unir tablas:
# <img src="https://duke.box.com/shared/static/km5c7scvo7u6aexzsy1i73wm28aizme1.jpg" width=400 alt="SELECT FROM WHERE" />
# 
# Las relaciones de tabla que tienen asignaciones de tabla a tabla mayores que 1 tienen efectos multiplicativos en los resultados de su consulta, debido a la forma en que las bases de datos relacionales combinan tablas. Para evitar problemas, es recomendable:
# 
# -  Verificar si los valores de las columnas con las que se relacionan las tablas, son únicos.
# -  verificar los resultados de las consultas. 
# -  Cuando sus consultas requieran varias capas de funciones o uniones, examine primero la salida de cada capa o unión antes de combinarlas todas juntas.

# Las combinaciones externas completas incluyen todas las filas de ambas tablas en una cláusula ON, independientemente de si existe un valor que vincule la fila de una tabla con una fila de la otra tabla.  Al igual que con las uniones izquierda o derecha, siempre que un valor en una fila no tenga un valor coincidente en la tabla unida, se ingresarán valores NULL para todos los valores en la tabla unida. 
# 
# Las uniones externas se usan muy raramente. La aplicación más práctica es si desea exportar todos sus datos sin procesar a otro programa para su visualización o análisis. La sintaxis para las uniones externas es la misma que para las uniones internas, pero reemplaza la palabra "inner" con "full outer".

# In[ ]:


get_ipython().run_cell_magic('sql', '', 'SELECT r.dog_guid AS rDogID, d.dog_guid AS dDogID, r.user_guid AS rUserID, d.user_guid AS dUserID, AVG(r.rating) AS AvgRating, COUNT(r.rating) AS NumRatings, d.breed, d.breed_group, d.breed_type\nFROM reviews r FULL OUTER JOIN dogs d\n  ON r.dog_guid=d.dog_guid AND r.user_guid=d.user_guid\nWHERE r.dog_guid IS NOT NULL\nGROUP BY r.dog_guid\nORDER BY AvgRating DESC\nLIMIT 5;')

