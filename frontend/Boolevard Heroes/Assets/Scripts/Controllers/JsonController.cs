using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
/// <summary>
/// This follow player controller class will update the events from the main camera .
/// It will follow the pleyaer with a speciffic offset.
/// </summary>
public class JsonController : MonoBehaviour
{
    // Variable goblal que hace referencia a una url para inicializar el juego
    private string startUrl = "http://127.0.0.1:5000/start/naive";
    // Variable global que hace raferencia a una url en la simulacion del juego
    private string stepUrl = "http://127.0.0.1:5000/turn";
    /// <summary>
    /// Start es llamado una sola vez al iniciar el script, y se valida que las urls
    /// sean validas y no esten vacias, ademas llama al servidor con la url de inicio
    /// y para despues empezar a llamar cada turno de la simulacion.
    /// </summary>
    void Start()
    {
        // Se imprimen las urls en la consola para verificar que esten correctas
        Debug.Log($"startUrl='{startUrl}', stepUrl='{stepUrl}'");
        if(!string.IsNullOrWhiteSpace(startUrl) && !string.IsNullOrWhiteSpace(stepUrl))
        {
            // Inicializa la simulacion con startUrl
            StartCoroutine(GetYeison(startUrl));
            // Inicializa cada turno de la simulacion con stepUrl
            StartCoroutine(CallStepLoop());
        }
        else
        {
            Debug.Log("Hola, algo salio mal, se puso mal la url");
        }
    }

    /// <summary>
    /// Aqui se que ejecuta el bucle infinito para llamar a stepUrl cada 4 segundos
    /// </summary>
    IEnumerator CallStepLoop()
    {
        // Empieza el bucle en donde se espera 4 segundos para cada turno
        while (true)
        {
            yield return GetYeison(stepUrl);
            yield return new WaitForSeconds(4f);
        }
    }
    /// <summary>
    /// Aqui se que realiza una petición get a la url del turno.
    /// </summary>
    IEnumerator GetYeison(string url)
    {
        using(UnityWebRequest web = UnityWebRequest.Get(url))
        {
            // Espera a la respuesta del servidor
            yield return web.SendWebRequest();

            // Valida si la peticion se realizo correctamente
            if (web.result != UnityWebRequest.Result.Success)
            {
                Debug.Log("No se pudo leer el yeison: " + web.error);
            }
            // Si la peticion es correcta se manda a imprimir el yeison
            else
            {
                string json = web.downloadHandler.text;
                PrintYeison(json);
            }
        }
    }
    /// <summary>
    /// Aqui se imprime el yeison en la consola para visualizar los datos
    /// </summary>
    void PrintYeison(string json)
    {
        Json data = JsonUtility.FromJson<Json>(json);
        Debug.Log("YEISON:\n" + JsonUtility.ToJson(data, true));

        // Verifica que el yeison no este vacio
        if(data == null)
        {
            Debug.Log("Hola, no se paso bien el yeison o no coinciden los nombres");
            return;
        }
        // Imprime los datos de los agentes
        if(data.agents != null)
        {
            foreach(Agent a in data.agents)
            {
                Debug.Log($"Agent action={a.action}, id={a.id}, order={a.order}, energy={a.energy}, pos=({a.x}, {a.y}), carrying={a.carrying}");
            }
        }
        // Imprime los datos de los fantasmas
        if(data.ghosts != null)
        {
            foreach(Ghost g in data.ghosts)
            {
                Debug.Log($"Ghost order={g.order}, status={g.status}, pos=({g.x}, {g.y})");
            }
        }
        // Imprime los datos de las paredes
        if(data.walls != null)
        {
            foreach(Wall w in data.walls)
            {
                Debug.Log($"Wall order={w.order}, dir={w.direction}, status={w.status}, pos=({w.x},{w.y})");
            }
        }
        // Imprime los datos de los pois
        if(data.pois != null)
        {
            foreach(Poi p in data.pois)
            {
                Debug.Log($"Poi order={p.order}, old={p.old_status}, new={p.new_status}, pos=({p.x},{p.y})");
            }
        }
    }
}
