import sqlite3
import json

manual = [
        {
            "sat": "NOAA-15",
            "trans": [
                {
                    "freq": "137.62",
                    "mode": "APT"
                },
                {
                    "freq": "1702.5",
                    "mode": "HRPT"
                }
            ]
        },
        {
            "sat": "NOAA-18",
            "trans": [
                {
                    "freq": "137.9125",
                    "mode": "APT"
                },
                {
                    "freq": "1707",
                    "mode": "HRPT"
                }
            ]
        },
        {
            "sat": "NOAA-19",
            "trans": [
                {
                    "freq": "137.1",
                    "mode": "APT"
                },
                {
                    "freq": "1702.5",
                    "mode": "HRPT"
                }
            ]
        },
        {
            "sat": "METOP-A",
            "trans": [
                {
                    "freq": "1701.3",
                    "mode": "AHRPT"
                }
            ]
        },
        {
            "sat": "METOP-B",
            "trans": [
                {
                    "freq": "1701.3",
                    "mode": "AHRPT"
                }
            ]
        },
        {
            "sat": "FENGYUN 3A",
            "trans": [
                {
                    "freq": "1704.5",
                    "mode": "RHCP"
                }
            ]
        },
        {
            "sat": "FENGYUN 3B",
            "trans": [
                {
                    "freq": "1704.5",
                    "mode": "RHCP"
                }
            ]
        },
        {
            "sat": "FENGYUN 3C",
            "trans": [
                {
                    "freq": "1701.3",
                    "mode": "RHCP"
                }
            ]
        },
        {
            "sat": "METEOR-M 2",
            "trans": [
                {
                    "freq": "137.1",
                    "mode": "LRPT"
                }
            ]
        },
        {
            "sat": "GOES 13",
            "trans": [
                {
                    "freq": "1685.7",
                    "mode": "GVAR"
                },
                {
                    "freq": "1691",
                    "mode": "LRIT"
                }
            ]
        },
        {
            "sat": "GOES 15",
            "trans": [
                {
                    "freq": "1685.7",
                    "mode": "GVAR"
                },
                {
                    "freq": "1691",
                    "mode": "LRIT"
                }
            ]
        },
        {
            "sat": "GOES 14",
            "trans": [
                {
                    "freq": "1685.7",
                    "mode": "GVAR"
                },
                {
                    "freq": "1691",
                    "mode": "LRIT"
                }
            ]
        },
        {
            "sat": "SO-50",
            "trans": [
                {
                    "frequ": "145.85",
                    "plu": 67,
                    "freq": "436.795",
                    "mode": "FM"
                }
            ]
        },
        {
            "sat": "ISS",
            "trans": [
                {
                    "freq": "145.825",
                    "frequ": "145.825",
                    "mode": "FM APRS"
                },
                {
                    "freq": "437.44",
                    "frequ": "437.44",
                    "mode": "FM APRS"
                },
                {
                    "frequ": "437.8",
                    "freq": "145.8",
                    "mode": "FM Voice RPT"
                },
                {
                    "freq": "145.8",
                    "mode": "FM SSTV"
                }
                
            ]
        },
        {
            "sat": "AO-73",
            "trans": [
                {
                    "freq": "145.935",
                    "mode": "BPSK Telemetry"
                },
                {
                    "freq": "145.950",
                    "frequ": "435.150",
                    "mode": "Inv SSB/CW"
                },
                {
                    "freq": "145.970",
                    "frequ": "435.130",
                    "mode": "Inv SSB/CW"
                }
            ]
        },
         {
            "sat": "FO-29",
            "trans": [
                {
                    "freq": "435.910",
                    "mode": "FM Mode U Digitalker"
                },
                {
                    "frequ": "145.900",
                    "freq": "435.800",
                    "mode": "Inv SSB/CW"
                },
                {
                    "frequ": "146.0",
                    "freq": "435.900",
                    "mode": "Inv SSB/CW"
                }
            ]
        }

    ]


conn = sqlite3.connect('satdb')
c = conn.cursor()

