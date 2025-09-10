using UnityEngine;
using System.Collections.Generic;

public class EntityManager : MonoBehaviour
{
    public static EntityManager Instance;
    public GameObject PosMgr;


    public GameObject agentPrefab;
    public GameObject ghostPrefab;
    public GameObject FogPrefab;
    public GameObject wallPrefab;
    public GameObject poiPrefab;
    public GameObject agentCarryingPrefab;

    private Dictionary<int, GameObject> agents = new Dictionary<int, GameObject>();
    private Dictionary<int, GameObject> ghosts = new Dictionary<int, GameObject>();
    private Dictionary<int, GameObject> walls = new Dictionary<int, GameObject>();
    private Dictionary<int, GameObject> pois = new Dictionary<int, GameObject>();

    void Awake()
    {
        Instance = this;
    }

    public void UpdateAgent(Agent a)
    {
        if(!agents.ContainsKey(a.id))
        {
            Vector3 pos = PosMgr.GetComponent<PositionManager>().get_coords(a.x, a.y);
            GameObject newAgent = Instantiate(agentPrefab, pos, Quaternion.identity);
            agents[a.id] = newAgent;
        }
        else
        {
            GameObject agent = agents[a.id];
            Vector3 pos = PosMgr.GetComponent<PositionManager>().get_coords(a.x, a.y);
            agent.transform.position = pos;
        }
    }

    public void UpdateGhost(Ghost g)
    {
        if(!ghosts.ContainsKey(g.order))
        {
            Vector3 pos = PosMgr.GetComponent<PositionManager>().get_coords(g.x, g.y);
            GameObject newGhost = Instantiate(ghostPrefab, pos, Quaternion.identity);
            ghosts[g.order] = newGhost;
        }
        else
        {
            Vector3 pos = PosMgr.GetComponent<PositionManager>().get_coords(g.x, g.y);
            ghosts[g.order].transform.position = pos;
        }
    }

    public void UpdateWalls(Wall w)
    {
        if(!walls.ContainsKey(w.order))
        {
            Vector3 pos = PosMgr.GetComponent<PositionManager>().get_coords(w.x, w.y);
            GameObject newWall = Instantiate(wallPrefab, pos, Quaternion.identity);
            walls[w.order] = newWall;
        }
        else
        {
            Vector3 pos = PosMgr.GetComponent<PositionManager>().get_coords(w.x, w.y);
            GameObject wall = walls[w.order];
            wall.transform.position = pos;
        }
    }

    public void UpdatePoi(Poi p)
    {
        if (!pois.ContainsKey(p.order))
        {
            Vector3 pos = PosMgr.GetComponent<PositionManager>().get_coords(p.x, p.y);
            GameObject newPoi = Instantiate(poiPrefab, pos, Quaternion.identity);
            pois[p.order] = newPoi;
        }
        else
        {
            Vector3 pos = PosMgr.GetComponent<PositionManager>().get_coords(p.x, p.y);
            pois[p.order].transform.position = pos;
        }
    }
}
