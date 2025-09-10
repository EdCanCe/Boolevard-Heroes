using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class Agent {
    public string action;
    public bool carrying;
    public int energy;
    public int id;
    public int order;
    public int x;
    public int y;
}

[Serializable]
public class Ghost {
    public int order;
    public int status;
    public int x;
    public int y;
}

[Serializable]
public class Poi {
    public int new_status;
    public int old_status;
    public int order;
    public int x;
    public int y;
}

[Serializable]
public class Wall {
    public int direction;
    public int order;
    public float status;
    public int x;
    public int y;
}

[Serializable]
public class Json {
    public List<Agent> agents;
    public int damaged_points;
    public List<Ghost> ghosts;
    public int num_steps;
    public List<Poi> pois;
    public int saved_victims;
    public int scared_victims;
    public List<Wall> walls;
}