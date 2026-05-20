''' 
estereo.py

Saül Muñoz Rodríguez

Incluye: 
    - estereo2mono(): convierte la señal de estereo a mono almacenando canal izquierdo, derecho, la semisuma o la semidiferencia
    - mono2estereo(): convierte la señal de mono a estereo se le debe pasar el canal L y el R
    - codEstereo(): lee el fichero ficEste que contiene una señal codificada en PCM lineal de 16 bits y construye una señal codificada a 32 bits 
    - decEstereo(): lee el fichero ficCod como una señal monofonica de 32 bits en la que los 16 MSB contienen la semisuma de los canales estereo y los 16 LSB la semidiferencia de los canales estereo y escribe el fichero ficEste (estereo)
'''

import struct

# 1 ESTEREO2MONO

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
        
# ---LECTURA DE ENCABEZADO RIFF Y CHUNK FMT ---
    
    with open(ficEste, "rb") as f:
        header = f.read(12)
        riffId, riffSize, waveId = struct.unpack("<4sI4s", header)
        fmtHeader = f.read(8)
        fmtId, fmtSize = struct.unpack("<4sI", fmtHeader)
        fmtData = f.read(fmtSize)
        audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample = \
            struct.unpack("<HHIIHH", fmtData[:16])
        dataHeader = f.read(8)
        dataId, dataSize = struct.unpack("<4sI", dataHeader)
        raw = f.read(dataSize)
    bytesPerFrame = blockAlign
    nframes = len(raw) // bytesPerFrame
    fmt = '<' + 'h' * (nframes * 2)
    muestras = struct.unpack(fmt, raw[:nframes * bytesPerFrame])

    salida = bytearray()

# --- CONSTRUCCION DE LOS ARCHIVOS DE SALIDA MONO SEGUN LA OPCION 'CANAL' ---
    
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
            mono = (L - R) // 2

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

# 2 MONO2ESTEREO

def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Une dos las entradas L y R de archivos mono en un archivo estereo

    Entradas: 
        - ficIzq: fichero mono del canal L
        - ficDer: fichero mono del canal R
    Salidas:
        - ficEste: fichero estereo de salida
    """
    
    # --- LECTURA DE FICHERO DE DATOS L ---
    
    with open(ficIzq, "rb") as f:
        h = f.read(44)
        (riffId, riffSize, waveId,
         fmtId, fmtSize,
         audioFormat, numChannels,
         sampleRate, byteRate,
         blockAlign, bitsPerSample,
         dataId, dataSize) = struct.unpack("<4sI4s4sIHHIIHH4sI", h)

        rawIzq = f.read(dataSize)
        muestrasIzq = struct.unpack("<" + "h"*(dataSize//2), rawIzq)

   # --- LECTURA DE FICHERO DE DATOS R ---
    
    with open(ficDer, "rb") as f:
        h = f.read(44)
        (riffId2, riffSize2, waveId2,
         fmtId2, fmtSize2,
         audioFormat2, numChannels2,
         sampleRate2, byteRate2,
         blockAlign2, bitsPerSample2,
         dataId2, dataSize2) = struct.unpack("<4sI4s4sIHHIIHH4sI", h)
        
        rawDer = f.read(dataSize2)
        muestrasDer = struct.unpack("<" + "h"*(dataSize2//2), rawDer)

    nFrames = len(muestrasIzq)

    # --- CONSTRUIR WAV Y DATOS ESTEREO ---
    
    outData = bytearray()
    for i in range(nFrames):
        L = muestrasIzq[i]
        R = muestrasDer[i]
        outData.extend(struct.pack("<h", L))
        outData.extend(struct.pack("<h", R))
    
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

    print("Se han convertido las señales a estereo!")

# 3 CODESTEREO

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
    
# 4 DECESTEREO

def decEstereo(ficCod, ficEste):
    """
    La funcion recibe un archivo de 32 bits MONO y lo convierte a un archivo 16 bits ESTEREO

    Entradas:
        - ficCod: este archivo contiene una señal codificada en 32 bits MONO donde los 16 MSB representan la semisuma de la señal original estereo y los 16 LSB representan la semidiferencia
    Salidas:
        - ficEste: fichero de salida estereo a 16 bits
    """
    with open(ficCod, 'rb') as f:
        cabecera = f.read(44)
        (riffId, riffSize, waveId,
         fmtId, fmtSize,
         audioFormat, numChannels,
         sampleRate, byteRate,
         blockAlign, bitsPerSample,
         dataId, dataSize) = struct.unpack("<4sI4s4sIHHIIHH4sI", cabecera)

        datos = f.read(dataSize)

    datosSalida = bytearray()
    for i in range(0, len(datos), 4):
        v32 = struct.unpack_from('<i', datos, i)[0]

        s = (v32 >> 16) & 0xFFFF
        d = v32 & 0xFFFF
        if s & 0x8000:
            s -= 0x10000
        if d & 0x8000:
            d -= 0x10000

        L = s + d
        R = s - d

        if L > 32767:
            L = 32767
        elif L < -32768:
            L = -32768
        if R > 32767:
            R = 32767
        elif R < -32768:
            R = -32768

        datosSalida.extend(struct.pack('<h', int(L)))
        datosSalida.extend(struct.pack('<h', int(R)))

    outChannels = 2
    outBits = 16
    outBlockAlign = outChannels * outBits // 8
    outByteRate = sampleRate * outBlockAlign
    outDataSize = len(datosSalida)
    outRiffSize = 4 + (8 + 16) + (8 + outDataSize)

    with open(ficEste, "wb") as salida:
        salida.write(struct.pack("<4sI4s", b"RIFF", outRiffSize, b"WAVE"))
        salida.write(struct.pack("<4sI", b"fmt ", 16))
        salida.write(struct.pack("<HHIIHH",
                              1,                
                              outChannels,
                              sampleRate,
                              outByteRate,
                              outBlockAlign,
                              outBits))
        salida.write(struct.pack("<4sI", b"data", outDataSize))
        salida.write(datosSalida)

    print("Se ha convertido la señal a 16 bits ESTEREO")
