# gpx.py — parsing et analyse des fichiers GPX (distance, dénivelé, côtes, descentes)

import pandas as pd


def analyser_gpx(gpx_file):
    """
    Parse un fichier GPX et retourne un dict avec :
    - distance_totale_km, altitude_min/max_m, D_plus_m
    - df : DataFrame avec les points (latitude, longitude, elevation, cum_distance)
    - cotes : liste des montées > 200 m de long
    - descentes : liste des descentes > 200 m de long
    """
    import gpxpy

    gpx = gpxpy.parse(gpx_file)
    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation,
                    'time': point.time
                })
    df = pd.DataFrame(points)

    if df.empty:
        return None

    # Calcul des distances cumulées
    distances = [0.0]
    for i in range(1, len(df)):
        d = gpxpy.geo.haversine_distance(
            df['latitude'].iloc[i-1], df['longitude'].iloc[i-1],
            df['latitude'].iloc[i], df['longitude'].iloc[i]
        ) / 1000
        distances.append(d)
    df['distance'] = distances
    df['cum_distance'] = df['distance'].cumsum()
    df['elevation_diff'] = df['elevation'].diff().fillna(0)

    D_plus = df.loc[df['elevation_diff'] > 0, 'elevation_diff'].sum()

    # Détection des côtes (montées > 200 m)
    cotes = _detecter_segments(df, sens='montee')

    # Détection des descentes (> 200 m)
    descentes = _detecter_segments(df, sens='descente')

    return {
        'distance_totale_km': df['cum_distance'].iloc[-1],
        'altitude_min_m': df['elevation'].min(),
        'altitude_max_m': df['elevation'].max(),
        'D_plus_m': D_plus,
        'df': df,
        'cotes': cotes,
        'descentes': descentes
    }


def _detecter_segments(df, sens='montee'):
    """
    Détecte les segments continus en montée ou descente de plus de 200 m.
    sens : 'montee' (elevation_diff > 0) ou 'descente' (elevation_diff < 0)
    """
    segments = []
    seg_distance = 0.0
    seg_elevation = 0.0
    cum_d = 0.0

    for d, e, cum_d in zip(df['distance'], df['elevation_diff'], df['cum_distance']):
        if (sens == 'montee' and e > 0) or (sens == 'descente' and e < 0):
            seg_distance += d
            seg_elevation += e
        else:
            if seg_distance >= 0.2:
                pente = (abs(seg_elevation) / (seg_distance * 1000)) * 100
                seg_start = cum_d - seg_distance
                segments.append({
                    'start_km': seg_start,
                    'end_km': cum_d,
                    'longueur_km': seg_distance,
                    'pente_pct': round(pente, 1)
                })
            seg_distance = 0.0
            seg_elevation = 0.0

    # Dernier segment en cours en fin de parcours
    if seg_distance >= 0.2:
        pente = (abs(seg_elevation) / (seg_distance * 1000)) * 100
        seg_start = cum_d - seg_distance
        segments.append({
            'start_km': seg_start,
            'end_km': cum_d,
            'longueur_km': seg_distance,
            'pente_pct': round(pente, 1)
        })

    return segments
