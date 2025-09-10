using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class JsonController : MonoBehaviour
{

    public string startUrl = "";
    public string stepUrl = "";
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        if(!string.IsNullOrWhiteSpace(stepUrl))
        {
            StartCoroutine(GetJson(startUrl, stepUrl));
        }
        else
        {
            Debug.Log("Hola, algo salio mal, se puso mal la url");
        }
    }

    IEnumerator GetJson(string startUrl, string stepUrl)
    {
        using (UnityWebRequest web = UnityWebRequest.Get(stepUrl))
        {
            yield return web.SendWebRequest();

            if(web.result != UnityWebRequest.Result.Success)
            {
                Debug.Log("No se pudo leer el yeison: " + web.error);
            }
            else
            {
                string json = web.downloadHandler.text;
                PrintJson(json);
            }
        }
    }

    void PrintJson(string json)
    {
        Json data = JsonUtility.FromJson<Json>(json);
        Debug.Log("JSON:\n" + JsonUtility.ToJson(data, true));


        if(data == null)
        {
            Debug.Log("Hola, no se paso bien el yeison o no coinciden los nombres");
            return;
        }

        if(data.agents != null)
        {
            foreach(Agent a in data.agents)
            {
                Debug.Log($"Agent action={a.action}, id={a.id}, order={a.order}, energy={a.energy}, pos=({a.x}, {a.y}), carrying={a.carrying}");
            }
        }

        if(data.ghosts != null)
        {
            foreach(Ghost g in data.ghosts)
            {
                Debug.Log($"Ghost order={g.order}, status={g.status}, pos=({g.x}, {g.y})");
            }
        }

        if(data.walls != null)
        {
            foreach(Wall w in data.walls)
            {
                Debug.Log($"Wall order={w.order}, dir={w.direction}, status={w.status}, pos=({w.x},{w.y})");
            }
        }

        if(data.pois != null)
        {
            foreach(Poi p in data.pois)
            {
                Debug.Log($"Poi order={p.order}, old={p.old_status}, new={p.new_status}, pos=({p.x},{p.y})");
            }
        }
    }
}
