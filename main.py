from datetime import timedelta, datetime
import xml.etree.ElementTree as ElementTree
import pandas as pd

from rich.console import Console
from rich.theme import Theme
from rich.progress import Progress

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


update_start = int(root.find("REGION").find("LASTUPDATE").text)
update_length = int(root.find("REGION[last()]").find("LASTUPDATE").text) - update_start

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

    if (wfe := region.find("FACTBOOK").text) is not None and any(
        substring in wfe.lower()
        for substring in [
            "[region]the brotherhood of malice[/region]",
            "[region]the black hawks[/region]",
            "[region]valle de arena[/region]",
            "[region]lily[/region]",
            "region=the_brotherhood_of_malice",
            "region=the_black_hawks",
            "region=valle_de_arena",
            "region=lily",
        ]
    ):
        issues.append("WFE")

    if any(
        officer.find("OFFICE").text
        in ["Raider Unity", "Thorn1000", "JOIN TBH", "Join %%Lily%%", "Lily"]
        for officer in region.find("OFFICERS").findall("OFFICER")
    ):
        issues.append("RO")

    if any(
        region.findall(f"./EMBASSIES/EMBASSY[.='{substring}']")
        for substring in [
            "The Black Hawks",
            "The Brotherhood of Malice",
            "Valle de Arena",
            "Red Front",
            "Plum Island",
        ]
        if region.find(f"./EMBASSIES/EMBASSY[.='{substring}']") is not None
        and region.find(f"./EMBASSIES/EMBASSY[.='{substring}']").get("type")
        not in ["closing", "rejected"]
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
        ]
    ):
        return True
    return False


region_nodes = root.findall("REGION")

log(f"Loaded all regions.", level="success")

for region in region_nodes:
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
            "Minor": str(minor_progress),
            "MinorTimestamp": f"{str(timedelta(seconds=minor_progress))}",
            "Major": str(major_progress),
            "MajorTimestamp": f"{str(timedelta(seconds=major_progress))}",
            "NativeEmbassies": str(embassy_status(region)),
            "Link": f"https://www.nationstates.net/region={name.lower().replace(' ', '_')}",
        }

        for key, value in region_data.items():
            if value[0] in ["=", "+", "-", "@"]:
                region_data[key] = f"'{value}"

        regions.append(region_data)

today = (datetime.utcfromtimestamp(update_start) - timedelta(1)).strftime("%d %B %Y")

detags = pd.DataFrame.from_records(regions, index="Region")
detags.to_csv("_data/detags.csv")
detags.to_excel("_data/detags.xlsx", sheet_name=today)
detags.reset_index().to_json("_data/detags.json", orient="records")

log(f"Recorded detags found.", level="success")

with open("_includes/count.html", "w") as outfile:
    outfile.write(str(len(regions)))

history = pd.read_csv("_data/history.csv", index_col="Date")

if today not in history.index:
    row = pd.DataFrame.from_records(
        [{"Date": today, "Count": str(len(regions))}], index="Date"
    )
    history = pd.concat([history, row])

history.to_csv("_data/history.csv")
history.to_excel("_data/history.xlsx", sheet_name="History")
history.reset_index().to_json("_data/history.json", orient="records")

log(f"Recorded history.", level="success")
