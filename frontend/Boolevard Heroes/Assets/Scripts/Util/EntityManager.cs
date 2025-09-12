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
    private Dictionary<float, GameObject> horizontalWalls = new Dictionary<float, GameObject>();
    private Dictionary<float, GameObject> verticalWalls = new Dictionary<float, GameObject>();

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

        Wall w = new Wall
        {
            direction = 3,
            order = 0,
            status = 3,
            x = 4,
            y = 1,
        };
        StartCoroutine(UpdateWalls(w));

        w.x = 5;
        w.y = 2;
        w.direction = 1;
        StartCoroutine(UpdateWalls(w));

        w.x = 8;
        w.y = 2;
        w.direction = 2;
        StartCoroutine(UpdateWalls(w));

        w.x = 7;
        w.y = 4;
        w.direction = 3;
        StartCoroutine(UpdateWalls(w));

        w.x = 3;
        w.y = 3;
        w.direction = 3;
        StartCoroutine(UpdateWalls(w));

        w.x = 4;
        w.y = 4;
        w.direction = 2;
        StartCoroutine(UpdateWalls(w));

        w.x = 6;
        w.y = 6;
        w.direction = 3;
        StartCoroutine(UpdateWalls(w));

        w.x = 8;
        w.y = 6;
        w.direction = 3;
        StartCoroutine(UpdateWalls(w));

        w.status = 2;

        w.x = 6;
        w.y = 0;
        w.direction = 2;
        StartCoroutine(UpdateWalls(w));

        w.x = 0;
        w.y = 3;
        w.direction = 1;
        StartCoroutine(UpdateWalls(w));

        w.x = 3;
        w.y = 7;
        w.direction = 0;
        StartCoroutine(UpdateWalls(w));

        w.x = 9;
        w.y = 4;
        w.direction = 3;
        StartCoroutine(UpdateWalls(w));
        
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
        GameObject human = positionManager.get_poi_human(g.x, g.y);
        GameObject unrevealed = positionManager.get_poi_unrevealed(g.x, g.y);
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

        if (human.activeSelf)
        {
            human.SetActive(false);
        }

        if (unrevealed.activeSelf)
        {
            unrevealed.SetActive(false);
        }

        yield return null;
    }

    public IEnumerator UpdateWalls(Wall w)
    {
        bool isHorizontal = w.direction % 2 == 0;
        float x = w.x, y = w.y;

        Vector3 originalPos = PosMgr.GetComponent<PositionManager>().get_coords(w.x, w.y);
        Vector3 actionPos;

        switch (w.direction)
        {
            case 0:
                actionPos = PosMgr.GetComponent<PositionManager>().get_coords(w.x, w.y - 1);
                y -= 0.5f;
                break;
            case 1:
                actionPos = PosMgr.GetComponent<PositionManager>().get_coords(w.x + 1, w.y);
                x -= 0.5f;
                break;
            case 2:
                actionPos = PosMgr.GetComponent<PositionManager>().get_coords(w.x, w.y + 1);
                x += 0.5f;
                break;
            default:
                actionPos = PosMgr.GetComponent<PositionManager>().get_coords(w.x - 1, w.y);
                y += 0.5f;
                break;
        }

        actionPos = (actionPos + originalPos) / 2;

        actionPos.y = 10;
        float position = y * 10 + x;
        GameObject editableToken;

        if (isHorizontal)
        {
            if (!horizontalWalls.ContainsKey(position))
            {
                GameObject newWallToken = Instantiate(wallPrefab, actionPos, Quaternion.identity);
                horizontalWalls[position] = newWallToken;
            }

            editableToken = horizontalWalls[position];
        }
        else
        {
            if (!verticalWalls.ContainsKey(position))
            {
                GameObject newWallToken = Instantiate(wallPrefab, actionPos, Quaternion.identity);
                verticalWalls[position] = newWallToken;
            }

            editableToken = verticalWalls[position];
        }

        Debug.Log("Habemus token");

        switch (w.status)
        {
            case 0:
                editableToken.transform.Find("DamageDoorOne").gameObject.SetActive(false);
                editableToken.transform.Find("DamageDoorTwo").gameObject.SetActive(true);
                break;
            case 0.5f:
                editableToken.transform.Find("DamageDoorTwo").gameObject.SetActive(false);
                editableToken.transform.Find("DamageDoorOne").gameObject.SetActive(true);
                break;
            case 2:
                editableToken.transform.Find("BrokenDoor").gameObject.SetActive(false);
                editableToken.transform.Find("ClosedDoor").gameObject.SetActive(false);
                editableToken.transform.Find("OpenDoor").gameObject.SetActive(true);
                break;
            case 3:
                editableToken.transform.Find("BrokenDoor").gameObject.SetActive(false);
                editableToken.transform.Find("OpenDoor").gameObject.SetActive(false);
                editableToken.transform.Find("ClosedDoor").gameObject.SetActive(true);
                break;
            case 4:
                editableToken.transform.Find("OpenDoor").gameObject.SetActive(false);
                editableToken.transform.Find("ClosedDoor").gameObject.SetActive(false);
                editableToken.transform.Find("BrokenDoor").gameObject.SetActive(true);
                break;
        }

        yield return null;
    }

    public IEnumerator UpdatePoi(Poi p)
    {
        GameObject human = positionManager.get_poi_human(p.x, p.y);
        GameObject unrevealed = positionManager.get_poi_unrevealed(p.x, p.y);
        GameObject ghost = positionManager.get_ghost(p.x, p.y);
        GameObject fog = positionManager.get_fog(p.x, p.y);

        Debug.Log(p.new_status);

        if (p.new_status == 0 || p.new_status == 5)
        {
            if (p.old_status == 3 || p.old_status == 5)
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

        if (ghost.activeSelf) {
            ghost.SetActive(false);
        }

        if (fog.activeSelf) {
            fog.SetActive(false);
        }

        yield return null;
    }
}
