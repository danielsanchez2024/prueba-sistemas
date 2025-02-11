# Prueba de Sistemas - Conocimientos mínimos

Para la realización de esta prueba no se puede usar ayuda de ningún tipo de IA y se debe entregar imagenes del funcionamiento de las aplicaciones en cada uno de los orquestadores solicitados.

Las imagenes se deben guardar dentro de la carpeta "evidencias" que hay dentro de la carpeta de los distintos orquestadores.
Los puntos que contengan un **(*)** deben contener una imagen de evidencia donde su nombre va a ser igual al punto desarrollado.

Todos los archivos deben ser subidos en un repositorio de github público, el cuál será enviado como respuesta a este correo.

**¡Suerte!**

# Creación de microservicios

## Python

En la carpeta [backoffice](./services/backoffice/) vamos a crear un nuevo microservicio de python con flask el cuál debe cumplir con los siguientes requerimientos:

- Cumplir una buena estructuración de directorios
- Traer los datos de conexiones a bases de datos desde un archivo de configuración, mismo que a su vez los trae de variables de entorno
- El microservicio va a estar conectado a 3 bases de datos diferentes de las cuales va a ingresar y sacar información, los endpoints son los siguientes:

### MongoDB
- **GET /mongo/user**: Trae todos los usuarios de la base de datos de mongo
- **POST /mongo/user**: Inserta un nuevo usuario en la base de datos de mongo (con los campos username, email y password)

### Redis
- **GET /redis/user**: Trae todos los usuarios de la base de datos de redis
- **POST /redis/user**: Inserta un nuevo usuario en la base de datos de redis (con los campos username, email y password)

### Elasticsearch
- **GET /elasticsearch/user**: Trae todos los usuarios de la base de datos de elasticsearch
- **POST /elasticsearch/user**: Inserta un nuevo usuario en la base de datos de elasticsearch en el índice "user" (con los campos username, email y password)

## Angular

Crear un proyecto de angular sencillo que me permita ingresar los datos de un usuario y guardarlo en mi backoffice seleccionando la base de datos que quiero, tambien me debe permitir listar los datos de los usuarios que tengo en una base de datos específica.

# Docker

## Microservicio de python

Crear un dockerfile óptimo para el microservicio de python creado el cuál contenga un label con la descripción del microservicio y otro con el nombre de la empresa.

Además de esto, el Dockerfile debe recibir como parámetro de construcción la fecha y hora de la máquina en la que se está construyendo y se debe agregar en el label **buildTime**

## Frontend

Se debe crear un Dockerfile multistage para el proyecto de angular creado, el cual debe tener un label con la descripción del proyecto y otro con el nombre de la empresa.

Este debe tener las etapas de instalación de las dependencias, generación de archivos estáticos y el servidor web que nos permita acceder a esos archivos estáticos.

# Subida de imagenes en docker hub **(*)**

Construir las imagenes de los microservicios y subirlas a un registry de docker hub con los siguientes nombres **(*)**: 
- gopenux-backoffice (debe ser un repo privado)
- gopenux-frontend

Ambas con el tag latest

# Docker compose **(*)**

Generar un docker compose en el directorio [docker-compose](./docker-compose/) que despliegue los servicios de las bases de datos (redis, mongodb y elasticsearch) y los servicios de los microservicios (backoffice y frontend).

Este docker compose debe hacer uso de volumenes persistentes en la máquina del desarrollador para las bases de datos y se deben usar secretos en las variables de entorno para la conexión y configuración de las bases de datos.

Se deben usar redes para comunicar los servicios donde:
- las bases de datos se pueden comunicar entre ellas y al backoffice.
- El backoffice se puede comunicar con las bases de datos y el frontal.
- El front solo se comunica con el backoffice.

(verificar funcionamiento y subir evidencias)

# Docker Swarm **(*)**

Generar un docker stack en el directorio [docker-swarm](./docker-swarm/) que despliegue los servicios de las bases de datos (redis, mongodb y elasticsearch) y los servicios de los microservicios (backoffice y frontend).

El clúster swarm debe contar con 3 nodos donde 1 toma el rol de manager y 2 workers.
- Uno de los nodos workers debe ir etiquetado con "databases" y el otro con "microservices"
- En el nodo worker "databases" se deben desplegar las bases de datos
- En el nodo worker "microservices" se deben desplegar el backoffice y el frontal
- El nodo manager solo debe desplegar el nginx con el cuál se va a acceder al backoffice y el frontal (por http y https)

