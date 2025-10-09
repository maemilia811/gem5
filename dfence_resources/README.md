## dfence_resources
#### Descripción
Este repositorio contiene los recursos necesarios para correr dfence en gem5. Incluye una imagen de
disco con un script para correr una batería de test.
Una vez que termina de bootear el sistema, correrá el script dfence.sh que se encuentra en /home/gem5/dfence.sh

Para definir el disco como recurso, se creó el archivo ...json que se encuentra en la raíz del repositorio.
Modo de uso para configuración de la simulación en gem5:

kernel = obtain_resource(
    "x86-linux-kernel-6.8.0-52-generic",
    resource_version="1.0.0",
    clients=["gem5-resources"],
)
disk = obtain_resource(
    "test-disk-dfence",
    resource_version="4.0.0",
    clients=["GEM5_RESOURCE_JSON_APPEND"],
)

board.set_kernel_disk_workload(kernel=kernel,
                               disk_image=disk,
                               readfile_contents="echo afterrrrrr")

#### Running simulations
Para correr la simulación usando este recurso, se debe setear la variable de entorno GEM5_RESOURCE_JSON_APPEND
con la ruta del archivo .json que define el recurso del disco. Luego, correr gem5 con la configuración dfence/config.py
Ejemplo:

"""
GEM5_RESOURCE_JSON_APPEND=./dfence_resources/test_resource.json build/X86/gem5.opt configs/dfence/config.py --resource x86-ubuntu-24.04-dfence
"""
Donde --resource es el nombre del recurso que se quiere usar (el nombre que se le dio en el archivo .json)


#### Crear una nueva imagen del disco
Para extender una imagen de disco y poder correr los binarios para probar dfence, realizar los siguientes pasos:

- Clonar repositorio gem5-resources
- Descargar qemu x86_64 system
- Navegar hasta directorio ubuntu-generics
- Crear archivo dfence.sh en files/x86/ con los comandos para instalar lo necesario y correr los tests.
- Descargar imagen de disco de ubuntu 24.04 (o la que se quiera usar) y hacerle gzip. (agregar link)
- Modificar x86.pkr:
    - Agregar la línea:
    disk_image = true #esto le dice a ubuntu install que en vez de usar .iso para instalar ubuntu lo haga de una imagen de disco  y no va a tratar de instalarlo por su cuenta.

    - Agregar archivo dfence.sh para que se cargue en la imagen del disco:
      provisioner "file" {
        destination = "/home/gem5/"
        source      = "files/x86/dfence.sh"
    }
    - Obtener sha del disco y pegarlo en x86.pkr clave sha256sum:
        sha256sum ubuntu-24.04-server-cloudimg-amd64.img.gz


- Build de la imagen del disco(ubuntu 24.04):
    ./build-x86.sh 24.04
