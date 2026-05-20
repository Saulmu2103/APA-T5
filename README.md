# Sonido estéreo y ficheros WAVE

## Nom i cognoms

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Saül Muñoz Rodríguez

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es manejar la lectura y escritura de ficheros binarios. Para ello, sólo se
> permite el uso de las funciones de la biblioteca `struct`. Aunque existen distintas bibliotecas que
> permiten manejar los ficheros WAVE de una manera más eficiente y sencilla, su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.

## Fecha de entrega: 24 de mayo a medianoche

## El formato WAVE

El formato WAVE es uno de los más extendidos para el almacenamiento y transmisión
de señales de audio. En el fondo, se trata de un tipo particular de fichero
[RIFF](https://en.wikipedia.org/wiki/Resource_Interchange_File_Format) (*Resource
Interchange File Format*), utilizado no sólo para señales de audio sino también para señales de
otros tipos, como las imágenes estáticas o en movimiento, o secuencias MIDI (aunque, en el caso
del MIDI, con pequeñas diferencias que los hacen incompatibles).

La base de los ficheros RIFF es el uso de *cachos* (*chunks*, en inglés). Cada cacho,
o subcacho, está encabezado por una cadena de cuatro caracteres ASCII, que indica el tipo del cacho,
seguido por un entero sin signo de cuatro bytes, que indica el tamaño en bytes de lo que queda de
cacho sin contar la cadena inicial y el propio tamaño. A continuación, y en función del tipo de
cacho, se colocan los datos que lo forman.

Todo fichero RIFF incluye un primer cacho que lo identifica como tal y que empieza por la cadena
`'RIFF'`. A continuación, después del tamaño del cacho y en otra cadena de cuatro caracteres,
se indica el tipo concreto de información que contiene el fichero. En el caso concreto de los
ficheros de audio WAVE, esta cadena es igual a `'WAVE'`, y el cacho debe contener dos
*subcachos*: el primero, de nombre `'fmt '`, proporciona la información de cómo está
codificada la señal. Por ejemplo, si es PCM lineal, ADPCM, etc., o si es monofónica o estéreo. El
segundo subcacho, de nombre `'data'`, incluye las muestras de la señal.