Las redes quedan igual que las de docker compose, exceptuando que el ingress de nginx solo puede comunicarse con el backoffice y el frontal.
Los volumenes de las bases de datos deben ser en la máquina, no gestionados por docker.
Tambien debe hacer uso de secretos.

(verificar funcionamiento y subir evidencias)

# Jenkins **(*)**

- Crear un docker compose en el directorio [jenkins](./jenkins/) el cual haga el despliegue de un servicio de jenkins capaz de usar docker dentro del contenedor

- Crear un Jenkinsfile para el backoffice y el frontend que haga el build de la imagen partiendo del dockerfile (y pasando los argumentos necesarios), despues de la creación que haga la subida de la imagen al registry de docker hub con el tag latest y un tag con un número random de 10 dígitos. Despues de subir la imagen, se debe hacer la actualización de esta en los servicios de docker swarm sin alterar el archivo de despliegue.

- Crear una tarea de Jenkins para cada servicio que parta del Jenkinsfile que se encuentra en el repositorio y ejecutarlo (funcional)

(verificar funcionamiento y subir evidencias)

# Kubernetes **(*)**

Crear los manifiestos necesarios en el folder [kubernetes](./kubernetes/) para el despliegue de la aplicación y sus dependencias (ordenando de la mejor manera los folders), donde:

- Cada microservicio o base de datos debe ir en un namespace diferente
- Las bases de datos se deben configurar con el kind correspondiente a un servicio que necesita mantener su identidad
- Las variables de entorno se agregan desde secretos cuando son datos sensibles (contraseñas, usuarios, etc)
- Las bases de datos deben tener volumenes peristente de tipo PVC configurados
- El servicio de backoffice debe tener un volumen de tipo empty dir en el directorio /tpm
- El servicio de backoffice y frontend deben tener un ingress para poder acceder a ellos con los DNS (backoffice.gopenux.lan y frontend.gopenux.lan)
- El servicio de la base de datos de mongo debe ser de tipo NodePort
- El servicio de frontend debe subir su configuración de nginx propia como un configmap
- Cada recursos desplegado debe tener sus límites de recursos

(verificar funcionamiento y subir evidencias)

# Kustomize y helm

Migrar el proyecto de kubernetes para el uso de kustomize en el folder [kustomize](./kustomize/) teniendo en cuenta su estructura de folders que lleva.

Se deben gestionar 2 entornos (pre y pro) en los cuales van a cambiar los límites de recursos (ya que dependen de la carga del entorno), los dominios, las claves de las bases de datos y las conexiones, etc.

las bases de datos deben ser desplegadas con charts de helm puestos en los archivos de kustomize para modificar el values.yaml

los dominios van a ser los siguientes:

**PRE**
frontend-pre.gopenux.lan
backoffice-pre.gopenux.lan

**PRO**
frontend.gopenux.lan
backoffice.gopenux.lan

Ambos entornos van a usar el mismo certificado de SSL el cuál tendrá que ser valido para *.gopenux.lan
(se deben usar las etiquetas kustomize para cargar, editar, parchar e interactuar con los recursos de las bases)

(verificar funcionamiento y subir evidencias)

# ArgoCD y monitorización

Mediante kustomize se necesita desplegar ArgoCD y tener acceso al panel de administración

- Se deben crear manifiestos para prometheus, grafana, loki, promtail y node-exporter (con el uso de helm)
- De deben subir los manifiestos compilados a un repositorio público
- Se deben desplegar las aplicaciones mediante argoCD apuntando al repositorio en una aplicación llamada "monitoring" y un namespace "monitoring"

- Acceder al grafana y crear cuadros de mando que me permita ver el uso de cpu y memoria de los nodos

# RBAC

Crear los manifiestos para darle permisos a un usuario llamado "developer" que interactue con el clúster en el namespace "backoffice"y "frontend" con todos los verbos y que en el namespace "default" solo tenga permisos para listar

# Scripting e interacción con bds

Generar un script con bash capaz de generar un backup de una base de datos de mongodb, comprimirlo y guardarlo en una ruta específica, este debe recibir la configuración de conexión mediante variables de entorno.