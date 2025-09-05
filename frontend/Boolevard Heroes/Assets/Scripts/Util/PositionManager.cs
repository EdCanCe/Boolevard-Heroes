using UnityEngine;
using System;
using System.Collections.Generic;


public class PositionManager : MonoBehaviour
{
    public List<GameObject> coordinates;

    public Vector3 get_coords(int x, int y)
    {
        return coordinates[y * 10 + x].transform.position;
    }
}