db = {}
for row in c.execute("SELECT name, tle FROM satdb"):
   num = int(row[1].split("\n")[1].split(" ")[1])
   
   name = row[0]
   if num == 43016:
       name = "AO-91"
   db[num] = name

res = {}
f = open("satslist.csv")
for line in f.readlines():
    a = line.rstrip().split(";")
    if a[7] == "active" or a[6] == "(non-amateur)" or a[6] == "(weather sat)":
        try:
            number = int(a[1].rstrip())
        except ValueError:
            continue
        satname = a[0]
        # doublon
        if satname == 'Fox-1B (RadFxSat AO-91)' or satname == 'RadFxSat (Fox-1B AO-91)':
            continue
        if number in db:
            name = db[number]
            uplink =  a[2].rstrip()
            downlink = a[3].rstrip()
            beacon = a[4].rstrip()
            mode = a[5].rstrip()
            bypass = False
            for sat in manual:
                if sat["sat"] == name:
                    print("bypass", name)
                    bypass = True
            if bypass:
                continue

            if not uplink and not downlink and not beacon:
                continue

            # cause SAUDISAT 1C (SO-50)
            if name == "SAUDISAT 1C" or name == "ISS (ZARYA)" or name == "FUNCUBE-1 (AO-73)" or name == "JAS-2 (FO-29)":
                continue
            if name == "NOAA 15" or name == "NOAA 18" or name == "NOAA 19":
                continue
           
            # old AO-91
            if name == '2017-073D':
                continue
            if name == "YUBILEINY (RS-30)":
                name = "RS-30"
            if name == "CUBESAT XI-V (CO-58)":
                name = "CO-58"
            if name == "MOZHAYETS 4 (RS-22)":
                name = "RS-22"
            if name == "ZACUBE-1 (TSHEPISOSAT)":
                name = "ZACUBE-1"
            if name == "CUBESAT XI-IV (CO-57)":
                name = "CO-57"
            if name == "SEEDS II (CO-66)":
                name = "CO-66"
            if name == "LUSAT (LO-19)":
                name = "LO-19"
            if name == "ITAMSAT (IO-26)":
                name = "IO-26"
            if name == "CUTE-1.7+APD II (CO-65)":
                name = "CO-65"
            if name == "CUBEBUG-2 (LO-74)":
                name = "LO-74"

            if name == "OSCAR 7 (AO-7)":
                name = "AO-07"
            if name == "TECHSAT 1B (GO-32)":
                name = "GO-32"
            if name == "AO-91 (Fox-1B RadFxSat)":
                name = "AO-91"
            if name == "FOX-1B (AO-91)":
                name = "AO-91"
            if name == "AO-92 (Fox-1D)":
                name = "AO-92"

            name = name.upper()

            if name not in res:
                res[name] = {"sat": name, "trans": []}

            if uplink and downlink:
                if mode == "FM_tone67Hz CW_only":
                    res[name]["trans"].append({"tone" : 67, "frequ": uplink, "freq": downlink, "mode": "CW"})
                else:
                    res[name]["trans"].append({"frequ": uplink, "freq": downlink, "mode": mode})

            elif downlink:
                if downlink.find("/") != -1:
                    freqs = downlink.split("/")
                    for f in freqs:
                        if f != "":
                            res[name]["trans"].append({"freq": f, "mode": mode})
                else:
                    if downlink == "980.000(bandwidth 25MHz)":
                        res[name]["trans"].append({"freq": "980", "mode": "bandwith 25MHz"})
                    else:
                        res[name]["trans"].append({"freq": downlink, "mode": mode})


            if beacon and beacon != "":
                if beacon != downlink:
                    if beacon.find("/") != -1:
                        freqs = beacon.split("/")
                        for f in freqs:
                            if f != "":
                                res[name]["trans"].append({"beacon": f})
                    else:
                        res[name]["trans"].append({"beacon": beacon})


a = []
for x in res:
    if len(res[x]["trans"]) == 0:
        continue
    a.append(res[x])

for x in manual:
    a.append(x)

d = {"list": a}
f= open("transponders-notcompacted.json", "w")
f.write(json.dumps(d, indent=4))
