using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class EntityManager : MonoBehaviour
{
    public static EntityManager Instance;
    public GameObject PosMgr;

    private PositionManager positionManager;

    public GameObject agentPrefab;
    public GameObject wallPrefab;

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
        StartCoroutine(positionManager.show(positionManager.get_poi_unrevealed(4, 2), 0, 0));
        StartCoroutine(positionManager.show(positionManager.get_poi_unrevealed(8, 5), 0, 0));
        StartCoroutine(positionManager.show(positionManager.get_poi_unrevealed(1, 5), 0, 0));

        Vector3 pos = PosMgr.GetComponent<PositionManager>().get_coords(6, 0);
        GameObject newAgent = Instantiate(agentPrefab, pos, Quaternion.identity);
        agents[1] = newAgent;
        pos = PosMgr.GetComponent<PositionManager>().get_coords(9, 4);
        newAgent = Instantiate(agentPrefab, pos, Quaternion.identity);
        agents[2] = newAgent;
        pos = PosMgr.GetComponent<PositionManager>().get_coords(3, 7);
        newAgent = Instantiate(agentPrefab, pos, Quaternion.identity);
        agents[3] = newAgent;
        pos = PosMgr.GetComponent<PositionManager>().get_coords(0, 3);
        newAgent = Instantiate(agentPrefab, pos, Quaternion.identity);
        agents[4] = newAgent;
        pos = PosMgr.GetComponent<PositionManager>().get_coords(4, 7);
        newAgent = Instantiate(agentPrefab, pos, Quaternion.identity);
        agents[5] = newAgent;
        pos = PosMgr.GetComponent<PositionManager>().get_coords(5, 0);
        newAgent = Instantiate(agentPrefab, pos, Quaternion.identity);
        agents[6] = newAgent;
    }

    public IEnumerator UpdateAgent(Agent a)
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

            GameObject normal = agent.transform.Find("AGENT").gameObject;
            GameObject withPoi = agent.transform.Find("AGENT_POI").gameObject;

            if (!withPoi.activeSelf && a.carrying)
            {
                withPoi.SetActive(true);
                normal.SetActive(false);
            }
            else if (!normal.activeSelf && !a.carrying)
            {
                normal.SetActive(true);
                withPoi.SetActive(false);
            }

            Vector3 initialPos = agent.transform.position;
            Vector3 endPos = PosMgr.GetComponent<PositionManager>().get_coords(a.x, a.y);

            endPos.y = initialPos.y;

            StartCoroutine(PosMgr.GetComponent<PositionManager>().animateFrom(agent, initialPos, endPos, animationTime));

        }

        yield return null;
    }

    public IEnumerator UpdateGhost(Ghost g)
    {
        GameObject ghost = positionManager.get_ghost(g.x, g.y);
        GameObject fog = positionManager.get_fog(g.x, g.y);
        bool ghostFlag = false;

        if (g.status == 2)
        {
            if (fog.activeSelf)
            {
                StartCoroutine(positionManager.hide(fog, 1, animationTime));
            }

            if (ghost.activeSelf)
            {
                StartCoroutine(positionManager.show(fog, 1, animationTime / 2f));
                ghostFlag = true;
            }

            StartCoroutine(positionManager.show(ghost, 0, animationTime));

            if (ghostFlag)
            {
                yield return new WaitForSeconds(animationTime / 2f);
                StartCoroutine(positionManager.hide(fog, 1, animationTime / 2f));
            }

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

        yield return null;
    }

    public IEnumerator UpdateWalls(Wall w)
    {
        yield return null;
    }

    public IEnumerator UpdatePoi(Poi p)
    {
        GameObject human = positionManager.get_poi_human(p.x, p.y);
        GameObject unrevealed = positionManager.get_poi_unrevealed(p.x, p.y);

        Debug.Log(p.new_status);

        if (p.new_status == 0 || p.new_status == 5)
        {
            if (p.old_status == 3)
            {
                StartCoroutine(positionManager.hide(unrevealed, 0, animationTime));
            }
            if (p.old_status == 4)
            {
                StartCoroutine(positionManager.hide(human, 0, animationTime));
            }
        }

        if (p.new_status == 3)
        {
            if (p.old_status == 0 || p.old_status == 3)
            {
                StartCoroutine(positionManager.show(unrevealed, 0, animationTime));
            }
            if (p.old_status == 4)
            {
                StartCoroutine(positionManager.hide(human, 0, animationTime));
                StartCoroutine(positionManager.show(unrevealed, 0, animationTime));
            }
        }

        if (p.new_status == 4)
        {
            if (p.old_status == 0)
            {
                StartCoroutine(positionManager.show(human, 0, animationTime));
            }
            if (p.old_status == 3)
            {
                StartCoroutine(positionManager.hide(unrevealed, 0, animationTime));
                StartCoroutine(positionManager.show(human, 0, animationTime));
            }
        }

        yield return null;
    }
}
