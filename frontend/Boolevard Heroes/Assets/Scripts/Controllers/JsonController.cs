using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using System.Collections.Generic;
using System.Linq;
using TMPro;

/// <summary>
/// This follow player controller class will update the events from the main camera .
/// It will follow the pleyaer with a speciffic offset.
/// </summary>
public class JsonController : MonoBehaviour
{
    public TextMeshProUGUI InfoText;
    // Variable goblal que hace referencia a una url para inicializar el juego
    private string startUrl = "http://127.0.0.1:5000/start/pro";
    // Variable global que hace raferencia a una url en la simulacion del juego
    private string stepUrl = "http://127.0.0.1:5000/turn";

    private bool callNext;

    /// <summary>
    /// Start es llamado una sola vez al iniciar el script, y se valida que las urls
    /// sean validas y no esten vacias, ademas llama al servidor con la url de inicio
    /// y para despues empezar a llamar cada turno de la simulacion.
    /// </summary>
    void Start()
    {
        callNext = true;

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
        yield return new WaitForSeconds(0.1f);

        // Empieza el bucle en donde se espera 4 segundos para cada turno
        while (true)
        {
            if (callNext)
            {
                callNext = false;
                yield return StartCoroutine(GetYeison(stepUrl));
            }
            yield return new WaitForSeconds(0.1f);
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
                if (string.IsNullOrWhiteSpace(json) || json == "null")
                {
                    Debug.LogWarning("Ya no hay más YEISON.");
                    yield break;
                }
                Dictionary<int, Step> steps = BuildStepsFromJson(json);
                StartCoroutine(GamePlay(steps));
            }
        }
    }

    Dictionary<int, Step> BuildStepsFromJson(string json)
    {
        Json data = JsonUtility.FromJson<Json>(json);
        Dictionary<int, Step> steps = new Dictionary<int, Step>();

        string winText = "";
        if (data.damaged_points >= 24 || data.scared_victims >= 4)
        {
            winText = "\n\nSIMULATION LOSES!";
        }
        else if (data.saved_victims >= 7)
        {
            winText = "\n\nSIMULATION WINS!";
        }

        InfoText.text =
                    $"Turn: {data.num_steps}\n" +
                    $"House Damage: {data.damaged_points}/24\n" +
                    $"Saved people: {data.saved_victims}/7\n" +
                    $"Scared people: {data.scared_victims}/4" +
                    winText;

        if (data == null)
        {
            return steps;
        }

        if(data.agents != null)
        {
            foreach(Agent a in data.agents)
            {
                if(!steps.ContainsKey(a.order))
                {
                    steps[a.order] = new Step();
                }
                steps[a.order].agents.Add(a);
            }
        }

        if(data.ghosts != null)
        {
            foreach(Ghost g in data.ghosts)
            {
                if(!steps.ContainsKey(g.order))
                {
                    steps[g.order] = new Step();
                }
                steps[g.order].ghosts.Add(g);
            }
        }

        if(data.walls != null)
        {
            foreach(Wall w in data.walls)
            {
                if(!steps.ContainsKey(w.order))
                {
                    steps[w.order] = new Step();
                }
                steps[w.order].walls.Add(w);
            }
        }

        if(data.pois != null)
        {
            foreach(Poi p in data.pois)
            {
                if(!steps.ContainsKey(p.order))
                {
                    steps[p.order] = new Step();
                }
                steps[p.order].pois.Add(p);
            }
        }

        return steps;
    }

    IEnumerator GamePlay(Dictionary<int, Step> steps)
    {
        List<int> orders = steps.Keys.OrderBy(o => o).ToList();

        foreach (int order in orders)
        {
            Step s = steps[order];

            foreach (Agent a in s.agents)
            {
                StartCoroutine(EntityManager.Instance.UpdateAgent(a));
            }

            foreach (Ghost g in s.ghosts)
            {
                StartCoroutine(EntityManager.Instance.UpdateGhost(g));
            }

            foreach (Wall w in s.walls)
            {
                StartCoroutine(EntityManager.Instance.UpdateWalls(w));
            }

            foreach (Poi p in s.pois)
            {
                StartCoroutine(EntityManager.Instance.UpdatePoi(p));
            }

            yield return new WaitForSeconds(1f);
        }

        callNext = true;
    }

    /// <summary>
    /// Aqui se imprime el yeison en la consola para visualizar los datos
    /// </summary>
    // void PrintYeison(string json)
    // {
    //     Json data = JsonUtility.FromJson<Json>(json);
    //     Debug.Log("YEISON:\n" + JsonUtility.ToJson(data, true));

    //     // Verifica que el yeison no este vacio
    //     if(data == null)
    //     {
    //         Debug.Log("Hola, no se paso bien el yeison o no coinciden los nombres");
    //         return;
    //     }
    //     // Imprime los datos de los agentes
    //     if(data.agents != null)
    //     {
    //         foreach(Agent a in data.agents)
    //         {
    //             Debug.Log($"Agent action={a.action}, id={a.id}, order={a.order}, energy={a.energy}, pos=({a.x}, {a.y}), carrying={a.carrying}");
    //         }
    //     }
    //     // Imprime los datos de los fantasmas
    //     if(data.ghosts != null)
    //     {
    //         foreach(Ghost g in data.ghosts)
    //         {
    //             Debug.Log($"Ghost order={g.order}, status={g.status}, pos=({g.x}, {g.y})");
    //         }
    //     }
    //     // Imprime los datos de las paredes
    //     if(data.walls != null)
    //     {
    //         foreach(Wall w in data.walls)
    //         {
    //             Debug.Log($"Wall order={w.order}, dir={w.direction}, status={w.status}, pos=({w.x},{w.y})");
    //         }
    //     }
    //     // Imprime los datos de los pois
    //     if(data.pois != null)
    //     {
    //         foreach(Poi p in data.pois)
    //         {
    //             Debug.Log($"Poi order={p.order}, old={p.old_status}, new={p.new_status}, pos=({p.x},{p.y})");
    //         }
    //     }
    // }
}
