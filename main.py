from datetime import timedelta, datetime
import xml.etree.ElementTree as ElementTree
import pandas as pd
import re

from rich.console import Console
from rich.theme import Theme
from rich.progress import track

console = Console(theme=Theme({"logging.level.success": "bright_green"}))


def log(message, level="info"):
    console.print(
        f"[log.time][{datetime.now().strftime('%H:%M:%S')}][/log.time] [logging.level.{level}]{level}[/logging.level.{level}] \t{message}"
    )


log("Running Purée CLI…", level="info")

passworded = (
    ElementTree.parse("passworded.xml").getroot().find("REGIONS").text.split(",")
)
log("Loaded passworded regions.", level="success")

tree = ElementTree.parse("regions.xml")
log("Loaded daily dump.", level="success")

root = tree.getroot()

regions = []

region_nodes = root.findall("REGION")
log("Loaded all regions.", level="success")

update_start = int(region_nodes[0].find("LASTUPDATE").text)
update_length = int(region_nodes[-1].find("LASTUPDATE").text) - update_start

log(f"Found update length: {update_length} seconds.", level="info")


def find_issues(region):

    if (
        region.find("NAME").text
        in [
            "Suspicious",
            "The Black Hawks",
            "The Brotherhood of Malice",
            "Lily",
            "Osiris",
        ]
        or "X" not in region.find("DELEGATEAUTH").text
        or region.findall("./EMBASSIES/EMBASSY[.='Antifa']")
        or region.find("DELEGATE").text != "0"
    ):
        return []

    issues = []

    wfe = (region.find("FACTBOOK").text or "").lower()

    if any(
        substring in wfe
        for substring in [
            "[region]the brotherhood of malice[/region]",
            "[region]the black hawks[/region]",
            "[region]valle de arena[/region]",
            "[region]lily[/region]",
            "[region]lone wolves united[/region]",
            "region=the_brotherhood_of_malice",
            "region=the_black_hawks",
            "region=valle_de_arena",
            "region=lily",
            "region=lone_wolves_united",
            "www.forum.the-black-hawks.org",
            "forums.europeians.com/index.php?forums/office-of-naval-recruitment.59364",
            "www.nationstates.net/page=dispatch/id=1344417",
        ]
    ):
        issues.append("WFE")

    officers = region.find("OFFICERS").findall("OFFICER")

    officer_appointers = [officer.find("BY").text.lower() for officer in officers]

    officer_offices = [officer.find("OFFICE").text.lower() for officer in officers]

    if any(
        officer_office
        in [
            "raider unity",
            "thorn1000",
            "join tbh",
            "join %%lily%%",
            "lily",
            "the funny",
            "empress wasc",
            "ern",
            "twpirate",
            "kanye omari west",
            "aga gang",
            "epsa",
        ]
        for officer_office in officer_offices
    ) or any(
        any(
            re.fullmatch(regex, officer_appointer)
            for regex in ["guy_\d+", "rc_cola_\d+", "bobberino\d+"]
        )
        for officer_appointer in officer_appointers
    ):
        issues.append("RO")

    embassies = [
        embassy.text
        for embassy in region.findall(f"./EMBASSIES/EMBASSY")
        if embassy.get("type") not in ["closing", "rejected"]
    ]

    if any(
        embassy
        in [
            "The Black Hawks",
            "The Brotherhood of Malice",
            "Valle de Arena",
            "Red Front",
            "Plum Island",
            "Kingdom of Australia",
            "Pasridi Confederacy",
        ]
        for embassy in embassies
    ):
        issues.append("Embassies")

    return issues


def embassy_status(region):
    if any(
        embassy.text
        for embassy in region.findall(f"./EMBASSIES/EMBASSY")
        if region.find(f"./EMBASSIES/EMBASSY") is not None
        and embassy.get("type") in ["closing", "rejected"]
        and embassy.text
        not in [
            "The Black Hawks",
            "The Brotherhood of Malice",
            "Valle de Arena",
            "Red Front",
            "Plum Island",
            "Kingdom of Australia",
            "Pasridi Confederacy",
        ]
    ):
        return True
    return False


for region in track(region_nodes, description="Flagging regions…"):
    if region.find("NAME").text in passworded:
        continue
    issues = find_issues(region)
    if len(issues) > 0:
        name = region.find("NAME").text
        progress = (int(region.find("LASTUPDATE").text) - update_start) / update_length
        minor_progress = round(progress * 3600)
        major_progress = round(progress * 5400)

        region_data = {
            "Region": f"{name}",
            "Issues": f"{', '.join(issues)}",
            "Minor": minor_progress,
            "MinorTimestamp": f"{str(timedelta(seconds=minor_progress))}",
            "Major": major_progress,
            "MajorTimestamp": f"{str(timedelta(seconds=major_progress))}",
            "NativeEmbassies": embassy_status(region),
            "Link": f"https://www.nationstates.net/region={name.lower().replace(' ', '_')}",
        }

        for key, value in region_data.items():
            if type(value) is str and value[0] in ["=", "+", "-", "@"]:
                region_data[key] = f"'{value}"

        regions.append(region_data)

today = (datetime.utcfromtimestamp(update_start) - timedelta(1)).strftime("%d %B %Y")

detags = pd.DataFrame.from_records(regions, index="Region")
detags.to_csv("_data/detags.csv")
detags.to_csv("data/detags.csv")
detags.to_excel("data/detags.xlsx", sheet_name=today)
detags.reset_index().to_json("data/detags.json", orient="records", indent=2)

log(f"Recorded {len(regions)} detags found.", level="success")

with open("_includes/count.html", "w") as outfile:
    outfile.write(str(len(regions)))

history = pd.read_csv("_data/history.csv", index_col="Date")

if today not in history.index:
    row = pd.DataFrame.from_records(
        [{"Date": today, "Count": len(regions)}], index="Date"
    )
    history = pd.concat([history, row])
    history.to_csv("_data/history.csv")
    history.to_csv("data/history.csv")
    history.to_excel("data/history.xlsx", sheet_name="History")
    history.reset_index().to_json("data/history.json", orient="records", indent=2)
    log("Recorded history.", level="info")
else:
    log("No new history entries found.", level="info")
