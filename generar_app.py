import pandas as pd
from jinja2 import Template
import os
import json

# Variable blindada para Google Analytics
codigo_analytics = """
<script async src="https://www.googletagmanager.com/gtag/js?id=G-334S1RVPFX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-334S1RVPFX');
</script>
"""

# --- 1. CONFIGURACIÓN ---
archivo_csv = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQSkICayf946zUmX2EpcUFtS9MnYgfMAZmNBLwSRMIy6u2X22k3mV8qGLMkjEwJcN0vI4JpbxsZIxf5/pub?gid=0&single=true&output=csv' 
ruta_portadas = 'portadas'
ruta_audios = 'audios'
archivo_logo = 'logo.png'

def buscar_archivo_inclusivo(nombre_celda, carpeta):
    if pd.isna(nombre_celda) or str(nombre_celda).strip() == "":
        return ""
    nombre_base = str(nombre_celda).strip().split('.')[0].lower()
    try:
        archivos = os.listdir(carpeta)
        for f in archivos:
            if f.lower().startswith(nombre_base):
                return os.path.join(carpeta, f)
    except: pass
    return ""

# --- 2. PROCESAMIENTO ---
try:
    df = pd.read_csv(archivo_csv, sep=None, engine='python', on_bad_lines='skip')
    df.columns = [str(c).strip() for c in df.columns]

    c_id = 'ID_Dia' if 'ID_Dia' in df.columns else df.columns[0]
    df[c_id] = pd.to_numeric(df[c_id], errors='coerce').fillna(0).astype(int)
    df = df.sort_values(by=c_id, ascending=False)

    df['ruta_img'] = df['Image_Cover'].apply(lambda x: buscar_archivo_inclusivo(x, ruta_portadas))
    df['ruta_audio'] = df['Archivo_Audio'].apply(lambda x: buscar_archivo_inclusivo(x, ruta_audios))

    datos_json = df.to_dict(orient='records')

    # --- 3. HTML / CSS / JS ---
    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
       
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Playfair+Display:ital,wght@0,700;0,900;1,700&display=swap" rel="stylesheet">
        
        <script src="https://cdn.tailwindcss.com"></script>
        
        <title>365 Notas - @SoyInciarte</title>
        
        <style>
            :root {
                --fuente-titulo: 'Playfair Display', serif;
                --fuente-cuerpo: 'Inter', sans-serif;
                /* PALETA EXACTA VOCABULARY */
                --bg-crema: #f2f0e4;
                --texto-oscuro: #1a1a1a;
                --correct-green: #a7c957;
                --incorrect-red: #d98e84;
            }
            
            body { 
                background-color: var(--bg-crema); 
                color: var(--texto-oscuro); 
                font-family: var(--fuente-cuerpo);
                margin: 0;
            }
            
            .font-serif { font-family: var(--fuente-titulo); }
            .modal-active { overflow: hidden; }
            
            #detalleModal { 
    background-color: var(--bg-crema); 
    scroll-behavior: smooth; /* Esto hace que el "Volver arriba" sea elegante */
}
            
            #detalleModal h3, #detalleModal h4, #detalleModal p, #detalleModal button {
                color: var(--texto-oscuro);
            }

            .tarjeta-musica {
    transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    background-color: transparent; 
    border: none;
}
            
            .tarjeta-musica:hover {
                transform: translateY(-8px);
                border-color: #c0bca0;
                box-shadow: 0 10px 30px rgba(0,0,0,0.04);
            }

            .linea-separadora { 
                border-top: 1px solid rgba(0,0,0,0.08); 
                margin: 2.5rem auto; 
                max-width: 80%;
            }

            /* Botones de Trivia Minimalistas (Estilo foto 17) */
            .btn-trivia {
                background-color: #ffffff;
                border: 2px solid var(--texto-oscuro) !important;
                border-radius: 20px !important;
                color: var(--texto-oscuro) !important;
                box-shadow: 0 5px 0 var(--texto-oscuro);
                transition: all 0.1s ease;
                text-align: left;
                padding: 1.25rem 2rem;
                font-weight: 600;
                width: 100%;
            }

            .btn-trivia:active {
                transform: translateY(3px);
                box-shadow: 0 2px 0 var(--texto-oscuro);
            }

            /* Colores de validación según tus fotos */
            .btn-correct {
                background-color: var(--correct-green) !important;
                box-shadow: 0 5px 0 #8aa846 !important;
            }

            .btn-incorrect {
                background-color: var(--incorrect-red) !important;
                box-shadow: 0 5px 0 #b57168 !important;
            }

            audio::-webkit-media-controls-panel { background-color: #e5e3d7; }
        </style>
    </head>
    <body class="antialiased">
        <div id="splash-screen" class="fixed inset-0 z-[100] bg-[#f2f0e4] flex items-center justify-center transition-opacity duration-1000">
    <div class="text-center">
        <img src="NuevoLogo.png" class="w-32 h-32 object-contain animate-pulse">
        <audio id="audioSplash" src="SplashScreen.mp3" preload="auto"></audio>

        <audio id="audioAcierto" src="acierto.mp3" preload="auto"></audio>
        <audio id="audioError" src="error.mp3" preload="auto"></audio>
        
    </div>
</div>
    <header class="py-6 px-6 max-w-md mx-auto">
            <div class="flex flex-col items-center justify-center text-center -space-y-1">
                <img src="NuevoLogo.png" class="h-16.1 w-16.1 object-contain opacity-95" onerror="this.style.display='none'">
                
                <div class="text-center">
                    <h1 class="text-5xl font-serif font-black italic tracking-tight text-zinc-900 leading-none ">365 Notas</h1>
                    <p class="text-[17px] font-light text-zinc-600 tracking-tighter mt-2">Derechos Reservados - @SoyInciarte</p>
                </div>
            </div>

            <div class="px-6 max-w-md mx-auto mt-9 mb-4">
                <div id="contenedorPublicidad" class="w-full overflow-hidden rounded-xl bg-zinc-50 flex items-center justify-center">
                    <img src="Banner_Lexicon.jpg" alt="Publicidad Lexicón C.A." class="w-full h-auto object-cover block">
                </div>
            </div>

            <div class="border-t border-zinc-300 my-8 opacity-50"></div>

    <div>
        <input type="text" id="inputBusqueda" onkeyup="filtrarTarjetas()" 
               placeholder="Buscar artista, género, número..." 
               class="w-full bg-white border border-zinc-300 rounded-full py-3 px-6 text-sm focus:outline-none focus:border-zinc-500 transition-all text-center text-zinc-900">
    </div>

            <div class="border-t border-zinc-300 my-8 opacity-50"></div>

</header>



        <main id="gridTarjetas" class="max-w-md mx-auto px-4 grid grid-cols-2 gap-x-4 gap-y-8 pb-32">
            {% for row in lista_datos %}
            <div class="tarjeta-musica cursor-pointer group" onclick='abrirDetalle({{ row | tojson | safe }})'>
                <div class="aspect-square rounded-[1.2rem] overflow-hidden border border-zinc-200 bg-zinc-100 mb-3">
                    <img src="{{ row.ruta_img or 'https://via.placeholder.com/600' }}" 
                         class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700">
                </div>
                
                <div class="px-1 text-left">
                    <p class="text-[11px] font-semibold text-zinc-900 uppercase tracking-tight mb-1">Día {{ row.ID_Dia }}</p>
                    <h2 class="text-[14px] font-serif font-black italic text-zinc-900 leading-tight line-clamp-2"> {{ row.Obra_Artista }} </h2>
                
                    <!-- LÍNEA INYECTADA: -->
                    <p class="text-[9px] font-medium text-zinc-500 uppercase tracking-wider mt-1"> {{ row.Genero_Tag }} </p>

                </div>
            </div>
            {% endfor %}
        </main>

         <div class="px-6 max-w-md mx-auto mb-4">
            <div id="contenedorPublicidadModal" class="w-full overflow-hidden rounded-xl bg-zinc-50 flex items-center justify-center">
                <img src="Banner_Lexicon.jpg" alt="Publicidad Lexicón C.A." class="w-full h-auto object-cover block">
            </div>
        </div> 

        <div class="text-center pb-20">
            <a href="#" class="text-[11px] font-semibold text-zinc-400 uppercase tracking-widest hover:text-zinc-900 transition-colors">
                ↑ Volver arriba
            </a>
        </div>

        <div id="detalleModal" class="fixed inset-0 z-50 hidden overflow-y-auto">
            <button onclick="cerrarDetalle()" class="fixed top-6 right-6 text-zinc-900 text-4xl font-light hover:text-zinc-500 z-[60]">&times;</button>
            
            <div class="max-w-xl mx-auto py-16 px-8">
                <div class="mb-12">
                    <img id="modalImg" class="w-full aspect-square object-cover rounded-[3rem] shadow-xl">
                </div>

                <div class="space-y-8">
                    <h3 id="modalTitulo" class="text-3xl md:text-4xl font-serif font-bold text-zinc-900 italic leading-tight text-center"></h3>
                    
                    <!-- INSERCIÓN QUIRÚRGICA AQUÍ -->
                    <p id="modalGenero" class="text-[12px] text-zinc-500 uppercase tracking-[0.2em] text-center -mt-6 mb-2 font-medium"></p>
                    
                    <div class="linea-separadora"></div>
                    <p id="modalAnalisis" class="text-zinc-800 text-lg leading-relaxed text-justify px-2 font-light italic"></p>
                </div>

                <div class="linea-separadora"></div>

                <div class="text-center">
                    <h4 class="text-[11px] font-black tracking-[0.5em] text-zinc-500 uppercase mb-8">Mini-Podcast</h4>
                    <div class="flex justify-center bg-white/50 p-6 rounded-[2rem] border border-zinc-200">
                        <audio id="modalAudio" controls class="w-full"></audio>
                    </div>
                </div>

                <div class="linea-separadora"></div>

                <div id="seccionTrivia" class="space-y-8 max-w-sm mx-auto pb-20">
                    <h4 class="text-2xl font-serif font-bold text-zinc-900 italic text-center uppercase tracking-tighter">Trivia del Día</h4>
                    <div class="bg-white/40 border border-zinc-200 p-6 rounded-[2rem] text-center">
                        <p id="triviaPregunta" class="text-zinc-900 font-medium"></p>
                    </div>
                    <div class="grid gap-4" id="contenedorOpciones"></div>
                    <div id="mensajeJuez" class="hidden py-4 px-6 rounded-2xl text-[11px] font-bold text-center uppercase tracking-widest"></div>
                    
                    <div id="seccionRegalo" class="hidden mt-4 p-4 border-2 border-dashed border-zinc-300 rounded-2xl text-center bg-white/50">
    <p class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">🎁 ¡Tienes un regalo por acertar!</p>
    <a id="linkRegalo" href="#" target="_blank" 
       class="inline-block bg-zinc-900 text-white font-bold py-2 px-6 rounded-full text-[11px] uppercase tracking-widest hover:bg-zinc-700 transition-all">
        <span id="textoRegalo">Descargar material</span>
    </a>
</div>
                    
                    <div id="seccionPista" class="hidden bg-white/60 border border-zinc-200 p-6 rounded-[2rem] text-center">
                        <h5 class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest mb-2">Pista del Maestro</h5>
                        <p id="modalPista" class="text-zinc-700 italic text-sm leading-relaxed"></p>
                    </div>
                </div>

                <div id="seccionYoutube" class="hidden">
    <div class="linea-separadora"></div>
    <div class="text-center pb-4">
        <a id="linkYoutube" href="#" target="_blank" 
           class="inline-block bg-[#ff0000] text-white font-bold py-3 px-8 rounded-full text-sm uppercase tracking-widest hover:bg-zinc-900 transition-all shadow-lg">
            ▶ Escucha el tema completo aquí
        </a>
    </div>
</div>

        <div class="linea-separadora"></div>

<div class="px-6 max-w-md mx-auto mb-4">
            <div id="contenedorPublicidad" class="w-full border-2 border-dashed border-zinc-300 rounded-xl bg-zinc-50 flex items-center justify-center p-4 text-center">
                <div class="text-zinc-500 font-medium">
                    <p class="text-sm uppercase tracking-wider mb-1">Espacio Publicitario Disponible</p>
                    <p class="text-xs">Tu empresa puede anunciar aquí. Contáctanos.</p>
                </div>
            </div>


                <!-- Mira el final de esta línea: le agregamos 'relative' -->
<div class="flex justify-between items-center pt-10 border-t border-zinc-200 mt-10 relative">
    
    <div class="absolute top-2 left-1/2 transform -translate-x-1/2">
        <img src="NuevoLogo.png" class="h-10 object-contain opacity-100">
    </div>
    
    <button onclick="cerrarDetalle()" class="text-[11px] font-bold text-zinc-400 uppercase tracking-widest hover:text-zinc-900 transition-colors">
        ← Atrás
    </button>
    <button onclick="document.getElementById('detalleModal').scrollTo({top: 0, behavior: 'smooth'})" class="text-[11px] font-bold text-zinc-400 uppercase tracking-widest hover:text-zinc-900 transition-colors">
        ↑ Volver arriba
    </button>
</div>

            </div>
        </div>

        <script>
            let respuestaCorrectaGlobal = "";

            function filtrarTarjetas() {
                let input = document.getElementById('inputBusqueda').value.toLowerCase();
                let tarjetas = document.getElementsByClassName('tarjeta-musica');
                for (let t of tarjetas) {
                    let info = t.innerText.toLowerCase();
                    t.style.display = info.includes(input) ? "block" : "none";
                }
            }

            function abrirDetalle(data) {
                document.getElementById('modalImg').src = data.ruta_img || '';
                document.getElementById('modalTitulo').innerText = data.Obra_Artista;

                // INSERCIÓN QUIRÚRGICA:
                document.getElementById('modalGenero').innerText = data.Genero_Tag || "";

                document.getElementById('modalAnalisis').innerText = data.Analisis_Sustancia || "";
                document.getElementById('triviaPregunta').innerText = data.Pregunta_Trivia || "";
                document.getElementById('modalPista').innerText = data.Pista_Maestro || "";
                respuestaCorrectaGlobal = data.Respuesta_Correcta.toString().toUpperCase().trim();

                const audio = document.getElementById('modalAudio');
                audio.src = data.ruta_audio || "";
                audio.parentElement.parentElement.style.display = data.ruta_audio ? 'block' : 'none';

                const contenedor = document.getElementById('contenedorOpciones');
                contenedor.innerHTML = "";
                document.getElementById('mensajeJuez').classList.add('hidden');
                document.getElementById('seccionPista').classList.add('hidden');

                const opciones = [
                    { letra: 'A', texto: data.Opcion_A },
                    { letra: 'B', texto: data.Opcion_B },
                    { letra: 'C', texto: data.Opcion_C }
                ];

                opciones.forEach(opt => {
                    if(opt.texto) {
                        let btn = document.createElement('button');
                        btn.className = "btn-trivia";
                        btn.innerText = opt.texto;
                        btn.onclick = () => verificarRespuesta(opt.letra, btn);
                        contenedor.appendChild(btn);
                    }
                });

                document.getElementById('detalleModal').classList.remove('hidden');
                document.body.classList.add('modal-active');
                // Lógica para el botón de YouTube
        const seccionYoutube = document.getElementById('seccionYoutube');
        const linkYoutube = document.getElementById('linkYoutube');

        if (data.Link_Audicion && data.Link_Audicion.trim() !== "") {
            linkYoutube.href = data.Link_Audicion;
            seccionYoutube.classList.remove('hidden');
        } else {
            seccionYoutube.classList.add('hidden');
        }
            // Preparar el regalo (se mantiene oculto hasta que acierte)
        const seccionRegalo = document.getElementById('seccionRegalo');
        const linkRegalo = document.getElementById('linkRegalo');
        const textoRegalo = document.getElementById('textoRegalo');

        seccionRegalo.classList.add('hidden');

        if (data.Link_Regalo && data.Link_Regalo.trim() !== "") {
            linkRegalo.href = data.Link_Regalo;
            textoRegalo.innerText = data.Etiqueta_Regalo || "Descargar material";
            seccionRegalo.dataset.tieneRegalo = "true"; 
        } else {
            seccionRegalo.dataset.tieneRegalo = "false";
        }



            }

            function verificarRespuesta(letra, boton) {
                const mensaje = document.getElementById('mensajeJuez');
                const pista = document.getElementById('seccionPista');
                const botones = document.querySelectorAll('#contenedorOpciones button');

                if (respuestaCorrectaGlobal.startsWith(letra)) {
                    botones.forEach(b => b.disabled = true);
                    boton.classList.add('btn-correct');
                    mensaje.innerText = "¡Correcto!✨";
                    mensaje.className = "block py-4 px-6 rounded-2xl text-zinc-900 bg-white/80 font-bold text-center border-2 border-zinc-900";
                    pista.classList.add('hidden');
                    document.getElementById('audioAcierto').play();

                    // Revelar regalo si existe para este día
            const seccionRegalo = document.getElementById('seccionRegalo');
            if (seccionRegalo.dataset.tieneRegalo === "true") {
                seccionRegalo.classList.remove('hidden');
            }

                } else {
                    boton.classList.add('btn-incorrect');
                    mensaje.innerText = "Casi. Lee la Pista-Maestro";
                    mensaje.className = "block py-4 px-6 rounded-2xl text-zinc-900 bg-white/80 font-bold text-center border-2 border-zinc-900";
                    pista.classList.remove('hidden');
                    document.getElementById('audioError').play();
                }
                mensaje.classList.remove('hidden');
            }

            function cerrarDetalle() {
                document.getElementById('modalAudio').pause();
                document.getElementById('detalleModal').classList.add('hidden');
                document.body.classList.remove('modal-active');
            }

 // Función para quitar la pantalla de bienvenida y activar audio
            window.onload = function() {
                const sonido = document.getElementById('audioSplash');
                const splash = document.getElementById('splash-screen');

                // 1. Lógica del Audio (Desbloqueador)
                const iniciarAudio = () => {
                    if (sonido) {
                        sonido.play().then(() => {
                            console.log("Audio reproducido con éxito");
                            document.removeEventListener('click', iniciarAudio);
                            document.removeEventListener('touchstart', iniciarAudio);
                        }).catch(e => {
                            console.log("Esperando interacción del usuario para sonar");
                        });
                    }
                };

                // Escuchamos el primer toque para el audio
                document.addEventListener('click', iniciarAudio);
                document.addEventListener('touchstart', iniciarAudio, { passive: true });

                // 2. Lógica de Salida del Splash (Única y limpia)
                setTimeout(() => {
                    if (splash) {
                        console.log("Saliendo del splash...");
                        splash.style.opacity = '0';
                        setTimeout(() => {
                            splash.style.display = 'none';
                        }, 1000);
                    } else {
                        console.log("Error: No se encontró el elemento splash-screen");
                    }
                }, 2500); 
            }; // Aquí termina la función correctamente
        </script>
    </body>
</html>
"""

    # 1. Generamos el contenido (aquí mantenemos tu logo y tus datos intactos)
    html_final = Template(html_template).render(lista_datos=datos_json, logo=archivo_logo)

    # 2. Inyectamos Analytics (usando la variable de la línea 14)
    html_final = html_final.replace('<head>', '<head>' + codigo_analytics)

    # 3. Guardamos el archivo final ya con todo incluido
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_final)  

        print(f"--- ¡Versión Minimalista Vocabulary Lista! ---")

except Exception as e:
    print(f"Error crítico: {e}")