Dispone de una descripción detallada del formato WAVE en la página
[WAVE PCM soundfile format](http://soundfile.sapp.org/doc/WaveFormat/) de Soundfile.

## Audio estéreo

La mayor parte de los animales, incluidos los del género *homo sapiens sapiens* sanos y completos,
están dotados de dos órganos que actúan como transductores acústico-sensoriales (es decir, tienen dos
*oídos*). Esta duplicidad orgánica permite al bicho, entre otras cosas, determinar la dirección de
origen del sonido. En el caso de la señal de música, además, la duplicidad proporciona una sensación
de *amplitud espacial*, de realismo y de confort acústico.

En un principio, los equipos de reproducción de audio no tenían en cuenta estos efectos y sólo permitían
almacenar y reproducir una única señal para los dos oídos. Es el llamado *sonido monofónico* o
*monoaural*. Una alternativa al sonido monofónico es el *estereofónico* o, simplemente, *estéreo*. En
él, se usan dos señales independientes, destinadas a ser reproducidas a ambos lados del oyente: los
llamados *canal izquierdo* (**L**) y *derecho* (**R**).

Aunque los primeros experimentos con sonido estereofónico datan de finales del siglo XIX, los primeros
equipos y grabaciones de este tipo no se popularizaron hasta los años 1950 y 1960. En aquel tiempo, la
gestión de los dos canales era muy rudimentaria. Por ejemplo, los instrumentos se repartían entre los
dos canales, con unos sonando exclusivamente a la izquierda y el resto a la derecha. Es el caso de las
primeras grabaciones en estéreo de los Beatles: las versiones en alemán de los singles *She loves you*
y *I want to hold your hand*. Así, en esta última (de la que dispone de un fichero en Atenea con sus
primeros treinta segundos, [Komm, gib mir deine Hand](wav/komm.wav)), la mayor parte de los instrumentos
suenan por el canal derecho, mientras que las voces y las características palmas lo hacen por el izquierdo.

Un problema habitual en los primeros años del sonido estereofónico, y aún vigente hoy en día, es que no
todos los equipos son capaces de reproducir los dos canales por separado. La solución comúnmente
adoptada consiste en no almacenar cada canal por separado, sino en la forma semisuma, $(L+R)/2$, y
semidiferencia, $(L-R)/2$, y de tal modo que los equipos monofónicos sólo accedan a la primera de ellas.
De este modo, estos equipos pueden reproducir una señal completa, formada por la suma de los dos
canales, y los estereofónicos pueden reconstruir los dos canales estéreo.

Por ejemplo, en la radio FM estéreo, la señal, de ancho de banda 15 kHz, se transmite del modo siguiente:

- En banda base, $0\le f\le 15$ kHz, se transmite la suma de los dos canales, $L+R$. Esta es la señal
  que son capaces de reproducir los equipos monofónicos.

- La señal diferencia, $L-R$, se transmite modulada en amplitud con una frecuencia de portadora
  $f_m = 38$ kHz.

  - Por tanto, ocupa la banda $23 \mathrm{kHz}\le f\le 53 \mathrm{kHz}$, que sólo es accedida por los
    equipos estéreo, y, en el caso de colarse en un reproductor monofónico, ocupa la banda no audible.

- También se emite una sinusoide de $19 \mathrm{kHz}$, denominada *señal piloto*, que se usa para
  demodular síncronamente la señal diferencia.

- Finalmente, la señal de audio estéreo puede acompañarse de otras señales de señalización y servicio en
  frecuencias entre $55.35 \mathrm{kHz}$ y $94 \mathrm{kHz}$.

En los discos fonográficos, la semisuma de las señales está grabada del mismo modo que se haría en una
grabación monofónica, es decir, en la profundidad del surco; mientras que la semidiferencia se graba en el
desplazamiento a izquierda y derecha de la aguja. El resultado es que un reproductor mono, que sólo atiende
a la profundidad del surco, reproduce casi correctamente la señal monofónica, mientras que un reproductor
estéreo es capaz de separar los dos canales. Es posible que algo de la información de la semisuma se cuele
en el reproductor mono, pero, como su amplitud es muy pequeña, se manifestará como un ruido muy débil,
apenas perceptible.

En general, todos estos sistemas se basan en garantizar que el reproductor mono recibe correctamente la
semisuma de canales y que, si algo de la semidiferencia se cuela en la reproducción, sea en forma de un
ruido inaudible.

## Tareas a realizar

Escriba el fichero `estereo.py` que incluirá las funciones que permitirán el manejo de los canales de una
señal estéreo y su codificación/decodificación para compatibilizar ésta con sistemas monofónicos.


### Manejo de los canales de una señal estéreo

En un fichero WAVE estéreo con señales de 16 bits, cada muestra de cada canal se codifica con un entero de
dos bytes. La señal se almacena en el *cacho* `'data'` alternando, para cada muestra de $x[n]$, el valor
del canal izquierdo y el derecho:

<img src="img/est%C3%A9reo.png" width="380px">

#### Función `estereo2mono(ficEste, ficMono, canal=2)`

La función lee el fichero `ficEste`, que debe contener una señal estéreo, y escribe el fichero `ficMono`,
con una señal monofónica. El tipo concreto de señal que se almacenará en `ficMono` depende del argumento
`canal`:

- `canal=0`: Se almacena el canal izquierdo $L$.
- `canal=1`: Se almacena el canal derecho $R$.
- `canal=2`: Se almacena la semisuma $(L+R)/2$. Ha de ser la opción por defecto.
- `canal=3`: Se almacena la semidiferencia $(L-R)/2$.

#### Función `mono2estereo(ficIzq, ficDer, ficEste)`

Lee los ficheros `ficIzq` y `ficDer`, que contienen las señales monofónicas correspondientes a los canales
izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero
`ficEste`.

### Codificación estéreo usando los bits menos significativos

En la línea de los sistemas usados para codificar la información estéreo en señales de radio FM o en los
surcos de los discos fonográficos, podemos usar enteros de 32 bits para almacenar los dos canales de 16 bits:

- En los 16 bits más significativos se almacena la semisuma de los dos canales.

- En los 16 bits menos significativos se almacena la semidiferencia.

Los sistemas monofónicos sólo son capaces de manejar la señal de 32 bits. Esta señal es prácticamente
idéntica a la señal semisuma, ya que la semisuma ocupa los 16 bits más significativos. La señal
semidiferencia aparece como un ruido añadido a la señal, pero, como su amplitud es $2^{16}$ veces más
pequeña, será prácticamente inaudible (la relación señal a ruido es del orden de 90 dB).

Los sistemas estéreo son capaces de aislar las dos partes de la señal y, con ellas, reconstruir los dos
canales izquierdo y derecho.

<img src="img/est%C3%A9reo_cod.png" width="510px">

#### Función `codEstereo(ficEste, ficCod)`

Lee el fichero `ficEste`, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y
construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
monofónicos como por sistemas estéreo preparados para ello.

#### Función `decEstereo(ficCod, ficEste)`

Lee el fichero `ficCod` con una señal monofónica de 32 bits en la que los 16 bits más significativos
contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
semidiferencia, y escribe el fichero `ficEste` con los dos canales por separado en el formato de los
ficheros WAVE estéreo.

### Entrega

#### Fichero `estereo.py`

- El fichero debe incluir una cadena de documentación que incluirá el nombre del alumno y una descripción
  del contenido del fichero.

- Es muy recomendable escribir, además, sendas funciones que *empaqueten* y *desempaqueten* las cabeceras
  de los ficheros WAVE a partir de los datos contenidos en ellas.

- Aparte de `struct`, no se puede importar o usar ningún módulo externo.

- Se deben evitar los bucles. Se valorará el uso, cuando sea necesario, de *comprensiones*.

- Los ficheros se deben abrir y cerrar usando gestores de contexto.

- Las funciones deberán comprobar que los ficheros de entrada tienen el formato correcto y, en caso
  contrario, elevar la excepción correspondiente.

- Los ficheros resultantes deben ser reproducibles correctamente usando cualquier reproductor estándar;
  por ejemplo, el Windows Media Player o similar. Es probable, muy probable, que tenga que modificar los
  datos de las cabeceras de los ficheros para conseguirlo.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el uso de los estándares
  marcados por PEP-ocho.

#### Comprobación del funcionamiento

Es responsabilidad del alumno comprobar que las distintas funciones realizan su cometido de manera correcta.
Para ello, se recomienda usar la canción [Komm, gib mir deine Hand](wav/komm.wav), suminstrada al efecto.
De todos modos, recuerde que, aunque sea en alemán, se trata de los Beatles, así que procure no destrozar
innecesariamente la canción.

#### Código desarrollado

Inserte a continuación el código de los métodos desarrollados en esta tarea, usando los comandos necesarios
para que se realice el realce sintáctico en Python del mismo (no vale insertar una imagen o una captura de
pantalla, debe hacerse en formato *markdown*).

##### Código de `estereo2mono()`

```python
def estereo2mono(ficEste, ficMono, canal=2):
    """
    Entradas: 
        - ficEste: fichero en formato estereo
        - canal: tipo concreto de la señal que se almacenara (0, 1, 2, 3) por defecto 2
    
    Salidas:
        - ficMono: fichero mono 
    """
    if canal not in (0, 1, 2, 3):
        raise ValueError("Canal debe ser 0, 1, 2 o 3")

    with open(ficEste, "rb") as f:

        # --- Leer encabezado RIFF estándar (12 bytes) ---
        
        header = f.read(12)
        riffId, riffSize, waveId = struct.unpack("<4sI4s", header)
        if riffId != b"RIFF" or waveId != b"WAVE":
            raise ValueError("No es un WAV válido")

        # --- Leer chunk fmt (24 bytes típicos) ---
        
        fmtHeader = f.read(8)
        fmtId, fmtSize = struct.unpack("<4sI", fmtHeader)
        if fmtId != b"fmt ":
            raise ValueError("No se encontró chunk fmt estándar")

        fmtData = f.read(fmtSize)
        audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample = \
            struct.unpack("<HHIIHH", fmtData[:16])

        if audioFormat != 1:
            raise ValueError("Solo PCM sin comprimir")
        if numChannels != 2:
            raise ValueError("Se requiere WAV estéreo")
        if bitsPerSample != 16:
            raise ValueError("Solo soporta 16 bits")

        dataHeader = f.read(8)
        dataId, dataSize = struct.unpack("<4sI", dataHeader)
        if dataId != b"data":
            raise ValueError("No se encontró chunk data estándar")
            
        raw = f.read(dataSize)
        
    bytesPerFrame = blockAlign
    nframes = len(raw) // bytesPerFrame
    fmt = '<' + 'h' * (nframes * 2)
    muestras = struct.unpack(fmt, raw[:nframes * bytesPerFrame])

    salida = bytearray()
        
    for i in range(0, len(muestras), 2):
        L = muestras[i]
        R = muestras[i+1]

        if canal == 0:
            mono = L
        elif canal == 1:
            mono = R
        elif canal == 2:
            mono = (L + R) // 2
        else:
            mono = (L - R) //2 
      
        if mono < -32768:
            mono = -32768
        elif mono > 32767:
            mono = 32767

        salida.extend(struct.pack('h', mono))

    canalesSalida = 1
    bitsSalida = 16
    outBlockAlignSalida = 2
    byteRateSalida = sampleRate * outBlockAlignSalida
    outDataSize = len(salida)
    riffSize = 4 + (8 + 16) + (8 + outDataSize)

    with open(ficMono, 'wb') as out:
        out.write(struct.pack("<4sI4s", b"RIFF", riffSize, b'WAVE'))
        out.write(struct.pack("<4sI", b"fmt ", 16))
        out.write(struct.pack("<HHIIHH",
                              1, 
                              canalesSalida,
                              sampleRate,
                              byteRateSalida,
                              outBlockAlignSalida,
                              bitsSalida))
        out.write(struct.pack('<4sI', b'data', outDataSize))
        out.write(salida)

    if canal == 0:
        print("Se ha convertido a mono usando el canal L")
    elif canal == 1:
        print("Se ha convertido a mono usando el canal R")
    elif canal == 2:
        print("Se ha convertido a mono usando la semisuma (L+R)/2")
    else:
        print("Se ha convertido a mono usando la semidiferencia (L-R)/2")

```

##### Código de `mono2estereo()`

```python
def mono2stereo(ficIzq, ficDer, ficEste):
    """
    Une dos las entradas L y R de archivos mono en un archivo estereo

    Entradas: 
        - ficIzq: fichero mono del canal L
        - ficDer: fichero mono del canal R
    Salidas:
        - ficEste: fichero estereo de salida
    """
    
    # --- Leer WAV izquierdo ---
    
    with open(ficIzq, "rb") as f:
        h = f.read(44)
        (riffId, riffSize, waveId,
         fmtId, fmtSize,
         audioFormat, numChannels,
         sampleRate, byteRate,
         blockAlign, bitsPerSample,
         dataId, dataSize) = struct.unpack("<4sI4s4sIHHIIHH4sI", h)

        if audioFormat != 1 or numChannels != 1 or bitsPerSample != 16:
            raise ValueError("ficIzq debe ser WAV PCM 16-bit MONO")

        rawIzq = f.read(dataSize)
        muestrasIzq = struct.unpack("<" + "h"*(dataSize//2), rawIzq)

   # --- Leer WAV derecho ---
    
    with open(ficDer, "rb") as f:
        h = f.read(44)
        (riffId2, riffSize2, waveId2,
         fmtId2, fmtSize2,
         audioFormat2, numChannels2,
         sampleRate2, byteRate2,
         blockAlign2, bitsPerSample2,
         dataId2, dataSize2) = struct.unpack("<4sI4s4sIHHIIHH4sI", h)

        if audioFormat2 != 1 or numChannels2 != 1 or bitsPerSample2 != 16:
            raise ValueError("ficDer debe ser WAV PCM 16-bit MONO")

        if sampleRate2 != sampleRate:
            raise ValueError("Ambos WAV deben tener la misma frecuencia")

        rawDer = f.read(dataSize2)
        muestrasDer = struct.unpack("<" + "h"*(dataSize2//2), rawDer)

    # --- Comprobar número de muestras ---
    
    if len(muestrasIzq) != len(muestrasDer):
        raise ValueError("Los dos WAV deben tener el mismo número de muestras")

    nFrames = len(muestrasIzq)

    # --- Construir datos estéreo ---
    
    outData = bytearray()
    for i in range(nFrames):
        L = muestrasIzq[i]
        R = muestrasDer[i]
        outData.extend(struct.pack("<h", L))
        outData.extend(struct.pack("<h", R))

    # --- Construir WAV estéreo ---
    
    outChannels = 2
    outBits = 16
    outBlockAlign = outChannels * outBits // 8
    outByteRate = sampleRate * outBlockAlign
    outDataSize = len(outData)
    riffSize = 4 + (8 + 16) + (8 + outDataSize)

    with open(ficEste, "wb") as out:
        out.write(struct.pack("<4sI4s", b"RIFF", riffSize, b"WAVE"))
        out.write(struct.pack("<4sI", b"fmt ", 16))
        out.write(struct.pack("<HHIIHH",
                              1,               
                              outChannels,
                              sampleRate,
                              outByteRate,
                              outBlockAlign,
                              outBits))
        out.write(struct.pack("<4sI", b"data", outDataSize))
        out.write(outData)

    print("Se han convertido las señales L y R a estereo!")

```

##### Código de `codEstereo()`

```python
def codEstereo(ficEste, ficCod):
    """
    Recibe un fichero estereo 16 bits y lo convierte a uno de 32 bits guardando la semisuma en los 16 MSB y la semidiferencia en los 16 LSB

    Entrada:
        - ficEste: fichero de audio estereo
    Salida:
        - ficCod: fichero de audio MONO a 32 bits

    """
    # --- LECTURA DE DATOS Y CREACION DE LA NUEVA CABECERA ---
        
    with open(ficEste, 'rb') as f:
        cabecera = f.read(44)
        datos = f.read()

    (chunkID, chunkSize, format,
    sub1ID, sub1Size, audioFormat, numChannels,
    sampleRate, byteRate, blockAlign, bitsPerSample,
    sub2ID, sub2Size) = struct.unpack('4sI4s4sIHHIIHH4sI', cabecera)
    nCanalesSalida = 1
    bitsPorMuestraSalida = 32
    blockAlignSalida = nCanalesSalida * (bitsPorMuestraSalida // 8)
    byteRateSalida = sampleRate * blockAlignSalida
    nFrames = len(datos) // 4

    newSub2Size = nFrames * blockAlignSalida
    newChunkSize = 36 + newSub2Size
    nuevaCabecera = struct.pack(
        '<4sI4s4sIHHIIHH4sI', 
        chunkID,
        newChunkSize,
        format,
        sub1ID,
        sub1Size,
        audioFormat,
        nCanalesSalida,
        sampleRate,
        byteRateSalida,
        blockAlignSalida,
        bitsPorMuestraSalida,
        sub2ID,
        newSub2Size
    )

    # --- LECTURA DE DATOS DE AUDIO CALCULO DE LA SEMISUMA Y LA SEMIDIFERENCIA Y PROCESADO ---

    with open(ficCod, 'wb') as s:
        s.write(nuevaCabecera)
        for i in range(nFrames):
            off = i * 4
            L = struct.unpack_from('<h', datos, off)[0]
            R = struct.unpack_from('<h', datos, off + 2)[0]
            semisuma = (L + R)  // 2
            semidiferencia = (L - R) // 2

            if semisuma > 32767: semisuma = 32767
            if semisuma < -32768: semisuma = -32768
            if semidiferencia > 32767: semidiferencia = 32767
            if semidiferencia < -32768: semidiferencia = -32768
            msbU = semisuma & 0xFFFF
            lsbU = semidiferencia & 0xFFFF
            u32 = (msbU << 16) | lsbU
            signed32 = u32 - (1 << 32) if u32 >= (1 << 31) else u32
            s.write(struct.pack('<i', signed32))

    print("Se ha convertido a 32 bits MONO siendo los 16 MSB la semisuma y los 16 LSB la semidiferencia")
```

##### Código de `decEstereo()`

```python

```

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
