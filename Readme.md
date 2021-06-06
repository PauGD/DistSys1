#Homework for Distributed Systems

En primer lloc, hem de dir que la pràctica l’hem realitzat presencialment i conjuntament sempre. Hem anat quedant durant el quadrimestre i l’hem fet entre els dos en tot moment. Algun dia l’hem avançat a l’ordinador de l’Oriol i alguns altres a l’ordinador del Pau, per això hi ha commits dels dos integrants del grup.

En quant a decisions de disseny, tenim tres fitxers principals que són el master.py, el client.py i el config.py i dos fitxers .txt per provar les funcions de CountWords i WordCount.
En el fitxer master.py tenim els següents imports perquè la pràctica funcioni:



Inicialitzem els servidors Redis i XMLRPC. Dins la funció startWorker creem els diferents workers que faran les funcions de comptar paraules. Per a fer-ho, tenim un bucle general on primer comprovem que el fitxer sigui correcte i anem tractant els treballs que ens van arribant, per exemple, si ens arriba un treball de tipus ‘Count’, fem una crida a la funció countWords amb el fitxer correspondent i ho guardem a un fitxer de sortida “result”. Fem el mateix pel tipus ‘Word’ i tot seguit ho apilem a la pila del redis el resultat amb la ID del treball. Pel tipus ‘Add’, haurem de cridar a la funció addResults. Cal tenir en compte també, que el bucle espera a que hi hagi un treball a la cua “JobList”.
Tot seguit, tenim les funcions countWords i wordCount. La primera és relativament bàsica, tenim un split del text del fitxer que guardem en una variable i retornem la llargada d’aquesta variable. En segon lloc, a la funció wordCount fem també un split i guardem totes les paraules diferenciades en una llista d’ocurrences, per tot seguit, comptar les que es repeteixen i guardar els resultats a un diccionari que retornem.
Més endavant, tenim les funcions addJob i addMultipleJobs, que farem servir depenent de si realitzarem un únic treball o bé més d’un. Al addJob, apilem l’argument que li passem per paràmetre a la llista “JobList” perquè tracti la tasca, tot seguit, esperem a la cua identificada per la ID del treball el resultat d’aquesta tasca, ho desapilem i ho retornem el resultat.
En quant a la funció addMultipleJobs, fem també un json.loads de l’argument que passem per paràmetre i obtenim les urls del treballs en una sola string. Fem un split d’aquesta String i guardem les diferents urls a una taula.Anem recorrent aquesta taula i afegint treballs individuals amb cada url a la cua, també anem tenint constància de quantes urls tenim. Quan sortim del bucle afegim un treball de tipus add que serà qui ens aguparà els resultats, en URL posaren el nùmero de treballs que hem tractat. Finalment generem una string que ens servirà per identificar la cua en que tindrem els resultats, esperarem en aquesta cua fins a obtenir-los i quan els tinguem els retornarem.

En la funció addResults, primer obtindrem l’ID per  poder trobar la cua on tenim els resultats i  el contingut d’URL que és on tindrem el número de treballs que hem d’espera. Després esperem rebre el primer resultat , un cop el tenim determinem de quin tipus és: si es un int o un dict. Si es un int cada vegada que rebem un resultat el sumem a un contador. Si es un dict primer recorrerem l’element anterior buscant si els elements del nou dict estan en el que hem , si no estan sumem els dos números sinó creem una nova entrada amb la nova clau.  Un cop hem tractat tots els resultats els encuem en la cua amb una ID generada de tal manera que addMultipleJobs la pugui identificar.

Al fitxer client.py importem les següents llibreries:



En primer lloc, obtenim la connexió de l’XMLRPC i obtenim el proxy.  Per poder cridar les comandes desde la shell hem usat la llibreria click. Aquesta ens ha permès crear un grup general del que dependran totes les comandes i configuracions amb les que cridarem a les accions.  Les accions que tenim són les següents:
addJob: Ens permet pujar una tasca al master. Li hem d’entrar una Url on tinguem un fitxer i quin mode volem sigui: Count (per contar el número de paraules) o Word (per contar les ocurrències de cada paraula). Definirem també una id aleatòria per la tasca. Amb aquestes dades crearem un diccionari que passarem a string utilitzant Json i cridarem a addJob del master utilitzant el proxy.
addWorker: Simplement crida a createWorker utilitzant el proxy.
listWorkers: Ens retorna una llista de tots els workers i si estan vius o morts.
deleteWorker: Li entrem la ID del worker i crida a deleteWorker.
addMultipleJobs: Funciona com addJob però se li pot introduir més d’una URL. Aquestes urls les ajunta en una sola string que posa al paràmetre URL del dict que s'enviarà.


Finalment, en el fitxer config.py tenim importada la llibreria Flask from flask i tenim una funció per cridar les rutes als fitxers de prova. Quan es compleix la ruta al request, aquest executa la rutina corresponent que envia un fitxer a qui ha fet la request.

