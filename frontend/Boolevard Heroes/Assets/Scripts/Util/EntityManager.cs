using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class EntityManager : MonoBehaviour
{
    public static EntityManager Instance;
    public GameObject PosMgr;

    private PositionManager positionManager;

    public GameObject agentPrefab;
    public GameObject ghostPrefab;
    public GameObject FogPrefab;
    public GameObject wallPrefab;
    public GameObject poiPrefab;
    public GameObject agentCarryingPrefab;

    private Dictionary<int, GameObject> agents = new Dictionary<int, GameObject>();
    private Dictionary<int, GameObject> walls = new Dictionary<int, GameObject>();

    private int left_movements;

    public float animationTime;

    void Awake()
    {
        Instance = this;
    }

    void Start()
    {
        left_movements = 0;
        positionManager = PosMgr.GetComponent<PositionManager>();
        Hide_Everything();
        InitializeMap();
        animationTime = 1f;
    }

    public void Hide_Everything()
    {
        Debug.Log("Me Metí al hide");
        for (int x = 0; x < 10; x++)
        {
            for (int y = 0; y < 8; y++)
            {
                StartCoroutine(positionManager.hide(positionManager.get_ghost(x, y), 0, 0));
                StartCoroutine(positionManager.hide(positionManager.get_fog(x, y), 1, 0));
                StartCoroutine(positionManager.hide(positionManager.get_poi_human(x, y), 2, 0));
                StartCoroutine(positionManager.hide(positionManager.get_poi_unrevealed(x, y), 3, 0));
            }
        }
    }


    public void InitializeMap()
    {
        StartCoroutine(positionManager.show(positionManager.get_ghost(2, 2), 0, 0));
        StartCoroutine(positionManager.show(positionManager.get_ghost(2, 3), 0, 0));
        StartCoroutine(positionManager.show(positionManager.get_ghost(3, 2), 0, 0));
        StartCoroutine(positionManager.show(positionManager.get_ghost(3, 3), 0, 0));
        StartCoroutine(positionManager.show(positionManager.get_ghost(4, 3), 0, 0));
        StartCoroutine(positionManager.show(positionManager.get_ghost(4, 4), 0, 0));
        StartCoroutine(positionManager.show(positionManager.get_ghost(5, 3), 0, 0));
        StartCoroutine(positionManager.show(positionManager.get_ghost(6, 5), 0, 0));
        StartCoroutine(positionManager.show(positionManager.get_ghost(6, 6), 0, 0));
        StartCoroutine(positionManager.show(positionManager.get_ghost(7, 5), 0, 0));
        StartCoroutine(positionManager.show(positionManager.get_poi_unrevealed(4, 2), 1, 0));
        StartCoroutine(positionManager.show(positionManager.get_poi_unrevealed(8, 5), 1, 0));
        StartCoroutine(positionManager.show(positionManager.get_poi_unrevealed(1, 5), 1, 0));
    }

    public void UpdateAgent(Agent a)
    {
        if (!agents.ContainsKey(a.id))
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
        GameObject ghost = positionManager.get_ghost(g.x, g.y);
        GameObject fog = positionManager.get_fog(g.x, g.y);

        if (g.status == 2)
        {
            if (fog.activeSelf)
            {
                StartCoroutine(positionManager.hide(fog, 1, animationTime));
            }
            StartCoroutine(positionManager.show(ghost, 0, animationTime));
        }

        else if (g.status == 1)
        {
            if (ghost.activeSelf)
            {
                StartCoroutine(positionManager.hide(ghost, 1, animationTime));
            }
            StartCoroutine(positionManager.show(fog, 0, animationTime));
        }

        else
        {
            StartCoroutine(positionManager.hide(ghost, 1, animationTime));
            StartCoroutine(positionManager.hide(fog, 1, animationTime));
        }
    }

    public void UpdateWalls(Wall w)
    {
        if (!walls.ContainsKey(w.order))
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
        GameObject human = positionManager.get_poi_human(p.x, p.y);
        GameObject unrevealed = positionManager.get_poi_unrevealed(p.x, p.y);

        if (p.new_status == 0)
        {
            if (p.old_status == 3)
            {
                StartCoroutine(positionManager.hide(unrevealed, 1, animationTime));
            }
            if (p.old_status == 4)
            {
                StartCoroutine(positionManager.hide(human, 1, animationTime));
            }
        }

        if (p.new_status == 3)
        {
            if (p.old_status == 0)
            {
                StartCoroutine(positionManager.show(unrevealed, 1, animationTime));
            }
            if (p.old_status == 4)
            {
                StartCoroutine(positionManager.hide(human, 1, animationTime));
                StartCoroutine(positionManager.show(unrevealed, 1, animationTime));
            }
        }

        if (p.new_status == 4)
        {
            if (p.old_status == 0)
            {
                StartCoroutine(positionManager.show(human, 1, animationTime));
            }
            if (p.old_status == 3)
            {
                StartCoroutine(positionManager.hide(unrevealed, 1, animationTime));
                StartCoroutine(positionManager.show(human, 1, animationTime));
            }
        }
    }
}
