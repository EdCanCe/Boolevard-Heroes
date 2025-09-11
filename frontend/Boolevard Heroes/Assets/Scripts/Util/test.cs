using UnityEngine;
using System;
using System.Collections.Generic;

public class test : MonoBehaviour
{
    public GameObject obj;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        Debug.Log(obj.GetComponent<PositionManager>().get_coords(5, 4));
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
