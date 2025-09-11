using UnityEngine;
using System;
using System.Collections;
using System.Collections.Generic;

public class PositionManager : MonoBehaviour
{
    public List<GameObject> coordinates;

    public Vector3 get_coords(int x, int y)
    {
        return coordinates[y * 10 + x].transform.position;
    }

    public GameObject get_ghost(int x, int y)
    {
        return coordinates[y * 10 + x].transform.Find("Elementos/GHOSTS/GHOST").gameObject;
    }

    public GameObject get_fog(int x, int y)
    {
        return coordinates[y * 10 + x].transform.Find("Elementos/GHOSTS/FOG").gameObject;
    }

    public GameObject get_poi_human(int x, int y)
    {
        return coordinates[y * 10 + x].transform.Find("Elementos/Pois/POI_HUMAN").gameObject;
    }

    public GameObject get_poi_unrevealed(int x, int y)
    {
        return coordinates[y * 10 + x].transform.Find("Elementos/Pois/POI_UNREVELED").gameObject;
    }

    public IEnumerator hide(GameObject hideable, int elementType, float tiempo)
    {
        float currentX = hideable.transform.position.x;
        float currentY = hideable.transform.position.y;
        float currentZ = hideable.transform.position.z;

        float endY = -15.44f;

        if (elementType == 0)
        {
            endY = -5.44f;
        }

        Vector3 endPos = new Vector3(currentX, endY, currentZ);

        if (tiempo == 0)
        {
            hideable.transform.position = endPos;
        }
        else
        {
            yield return StartCoroutine(animateFrom(hideable, hideable.transform.position, endPos, tiempo));
        }

        hideable.SetActive(false);
    }

    public IEnumerator show(GameObject showable, int elementType, float tiempo)
    {
        showable.SetActive(true);

        float currentX = showable.transform.position.x;
        float currentY = showable.transform.position.y;
        float currentZ = showable.transform.position.z;

        float endY = -0.44f;

        if (elementType == 0)
        {
            endY = 9.56f;
        }

        Vector3 endPos = new Vector3(currentX, endY, currentZ);

        if (tiempo == 0)
        {
            showable.transform.position = endPos;
        }
        else
        {
            StartCoroutine(animateFrom(showable, showable.transform.position, endPos, tiempo));
        }

        yield return null;
    }

    IEnumerator animateFrom(GameObject animatable, Vector3 posInicial, Vector3 posFinal, float tiempo)
    {
        float pasado = 0f;

        animatable.transform.position = posInicial;

        while (pasado < tiempo)
        {
            float t = pasado / tiempo;

            animatable.transform.position = Vector3.Lerp(posInicial, posFinal, t);

            pasado += Time.deltaTime;
            yield return null;
        }

        animatable.transform.position = posFinal;
    }

}