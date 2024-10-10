En esta estapa se llevó a cabo el despliegue del modelo de clasificación y, por ende, se creo tanto un API como una aplicación web para permitir la interacción por parte del usuario. A continuación, se presentan los pasos necesarios para ejecutar la totalidad de la aplicación.

### **Instrucciones de uso**
1. Clonar el repositorio
2. Dirigirse al directorio `ETAPA 2/backend` y ejecutar el comando ```pip install -r requirements.txt```
3. En el mismo directorio, abrir el interprete de python usando el comando `python` o `py` y ejecutar el siguiente script

```
  import nltk
  nltk.download('stopwords')
  nltk.download('punkt')
  nltk.download('wordnet')
  ```
4. Posteriormente, ejecutar el comando `uvicorn main:app --reload`. Si todo salio bien debería obtener una vista similar a la siguiente.

   ![image](https://github.com/user-attachments/assets/1f177dae-6081-4d46-ac02-31d25c13f596)

5. Dirigirse al directorio `ETAPA 2/frontend` y ejecutar los comandos `npm config set legacy-peer-deps true` y `npm install`.
6. Posteriormente, ejecutar el comando `npm start`. Si todo salio bien debería obtener una vista similar a la siguiente en la consolo y se debería abrir la aplicación en su navegador predeterminado.

   ![image](https://github.com/user-attachments/assets/f81e3b9d-1c19-42dc-8bfd-1683f7390ab5)

### **Aviso importante**

En caso de que haya reentrenado el modelo por medio de la aplicación Web y desee volver a la versión inicial del mismo, dirigase al directorio `ETAPA 2/backend` y ejecute el archivo llamado `Pipeline.py`. Esta acción restaurara el modelo a su versión inicial.
